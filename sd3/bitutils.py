from collections import namedtuple
import sd3.rom

BitReaderSrc = namedtuple("BitReaderSrc", ["bitsrc", "width"])


class BitReader:
    def __init__(self, src):
        self.src = src
        self.mask = (1 << self.src.width) - 1

        self.value = 0
        self.count = 0

    @staticmethod
    def from_src(bitsrc, width):
        src = BitReaderSrc(bitsrc, width)
        return BitReader(src)

    @staticmethod
    def from_rom_u16_big(rom, addr):
        # Prepare BitReader input
        rom_reader = sd3.rom.Rom.from_rom(rom)
        rom_reader.seek(addr)

        def bitreader_provider():
            return rom_reader.read_u16(endianess=sd3.rom.BIG_ENDIAN)

        return BitReader.from_src(bitreader_provider, 16)

    def read_bits(self, remaining):
        value = 0

        while remaining > 0:
            if self.count == 0:
                self.value = self.src.bitsrc()
                if self.value is None:
                    return None

                self.count = self.src.width

            bit_used = min(self.count, remaining)
            value <<= bit_used
            value |= self.value >> (self.src.width - bit_used)

            self.value = (self.value << bit_used) & self.mask
            self.count -= bit_used

            remaining -= bit_used

        return value
