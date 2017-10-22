import hashlib

_FILE_SHA1 = "209c55fd2a8d7963905e3048b7d40094d6bea965"
_FILE_SIZE = 4194304


class RomTracer:
    def __init__(self):
        self.data = {}

    def __call__(self, addr, v):
        self.data[addr] = v

    def get_data(self):
        merged_data = {}
        next_addr = None
        current_block = None

        for addr in sorted(self.data.keys()):
            data = self.data[addr]
            if next_addr is None or next_addr != addr:
                current_block = bytearray()
                merged_data[addr] = current_block

            current_block += data
            next_addr = addr + len(data)

        return merged_data


class FileMock:
    def __init__(self, filesize, dump):
        self.data = bytearray(filesize)

        for addr, addr_data in dump.items():
            i = 0
            for b in addr_data:
                self.data[addr+i] = b
                i += 1

        self.addr = None

    def seek(self, addr):
        self.addr = addr

    def tell(self):
        return self.addr

    def read(self):
        return self.data


def get_rom_size():
    return _FILE_SIZE


def check_rom_valid(f):
    sha1 = hashlib.sha1(f.read()).hexdigest()
    return _FILE_SHA1.lower() == sha1.lower()
