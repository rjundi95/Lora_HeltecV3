# MicroPython SSD1306 OLED driver
# 128x64 I2C

from micropython import const
import framebuf

SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)


class SSD1306(framebuf.FrameBuffer):

    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc

        self.pages = height // 8
        self.buffer = bytearray(self.pages * width)

        super().__init__(
            self.buffer,
            width,
            height,
            framebuf.MONO_VLSB
        )

        self.init_display()

    def init_display(self):

        self.write_cmd(SET_DISP | 0x00)

        self.write_cmd(SET_MEM_ADDR)
        self.write_cmd(0x00)

        self.write_cmd(SET_DISP_START_LINE | 0x00)
        self.write_cmd(SET_SEG_REMAP | 0x01)

        self.write_cmd(SET_MUX_RATIO)
        self.write_cmd(self.height - 1)

        self.write_cmd(SET_COM_OUT_DIR | 0x08)

        self.write_cmd(SET_DISP_OFFSET)
        self.write_cmd(0x00)

        self.write_cmd(SET_COM_PIN_CFG)

        if self.width > 2 * self.height:
            self.write_cmd(0x02)
        else:
            self.write_cmd(0x12)

        self.write_cmd(SET_DISP_CLK_DIV)
        self.write_cmd(0x80)

        self.write_cmd(SET_PRECHARGE)

        if self.external_vcc:
            self.write_cmd(0x22)
        else:
            self.write_cmd(0xF1)

        self.write_cmd(SET_VCOM_DESEL)
        self.write_cmd(0x30)

        self.write_cmd(SET_CONTRAST)
        self.write_cmd(0xFF)

        self.write_cmd(SET_ENTIRE_ON)
        self.write_cmd(SET_NORM_INV)

        self.write_cmd(SET_CHARGE_PUMP)

        if self.external_vcc:
            self.write_cmd(0x10)
        else:
            self.write_cmd(0x14)

        self.write_cmd(SET_DISP | 0x01)

        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1

        if self.width == 64:
            x0 += 32
            x1 += 32

        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)

        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)

        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):

    def __init__(
        self,
        width,
        height,
        i2c,
        addr=0x3C,
        external_vcc=False
    ):
        self.i2c = i2c
        self.addr = addr

        self.temp = bytearray(2)

        super().__init__(
            width,
            height,
            external_vcc
        )

    def write_cmd(self, cmd):
        self.temp[0] = 0x80
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.i2c.writeto(
            self.addr,
            b'\x40' + buf
        )
