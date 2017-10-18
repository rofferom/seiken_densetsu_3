from sd3.disasm.attributes import Attr
from sd3.disasm.addr_modes import AddrMode


class OperandDesc:
    def __init__(self, *, mnemonic, opcodes, attrs=None):
        self.mnemonic = mnemonic
        self.opcodes = opcodes

        if attrs is None:
            self.attrs = []
        else:
            self.attrs = attrs


class OpcodeDesc:
    def __init__(self, opcode, addr_mode, attrs=None):
        self.opcode = opcode
        self.addr_mode = addr_mode

        if attrs is None:
            self.attrs = []
        else:
            self.attrs = attrs


def get_desc_list():
    return [
        OperandDesc(
            mnemonic="ADC",
            opcodes=[
                OpcodeDesc(0x65, AddrMode.direct),
                OpcodeDesc(0x6D, AddrMode.absolute),
                OpcodeDesc(0x6F, AddrMode.absolute_long),
                OpcodeDesc(0x7F, AddrMode.absolute_long_indexed, [Attr.indexed_x]),
                OpcodeDesc(0x69, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0x7D, AddrMode.absolute_indexed, [Attr.indexed_x]),
                OpcodeDesc(0x79, AddrMode.absolute_indexed, [Attr.indexed_y]),
                OpcodeDesc(0x63, AddrMode.stack_relative),
                OpcodeDesc(0x71, AddrMode.direct_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="AND",
            opcodes=[
                OpcodeDesc(0x25, AddrMode.direct),
                OpcodeDesc(0x2D, AddrMode.absolute),
                OpcodeDesc(0x29, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0x31, AddrMode.direct_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="ASL",
            opcodes=[
                OpcodeDesc(0x06, AddrMode.direct),
                OpcodeDesc(0x0A, AddrMode.accumulator),
                OpcodeDesc(0x0E, AddrMode.absolute),
                OpcodeDesc(0x1E, AddrMode.absolute_indexed, [Attr.indexed_x]),
            ]
        ),
        OperandDesc(
            mnemonic="BCC",
            opcodes=[
                OpcodeDesc(0x90, AddrMode.pc_relative),
            ],
            attrs=[Attr.branch]
        ),
        OperandDesc(
            mnemonic="BCS",
            opcodes=[
                OpcodeDesc(0xB0, AddrMode.pc_relative),
            ],
            attrs=[Attr.branch]
        ),
        OperandDesc(
            mnemonic="BEQ",
            opcodes=[
                OpcodeDesc(0xF0, AddrMode.pc_relative),
            ],
            attrs=[Attr.branch]
        ),
        OperandDesc(
            mnemonic="BIT",
            opcodes=[
                OpcodeDesc(0x24, AddrMode.direct),
                OpcodeDesc(0x89, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0x3C, AddrMode.absolute_indexed, [Attr.indexed_x]),
            ]
        ),
        OperandDesc(
            mnemonic="BMI",
            opcodes=[
                OpcodeDesc(0x30, AddrMode.pc_relative),
            ],
            attrs=[Attr.branch]
        ),
        OperandDesc(
            mnemonic="BNE",
            opcodes=[
                OpcodeDesc(0xD0, AddrMode.pc_relative),
            ],
            attrs=[Attr.branch]
        ),
        OperandDesc(
            mnemonic="BPL",
            opcodes=[
                OpcodeDesc(0x10, AddrMode.pc_relative),
            ],
            attrs=[Attr.branch]
        ),
        OperandDesc(
            mnemonic="BRA",
            opcodes=[
                OpcodeDesc(0x80, AddrMode.pc_relative),
            ],
            attrs=[Attr.branch, Attr.unconditional]
        ),
        OperandDesc(
            mnemonic="BRK",
            opcodes=[
                OpcodeDesc(0x00, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="CLC",
            opcodes=[
                OpcodeDesc(0x18, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="CLD",
            opcodes=[
                OpcodeDesc(0xD8, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="CLI",
            opcodes=[
                OpcodeDesc(0x58, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="CLV",
            opcodes=[
                OpcodeDesc(0xB8, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="CMP",
            opcodes=[
                OpcodeDesc(0xC5, AddrMode.direct),
                OpcodeDesc(0xD5, AddrMode.direct_indexed, [Attr.indexed_x]),
                OpcodeDesc(0xCD, AddrMode.absolute),
                OpcodeDesc(0xCF, AddrMode.absolute_long),
                OpcodeDesc(0xC9, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0xC3, AddrMode.stack_relative),
                OpcodeDesc(0xD9, AddrMode.absolute_indexed, [Attr.indexed_y]),
                OpcodeDesc(0xDD, AddrMode.absolute_indexed, [Attr.indexed_x]),
                OpcodeDesc(0xDF, AddrMode.absolute_long_indexed, [Attr.indexed_x]),
                OpcodeDesc(0xD7, AddrMode.indirect_long_indexed, [Attr.indexed_y]),
                OpcodeDesc(0xD1, AddrMode.direct_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="COP",
            opcodes=[
                OpcodeDesc(0x02, AddrMode.immediate),
            ]
        ),
        OperandDesc(
            mnemonic="CPX",
            opcodes=[
                OpcodeDesc(0xE0, AddrMode.immediate, [Attr.x_dependant]),
                OpcodeDesc(0xE4, AddrMode.direct),
                OpcodeDesc(0xEC, AddrMode.absolute),
            ]
        ),
        OperandDesc(
            mnemonic="CPY",
            opcodes=[
                OpcodeDesc(0xC4, AddrMode.direct),
                OpcodeDesc(0xC0, AddrMode.immediate, [Attr.x_dependant]),
            ]
        ),
        OperandDesc(
            mnemonic="DEC",
            opcodes=[
                OpcodeDesc(0x3A, AddrMode.accumulator),
                OpcodeDesc(0xC6, AddrMode.direct),
                OpcodeDesc(0xCE, AddrMode.absolute),
                OpcodeDesc(0xDE, AddrMode.absolute_indexed, [Attr.indexed_x]),
            ]
        ),
        OperandDesc(
            mnemonic="DEX",
            opcodes=[
                OpcodeDesc(0xCA, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="DEY",
            opcodes=[
                OpcodeDesc(0x88, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="EOR",
            opcodes=[
                OpcodeDesc(0x45, AddrMode.direct),
                OpcodeDesc(0x49, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0x51, AddrMode.direct_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="INC",
            opcodes=[
                OpcodeDesc(0xE6, AddrMode.direct),
                OpcodeDesc(0x1A, AddrMode.accumulator),
                OpcodeDesc(0xEE, AddrMode.absolute),
                OpcodeDesc(0xFE, AddrMode.absolute_indexed, [Attr.indexed_x]),
            ]
        ),
        OperandDesc(
            mnemonic="INX",
            opcodes=[
                OpcodeDesc(0xE8, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="INY",
            opcodes=[
                OpcodeDesc(0xC8, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="JMP",
            opcodes=[
                OpcodeDesc(0x4C, AddrMode.absolute),
                OpcodeDesc(0x5C, AddrMode.absolute_long),
            ],
            attrs=[Attr.jump]
        ),
        OperandDesc(
            mnemonic="JSL",
            opcodes=[
                OpcodeDesc(0x22, AddrMode.absolute_long),
                OpcodeDesc(0xFC, AddrMode.absolute_indexed_indirect, [Attr.indexed_x]),
            ],
            attrs=[Attr.enter_sub]
        ),
        OperandDesc(
            mnemonic="JSR",
            opcodes=[
                OpcodeDesc(0x20, AddrMode.absolute),
            ],
            attrs=[Attr.enter_sub]
        ),
        OperandDesc(
            mnemonic="LDA",
            opcodes=[
                OpcodeDesc(0xA9, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0xA5, AddrMode.direct),
                OpcodeDesc(0xB2, AddrMode.indirect),
                OpcodeDesc(0xB5, AddrMode.direct_indexed, [Attr.indexed_x]),
                OpcodeDesc(0xAD, AddrMode.absolute),
                OpcodeDesc(0xBF, AddrMode.absolute_long_indexed, [Attr.indexed_x]),
                OpcodeDesc(0xBD, AddrMode.absolute_indexed, [Attr.indexed_x]),
                OpcodeDesc(0xB9, AddrMode.absolute_indexed, [Attr.indexed_y]),
                OpcodeDesc(0xA3, AddrMode.stack_relative),
                OpcodeDesc(0xAF, AddrMode.absolute_long),
                OpcodeDesc(0xA7, AddrMode.indirect_long),
                OpcodeDesc(0xB1, AddrMode.indirect_indexed, [Attr.indexed_y]),
                OpcodeDesc(0xB7, AddrMode.indirect_long_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="LDX",
            opcodes=[
                OpcodeDesc(0xAE, AddrMode.absolute),
                OpcodeDesc(0xBE, AddrMode.absolute_indexed, [Attr.indexed_y]),
                OpcodeDesc(0xA6, AddrMode.direct),
                OpcodeDesc(0xA2, AddrMode.immediate, [Attr.x_dependant]),
            ]
        ),
        OperandDesc(
            mnemonic="LDY",
            opcodes=[
                OpcodeDesc(0xAC, AddrMode.absolute),
                OpcodeDesc(0xA0, AddrMode.immediate, [Attr.x_dependant]),
                OpcodeDesc(0xA4, AddrMode.direct),
                OpcodeDesc(0xBC, AddrMode.absolute_indexed, [Attr.indexed_x]),
            ]
        ),
        OperandDesc(
            mnemonic="LSR",
            opcodes=[
                OpcodeDesc(0x4A, AddrMode.accumulator),
                OpcodeDesc(0x46, AddrMode.direct),
            ]
        ),
        OperandDesc(
            mnemonic="NOP",
            opcodes=[
                OpcodeDesc(0xEA, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="MVN",
            opcodes=[
                OpcodeDesc(0x54, AddrMode.block_move),
            ]
        ),
        OperandDesc(
            mnemonic="MVP",
            opcodes=[
                OpcodeDesc(0x44, AddrMode.block_move),
            ]
        ),
        OperandDesc(
            mnemonic="ORA",
            opcodes=[
                OpcodeDesc(0x05, AddrMode.direct),
                OpcodeDesc(0x0D, AddrMode.absolute),
                OpcodeDesc(0x0F, AddrMode.absolute_long),
                OpcodeDesc(0x03, AddrMode.stack_relative),
                OpcodeDesc(0x09, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0x1D, AddrMode.absolute_indexed, [Attr.indexed_x]),
                OpcodeDesc(0x19, AddrMode.absolute_indexed, [Attr.indexed_y]),
                OpcodeDesc(0x11, AddrMode.direct_indexed, [Attr.indexed_y]),
                OpcodeDesc(0x07, AddrMode.indirect_long),
                OpcodeDesc(0x17, AddrMode.indirect_long_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="PEA",
            opcodes=[
                OpcodeDesc(0xF4, AddrMode.absolute),
            ]
        ),
        OperandDesc(
            mnemonic="PHA",
            opcodes=[
                OpcodeDesc(0x48, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PHB",
            opcodes=[
                OpcodeDesc(0x8B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PHD",
            opcodes=[
                OpcodeDesc(0x0B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PHK",
            opcodes=[
                OpcodeDesc(0x4B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PHP",
            opcodes=[
                OpcodeDesc(0x08, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PHX",
            opcodes=[
                OpcodeDesc(0xDA, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PHY",
            opcodes=[
                OpcodeDesc(0x5A, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PLA",
            opcodes=[
                OpcodeDesc(0x68, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PLB",
            opcodes=[
                OpcodeDesc(0xAB, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PLD",
            opcodes=[
                OpcodeDesc(0x2B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PLP",
            opcodes=[
                OpcodeDesc(0x28, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PLX",
            opcodes=[
                OpcodeDesc(0xFA, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="PLY",
            opcodes=[
                OpcodeDesc(0x7A, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="REP",
            opcodes=[
                OpcodeDesc(0xC2, AddrMode.immediate, [Attr.reset_p]),
            ]
        ),
        OperandDesc(
            mnemonic="ROL",
            opcodes=[
                OpcodeDesc(0x26, AddrMode.direct),
                OpcodeDesc(0x2A, AddrMode.accumulator),
                OpcodeDesc(0x2E, AddrMode.absolute),
            ]
        ),
        OperandDesc(
            mnemonic="ROR",
            opcodes=[
                OpcodeDesc(0x6A, AddrMode.accumulator),
                OpcodeDesc(0x7E, AddrMode.absolute_indexed, [Attr.indexed_x]),
            ]
        ),
        OperandDesc(
            mnemonic="RTI",
            opcodes=[
                OpcodeDesc(0x40, AddrMode.none),
            ],
            attrs=[Attr.return_sub]
        ),
        OperandDesc(
            mnemonic="RTL",
            opcodes=[
                OpcodeDesc(0x6B, AddrMode.none),
            ],
            attrs=[Attr.return_sub]
        ),
        OperandDesc(
            mnemonic="RTS",
            opcodes=[
                OpcodeDesc(0x60, AddrMode.none),
            ],
            attrs=[Attr.return_sub]
        ),
        OperandDesc(
            mnemonic="SBC",
            opcodes=[
                OpcodeDesc(0xE9, AddrMode.immediate, [Attr.m_dependant]),
                OpcodeDesc(0xE5, AddrMode.direct),
                OpcodeDesc(0xED, AddrMode.absolute),
                OpcodeDesc(0xFD, AddrMode.absolute_indexed, [Attr.indexed_x]),
                OpcodeDesc(0xF9, AddrMode.absolute_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="SEC",
            opcodes=[
                OpcodeDesc(0x38, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="SED",
            opcodes=[
                OpcodeDesc(0xF8, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="SEI",
            opcodes=[
                OpcodeDesc(0x78, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="SEP",
            opcodes=[
                OpcodeDesc(0xE2, AddrMode.immediate, [Attr.set_p]),
            ]
        ),
        OperandDesc(
            mnemonic="STA",
            opcodes=[
                OpcodeDesc(0x85, AddrMode.direct),
                OpcodeDesc(0x95, AddrMode.direct_indexed, [Attr.indexed_x]),
                OpcodeDesc(0x92, AddrMode.indirect),
                OpcodeDesc(0x83, AddrMode.stack_relative),
                OpcodeDesc(0x8D, AddrMode.absolute),
                OpcodeDesc(0x8F, AddrMode.absolute_long),
                OpcodeDesc(0x99, AddrMode.absolute_indexed, [Attr.indexed_y]),
                OpcodeDesc(0x9D, AddrMode.absolute_indexed, [Attr.indexed_x]),
                OpcodeDesc(0x9F, AddrMode.absolute_long_indexed, [Attr.indexed_x]),
                OpcodeDesc(0x91, AddrMode.indirect_indexed, [Attr.indexed_y]),
                OpcodeDesc(0x97, AddrMode.indirect_long_indexed, [Attr.indexed_y]),
            ]
        ),
        OperandDesc(
            mnemonic="STX",
            opcodes=[
                OpcodeDesc(0x86, AddrMode.direct),
                OpcodeDesc(0x8E, AddrMode.absolute),
            ]
        ),
        OperandDesc(
            mnemonic="STY",
            opcodes=[
                OpcodeDesc(0x84, AddrMode.direct),
                OpcodeDesc(0x8C, AddrMode.absolute),
            ]
        ),
        OperandDesc(
            mnemonic="STZ",
            opcodes=[
                OpcodeDesc(0x9C, AddrMode.absolute),
                OpcodeDesc(0x64, AddrMode.direct),
                OpcodeDesc(0x9E, AddrMode.absolute_indexed, [Attr.indexed_x]),
                OpcodeDesc(0x74, AddrMode.direct_indexed, [Attr.indexed_x]),
            ]
        ),
        OperandDesc(
            mnemonic="TAX",
            opcodes=[
                OpcodeDesc(0xAA, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TAY",
            opcodes=[
                OpcodeDesc(0xA8, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TCD",
            opcodes=[
                OpcodeDesc(0x5B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TCS",
            opcodes=[
                OpcodeDesc(0x1B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TDB",
            opcodes=[
                OpcodeDesc(0x14, AddrMode.direct),
            ]
        ),
        OperandDesc(
            mnemonic="TDC",
            opcodes=[
                OpcodeDesc(0x7B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TSB",
            opcodes=[
                OpcodeDesc(0x04, AddrMode.direct),
                OpcodeDesc(0x0C, AddrMode.absolute),
            ]
        ),
        OperandDesc(
            mnemonic="TSC",
            opcodes=[
                OpcodeDesc(0x3B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TSX",
            opcodes=[
                OpcodeDesc(0xBA, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TXA",
            opcodes=[
                OpcodeDesc(0x8A, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TXS",
            opcodes=[
                OpcodeDesc(0x9A, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TXY",
            opcodes=[
                OpcodeDesc(0x9B, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TYA",
            opcodes=[
                OpcodeDesc(0x98, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="TYX",
            opcodes=[
                OpcodeDesc(0xBB, AddrMode.none),
            ]
        ),
        OperandDesc(
            mnemonic="XBA",
            opcodes=[
                OpcodeDesc(0xEB, AddrMode.none),
            ]
        ),
    ]
