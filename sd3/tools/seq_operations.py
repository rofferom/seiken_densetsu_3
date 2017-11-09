import os
import sd3.tools.jinja2


def get_op_list(rom):
    _BASE = 0xC43128
    _COUNT = 0x100
    _BANK = 0xC4

    for op_id in range(_COUNT):
        sub_addr = rom.read_addr_from_ptr(_BASE, op_id, _BANK)
        yield (op_id, sub_addr)

def gen_map(rom, output_path):
    # List subroutines
    operation_map = {}
    subroutines = set()

    for op_id, sub_addr in get_op_list(rom):
        subroutines.add(sub_addr)
        operation_map[op_id] = sub_addr

    # Generate template
    template = sd3.tools.jinja2.load_template(
        "gen_operation_map.template",
        os.path.dirname(os.path.abspath(__file__)))

    rendered = template.render(
        operation_map=operation_map,
        subroutines=subroutines)

    # Write output file
    sd3.tools.jinja2.write_rendered(rendered, output_path)
