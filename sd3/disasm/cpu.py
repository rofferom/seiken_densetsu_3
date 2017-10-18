import logging
import sd3.disasm.operands
import sd3.disasm.addr_modes
import sd3.disasm.routine
from sd3.disasm.attributes import Attr


class PRegister:
    def __init__(self, *, X, M):
        self.X = X
        self.M = M

    def clone(self):
        return PRegister(X=self.X, M=self.M)


class Opcode:
    def __init__(self, mnemonic, operand_attrs, opcode_desc):
        self.mnemonic = mnemonic
        self.addr_mode = opcode_desc.addr_mode

        self.attrs = list(operand_attrs)
        self.attrs.extend(opcode_desc.attrs)


class Reader:
    def __init__(self, rom):
        self.rom = rom
        self._build_opcode_map()
        self._build_addr_modes_map()

    def _build_opcode_map(self):
        self.opcode_map = {}
        mnemonic_set = set()

        for operand in sd3.disasm.operands.get_desc_list():
            if operand.mnemonic in mnemonic_set:
                raise Exception(
                    "Mnemonic %s is already registered" % operand.mnemonic)

            for opcode in operand.opcodes:
                new_opcode = Opcode(operand.mnemonic, operand.attrs, opcode)

                if opcode.opcode in self.opcode_map:
                    raise Exception(
                        "Opcode %02X is already registered" % opcode.opcode)

                self.opcode_map[opcode.opcode] = new_opcode

            mnemonic_set.add(operand.mnemonic)

    def _build_addr_modes_map(self):
        self.addr_modes_map = {}

        for mode_cls in sd3.disasm.addr_modes.get_addr_mode_list():
            mode = mode_cls()
            self.addr_modes_map[mode.mode] = mode

        return self.addr_modes_map

    def _get_opcode(self):
        code = self.rom.read_u8()
        if code not in self.opcode_map:
            raise Exception("Opcode %02X unknown" % code)

        return self.opcode_map[code]

    def _get_addr_mode(self, opcode):
        mode_id = opcode.addr_mode
        if mode_id not in self.addr_modes_map:
            raise Exception("Addressing mode '%s' unimplemented" % mode_id)

        return self.addr_modes_map[mode_id]

    def _read_instruction(self, p):
        instr = sd3.disasm.routine.Instruction()

        instr.addr = self.rom.tell()
        instr.opcode = self._get_opcode()
        instr.addr_mode = self._get_addr_mode(instr.opcode)

        param, param_len = instr.addr_mode.read_param(
            self.rom, instr.opcode, p)

        instr.param = param
        instr.param_len = param_len

        return instr

    def read_routine(self, addr, p):
        routine = sd3.disasm.routine.Routine(addr)

        logging.debug("Read routine 0x%06X", addr)
        self.rom.seek(addr)

        while True:
            # Build instruction
            instr = self._read_instruction(p)
            routine.add_instruction(instr)

            # The instruction can update P. Request update.
            instr.update_p(p)

            if instr.has_attr(Attr.enter_sub):
                target = instr.get_jump_target()
                if not target:
                    logging.debug("Ignore jump")
                    continue

                routine.add_subroutine(target, p)
            elif instr.has_attr(Attr.return_sub):
                next_jump = routine.get_next_jump()
                if next_jump:
                    logging.debug("Jump to %06X", next_jump)
                    self.rom.seek(next_jump)
                else:
                    break
            elif instr.has_attr(Attr.branch):
                target = instr.get_jump_target()

                new_jump = routine.add_jump(target)
                if new_jump:
                    logging.debug("Make branch to %06X as pending", target)
                else:
                    logging.debug("Branch to %06X ignored", target)
            elif instr.has_attr(Attr.jump):
                target = instr.get_jump_target()
                is_new_jump = routine.add_jump(target)
                if is_new_jump:
                    logging.debug("Jump to %06X", target)
                    self.rom.seek(target)
                else:
                    logging.debug("Jump to %06X ignored", target)

        return routine
