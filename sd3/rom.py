import struct


_U8_SIZE = 1
_I8_SIZE = 1
_U16_SIZE = 2

BIG_ENDIAN = 0
LITTLE_ENDIAN = 1


class HighRomConv:
    _ADDR_OFFSET = 0xC00000

    @staticmethod
    def snes_to_rom(addr):
        return addr - HighRomConv._ADDR_OFFSET

    @staticmethod
    def rom_to_snes(addr):
        return addr + HighRomConv._ADDR_OFFSET


class Rom:
    def __init__(self):
        self.data = None
        self.addr = 0

        self.conv_addr = None
        self.tracer = None

    @staticmethod
    def from_file(f, conv_addr, tracer=None):
        rom = Rom()

        f.seek(0)
        rom.data = f.read()
        rom.addr = 0

        rom.conv_addr = conv_addr
        rom.tracer = tracer

        return rom

    @staticmethod
    def from_rom(src):
        rom = Rom()

        rom.data = src.data
        rom.addr = src.addr

        rom.conv_addr = src.conv_addr
        rom.tracer = src.tracer

        return rom

    def seek(self, addr):
        self.addr = self.conv_addr.snes_to_rom(addr)

    def tell(self):
        return self.conv_addr.rom_to_snes(self.addr)

    def read_u8(self):
        value = self.read_buf(_U8_SIZE)
        return struct.unpack("B", value)[0]

    def read_i8(self):
        value = self.read_buf(_U8_SIZE)
        return struct.unpack("b", value)[0]

    def read_u16(self, endianess=LITTLE_ENDIAN):
        value = self.read_buf(_U16_SIZE)

        if endianess == LITTLE_ENDIAN:
            fmt = "<H"
        else:
            fmt = ">H"

        return struct.unpack(fmt, value)[0]

    def read_buf(self, count):
        buf = self.data[self.addr:self.addr+count]

        if self.tracer:
            self.tracer(self.addr, buf)

        self.addr += count

        return buf

    def read_addr_from_ptr(self, tbl_base, ptr_idx, target_bank):
        addr = tbl_base + _U16_SIZE * ptr_idx
        self.seek(addr)

        return (target_bank << 16) | self.read_u16()
