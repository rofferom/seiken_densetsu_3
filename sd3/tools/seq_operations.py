import os
import jinja2


def _get_op_list(rom):
    _BASE = 0xC43128
    _COUNT = 0x100
    _BANK = 0xC4

    for op_id in range(_COUNT):
        sub_addr = rom.read_addr_from_ptr(_BASE, op_id, _BANK)
        yield (op_id, sub_addr)


def _load_jina_template(name):
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                             trim_blocks=True, lstrip_blocks=True)
    return env.get_template(name)


def gen_map(rom, output_path):
    # List subroutines
    operation_map = {}
    subroutines = set()

    for op_id, sub_addr in _get_op_list(rom):
        subroutines.add(sub_addr)
        operation_map[op_id] = sub_addr

    # Generate template
    template = _load_jina_template("gen_operation_map.template")

    rendered = template.render(
        operation_map=operation_map,
        subroutines=subroutines)

    # Write output file
    with open(output_path, 'w') as out:
        out.write(rendered)
