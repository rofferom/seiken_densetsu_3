import os
import logging
from collections import namedtuple
import sd3.disasm.cpu
from sd3.disasm.attributes import Attr
from sd3.disasm.addr_modes import AddrMode
import sd3.cfa.graph
import sd3.cfa.shortestpath
import sd3.cfa.cfg
import sd3.cfa.dominator
import sd3.cfa.loop
import sd3.tools.seq_operations
import sd3.tools.jinja2

_STATUS_OK = "OK"
_STATUS_KO = "KO"
_STATUS_IGNORED = "Ignored"

_IndexedCall = namedtuple("_SubCall", ["addr"])
_SubCall = namedtuple("_SubCall", ["routine", "addr", "sub_descr"])
_Jump = namedtuple("_Jump", ["addr", "dest"])


class Cfg:
    def __init__(self):
        self.track_routine = None
        self.ignore_list = []


class _HtmlReport:
    def __init__(self):
        self.routines_ok = []
        self.routines_ko = []
        self.routines_ignored = []
        self.all_routines = []

    def finalize(self):
        self.routines_ko.sort(key=lambda sub: sub.calls)

        self.all_routines.extend(self.routines_ok)
        self.all_routines.extend(self.routines_ko)
        self.all_routines.extend(self.routines_ignored)


_HtmlSubroutine = namedtuple("_HtmlSubroutine", ["addr", "count", "depth"])


class _HtmlHandlerReport:
    def __init__(self, addr):
        self.addr = addr
        self.calls = 0
        self.indexed_calls = 0
        self.jumps = 0
        self.subroutines = []

        self.cond_calls = False
        self.in_loop_calls = False

        self.status = _STATUS_KO

    def set_ignored(self):
        self.status = _STATUS_IGNORED

    def _compute_status(self):
        self.status = _STATUS_OK

        if self.calls > 0:
            if self.cond_calls:
                self.status = _STATUS_KO

            if self.in_loop_calls:
                self.status = _STATUS_KO
        if self.indexed_calls > 0:
            self.status = _STATUS_KO

        if self.subroutines:
            self.status = _STATUS_KO

    def _find_subcalls(self, handler_info, cfg):
        entry_node = handler_info.graph.get_entry()
        for _, node in handler_info.graph.get_node_it():
            if node is entry_node:
                continue

            # Get routine info
            sub_info = node.get_data()
            sub_call_count = sub_info.get_sub_call_count(cfg.track_routine)
            if sub_call_count == 0:
                continue

            distance_from_root = sd3.cfa.shortestpath.get(
                handler_info.graph, entry_node, node)

            # Append subroutine call info
            html_subroutine = _HtmlSubroutine(
                sub_info.routine.addr,
                sub_call_count,
                distance_from_root)

            self.subroutines.append(html_subroutine)

    def fill(self, handler_info, cfg):
        routine_info = handler_info.get_main_routine_info()

        # Find direct calls
        for sub_call in routine_info.sub_calls:
            if sub_call.sub_descr.addr == cfg.track_routine:
                self.calls += 1

        # Fill other fields
        self.indexed_calls = len(routine_info.indexed_sub_calls)
        self.jumps = len(routine_info.jumps)
        self.cond_calls = handler_info.cond_calls
        self.in_loop_calls = handler_info.in_loop_calls

        # Find calls done by subroutines
        self._find_subcalls(handler_info, cfg)

        # Compute
        self._compute_status()


class _HandlerInfo:
    def __init__(self, addr):
        self.addr = addr
        self.graph = sd3.cfa.graph.Graph()
        self.cond_calls = False
        self.in_loop_calls = False

    def get_main_routine_info(self):
        entry = self.graph.get_entry()
        return entry.get_data()

    def get_main_routine(self):
        info = self.get_main_routine_info()
        return info.routine


class _RoutineInfo:
    def __init__(self, routine):
        self.routine = routine

        self.jumps = []
        self.sub_calls = []
        self.indexed_sub_calls = []

    def get_sub_call_count(self, addr):
        count = 0

        for sub_call in self.get_sub_calls(addr):
            count += 1

        return count

    def get_sub_calls(self, addr):
        for sub in self.sub_calls:
            if sub.sub_descr.addr == addr:
                yield sub


class _HandlerAnalyser:
    def __init__(self, cpu_reader, cfg, root_addr):
        self.cpu_reader = cpu_reader
        self.cfg = cfg
        self.root_addr = root_addr

        self.routine = None
        self.cfg_graph = None
        self.dom_graph = None
        self.loop_list = None

    def _node_has_tracked_call(self, node, routine_info):
        data = node.get_data()

        for sub_call in routine_info.get_sub_calls(self.cfg.track_routine):
            if data.has_instruction(sub_call.addr):
                return True

    def _build_routine_info(self, routine):
        info = _RoutineInfo(routine)

        for instr in routine.instructions:
            if instr.has_attr(Attr.enter_sub):
                if instr.addr_mode.mode == AddrMode.absolute_indexed_indirect:
                    subcall = _IndexedCall(instr.addr)

                    info.indexed_sub_calls.append(subcall)
                else:
                    call_addr = instr.get_jump_target()
                    sub_descr = routine.get_subroutine_desc(call_addr)
                    subcall = _SubCall(routine, instr.addr, sub_descr)

                    info.sub_calls.append(subcall)
            elif instr.has_attr(Attr.jump):
                jump_addr = instr.get_jump_target()
                jump = _Jump(instr.addr, jump_addr)

                info.jumps.append(jump)

        return info

    def _build_call_graph(self, handler_info):
        # Build graph root node (subroutine to analyse)
        p = sd3.disasm.cpu.PRegister(X=0, M=0)
        routine = self.cpu_reader.read_routine(handler_info.addr, p)

        info = self._build_routine_info(routine)

        root_node, _ = handler_info.graph.add_node(handler_info.addr)
        root_node.set_data(info)
        handler_info.graph.set_entry(root_node)

        # Initial pending routines: list of subroutines calls by the handler
        subroutine_stack = []
        for subcall in info.sub_calls:
            subroutine_stack.append(subcall)

        # Visit subroutines
        while subroutine_stack:
            # Get next node to visit. Ignore already known nodes
            subcall = subroutine_stack.pop()
            subcall_addr = subcall.sub_descr.addr

            # Also ignore the routine to track
            if subcall_addr == self.cfg.track_routine:
                continue

            if handler_info.graph.has_node(subcall_addr):
                continue

            # Read the subroutine
            routine = self.cpu_reader.read_routine(subcall_addr,
                                                   subcall.sub_descr.p)

            info = self._build_routine_info(routine)

            # Put the subroutine in the graph
            node, _ = handler_info.graph.add_node(subcall_addr)
            node.set_data(info)

            parent_node = handler_info.graph.get_node(subcall.routine.get_addr())
            parent_node.add_successor(node)

            # Put subroutines in the stack
            for subcall in info.sub_calls:
                subroutine_stack.append(subcall)

    def _get_loop_nodes(self, loop_list):
        for loop in loop_list:
            for node in loop.get_node_list():
                yield node

    def _find_subcall_in_loops(self, handler_info):
        routine_info = handler_info.get_main_routine_info()

        for node in self._get_loop_nodes(self.loop_list):
            if self._node_has_tracked_call(node, routine_info):
                return True

        return False

    def _find_conditional_subcalls(self, handler_info):
        if len(self.cfg_graph.get_node_list()) == 1:
            return False

        routine_info = handler_info.get_main_routine_info()
        dom_exit = self.dom_graph.get_node(self.cfg_graph.get_exit().get_id())

        # Dom graph traversal
        stack = [self.dom_graph.get_entry()]
        while stack:
            # Get next node to visit
            dom_node = stack.pop()
            cfg_node = self.cfg_graph.get_node(dom_node.get_id())

            # Push childs in the node stack
            for successor in dom_node.get_successors():
                stack.append(successor.get_dest())

            # Ignore the current block if it doesn't call the tracked routine
            block_has_call = self._node_has_tracked_call(
                dom_node, routine_info)
            if not block_has_call:
                continue

            # If the node doesn't dominate the exit, it means it won't be
            # always called
            node_dominates_exit = sd3.cfa.dominator.dominates(
                dom_node, dom_exit)
            if not node_dominates_exit:
                return True

        return False

    def run(self):
        handler_info = _HandlerInfo(self.root_addr)

        logging.info("Read routine %X", self.root_addr)

        # Build call graph for the routine
        self._build_call_graph(handler_info)

        # Build CFG, dominator tree and loop list
        self.routine = handler_info.get_main_routine()

        self.cfg_graph = sd3.cfa.cfg.build_graph(self.routine)

        self.dom_graph = sd3.cfa.dominator.build_graph(self.cfg_graph)

        self.loop_list = sd3.cfa.loop.find_loops(self.cfg_graph, self.dom_graph)

        # Check if there is at least one conditionnal call
        handler_info.cond_calls = self._find_conditional_subcalls(handler_info)

        # Check if there are calls in a loop
        handler_info.in_loop_calls = self._find_subcall_in_loops(handler_info)

        return handler_info


class _RoutineAddrGenerator:
    def __init__(self, rom, cfg):
        self.visited = set()
        self.pending = set(self._get_sub_list(rom))
        self.cfg = cfg

    def _get_sub_list(self, rom):
        subroutines = set()

        for _, sub_addr in sd3.tools.seq_operations.get_op_list(rom):
            if sub_addr not in subroutines:
                subroutines.add(sub_addr)
                yield sub_addr

    def routines(self):
        while self.pending:
            sud_addr = self.pending.pop()
            self.visited.add(sud_addr)
            yield sud_addr

    def _add_new_subcalls(self, routine_info):
        routine_addr = routine_info.routine.addr

        for sub_call in routine_info.get_sub_calls(self.cfg.track_routine):
            subcall_addr = sub_call.sub_descr.addr
            if routine_addr not in self.visited:
                logging.info("Add subroutine %X", subcall_addr)
                self.pending.add(routine_addr)
                break

    def process_handler_info(self, handler_info):
        entry_node = handler_info.graph.get_entry()

        # Check in every node if there is at least one call to the routine
        for _, node in handler_info.graph.get_node_it():
            if node is entry_node:
                continue

            # Check if the tracked routine is called by this one
            routine_info = node.get_data()
            self._add_new_subcalls(routine_info)

def gen_html_report(rom, cfg, output_path):
    report = _HtmlReport()
    cpu_reader = sd3.disasm.cpu.Reader(rom)

    # Analyse and build report for all the handler and interesting subroutines
    routine_gen = _RoutineAddrGenerator(rom, cfg)
    for sub_addr in routine_gen.routines():
        # Some routines can be ignored
        if sub_addr in cfg.ignore_list:
            handler_report = _HtmlHandlerReport(sub_addr)
            handler_report.set_ignored()
            report.routines_ignored.append(handler_report)
            continue

        # Analyse handler and build html report
        analyser = _HandlerAnalyser(cpu_reader, cfg, sub_addr)
        handler_info = analyser.run()

        handler_report = _HtmlHandlerReport(sub_addr)
        handler_report.fill(handler_info, cfg)

        # Add the report in the correct list
        if handler_report.status == _STATUS_OK:
            report.routines_ok.append(handler_report)
        else:
            report.routines_ko.append(handler_report)

        # The handler analysis may detect some subroutines that call the
        # tracked routine. In this case, append them in the pending list.
        routine_gen.process_handler_info(handler_info)

    # Finalize report creation
    report.finalize()

    # Generate html report
    template = sd3.tools.jinja2.load_template(
        "gen_op_report.template",
        os.path.dirname(os.path.abspath(__file__)))

    rendered = template.render(report=report)

    # Write output file
    sd3.tools.jinja2.write_rendered(rendered, output_path)
