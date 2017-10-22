import unittest
import sd3.bitutils


class _U16Generator:
    def __init__(self, values):
        self.values = values
        self.idx = 0

    def __call__(self):
        if self.idx < len(self.values):
            v = self.values[self.idx]
            self.idx += 1
        else:
            v = None

        return v


class TestBitReader(unittest.TestCase):
    def setUp(self):
        values = [
            0b0000000100100011,
            0b1000100110101011,
            0b1100110111101111
        ]

        self.src = _U16Generator(values)

    def tearDown(self):
        self.src = None

    def test(self):
        reader = sd3.bitutils.BitReader(self.src, 16)

        # Read a complete word
        v = reader.read_bits(4)
        self.assertEqual(v, 0b0000)

        v = reader.read_bits(4)
        self.assertEqual(v, 0b0001)

        v = reader.read_bits(4)
        self.assertEqual(v, 0b0010)

        v = reader.read_bits(4)
        self.assertEqual(v, 0b0011)

        # Read a large part of the next word
        v = reader.read_bits(12)
        self.assertEqual(v, 0b100010011010)

        # Read more than the remaining size. Force a new read
        v = reader.read_bits(8)
        self.assertEqual(v, 0b10111100)

        v = reader.read_bits(4)
        self.assertEqual(v, 0b1101)

        v = reader.read_bits(8)
        self.assertEqual(v, 0b11101111)

        v = reader.read_bits(1)
        self.assertIsNone(v)


if __name__ == '__main__':
    unittest.main()
