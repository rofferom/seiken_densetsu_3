import os
import enum
import logging
import graphviz
import sd3.cfa.graph
from sd3.disasm.attributes import Attr as CpuAttr


class EdgeAttr(enum.Enum):
    true_cond = 1
    false_cond = 2


class NodeData:
    def __init__(self, addr):
        self._start_addr = addr
        self._instructions = []

    def get_name(self):
        return "%06X" % self._start_addr

    def display(self):
        for instr in self._instructions:
            print(instr)

    def add_instruction(self, inst):
        self._instructions.append(inst)

    def get_instructions(self):
        return self._instructions

    def has_instruction(self, addr):
        for inst in self._instructions:
            if inst.addr == addr:
                return True

        return False


class _GraphBuilder:
    def __init__(self, routine):
        self.routine = routine
        self.cfg = None
        self.curr_block = None

    def _add_node(self, addr):
        (node, new_node) = self.cfg.add_node("%X" % addr)
        if new_node:
            node.set_data(NodeData(addr))

        return node

    def _find_labels(self):
        labels = set()

        for instr in self.routine.instructions:
            if instr.has_attr(CpuAttr.branch):
                target = instr.get_jump_target()
                labels.add(target)

        return labels

    def _handle_branch(self, instr):
        logging.debug("Found branch 0x%06X", instr.addr)
        # Block ends
        data = self.curr_block.get_data()
        data.add_instruction(instr)

        # Get the following block if exists
        if not instr.has_attr(CpuAttr.unconditional):
            next_instr_addr = instr.get_next_instr_addr()
            false_block = self._add_node(next_instr_addr)
        else:
            false_block = None

        # Get targeted block
        true_addr = instr.get_jump_target()
        logging.debug("Target: %X", true_addr)
        true_block = self._add_node(true_addr)

        # Store output edges into current block
        if false_block is not None:
            edge = self.curr_block.add_successor(false_block)
            edge.add_attr(EdgeAttr.false_cond)

            edge = self.curr_block.add_successor(true_block)
            edge.add_attr(EdgeAttr.true_cond)

            # Continue to visit the routine
            self.curr_block = false_block
        else:
            self.curr_block.add_successor(true_block)
            self.curr_block = None

    def _handle_label(self, instr):
        logging.debug("Found label 0x%06X", instr.addr)
        prev_block = self.curr_block

        # Block starts
        self.curr_block = self._add_node(instr.addr)
        data = self.curr_block.get_data()
        data.add_instruction(instr)

        # Create link with previous block if we are transitioning
        # between blocks
        if prev_block is not None and prev_block != self.curr_block:
            prev_block.add_successor(self.curr_block)

    def _handle_body(self, instr):
        if self.curr_block is None:
            self.curr_block = self.cfg.get_node(instr.addr)

        data = self.curr_block.get_data()
        data.add_instruction(instr)

    def _set_exit_node(self):
        entry_node = self.cfg.get_entry()
        exit_node = None

        for (_, node) in self.cfg.get_node_it():
            successors_count = len(node.get_successors())
            if successors_count == 0 and node is not entry_node:
                if exit_node is not None:
                    raise Exception("Exit node already found")

                exit_node = node

        if exit_node is None:
            exit_node = entry_node

        self.cfg.set_exit(exit_node)

    def run(self):
        self.cfg = sd3.cfa.graph.Graph()

        # Add entry block
        entry_addr = self.routine.get_addr()
        self.curr_block = self._add_node(entry_addr)
        self.curr_block.set_data(NodeData(entry_addr))

        self.cfg.set_entry(self.curr_block)

        labels = self._find_labels()

        for instr in self.routine.instructions:
            if instr.has_attr(CpuAttr.branch):
                self._handle_branch(instr)
            elif instr.addr in labels:
                self._handle_label(instr)
            else:
                self._handle_body(instr)

        # Set exit node
        self._set_exit_node()

        return self.cfg


class _GraphDrawer:
    @staticmethod
    def _node_to_str(node):
        node_str = ""

        data = node.get_data()
        for instr in data.get_instructions():
            node_str += "%s\l" % instr.to_str(display_addr=False)

        return node_str

    @staticmethod
    def _build_edge_attrs(edge):
        attrs = {}

        if edge.has_attr(EdgeAttr.true_cond):
            color = "green"
            attrs["color"] = color
            attrs["label"] = "true"
            attrs["fontcolor"] = color
        elif edge.has_attr(EdgeAttr.false_cond):
            color = "red"
            attrs["color"] = color
            attrs["label"] = "false"
            attrs["fontcolor"] = color

        return attrs

    @staticmethod
    def draw(cfg, out_path):
        basename, extension = os.path.splitext(out_path)

        # Build graph
        dot = graphviz.Digraph(
            format=extension[1:],
            node_attr={"shape": "box"})

        # Build nodes
        for _, node in cfg.get_node_it():
            node_str = _GraphDrawer._node_to_str(node)
            dot.node(node.get_data().get_name(), node_str)

        # Build edges
        for edge in cfg.get_edges_it():
            attrs = _GraphDrawer._build_edge_attrs(edge)

            dot.edge(
                edge.get_src().get_data().get_name(),
                edge.get_dest().get_data().get_name(),
                **attrs)

        return dot.render(filename=basename, cleanup=True)


def build_graph(routine):
    builder = _GraphBuilder(routine)
    return builder.run()


def draw_graph(cfg, out_path):
    return _GraphDrawer.draw(cfg, out_path)
