from collections import namedtuple
from sd3.disasm.attributes import Attr
from sd3.disasm.addr_modes import AddrMode

RoutineDesc = namedtuple("RoutineDesc", ["addr", "p"])


class Instruction:
    def __init__(self):
        self.addr = None
        self.opcode = None
        self.addr_mode = None
        self.param = None
        self.param_len = None

    def __str__(self):
        return self.to_str()

    def to_str(self, display_addr=True):
        # Put address and menemonic
        if display_addr:
            s = "%06X %s" % (self.addr, self.opcode.mnemonic)
        else:
            s = "%s" % self.opcode.mnemonic

        # Append parameter if any
        if self.addr_mode.mode != AddrMode.none:
            str_param = self.addr_mode.to_str(self.opcode, self.param,
                                              self.param_len)
            s += " %s" % str_param

        # Append jump location is any
        if self.has_attr(Attr.branch) or self.has_attr(Attr.enter_sub):
            target = self.get_jump_target()
            if target is not None:
                s += " [%06X]" % target

        return s

    def get_next_instr_addr(self):
        # Instruction size: Opcode(1) + Params
        return self.addr + 1 + self.param_len

    def has_attr(self, attr):
        return attr in self.opcode.attrs

    def get_jump_target(self):
        jump_attrs = {Attr.enter_sub, Attr.branch, Attr.jump}

        if not jump_attrs.intersection(self.opcode.attrs):
            raise Exception("%s is not a jump instruction" %
                            self.opcode.mnemonic)

        next_addr = self.get_next_instr_addr()

        return self.addr_mode.get_jump_target(self.addr, self.param, next_addr)

    def update_p(self, p):
        M_BIT = 0b00100000
        X_BIT = 0b00010000

        if self.has_attr(Attr.reset_p):
            if self.param & M_BIT:
                p.M = 0
            elif self.param & X_BIT:
                p.X = 0
        elif self.has_attr(Attr.set_p):
            if self.param & M_BIT:
                p.M = 1
            elif self.param & X_BIT:
                p.X = 1


class Routine:
    def __init__(self, addr):
        self.addr = addr

        self.instructions = []
        self.addr_map = set()

        self.subroutines = {}

        self.pending_jumps = set()

    def display(self):
        for instr in self.instructions:
            print(instr)

    def get_addr(self):
        return self.addr

    def add_instruction(self, instr):
        self.instructions.append(instr)
        self.addr_map.add(instr.addr)

        if instr.addr in self.pending_jumps:
            self.pending_jumps.remove(instr.addr)

    def add_jump(self, addr):
        if addr not in self.addr_map:
            self.pending_jumps.add(addr)
            return True

        return False

    def get_next_jump(self):
        if not self.pending_jumps:
            return None

        return self.pending_jumps.pop()

    def is_addr_known(self, addr):
        return addr in self.addr_map

    def add_subroutine(self, addr, p):
        if addr in self.subroutines:
            return

        desc = RoutineDesc(addr, p.clone())
        self.subroutines[addr] = desc

    def get_subroutine_desc(self, addr):
        return self.subroutines[addr]
