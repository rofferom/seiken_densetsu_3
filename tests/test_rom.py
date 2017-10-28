import unittest
import sd3.rom
import tests.trace_tools


class TestRom(unittest.TestCase):
    def test_highrom_conv(self):
        addr = sd3.rom.HighRomConv.snes_to_rom(0xC00000)
        self.assertEqual(addr, 0)

        addr = sd3.rom.HighRomConv.rom_to_snes(0)
        self.assertEqual(addr, 0xC00000)

    def test_rom(self):
        data_map = {
            0x000000: bytearray.fromhex("001122334455"),
            0x300000: bytearray.fromhex("AABBCCDDEEFF"),
            0x3ECCD0: bytearray.fromhex("1234")
        }

        file_mock = tests.trace_tools.FileMock(tests.trace_tools.get_rom_size(),
                                               data_map)
        rom = sd3.rom.Rom.from_file(file_mock, sd3.rom.HighRomConv)

        rom.seek(0xC00000)
        self.assertEqual(rom.tell(), 0xC00000)

        v = rom.read_u8()
        self.assertEqual(v, 0x00)

        v = rom.read_u8()
        self.assertEqual(v, 0x11)

        v = rom.read_u16()
        self.assertEqual(v, 0x3322)

        v = rom.read_u16(endianess=sd3.rom.BIG_ENDIAN)
        self.assertEqual(v, 0x4455)

        rom.seek(0xF00000)
        self.assertEqual(rom.tell(), 0xF00000)

        v = rom.read_u16(endianess=sd3.rom.BIG_ENDIAN)
        self.assertEqual(v, 0xAABB)

        addr = rom.read_addr_from_ptr(0xFEC000, 1640, 0xF8)
        self.assertEqual(addr, 0xF83412)


if __name__ == '__main__':
    unittest.main()
