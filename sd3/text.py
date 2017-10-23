import logging
import sd3.rom
import sd3.tree
import sd3.bitutils

_CODE_TXT = [0x58, 0x5E]

_MAIN_TREE_FIRST_IDX = 0
_MAIN_TREE_SECOND_IDX = 1

_SUB_TREE_FIRST_IDX = 2
_SUB_TREE_SECOND_IDX = 3

_PTR_BASE = 0xF80000
_TXT_BANK = 0xF9

_SUBBLOCK_BASE = 0xF89800
_SUBBLOCK_BANK = 0xF8


class _RomReader:
    def __init__(self, rom, addr):
        self.rom = rom
        self.addr = addr

    def __call__(self):
        self.rom.seek(self.addr)
        value = self.rom.read_u16(endianess=sd3.rom.BIG_ENDIAN)
        self.addr = self.rom.tell()

        return value


class _CtrlReader:
    def __init__(self, reader, tree):
        self.reader = reader
        self.tree = tree

    def __call__(self):
        high = self.tree.decode(self.reader) & 0xFF
        low = self.tree.decode(self.reader) & 0xFF

        return (high << 8) | low


class _Reader:
    def __init__(self, reader, tree, parent=None):
        self.reader = reader
        self.tree = tree
        self.parent = parent

    def read_char(self, tree_idx):
        return self.tree[tree_idx].decode(self.reader)

    def get_parent(self):
        return self.parent

    def get_pending_byte(self):
        if self.reader.count < 8:
            return None

        # Get the last 8 bits
        return (self.reader.value >> (16 - self.reader.count)) & 0xFF


class Decoder:
    def __init__(self, rom):
        self.rom = rom

        self.ctrl_tree = sd3.tree.build_ctrl_tree(self.rom)

        self.txt_main_tree = [
            sd3.tree.build_txt_tree(self.rom, _MAIN_TREE_FIRST_IDX),
            sd3.tree.build_txt_tree(self.rom, _MAIN_TREE_SECOND_IDX)
        ]

        self.txt_sub_tree = [
            sd3.tree.build_txt_tree(self.rom, _SUB_TREE_FIRST_IDX),
            sd3.tree.build_txt_tree(self.rom, _SUB_TREE_SECOND_IDX)
        ]

        self.op_map = self._build_operation_map()

        self.decoded = None

    def _build_operation_map(self):
        op_map = {
            0x1C: self._build_byte_ignore_op(1),
            0x55: self._build_byte_ignore_op(1),
            0xFA: self._build_byte_ignore_op(1),
            0x68: self._sub_0x68
        }

        for i in _CODE_TXT:
            op_map[i] = self._read_dialog

        return op_map

    def _build_byte_ignore_op(self, count):
        def do_ignore(ctrl_reader):
            for _ in range(count):
                self.ctrl_tree.decode(ctrl_reader)
                return None

        return do_ignore

    def _sub_0x68(self, ctrl_reader):
        # Skip two values
        self.ctrl_tree.decode(ctrl_reader)
        self.ctrl_tree.decode(ctrl_reader)

        # Two other values are often skipped, but the routine may
        # to read them. Raise an exception if some text ops are
        # ignored.
        byte1 = self.ctrl_tree.decode(ctrl_reader)
        byte2 = self.ctrl_tree.decode(ctrl_reader)

        intersection = list(set(_CODE_TXT) & {byte1, byte2})
        if intersection:
            raise Exception("Decode error (maybe skipping text)")

        return None

    def _get_text_addr(self, idx):
        # Get bank
        if idx < 0x600:
            bank = 0xF9
        elif idx < 0xA00:
            bank = 0xFA
        elif idx < 0xC00:
            bank = 0xFB
        else:
            raise Exception("Unexpected bank")

        return self.rom.read_addr_from_ptr(_PTR_BASE, idx, bank)

    def _read_dialog(self, ctrl_reader):
        decoded = []

        # Setup main text reader
        txt_main_reader = _Reader(
            sd3.bitutils.BitReader(
                _CtrlReader(ctrl_reader, self.ctrl_tree), 16),
            self.txt_main_tree)

        # Default reader is main text reader
        # It can be replaced by a sub reader
        last_reader = None
        txt_reader = txt_main_reader

        # Start decode
        while txt_reader is not None:
            char = txt_reader.read_char(tree_idx=0)

            if char == 0:
                last_reader = txt_reader
                txt_reader = txt_reader.get_parent()
            elif char < 0x10:
                char = (char << 8) | txt_reader.read_char(tree_idx=1)
                if char < 0x400:
                    decoded.append(char)
                elif char < 0x410:
                    char &= 0xFF
                    decoded.append(char)
                else:
                    txt_reader = self._build_sub_reader(char, txt_reader)
            else:
                decoded.append(char)

        logging.debug("Partial decode: %s", decoded)
        self.decoded.append(decoded)
        return last_reader.get_pending_byte()

    def _build_sub_reader(self, idx, parent):
        idx -= 0x040C

        addr = self.rom.read_addr_from_ptr(
            _SUBBLOCK_BASE, idx, _SUBBLOCK_BANK)
        logging.debug("Jump to: %X", addr)

        return _Reader(
            sd3.bitutils.BitReader(_RomReader(self.rom, addr), 16),
            self.txt_sub_tree,
            parent)

    def get_dialog(self, idx):
        # Configure rom read
        txt_addr = self._get_text_addr(idx)

        ctrl_reader = sd3.bitutils.BitReader(
            _RomReader(self.rom, txt_addr), 16)

        # Decode control stream
        self.decoded = []
        next_ctrl_byte = None
        while True:
            if next_ctrl_byte is not None:
                op_id = next_ctrl_byte
                next_ctrl_byte = None
                logging.debug("Ctrl byte: 0x%04X (from previous decode)",
                              op_id)
            else:
                op_id = self.ctrl_tree.decode(ctrl_reader) & 0xFF
                logging.debug("Ctrl byte: 0x%04X (from ctrl stream)", op_id)

            if op_id == 0:
                logging.debug("End of stream")
                break

            try:
                op_cb = self.op_map[op_id]
            except KeyError:
                logging.error("Unknown operation code %02X", op_id)
                raise

            next_ctrl_byte = op_cb(ctrl_reader)

        return self.decoded
