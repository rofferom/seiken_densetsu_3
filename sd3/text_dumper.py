import enum
import logging
from collections import namedtuple
import sd3.seq.reader
import sd3.text_table

_SEQ_COUNT = 0x1000


class _SeqObserver(sd3.seq.reader.Observer):
    def __init__(self):
        self.decoded = []

    def text_decoded(self, decoded):
        self.decoded.append(decoded)


class _DecodeStatus(enum.Enum):
    ok = 1
    empty = 2


class DumpStats:
    def __init__(self):
        self.seq_count = 0
        self.seq_ok = 0
        self.seq_error = 0
        self.seq_empty = 0
        self.opcode_errors = {}

    def record_read_error(self, opcode, idx):
        if opcode not in self.opcode_errors:
            self.opcode_errors[opcode] = [idx]
        else:
            self.opcode_errors[opcode].append(idx)


class _Dumper:
    def __init__(self, rom, tbl_path, output_path):
        self.decoder = sd3.seq.reader.Reader(rom)

        self.tbl = sd3.text_table.Table()
        self.tbl.load(tbl_path)

        self.output_path = output_path
        self.out = None

    def _write_txt(self, txt, out):
        i = 0
        while i < len(txt):
            c = txt[i]

            if c >= 0x20:
                out.write("%s" % self.tbl.decode_char(c))
                i += 1
            elif c == 0x19:
                out.write("[Character:%02X]" % txt[i+1])
                i += 2
            elif c == 0x17:
                out.write("\n")
                i += 1
            else:
                out.write("[0x%02X]" % c)
                i += 1

    def _read_seq(self, idx, seq_addr, out):
        logging.info("Decoding %04X", idx)

        # The read sequence can fail if an operation code is unknown
        obs = _SeqObserver()
        self.decoder.read_sequence_from_addr(seq_addr, obs)

        # Some blocks are empty
        if not obs.decoded:
            return _DecodeStatus.empty

        out.write("Block 0x%04X" % idx)
        for i, txt in enumerate(obs.decoded):
            out.write("\nSublock %d\n" % i)
            self._write_txt(txt, out)

        out.write("\nEnd of block %04X\n\n" % idx)
        return _DecodeStatus.ok

    def run(self):
        known_seq_addr = set()
        stats = DumpStats()
        out = open(self.output_path, "w")

        for idx in range(_SEQ_COUNT):
            seq_addr = self.decoder.get_sequence_addr(idx)
            if seq_addr in known_seq_addr:
                logging.info("Skip %04X (already known)", idx)
                continue

            try:
                read_res = self._read_seq(idx, seq_addr, out)
                if read_res == _DecodeStatus.ok:
                    stats.seq_ok += 1
                elif read_res == _DecodeStatus.empty:
                    stats.seq_empty += 1
                else:
                    raise Exception("Unexpected read result %s" % read_res)
            except sd3.seq.reader.ReadException as e:
                stats.record_read_error(e.op_id, idx)
                stats.seq_error += 1

            known_seq_addr.add(seq_addr)
            stats.seq_count += 1

        out.close()

        return stats


def dump(rom, tbl_path, output_path):
    dumper = _Dumper(rom, tbl_path, output_path)
    return dumper.run()
