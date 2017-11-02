import os
import tempfile
import unittest
import sd3.cfa.cfg
import sd3.disasm.cpu
import sd3.disasm.routine
import sd3.disasm.operands
from sd3.disasm.attributes import Attr
from sd3.disasm.addr_modes import AddrMode, AddrModePcRelative, AddrModeNone

class TestCfg(unittest.TestCase):
    def test_cfg(self):
        empty_opcode = sd3.disasm.cpu.Opcode(
            "FakeMnemonic",
            [],
            sd3.disasm.operands.OpcodeDesc(
                0,
                AddrMode.none
            ))

        routine = sd3.disasm.routine.Routine(0x0)

        # Create a first block of 3 instruction
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x0
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x1
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x2
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        # Create a small block that be used for a futur jump
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x3
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x4
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        # Add a branch in the block
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x5
        inst.addr_mode = AddrModePcRelative()
        inst.param = 0x3
        inst.param_len = 1

        inst.opcode = sd3.disasm.cpu.Opcode(
            "BCS",
            [Attr.branch],
            sd3.disasm.operands.OpcodeDesc(
                0,
                AddrMode.pc_relative
            )
        )

        routine.add_instruction(inst)

        # Add false branch
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x7
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x8
        inst.addr_mode = AddrModePcRelative()
        inst.param = 0x1
        inst.param_len = 1

        inst.opcode = sd3.disasm.cpu.Opcode(
            "BRA",
            [Attr.branch, Attr.unconditional],
            sd3.disasm.operands.OpcodeDesc(
                0,
                AddrMode.pc_relative
            )
        )

        routine.add_instruction(inst)

        # Add true branch
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0xA
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        # Add instructions after if/else
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0xB
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        # Add instruction to loop
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0xC
        inst.addr_mode = AddrModePcRelative()
        inst.param = -11
        inst.param_len = 1

        inst.opcode = sd3.disasm.cpu.Opcode(
            "BCC",
            [Attr.branch],
            sd3.disasm.operands.OpcodeDesc(
                0,
                AddrMode.pc_relative
            )
        )

        routine.add_instruction(inst)

        # Add end of function
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0xE
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        # Create cfg
        cfg = sd3.cfa.cfg.build_graph(routine)

        self.assertEqual(len(cfg.get_node_list()), 6)

        # Get and test nodes
        node0 = cfg.get_node("0")
        self.assertIsNotNone(node0)
        self.assertTrue(node0.get_data().has_instruction(0x1))
        self.assertFalse(node0.get_data().has_instruction(0xC))
        node0.get_data().display()

        node3 = cfg.get_node("3")
        self.assertIsNotNone(node3)

        node7 = cfg.get_node("7")
        self.assertIsNotNone(node7)

        nodeA = cfg.get_node("A")
        self.assertIsNotNone(nodeA)

        nodeB = cfg.get_node("B")
        self.assertIsNotNone(nodeB)

        nodeE = cfg.get_node("E")
        self.assertIsNotNone(nodeE)

        node_list = [node0, node3, node7, nodeA, nodeB, nodeE]

        # Test edges
        self._test_successors(node_list, node0, [node3])
        self._test_successors(node_list, node3, [node7, nodeA])
        self._test_successors(node_list, node7, [nodeB])
        self._test_successors(node_list, nodeA, [nodeB])
        self._test_successors(node_list, nodeB, [node3, nodeE])
        self._test_successors(node_list, nodeE, [])

        # Test exit node
        self.assertIs(cfg.get_exit(), nodeE)

        # Run draw to test that the function doesn't crash
        (fd, path) = tempfile.mkstemp(suffix=".png")
        sd3.cfa.cfg.draw_graph(cfg, path)

        os.close(fd)
        os.remove(path)

    def _test_successors(self, node_list, node, successors):
        for successor in successors:
            self.assertTrue(node.has_successor(successor))

        for not_successor in node_list:
            if not_successor in successors:
                continue

            self.assertFalse(node.has_successor(not_successor))

    def test_exit_single_node(self):
        empty_opcode = sd3.disasm.cpu.Opcode(
            "FakeMnemonic",
            [],
            sd3.disasm.operands.OpcodeDesc(
                0,
                AddrMode.none
            ))

        routine = sd3.disasm.routine.Routine(0x0)

        # Create a first block of 3 instruction
        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x0
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x1
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        inst = sd3.disasm.routine.Instruction()
        inst.addr = 0x2
        inst.addr_mode = AddrModeNone()
        inst.opcode = empty_opcode
        routine.add_instruction(inst)

        # Create cfg
        cfg = sd3.cfa.cfg.build_graph(routine)

        self.assertEqual(len(cfg.get_node_list()), 1)

        # Get and test nodes
        node0 = cfg.get_node("0")
        self.assertIsNotNone(node0)

        # Test exit node
        self.assertIs(cfg.get_exit(), node0)
