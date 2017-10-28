import sys
import unittest
import sd3.gfx
import tests.trace_tools
import tests.gfx_data


class TestReadTile(unittest.TestCase):
    def test(self):
        f = tests.trace_tools.FileMock(tests.trace_tools.get_rom_size(),
                                       tests.gfx_data.decode_dump)
        rom = sd3.rom.Rom.from_file(f, sd3.rom.HighRomConv)
        font_reader = sd3.gfx.FontReader(rom)

        for c in tests.gfx_data.char_list:
            print("Read char %04X" % c.idx)

            decoded = font_reader.read_char(c.idx)
            self.assertListEqual(decoded.get_raw_content(), c.decoded)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Missing ROM param")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        if not tests.trace_tools.check_rom_valid(f):
            print("ROM invalid")
            sys.exit(1)

        tracer = tests.trace_tools.RomTracer()
        rom = sd3.rom.Rom(f, sd3.rom.HighRomConv, tracer=tracer)
        font_reader = sd3.gfx.FontReader(rom)

        for c in tests.gfx_data.char_list:
            print("Read char %04X" % c.idx)
            tile = font_reader.read_char(c.idx)

            print("Decoded char")
            print(tile.get_raw_content())

        print("Used data")
        print(tracer.get_data())
