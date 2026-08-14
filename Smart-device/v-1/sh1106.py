from micropython import const
import framebuf

_SET_CONTRAST = const(0x81)
_SET_NORM_INV = const(0xA6)
_SET_DISP = const(0xAE)
_SET_MEM_ADDR = const(0x20)
_SET_DISP_START_LINE = const(0x40)
_SET_SEG_REMAP = const(0xA0)
_SET_MUX_RATIO = const(0xA8)
_SET_COM_OUT_DIR = const(0xC0)
_SET_DISP_OFFSET = const(0xD3)
_SET_COM_PIN_CFG = const(0xDA)
_SET_DISP_CLK_DIV = const(0xD5)
_SET_PRECHARGE = const(0xD9)
_SET_VCOM_DESEL = const(0xDB)
_SET_CHARGE_PUMP = const(0x8D)


class SH1106_I2C:

    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr

        self.buffer = bytearray(width * height // 8)

        self.framebuf = framebuf.FrameBuffer(
            self.buffer,
            width,
            height,
            framebuf.MONO_VLSB
        )

        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(
            self.addr,
            bytes([0x00, cmd])
        )

    def write_data(self, data):
        self.i2c.writeto(
            self.addr,
            bytes([0x40]) + data
        )

    def init_display(self):

        self.write_cmd(_SET_DISP | 0x00)

        self.write_cmd(_SET_DISP_CLK_DIV)
        self.write_cmd(0x80)

        self.write_cmd(_SET_MUX_RATIO)
        self.write_cmd(0x3F)

        self.write_cmd(_SET_DISP_OFFSET)
        self.write_cmd(0x00)

        self.write_cmd(_SET_DISP_START_LINE | 0x00)

        self.write_cmd(_SET_CHARGE_PUMP)
        self.write_cmd(0x14)

        self.write_cmd(_SET_MEM_ADDR)
        self.write_cmd(0x00)

        # --------------------------------
        # DISPLAY ORIENTATION
        # --------------------------------

        # Horizontal orientation
        self.write_cmd(_SET_SEG_REMAP | 0x00)

        # Vertical orientation
        self.write_cmd(_SET_COM_OUT_DIR | 0x00)

        # --------------------------------

        self.write_cmd(_SET_COM_PIN_CFG)
        self.write_cmd(0x12)

        self.write_cmd(_SET_CONTRAST)
        self.write_cmd(0xCF)

        self.write_cmd(_SET_PRECHARGE)
        self.write_cmd(0xF1)

        self.write_cmd(_SET_VCOM_DESEL)
        self.write_cmd(0x40)

        # Normal display
        self.write_cmd(_SET_NORM_INV)

        self.write_cmd(_SET_DISP | 0x01)

        self.fill(0)
        self.show()

    def fill(self, color):
        self.framebuf.fill(color)

    def pixel(self, x, y, color):
        self.framebuf.pixel(x, y, color)

    def text(self, text, x, y, color=1):
        self.framebuf.text(text, x, y, color)

    def line(self, x1, y1, x2, y2, color=1):
        self.framebuf.line(x1, y1, x2, y2, color)

    def rect(self, x, y, w, h, color=1):
        self.framebuf.rect(x, y, w, h, color)

    def fill_rect(self, x, y, w, h, color=1):
        self.framebuf.fill_rect(x, y, w, h, color)

    def show(self):

        for page in range(8):

            self.write_cmd(0xB0 + page)

            # SH1106 column offset
            self.write_cmd(0x02)
            self.write_cmd(0x10)

            start = page * 128
            end = start + 128

            self.write_data(self.buffer[start:end])
