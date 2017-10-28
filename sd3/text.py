import logging
import sd3.rom
import sd3.tree
import sd3.bitutils


_MAIN_TREE_FIRST_IDX = 0
_MAIN_TREE_SECOND_IDX = 1

_SUB_TREE_FIRST_IDX = 2
_SUB_TREE_SECOND_IDX = 3

_SUBBLOCK_BASE = 0xF89800
_SUBBLOCK_BANK = 0xF8


class _TxtReader:
    def __init__(self, bitreader, tree, parent=None):
        self.bitreader = bitreader
        self.tree = tree
        self.parent = parent

    def read_char(self, tree_idx):
        return self.tree[tree_idx].decode(self.bitreader)

    def get_parent(self):
        return self.parent

    def get_pending_byte(self):
        if self.bitreader.count < 8:
            return None

        # Get the last 8 bits
        return (self.bitreader.value >> (16 - self.bitreader.count)) & 0xFF


class Reader:
    def __init__(self, rom):
        self.rom = sd3.rom.Rom.from_rom(rom)

        self.txt_main_tree = [
            sd3.tree.build_txt_tree(self.rom, _MAIN_TREE_FIRST_IDX),
            sd3.tree.build_txt_tree(self.rom, _MAIN_TREE_SECOND_IDX)
        ]

        self.txt_sub_tree = [
            sd3.tree.build_txt_tree(self.rom, _SUB_TREE_FIRST_IDX),
            sd3.tree.build_txt_tree(self.rom, _SUB_TREE_SECOND_IDX)
        ]

    def _build_main_txt_reader(self, seq_reader):
        def bitreader_provider():
            high = seq_reader() & 0xFF
            low = seq_reader() & 0xFF

            return (high << 8) | low

        bitreader = sd3.bitutils.BitReader.from_src(bitreader_provider, 16)

        return _TxtReader(bitreader, self.txt_main_tree)

    def _build_sub_txt_reader(self, idx, parent):
        idx -= 0x040C

        addr = self.rom.read_addr_from_ptr(
            _SUBBLOCK_BASE, idx, _SUBBLOCK_BANK)
        logging.debug("Jump to: %X", addr)

        bitreader = sd3.bitutils.BitReader.from_rom_u16_big(self.rom, addr)

        return _TxtReader(bitreader, self.txt_sub_tree, parent)

    def __call__(self, op_id, seq_reader, observer):
        decoded = []

        # Setup main text reader
        main_txt_reader = self._build_main_txt_reader(seq_reader)

        # Default reader is main text reader
        # It can be replaced by a sub reader
        last_reader = None
        txt_reader = main_txt_reader

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
                    txt_reader = self._build_sub_txt_reader(char, txt_reader)
            else:
                decoded.append(char)

        logging.debug("Partial decode: %s", decoded)
        observer.text_decoded(decoded)

        return last_reader.get_pending_byte()
