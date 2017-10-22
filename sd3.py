#!/usr/bin/env python3

import logging
import sys
import argparse
import sd3.gfx
import sd3.text


def int_parse(value):
    return int(value, 0)


def open_rom(path):
    f = open(path, "rb")
    return sd3.rom.Rom(f, sd3.rom.HighRomConv)


class Cmd:
    pass


class DumpFont(Cmd):
    @staticmethod
    def register_parser(subparsers):
        name = "dump_font"

        parser = subparsers.add_parser(name)
        parser.add_argument("rom", help="Source ROM")
        parser.add_argument("out", help="Output path")

        return name

    @staticmethod
    def run(args):
        logging.info("Extract font of %s to %s", args.rom, args.out)

        rom = open_rom(args.rom)
        font_reader = sd3.gfx.FontReader(rom)
        font_reader.dump_to_file(args.out)


class DumpDialog(Cmd):
    @staticmethod
    def register_parser(subparsers):
        name = "dump_dialog"

        parser = subparsers.add_parser(name)
        parser.add_argument("rom", help="Source ROM")
        parser.add_argument("idx", type=int_parse, help="Dialog index")
        parser.add_argument("out", help="Output path")

        return name

    @staticmethod
    def run(args):
        logging.info("Extract dialog %X from %s", args.idx, args.rom)

        rom = open_rom(args.rom)
        decoder = sd3.text.Decoder(rom)
        decoded = decoder.get_dialog(args.idx)

        logging.info("Decoded data")
        logging.info(decoded)

        drawer = sd3.gfx.DialogDrawer(rom)
        drawer.write_to_img(decoded, args.out)


class GetOperationSub(Cmd):
    @staticmethod
    def register_parser(subparsers):
        name = "get_operation_sub"

        parser = subparsers.add_parser(name)
        parser.add_argument("rom", help="Source ROM")
        parser.add_argument("idx", type=int_parse, help="Operation id")

        return name

    @staticmethod
    def run(args):
        _BASE = 0xC43128
        _COUNT = 0x100
        _BANK = 0xC4

        if args.idx >= _COUNT:
            logging.error("Invalid index. Got %X, count=%X", args.idx, _COUNT)

        with open(args.rom, "rb") as rom:
            rom = sd3.rom.Rom(rom, sd3.rom.HighRomConv)
            addr = rom.read_addr_from_ptr(_BASE, args.idx, _BANK)
            logging.info("Routine location: %06X", addr)


def setup_logs():
    logging.basicConfig(
        level=logging.WARNING,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr)

    logging.addLevelName(logging.CRITICAL, "C")
    logging.addLevelName(logging.ERROR, "E")
    logging.addLevelName(logging.WARNING, "W")
    logging.addLevelName(logging.INFO, "I")
    logging.addLevelName(logging.DEBUG, "D")

    logging.getLogger().setLevel(logging.INFO)


def main():
    setup_logs()

    parser = argparse.ArgumentParser(description="Seiken Densetsu 3 dump tool")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity",
                        action="store_true")

    subparsers = parser.add_subparsers(dest="cmd", help="sub-command help")

    cmd_map = {}
    for cmd in Cmd.__subclasses__():
        name = cmd.register_parser(subparsers)
        cmd_map[name] = cmd

    args = parser.parse_args()
    if args.cmd is None:
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    cmd_map[args.cmd].run(args)


if __name__ == "__main__":
    main()
