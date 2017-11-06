import logging
import sd3.rom
import sd3.tree
import sd3.bitutils
import sd3.seq.ops


_PTR_BASE = 0xF80000


class ReadException(Exception):
    def __init__(self, op_id):
        super().__init__(self)
        self.op_id = op_id


class Observer:
    def text_decoded(self, decoded):
        pass


class Reader:
    def __init__(self, rom):
        self.rom = rom
        self.tree = sd3.tree.build_ctrl_tree(self.rom)
        self.op_map = sd3.seq.ops.get_op_map(self.rom)

    def _get_sequence_addr(self, idx):
        # Get bank
        if idx < 0x600:
            bank = 0xF9
        elif idx < 0xA00:
            bank = 0xFA
        elif idx < 0xC00:
            bank = 0xFB
        else:
            bank = 0xF8

        return self.rom.read_addr_from_ptr(_PTR_BASE, idx, bank)

    def _build_seq_reader(self, addr):
        bitreader = sd3.bitutils.BitReader.from_rom_u16_big(self.rom, addr)

        def reader_cb():
            v = self.tree.decode(bitreader)
            logging.debug("seq_reader: got %04X", v)
            return v

        return reader_cb

    def read_sequence(self, idx, observer):
        # Configure rom read
        seq_addr = self._get_sequence_addr(idx)
        seq_reader = self._build_seq_reader(seq_addr)

        # Decode control stream
        next_ctrl_byte = None
        while True:
            if next_ctrl_byte is not None:
                op_id = next_ctrl_byte
                next_ctrl_byte = None
                logging.debug("Ctrl byte: 0x%04X (from previous decode)",
                              op_id)
            else:
                op_id = seq_reader() & 0xFF
                logging.debug("Ctrl byte: 0x%04X (from ctrl stream)", op_id)

            if op_id == 0:
                logging.debug("End of stream")
                break

            op_cb = self.op_map[op_id]

            try:
                next_ctrl_byte = op_cb(op_id, seq_reader, observer)
            except Exception:
                logging.error("Operation code %02X processing failed", op_id)
                raise ReadException(op_id)
