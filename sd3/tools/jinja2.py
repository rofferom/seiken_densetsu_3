import jinja2

def load_template(name, template_dir):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                             trim_blocks=True, lstrip_blocks=True)
    return env.get_template(name)

def write_rendered(rendered, output_path):
    with open(output_path, 'w') as out:
        out.write(rendered)
