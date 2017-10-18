import enum
import struct
from sd3.disasm.attributes import Attr


class AddrMode(enum.Enum):
    none = 0
    immediate = 1
    direct = 2
    direct_indexed = 3
    indirect = 4
    indirect_indexed = 5
    indirect_long = 6
    indirect_long_indexed = 7
    absolute = 8
    absolute_indexed = 9
    absolute_long = 10
    absolute_long_indexed = 11
    absolute_indexed_indirect = 12
    accumulator = 13
    stack_relative = 14
    pc_relative = 15
    block_move = 16


def _get_str_index(opcode):
    if Attr.indexed_x in opcode.attrs:
        return "X"
    elif Attr.indexed_y in opcode.attrs:
        return "Y"
    else:
        raise Exception("Opcode not indexed")


class AddrModeBase:
    def __init__(self, mode):
        self.mode = mode

    def _read_u24(self, rom):
        v = 0
        for i in range(3):
            v |= rom.read_u8() << (8 * i)

        return v

    def read_param(self, rom, opcode, p):
        raise Exception("Not implemented")

    def to_str(self, opcode, param, param_len):
        raise Exception("Not implemented")

    def get_jump_target(self, addr, param, next_addr):
        raise Exception("Not implemented")


class AddrModeNone(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.none)

    def read_param(self, rom, opcode, p):
        return (None, None)

    def to_str(self, opcode, param, param_len):
        return None


class AddrModeImmediate(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.immediate)

    def _check_len(self, opcode, p):
        if Attr.m_dependant in opcode.attrs and p.M == 0:
            return 2

        if Attr.x_dependant in opcode.attrs and p.X == 0:
            return 2

        return 1

    def read_param(self, rom, opcode, p):
        param_len = self._check_len(opcode, p)
        if param_len == 2:
            return (rom.read_u16(), param_len)
        elif param_len == 1:
            return (rom.read_u8(), param_len)
        else:
            raise Exception("Unexpected length")

    def to_str(self, opcode, param, param_len):
        if param_len == 2:
            return "#$%04X" % param
        elif param_len == 1:
            return "#$%02X" % param
        else:
            raise Exception("Unexpected length")


class AddrModeDirect(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.direct)

    def read_param(self, rom, opcode, p):
        return (rom.read_u8(), 1)

    def to_str(self, opcode, param, param_len):
        return "$%02X" % param

    def get_jump_target(self, addr, param, next_addr):
        return next_addr + param


class AddrModeDirectIndexed(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.direct_indexed)

    def read_param(self, rom, opcode, p):
        return (rom.read_u8(), 1)

    def to_str(self, opcode, param, param_len):
        str_index = _get_str_index(opcode)
        return "$%02X,%s" % (param, str_index)


class AddrModeIndirect(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.indirect)

    def read_param(self, rom, opcode, p):
        return (rom.read_u8(), 1)

    def to_str(self, opcode, param, param_len):
        return "($%02X)" % param


class AddrModeIndirectLong(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.indirect_long)

    def read_param(self, rom, opcode, p):
        return (rom.read_u8(), 1)

    def to_str(self, opcode, param, param_len):
        return "[$%02X]" % param


class AddrModeIndirectIndexed(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.indirect_indexed)

    def read_param(self, rom, opcode, p):
        return (rom.read_u8(), 1)

    def to_str(self, opcode, param, param_len):
        str_index = _get_str_index(opcode)
        return "($%02X),%s" % (param, str_index)


class AddrModeIndirectLongIndexed(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.indirect_long_indexed)

    def read_param(self, rom, opcode, p):
        return (rom.read_u8(), 1)

    def to_str(self, opcode, param, param_len):
        str_index = _get_str_index(opcode)
        return "[$%02X],%s" % (param, str_index)


class AddrModeAbsolute(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.absolute)

    def read_param(self, rom, opcode, p):
        return (rom.read_u16(), 2)

    def to_str(self, opcode, param, param_len):
        return "$%04X" % param

    def get_jump_target(self, addr, param, next_addr):
        return (addr & 0xFF0000) | param


class AddrModeAbsoluteIndexed(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.absolute_indexed)

    def read_param(self, rom, opcode, p):
        return (rom.read_u16(), 2)

    def to_str(self, opcode, param, param_len):
        str_index = _get_str_index(opcode)
        return "$%04X,%s" % (param, str_index)


class AddrModeAbsoluteLong(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.absolute_long)

    def read_param(self, rom, opcode, p):
        return (self._read_u24(rom), 3)

    def to_str(self, opcode, param, param_len):
        return "$%06X" % param

    def get_jump_target(self, addr, param, next_addr):
        return param


class AddrModeAbsoluteLongIndexed(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.absolute_long_indexed)

    def read_param(self, rom, opcode, p):
        return (self._read_u24(rom), 3)

    def to_str(self, opcode, param, param_len):
        str_index = _get_str_index(opcode)
        return "$%06X,%s" % (param, str_index)


class AddrModeAbsoluteIndexedIndirect(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.absolute_indexed_indirect)

    def read_param(self, rom, opcode, p):
        return (rom.read_u16(), 2)

    def to_str(self, opcode, param, param_len):
        str_index = _get_str_index(opcode)
        return "($%04X),%s" % (param, str_index)

    def get_jump_target(self, addr, param, next_addr):
        return None


class AddrModeAccumulator(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.accumulator)

    def read_param(self, rom, opcode, p):
        return (None, None)

    def to_str(self, opcode, param, param_len):
        return "A"


class AddrModeStackRelative(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.stack_relative)

    def read_param(self, rom, opcode, p):
        return (rom.read_u8(), 1)

    def to_str(self, opcode, param, param_len):
        return "$%02X,S" % param


class AddrModePcRelative(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.pc_relative)

    def read_param(self, rom, opcode, p):
        return (rom.read_i8(), 1)

    def to_str(self, opcode, param, param_len):
        v = struct.pack("b", param)
        v = struct.unpack("B", v)[0]
        return "$%02X" % v

    def get_jump_target(self, addr, param, next_addr):
        return next_addr + param


class AddrModeBlockMove(AddrModeBase):
    def __init__(self):
        super().__init__(AddrMode.block_move)

    def read_param(self, rom, opcode, p):
        return (rom.read_u16(), 2)

    def to_str(self, opcode, param, param_len):
        return "$%02X,$%02X" % (param & 0xFF, param >> 8)


def get_addr_mode_list():
    return AddrModeBase.__subclasses__()
