import os
import errno
import threading
import queue
from collections import namedtuple
import jinja2
from PIL import Image
import tesserocr
import sd3.gfx
import sd3.text_table

_Char = namedtuple("_Char", ["idx", "char", "img_path"])
_WorkDesc = namedtuple("_WorkDesc", ["idx", "tile"])
_WorkRes = namedtuple("_WorkDesc", ["idx", "char"])

_HTML_RESIZE_FACTOR = 2
_OCR_RESIZE_FACTOR = 5

_FIRST_CHAR_IDX = 0x20
_JPN_CHAR_START = 0x5F

_JPN_TESSEROCR_ID = "jpn"
_ENG_TESSEROCR_ID = "eng"


def _tile_to_char(tile, lang):
    char_img = tile.to_img()

    new_dim = (char_img.width * _OCR_RESIZE_FACTOR,
               char_img.height * _OCR_RESIZE_FACTOR)
    char_img = char_img.resize(new_dim, Image.LANCZOS)

    return tesserocr.image_to_text(char_img, lang=lang, psm=10)


class _Worker:
    def __init__(self, work_queue, result_queue):
        self.work_queue = work_queue
        self.result_queue = result_queue

    def __call__(self):
        while True:
            work_desc = self.work_queue.get()
            if work_desc is None:
                break

            if work_desc.idx >= _JPN_CHAR_START:
                char = _tile_to_char(work_desc.tile, _JPN_TESSEROCR_ID)
            else:
                char = _tile_to_char(work_desc.tile, _ENG_TESSEROCR_ID)

            if char:
                char = char[0]
            else:
                char = "???"

            print("%04X=%s" % (work_desc.idx, char))
            self.result_queue.put(_WorkRes(work_desc.idx, char))


def generate(rom, output_path):
    # Prepare communication tools
    work_queue = queue.Queue()
    result_queue = queue.Queue()

    # Create and start workers
    worker_list = []
    thread_count = len(os.sched_getaffinity(0))
    for _ in range(thread_count):
        worker = _Worker(work_queue, result_queue)
        t = threading.Thread(target=worker)
        t.start()
        worker_list.append(t)

    # Dispatch tiles to decode
    font_reader = sd3.gfx.FontReader(rom)
    for idx, tile in font_reader.read_char_gen():
        work_queue.put(_WorkDesc(idx, tile))

    # Add a None work for each worker
    for _ in worker_list:
        work_queue.put(None)

    for worker in worker_list:
        worker.join()

    print("Workers stopped")

    # Gather results
    decoded_dict = {}
    while not result_queue.empty():
        work_res = result_queue.get(block=False)

        idx = work_res.idx + _FIRST_CHAR_IDX
        decoded_dict[idx] = work_res.char

    # Flush result in a file
    out = open(output_path, "w")

    for idx in sorted(decoded_dict.keys()):
        out.write("%04X=%s\n" % (idx, decoded_dict[idx]))

    out.close()


def _load_jina_template(name):
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                             trim_blocks=True, lstrip_blocks=True)
    return env.get_template(name)


def generate_html(rom, tbl_path, out_folder):
    char_list = []

    tbl = sd3.text_table.Table()
    tbl.load(tbl_path)

    # Create output folder
    try:
        os.makedirs(out_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Read font
    font_reader = sd3.gfx.FontReader(rom)
    for idx, tile in font_reader.read_char_gen():
        # Write file
        img_name = "char_%04X.png" % idx
        img_path = os.path.join(out_folder, img_name)

        # Get and resize tile
        img = tile.to_img()
        new_dim = (img.width * _HTML_RESIZE_FACTOR,
                   img.height * _HTML_RESIZE_FACTOR)
        img = img.resize(new_dim, Image.LANCZOS)

        img.save(img_path)

        idx += _FIRST_CHAR_IDX
        char_list.append(_Char(idx, tbl.decode_char(idx), img_name))

    # Generate html
    template = _load_jina_template("jap_html_table.template")
    rendered = template.render(char_list=char_list)

    # Write output file
    output_index = os.path.join(out_folder, "index.html")
    with open(output_index, 'w') as out:
        out.write(rendered)
