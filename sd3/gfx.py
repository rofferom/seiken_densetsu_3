from PIL import Image, ImageDraw

_FONT_START_CHAR = 0x20

_FONT_ADDRESS = 0xFE2F00
_FONT_CHAR_SIZE = 25

_FONT_CHAR_WIDTH = 14
_FONT_CHAR_HEIGHT = 14

_FONT_CHAR_DISPLAY_WIDTH = 16
_FONT_CHAR_DISPLAY_HEIGHT = _FONT_CHAR_HEIGHT * 2

_FONT_CHAR_COUNT = 988

_IMG_COLUMN_COUNT = 16


class Tile:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tile = [0] * self.width * self.height

    def __getitem__(self, key):
        x, y = key[0], key[1]
        return self.tile[self.width * x + y]

    def __setitem__(self, key, value):
        x, y = key[0], key[1]
        self.tile[self.width * x + y] = value

    def get_raw_content(self):
        return self.tile

    def to_img(self):
        img = Image.new("RGB", (_FONT_CHAR_WIDTH, _FONT_CHAR_DISPLAY_HEIGHT))
        draw = ImageDraw.Draw(img)

        _DrawUtils.draw_char(draw, self, 0, 0)

        del draw
        return img


class _FontCharReader:
    def __init__(self, raw_char):
        self.raw_char = raw_char
        self.read_idx = 0
        self.tile = Tile(_FONT_CHAR_WIDTH, _FONT_CHAR_HEIGHT)

    def _get_byte(self):
        value = self.raw_char[self.read_idx]
        self.read_idx += 1
        return value

    def _write_line(self, y, raw_line):
        for i in range(_FONT_CHAR_WIDTH):
            self.tile[i, y] = (raw_line >> (_FONT_CHAR_WIDTH-i-1)) & 1

    def _write_line_block(self, y, line_count):
        next_line = 0

        for i in range(y, y + line_count):
            # A line is 14 bits width. The first read bits are the most
            # significants.
            raw_line = self._get_byte() << 6

            # The next byte is composed of 6 bits (MSB) to complete the line,
            # and 2 bits to gather to build the last line
            b = self._get_byte()
            raw_line |= (b >> 2) & 0b111111
            next_line = (next_line << 2) | (b & 0b11)

            self._write_line(y=i, raw_line=raw_line)

        return next_line

    def decode(self):
        # Reset read index
        self.read_idx = 0

        # Fill the first 7 lines. We will get 14 extra bits
        # that will be used to build the 8th line
        next_line = self._write_line_block(y=0, line_count=7)

        # We get 2 bits per decoded line, so we have a full line here
        self._write_line(y=7, raw_line=next_line)

        # Fill the next 5 lines. We will get 10 extra bits
        # that will be used to build the 14th line
        next_line = self._write_line_block(y=8, line_count=5)

        # The last byte is used to fill the last line.
        next_line = (next_line << 4) | self._get_byte()
        # For an unknown reason, the last line is shifted to the right.
        # But it seems to match the behaviour of the ROM code.
        next_line >>= 2

        # Write the last line
        self._write_line(y=13, raw_line=next_line)

        return self.tile


class _DrawUtils:
    @staticmethod
    def draw_char(draw, char, start_x, start_y):
        char_color = (255, 255, 255)

        for x in range(_FONT_CHAR_WIDTH):
            for y in range(_FONT_CHAR_HEIGHT):
                value = char[x, y]
                if value == 0:
                    continue

                pixel_x = start_x + x
                pixel_y = start_y + y * 2

                draw.point([(pixel_x, pixel_y)], char_color)

                draw.point([(pixel_x, pixel_y)], char_color)
                draw.point([(pixel_x, pixel_y+1)], char_color)


class FontImgBuilder:
    def __init__(self, font_reader):
        self.font_reader = font_reader

        self.row_count = None
        self.column_count = None

        self.dim = None

        self._compute_dim()

    def _compute_dim(self):
        self.column_count = _IMG_COLUMN_COUNT

        self.row_count = _FONT_CHAR_COUNT // self.column_count
        if _FONT_CHAR_COUNT % self.column_count > 0:
            self.row_count += 1

        # Compute width to place a grid
        self.width = 1 + (_FONT_CHAR_WIDTH + 1) * self.column_count
        self.height = 1 + (_FONT_CHAR_DISPLAY_HEIGHT + 1) * self.row_count

    def _draw_grid(self, draw):
        grid_color = (0, 0, 255)

        # Draw right and bottom borders. The two others will be built
        # with the vertical and horizontal lines
        top_right = (self.width-1, 0)
        bottom_left = (0, self.height-1)
        bottom_right = (self.width-1, self.height-1)

        draw.line([bottom_left, bottom_right], grid_color)
        draw.line([top_right, bottom_right], grid_color)

        # Draw horizontal lines
        for i in range(self.row_count):
            origin_x = 0
            origin_y = (_FONT_CHAR_DISPLAY_HEIGHT+1) * i

            end_x = self.width-1
            end_y = origin_y

            draw.line([(origin_x, origin_y), (end_x, end_y)], grid_color)

        # Draw vertical lines
        for i in range(self.column_count):
            origin_x = (_FONT_CHAR_WIDTH+1) * i
            origin_y = 0

            end_x = origin_x
            end_y = self.height-1

            draw.line([(origin_x, origin_y), (end_x, end_y)], grid_color)

    def _draw_char(self, draw, i, char):
        char_color = (255, 255, 255)

        row_idx = i // self.column_count
        column_idx = i % self.column_count

        for x in range(_FONT_CHAR_WIDTH):
            for y in range(_FONT_CHAR_HEIGHT):
                value = char[x, y]
                if value == 0:
                    continue

                p_x = 1 + column_idx * (_FONT_CHAR_WIDTH + 1) + x
                p_y = 1 + row_idx * (_FONT_CHAR_HEIGHT + 1) + y
                draw.point([(p_x, p_y)], char_color)
                draw.point([(p_x, p_y+1)], char_color)

    def dump_to_file(self, path):
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        self._draw_grid(draw)

        for i in range(_FONT_CHAR_COUNT):
            char = self.font_reader.read_char(i)

            row_idx = i // self.column_count
            column_idx = i % self.column_count

            start_x = 1 + column_idx * (_FONT_CHAR_WIDTH + 1)
            start_y = 1 + row_idx * (_FONT_CHAR_DISPLAY_HEIGHT + 1)

            _DrawUtils.draw_char(draw, char, start_x, start_y)

        del draw
        img.save(path)


class FontReader:
    def __init__(self, rom):
        self.rom = rom

    def read_char(self, idx):
        # Read
        addr = _FONT_ADDRESS + _FONT_CHAR_SIZE * idx
        self.rom.seek(addr)
        raw_char = self.rom.read_buf(_FONT_CHAR_SIZE)

        reader = _FontCharReader(raw_char)
        return reader.decode()

    def read_char_gen(self):
        for idx in range(_FONT_CHAR_COUNT):
            tile = self.read_char(idx)
            yield (idx, tile)

    def dump_to_file(self, path):
        img_builder = FontImgBuilder(self)
        img_builder.dump_to_file(path)


class DialogDrawer:
    def __init__(self, rom):
        self.rom = rom
        self.font_reader = FontReader(self.rom)

    @staticmethod
    def _get_char_count(txt):
        width = 0

        for char in txt:
            if char >= _FONT_START_CHAR:
                width += 1

        return width

    def _get_img_dim(self, dialog):
        height = len(dialog)

        width = 0
        for txt in dialog:
            count = self._get_char_count(txt)
            width = max(width, count)

        return (width * _FONT_CHAR_DISPLAY_WIDTH,
                height * _FONT_CHAR_DISPLAY_HEIGHT)

    def _write_txt(self, draw, txt, line):
        start_x = 0
        start_y = line * _FONT_CHAR_DISPLAY_HEIGHT

        for char in txt:
            if char < _FONT_START_CHAR:
                continue

            tile = self.font_reader.read_char(char - _FONT_START_CHAR)
            _DrawUtils.draw_char(draw, tile, start_x, start_y)

            start_x += _FONT_CHAR_DISPLAY_WIDTH

    def write_to_img(self, dialog, path):
        dim = self._get_img_dim(dialog)
        img = Image.new("RGB", dim, "black")
        draw = ImageDraw.Draw(img)

        for i, txt in enumerate(dialog):
            self._write_txt(draw, txt, i)

        img.save(path)
