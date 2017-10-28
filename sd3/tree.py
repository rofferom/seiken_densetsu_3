import logging
from collections import namedtuple

import sd3.bitutils
import sd3.rom

_TreeCfg = namedtuple("_TreeCfg", ["depth_size", "depth_offset", "data_size"])


class _CtrlTreeDecoder:
    def __init__(self, reader, cfg, depth):
        self.reader = reader
        self.cfg = cfg
        self.depth = depth


class _DecodeTreeDecoder:
    def __init__(self, rom, tree_addr, data_offset):
        self.rom = rom
        self.tree_addr = tree_addr
        self.data_offset = data_offset


class Node:
    def __init__(self):
        self.value = None
        self.children = [None, None]


class Tree:
    def __init__(self, root):
        self.root = root

    def decode(self, reader):
        node = self.root

        while node.value is None:
            bit = reader.read_bits(1)
            node = node.children[bit]

        return node.value


def _get_next_depth(reader, cfg):
    return reader.read_bits(cfg.depth_size) + cfg.depth_offset


def _decode_ctrl_tree(decoder, current_depth=0):
    if current_depth == decoder.depth:
        node = Node()
        node.value = decoder.reader.read_bits(decoder.cfg.data_size)

        decoder.depth = _get_next_depth(decoder.reader, decoder.cfg)
    else:
        current_depth += 1

        node = Node()
        node.children[0] = _decode_ctrl_tree(decoder, current_depth)
        node.children[1] = _decode_ctrl_tree(decoder, current_depth)

    return node


def build_ctrl_tree(rom):
    PTR_ADDR = 0xF82000
    TREE_BANK = 0xF8
    WORD_SIZE = 16

    # Configure ROM reader
    rom.seek(PTR_ADDR)
    addr = (TREE_BANK << 16) | rom.read_u16()
    logging.debug("Build tree at address 0x%06X", addr)
    rom.seek(addr)

    # Configure bit reader
    def rom_reader():
        return rom.read_u16(endianess=sd3.rom.BIG_ENDIAN)

    reader = sd3.bitutils.BitReader.from_src(rom_reader, WORD_SIZE)

    # Decode config
    reader.read_bits(4)  # Ignore first 4 bits
    depth_size = reader.read_bits(4)
    depth_offset = reader.read_bits(4)
    data_size = reader.read_bits(4)

    # Read 16 bits that are used to compute write offset in RAM.
    # Not required for us.
    reader.read_bits(16)

    # Get depth of the first branch
    cfg = _TreeCfg(depth_size, depth_offset, data_size)
    depth = _get_next_depth(reader, cfg)

    # Configure and run decode
    decoder = _CtrlTreeDecoder(reader, cfg, depth)

    root = _decode_ctrl_tree(decoder)

    return Tree(root)


def _decode_txt_tree(decoder, idx=1):
    U16_SIZE = 2

    if idx >= decoder.data_offset:
        node = Node()

        # Go to node
        addr = decoder.tree_addr + decoder.data_offset + idx
        decoder.rom.seek(addr)

        node.value = decoder.rom.read_u8()
    else:
        node = Node()

        # Go to node
        addr = decoder.tree_addr + U16_SIZE * idx

        # Visit children
        for i in range(2):
            decoder.rom.seek(addr + i)
            offset = decoder.rom.read_u8()
            next_idx = idx + offset + 1
            node.children[i] = _decode_txt_tree(decoder, next_idx)

    return node


def build_txt_tree(rom, idx):
    PTR_BASE = 0xF89800
    TREE_BANK = 0xF8

    # Read tree address
    tree_addr = rom.read_addr_from_ptr(PTR_BASE, idx, TREE_BANK)
    rom.seek(tree_addr)

    data_offset = rom.read_u16(endianess=sd3.rom.BIG_ENDIAN) + 1
    logging.debug("data_offset=0x%04X", data_offset)

    decoder = _DecodeTreeDecoder(rom, tree_addr, data_offset)
    root = _decode_txt_tree(decoder)

    return Tree(root)
