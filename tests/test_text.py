import sys
import unittest
import tests.text_data
import tests.trace_tools
import sd3.seq.reader


class TestText(unittest.TestCase):
    class SeqObserver(sd3.seq.reader.Observer):
        def __init__(self):
            self.decoded = []

        def text_decoded(self, decoded):
            self.decoded.append(decoded)

    def test_decode(self):
        observer = TestText.SeqObserver()

        f = tests.trace_tools.FileMock(tests.trace_tools.get_rom_size(),
                                       tests.text_data.decode_dump)
        rom = sd3.rom.Rom.from_file(f, sd3.rom.HighRomConv)

        decoder = sd3.seq.reader.Reader(rom)
        decoded = decoder.read_sequence(tests.text_data.decode_idx, observer)

        self.assertListEqual(observer.decoded, tests.text_data.decode_result)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Missing ROM param")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        if not tests.trace_tools.check_rom_valid(f):
            print("ROM invalid")
            sys.exit(1)

        tracer = tests.trace_tools.RomTracer()
        rom = sd3.rom.Rom.from_file(f, sd3.rom.HighRomConv, tracer=tracer)
        decoder = sd3.text.Decoder(rom)
        decoded = decoder.get_dialog(tests.text_data.decode_idx)

        print("Used data")
        print(tracer.get_data())

        print("Decoded data")
        print(decoded)
