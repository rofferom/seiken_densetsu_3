import sd3.text


_CODE_TXT = [0x58, 0x5E]


def _build_byte_ignore_op(count):
    def do_ignore(op_id, seq_reader, observer):
        for _ in range(count):
            seq_reader()
            return None

    return do_ignore


def _sub_0x68(op_id, seq_reader, observer):
    # Skip two values
    for _ in range(2):
        seq_reader()

    # Two other values are often skipped, but the routine may
    # to read them. Raise an exception if some text ops are
    # ignored.
    byte1 = seq_reader()
    byte2 = seq_reader()

    intersection = list(set(_CODE_TXT) & {byte1, byte2})
    if intersection:
        raise Exception("Decode error (maybe skipping text)")

    return None


def get_op_map(rom):
    op_map = {
        0x55: _build_byte_ignore_op(1),
        0xFA: _build_byte_ignore_op(1),
        0x68: _sub_0x68
    }

    # Register text decoder
    txt_reader = sd3.text.Reader(rom)
    for txt_op in _CODE_TXT:
        op_map[txt_op] = txt_reader

    return op_map
