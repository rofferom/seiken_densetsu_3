import sd3.text


_CODE_TXT = [0x58, 0x5E]


def _read_n_bytes(n, seq_reader):
    for _ in range(n):
        seq_reader()


def sub_C43E81(op_id, seq_reader, observer):
    raise Exception("Subroutine C43E81 unimplemented (from op 0x%02X)" % op_id)


def sub_C43F02(op_id, seq_reader, observer):
    pass


def sub_C43B03(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43784(op_id, seq_reader, observer):
    raise Exception("Subroutine C43784 unimplemented (from op 0x%02X)" % op_id)


def sub_C44105(op_id, seq_reader, observer):
    pass


def sub_C43804(op_id, seq_reader, observer):
    raise Exception("Subroutine C43804 unimplemented (from op 0x%02X)" % op_id)


def sub_C43B87(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43688(op_id, seq_reader, observer):
    raise Exception("Subroutine C43688 unimplemented (from op 0x%02X)" % op_id)


def sub_C43D89(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C4390B(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C4410C(op_id, seq_reader, observer):
    pass


def sub_C43927(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43F0E(op_id, seq_reader, observer):
    pass


def sub_C43B0E(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43391(op_id, seq_reader, observer):
    pass


def sub_C43A13(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43D14(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43E14(op_id, seq_reader, observer):
    raise Exception("Subroutine C43E14 unimplemented (from op 0x%02X)" % op_id)


def sub_C43516(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43A97(op_id, seq_reader, observer):
    pass


def sub_C44198(op_id, seq_reader, observer):
    pass


def sub_C43B19(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43613(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43896(op_id, seq_reader, observer):
    _read_n_bytes(2, seq_reader)


def sub_C43F1C(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43E9D(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C434A0(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43978(op_id, seq_reader, observer):
    pass


def sub_C43B24(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C439A6(op_id, seq_reader, observer):
    pass


def sub_C43CA6(op_id, seq_reader, observer):
    pass


def sub_C43328(op_id, seq_reader, observer):
    pass


def sub_C43A27(op_id, seq_reader, observer):
    pass


def sub_C43AAA(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C440A6(op_id, seq_reader, observer):
    _read_n_bytes(2, seq_reader)


def sub_C435A9(op_id, seq_reader, observer):
    raise Exception("Subroutine C435A9 unimplemented (from op 0x%02X)" % op_id)


def sub_C43724(op_id, seq_reader, observer):
    raise Exception("Subroutine C43724 unimplemented (from op 0x%02X)" % op_id)


def sub_C433AE(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43B2F(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C437AE(op_id, seq_reader, observer):
    raise Exception("Subroutine C437AE unimplemented (from op 0x%02X)" % op_id)


def sub_C4382E(op_id, seq_reader, observer):
    raise Exception("Subroutine C4382E unimplemented (from op 0x%02X)" % op_id)


def sub_C43537(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43A39(op_id, seq_reader, observer):
    raise Exception("Subroutine C43A39 unimplemented (from op 0x%02X)" % op_id)


def sub_C43B3A(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43FBA(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C4363D(op_id, seq_reader, observer):
    # Skip two values
    _read_n_bytes(2, seq_reader)

    # Two other values are often skipped, but the routine may
    # to read them. Raise an exception if some text ops are
    # ignored.
    byte1 = seq_reader()
    byte2 = seq_reader()

    intersection = list(set(_CODE_TXT) & {byte1, byte2})
    if intersection:
        raise Exception("Decode error (maybe skipping text)")


def sub_C43443(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C439C4(op_id, seq_reader, observer):
    pass


def sub_C43B45(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43C46(op_id, seq_reader, observer):
    pass


def sub_C43BC6(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C435C7(op_id, seq_reader, observer):
    raise Exception("Subroutine C435C7 unimplemented (from op 0x%02X)" % op_id)


def sub_C438C3(op_id, seq_reader, observer):
    raise Exception("Subroutine C438C3 unimplemented (from op 0x%02X)" % op_id)


def sub_C434CB(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43CCC(op_id, seq_reader, observer):
    pass


def sub_C43DCD(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43B50(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43AD1(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43D52(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C436D3(op_id, seq_reader, observer):
    raise Exception("Subroutine C436D3 unimplemented (from op 0x%02X)" % op_id)


def sub_C43354(op_id, seq_reader, observer):
    pass


def sub_C43355(op_id, seq_reader, observer):
    pass


def sub_C439D4(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C44056(op_id, seq_reader, observer):
    _read_n_bytes(2, seq_reader)


def sub_C43458(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43F5A(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43B5B(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C4355B(op_id, seq_reader, observer):
    _read_n_bytes(2, seq_reader)


def sub_C437DA(op_id, seq_reader, observer):
    raise Exception("Subroutine C437DA unimplemented (from op 0x%02X)" % op_id)


def sub_C438E5(op_id, seq_reader, observer):
    raise Exception("Subroutine C438E5 unimplemented (from op 0x%02X)" % op_id)


def sub_C43B66(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43E67(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C435ED(op_id, seq_reader, observer):
    raise Exception("Subroutine C435ED unimplemented (from op 0x%02X)" % op_id)


def sub_C434EF(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43B71(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43CF5(op_id, seq_reader, observer):
    pass


def sub_C43C76(op_id, seq_reader, observer):
    pass


def sub_C43475(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43AF8(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C43779(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def sub_C43B7C(op_id, seq_reader, observer):
    _read_n_bytes(3, seq_reader)


def sub_C433FE(op_id, seq_reader, observer):
    _read_n_bytes(1, seq_reader)


def get_op_map(rom):
    op_map = {
        0x00: sub_C43328,
        0x01: sub_C43354,
        0x02: sub_C43978,
        0x03: sub_C439A6,
        0x04: sub_C439C4,
        0x05: sub_C43F02,
        0x06: sub_C43F0E,
        0x07: sub_C43C46,
        0x08: sub_C43C76,
        0x09: sub_C43CA6,
        0x0A: sub_C43CCC,
        0x0B: sub_C43A27,
        0x0C: sub_C43CF5,
        0x0D: sub_C43A97,
        0x0E: sub_C43391,
        0x0F: sub_C43355,
        0x10: sub_C433AE,
        0x11: sub_C433AE,
        0x12: sub_C433AE,
        0x13: sub_C433AE,
        0x14: sub_C433AE,
        0x15: sub_C433AE,
        0x16: sub_C433AE,
        0x17: sub_C433AE,
        0x18: sub_C433AE,
        0x19: sub_C433AE,
        0x1A: sub_C433AE,
        0x1B: sub_C433AE,
        0x1C: sub_C433AE,
        0x1D: sub_C433AE,
        0x1E: sub_C433AE,
        0x1F: sub_C433AE,
        0x20: sub_C433FE,
        0x21: sub_C433FE,
        0x22: sub_C433FE,
        0x23: sub_C433FE,
        0x24: sub_C433FE,
        0x25: sub_C433FE,
        0x26: sub_C433FE,
        0x27: sub_C433FE,
        0x28: sub_C433FE,
        0x29: sub_C433FE,
        0x2A: sub_C433FE,
        0x2B: sub_C433FE,
        0x2C: sub_C433FE,
        0x2D: sub_C433FE,
        0x2E: sub_C433FE,
        0x2F: sub_C433FE,
        0x30: sub_C43AAA,
        0x31: sub_C43AD1,
        0x32: sub_C43AF8,
        0x33: sub_C43B03,
        0x34: sub_C43B0E,
        0x35: sub_C43B19,
        0x36: sub_C43B24,
        0x37: sub_C43B2F,
        0x38: sub_C43B3A,
        0x39: sub_C43B45,
        0x3A: sub_C43B50,
        0x3B: sub_C43B5B,
        0x3C: sub_C43B66,
        0x3D: sub_C43B71,
        0x3E: sub_C43B7C,
        0x3F: sub_C43B87,
        0x40: sub_C43BC6,
        0x41: sub_C43BC6,
        0x42: sub_C43BC6,
        0x43: sub_C43BC6,
        0x44: sub_C43BC6,
        0x45: sub_C43BC6,
        0x46: sub_C43BC6,
        0x47: sub_C43BC6,
        0x48: sub_C43443,
        0x49: sub_C43475,
        0x4A: sub_C434A0,
        0x4B: sub_C434CB,
        0x4C: sub_C434EF,
        0x4D: sub_C43516,
        0x4E: sub_C43537,
        0x4F: sub_C439D4,
        0x50: sub_C43A13,
        0x51: sub_C43F1C,
        0x52: sub_C43F5A,
        0x53: sub_C43FBA,
        0x54: sub_C43D14,
        0x55: sub_C43D52,
        0x56: sub_C43E9D,
        0x57: sub_C43D89,
        0x59: sub_C4355B,
        0x5A: sub_C44056,
        0x5B: sub_C440A6,
        0x5C: sub_C44198,
        0x5D: sub_C44105,
        0x5F: sub_C43D89,
        0x60: sub_C435A9,
        0x61: sub_C43E14,
        0x62: sub_C435C7,
        0x63: sub_C435ED,
        0x64: sub_C43E67,
        0x65: sub_C43E81,
        0x66: sub_C43D89,
        0x67: sub_C43613,
        0x68: sub_C4363D,
        0x69: sub_C43688,
        0x6A: sub_C436D3,
        0x6B: sub_C43724,
        0x6C: sub_C43A39,
        0x6D: sub_C43779,
        0x6E: sub_C43458,
        0x6F: sub_C43DCD,
        0x70: sub_C43784,
        0x71: sub_C437AE,
        0x72: sub_C437DA,
        0x73: sub_C43804,
        0x74: sub_C4382E,
        0x75: sub_C43896,
        0x76: sub_C4410C,
        0x77: sub_C43D89,
        0x78: sub_C438C3,
        0x79: sub_C438E5,
        0x7A: sub_C4390B,
        0x7B: sub_C43927,
        0x7C: sub_C44198,
        0x7D: sub_C44198,
        0x7E: sub_C44198,
        0x7F: sub_C44198,
        0x80: sub_C43E9D,
        0x81: sub_C43E9D,
        0x82: sub_C43E9D,
        0x83: sub_C43E9D,
        0x84: sub_C43E9D,
        0x85: sub_C43E9D,
        0x86: sub_C43E9D,
        0x87: sub_C43E9D,
        0x88: sub_C43E9D,
        0x89: sub_C43E9D,
        0x8A: sub_C43E9D,
        0x8B: sub_C43E9D,
        0x8C: sub_C43E9D,
        0x8D: sub_C43E9D,
        0x8E: sub_C43E9D,
        0x8F: sub_C43E9D,
        0x90: sub_C43E9D,
        0x91: sub_C43E9D,
        0x92: sub_C43E9D,
        0x93: sub_C43E9D,
        0x94: sub_C43E9D,
        0x95: sub_C43E9D,
        0x96: sub_C43E9D,
        0x97: sub_C43E9D,
        0x98: sub_C43E9D,
        0x99: sub_C43E9D,
        0x9A: sub_C43E9D,
        0x9B: sub_C43E9D,
        0x9C: sub_C43E9D,
        0x9D: sub_C43E9D,
        0x9E: sub_C43E9D,
        0x9F: sub_C43E9D,
        0xA0: sub_C43E9D,
        0xA1: sub_C43E9D,
        0xA2: sub_C43E9D,
        0xA3: sub_C43E9D,
        0xA4: sub_C43E9D,
        0xA5: sub_C43E9D,
        0xA6: sub_C43E9D,
        0xA7: sub_C43E9D,
        0xA8: sub_C43E9D,
        0xA9: sub_C43E9D,
        0xAA: sub_C43E9D,
        0xAB: sub_C43E9D,
        0xAC: sub_C43E9D,
        0xAD: sub_C43E9D,
        0xAE: sub_C43E9D,
        0xAF: sub_C43E9D,
        0xB0: sub_C43E9D,
        0xB1: sub_C43E9D,
        0xB2: sub_C43E9D,
        0xB3: sub_C43E9D,
        0xB4: sub_C43E9D,
        0xB5: sub_C43E9D,
        0xB6: sub_C43E9D,
        0xB7: sub_C43E9D,
        0xB8: sub_C43E9D,
        0xB9: sub_C43E9D,
        0xBA: sub_C43E9D,
        0xBB: sub_C43E9D,
        0xBC: sub_C43E9D,
        0xBD: sub_C43E9D,
        0xBE: sub_C43E9D,
        0xBF: sub_C43E9D,
        0xC0: sub_C43E9D,
        0xC1: sub_C43E9D,
        0xC2: sub_C43E9D,
        0xC3: sub_C43E9D,
        0xC4: sub_C43E9D,
        0xC5: sub_C43E9D,
        0xC6: sub_C43E9D,
        0xC7: sub_C43E9D,
        0xC8: sub_C43E9D,
        0xC9: sub_C43E9D,
        0xCA: sub_C43E9D,
        0xCB: sub_C43E9D,
        0xCC: sub_C43E9D,
        0xCD: sub_C43E9D,
        0xCE: sub_C43E9D,
        0xCF: sub_C43E9D,
        0xD0: sub_C43E9D,
        0xD1: sub_C43E9D,
        0xD2: sub_C43E9D,
        0xD3: sub_C43E9D,
        0xD4: sub_C43E9D,
        0xD5: sub_C43E9D,
        0xD6: sub_C43E9D,
        0xD7: sub_C43E9D,
        0xD8: sub_C43E9D,
        0xD9: sub_C43E9D,
        0xDA: sub_C43E9D,
        0xDB: sub_C43E9D,
        0xDC: sub_C43E9D,
        0xDD: sub_C43E9D,
        0xDE: sub_C43E9D,
        0xDF: sub_C43E9D,
        0xE0: sub_C43E9D,
        0xE1: sub_C43E9D,
        0xE2: sub_C43E9D,
        0xE3: sub_C43E9D,
        0xE4: sub_C43E9D,
        0xE5: sub_C43E9D,
        0xE6: sub_C43E9D,
        0xE7: sub_C43E9D,
        0xE8: sub_C43E9D,
        0xE9: sub_C43E9D,
        0xEA: sub_C43E9D,
        0xEB: sub_C43E9D,
        0xEC: sub_C43E9D,
        0xED: sub_C43E9D,
        0xEE: sub_C43E9D,
        0xEF: sub_C43E9D,
        0xF0: sub_C43E9D,
        0xF1: sub_C43E9D,
        0xF2: sub_C43E9D,
        0xF3: sub_C43E9D,
        0xF4: sub_C43E9D,
        0xF5: sub_C43E9D,
        0xF6: sub_C43E9D,
        0xF7: sub_C43E9D,
        0xF8: sub_C43E9D,
        0xF9: sub_C43E9D,
        0xFA: sub_C43E9D,
        0xFB: sub_C43E9D,
        0xFC: sub_C43E9D,
        0xFD: sub_C43E9D,
        0xFE: sub_C43E9D,
        0xFF: sub_C43E9D,
    }

    # Register text decoder
    txt_reader = sd3.text.Reader(rom)
    for txt_op in _CODE_TXT:
        op_map[txt_op] = txt_reader

    return op_map
