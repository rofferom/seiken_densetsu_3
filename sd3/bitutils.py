class BitReader:
    def __init__(self, src, width):
        self.src = src
        self.width = width
        self.mask = (1 << width) - 1

        self.value = 0
        self.count = 0

    def read_bits(self, remaining):
        value = 0

        while remaining > 0:
            if self.count == 0:
                self.value = self.src()
                if self.value is None:
                    return None

                self.count = self.width

            bit_used = min(self.count, remaining)
            value <<= bit_used
            value |= self.value >> (self.width - bit_used)

            self.value = (self.value << bit_used) & self.mask
            self.count -= bit_used

            remaining -= bit_used

        return value
