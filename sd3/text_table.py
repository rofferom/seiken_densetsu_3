class Table:
    def __init__(self):
        self._entries = {}

    def load(self, path):
        # Read table
        with open(path, "r") as f:
            for line in f:
                if line[-1] == '\n':
                    line = line[:-1]

                sep_idx = line.find("=")
                idx = int(line[:sep_idx], base=16)
                char = line[sep_idx+1:]
                self._entries[idx] = char

    def decode_char(self, char):
        return self._entries[char]
