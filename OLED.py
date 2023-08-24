from machine import Pin, SPI
import framebuf
import time
from _thread import get_ident

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


# In this file, CTDC refers to cross-thread display communication, where
# multiple threads attempt to communicate with the display at the same time,
# causing communication errors.


class OledLowLevel(framebuf.FrameBuffer):
    """OLED without CTDC protection"""

    def __init__(self):
        self.width = 128
        self.height = 64

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 2000_000)
        self.spi = SPI(1, 20000_000, polarity=0, phase=0, sck=Pin(SCK),
                       mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height,
                         framebuf.MONO_HMSB)
        self.init_display()

        self.white = 0xffff
        self.balck = 0x0000

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)

        self.write_cmd(0xAE)  # turn off oled display

        self.write_cmd(0x00)  # set lower column address
        self.write_cmd(0x10)  # set higher column address

        self.write_cmd(0xB0)  # set page address

        self.write_cmd(0xdc)  # et display start line
        self.write_cmd(0x00)
        self.write_cmd(0x81)  # contract control
        self.write_cmd(0x6f)  # 128
        self.write_cmd(0x21)  # Set Memory addressing mode (0x20/0x21) #

        self.write_cmd(0xa0)  # set segment remap
        self.write_cmd(0xc0)  # Com scan direction
        self.write_cmd(0xa4)  # Disable Entire Display On (0xA4/0xA5)

        self.write_cmd(0xa6)  # normal / reverse
        self.write_cmd(0xa8)  # multiplex ratio
        self.write_cmd(0x3f)  # duty = 1/64

        self.write_cmd(0xd3)  # set display offset
        self.write_cmd(0x60)

        self.write_cmd(0xd5)  # set osc division
        self.write_cmd(0x41)

        self.write_cmd(0xd9)  # set pre-charge period
        self.write_cmd(0x22)

        self.write_cmd(0xdb)  # set vcomh
        self.write_cmd(0x35)

        self.write_cmd(0xad)  # set charge pump enable
        self.write_cmd(0x8a)  # Set DC-DC enable (a=0:disable; a=1:enable)
        self.write_cmd(0XAF)

    def show(self):
        self.write_cmd(0xb0)
        for page in range(0, 64):
            self.column = 63 - page
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0, 16):
                self.write_data(self.buffer[page * 16 + num])


class Oled:
    """OLED with CTDC protection"""

    def __init__(self):
        self.oled = OledLowLevel()
        self.writing_to_display_currently = None  # To prevent CTDC

    def fill(self, c: int) -> None:
        """
       Fill the entire FrameBuffer with the specified color.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.fill(c)

    def pixel(self, x: int, y: int, c: int = None) -> int:
        """
       If *c* is not given, get the color value of the specified pixel.
       If *c* is given, set the specified pixel to the given color.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        return self.oled.pixel(x, y, c)

    def hline(self, x: int, y: int, w: int, c: int) -> None:
        """
       Draw a line from a set of coordinates using the given color and
       a thickness of 1 pixel. The `line` method draws the line up to
       a second set of coordinates whereas the `hline` and `vline`
       methods draw horizontal and vertical lines respectively up to
       a given length.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.hline(x, y, w, c)

    def vline(self, x: int, y: int, h: int, c: int) -> None:
        """
       Draw a line from a set of coordinates using the given color and
       a thickness of 1 pixel. The `line` method draws the line up to
       a second set of coordinates whereas the `hline` and `vline`
       methods draw horizontal and vertical lines respectively up to
       a given length.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.vline(x, y, h, c)

    def line(self, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
       Draw a line from a set of coordinates using the given color and
       a thickness of 1 pixel. The `line` method draws the line up to
       a second set of coordinates whereas the `hline` and `vline`
       methods draw horizontal and vertical lines respectively up to
       a given length.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.line(x1, y1, x2, y2, c)

    def rect(self, x: int, y: int, w: int, h: int, c: int,
             fill: bool = False) -> None:
        """
       Draw a rectangle at the given location, size and color. The `rect`
       method draws only a 1 pixel outline whereas the `fill_rect` method
       draws both the outline and interior.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.rect(x, y, w, h, c, fill)

    def ellipse(self, x, y, xr, yr, c, f: bool = False,
                m: int = 0) -> None:
        """
        Draw an ellipse at the given location. Radii xr and yr define the
        geometry; equal values cause a circle to be drawn. The c parameter
        defines the color.

The optional f parameter can be set to True to fill the ellipse. Otherwise
just a one pixel outline is drawn.

The optional m parameter enables drawing to be restricted to certain
quadrants of the ellipse. The LS four bits determine which quadrants are to
be drawn, with bit 0 specifying Q1, b1 Q2, b2 Q3 and b3 Q4. Quadrants are
numbered counterclockwise with Q1 being top right.
        """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.ellipse(x, y, xr, yr, c, f, m)

    def text(self, s: str, x: int, y: int, c: int = 1) -> None:
        """
       Write text to the FrameBuffer using the the coordinates as the
       upper-left
       corner of the text. The color of the text can be defined by the optional
       argument but is otherwise a default value of 1. All characters have
       dimensions of 8x8 pixels and there is currently no way to change the
       font.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.text(s, x, y, c)

    def scroll(self, xstep: int, ystep: int) -> None:
        """
       Shift the contents of the FrameBuffer by the given vector. This may
       leave a footprint of the previous colors in the FrameBuffer.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.scroll(xstep, ystep)

    def blit(
            self,
            fbuf: framebuf.FrameBuffer,
            x: int,
            y: int,
            key: int = -1,
            pallet: framebuf.FrameBuffer | None = None,
    ) -> None:
        """
       Draw another FrameBuffer on top of the current one at the given
       coordinates.
       If *key* is specified then it should be a color integer and the
       corresponding color will be considered transparent: all pixels with that
       color value will not be drawn.

       The *palette* argument enables blitting between FrameBuffers with
       differing
       formats. Typical usage is to render a monochrome or grayscale
       glyph/icon to
       a color display. The *palette* is a FrameBuffer instance whose format is
       that of the current FrameBuffer. The *palette* height is one pixel
       and its
       pixel width is the number of colors in the source FrameBuffer. The
       *palette*
       for an N-bit source needs 2**N pixels; the *palette* for a monochrome
       source
       would have 2 pixels representing background and foreground colors. The
       application assigns a color to each pixel in the *palette*. The color
       of the
       current pixel will be that of that *palette* pixel whose x position
       is the
       color of the corresponding source pixel.
      """
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.blit(fbuf, x, y, key, pallet)

    def show(self):
        native_id = get_ident()
        while self.writing_to_display_currently and self.writing_to_display_currently != native_id:  # Wait for CTDC to finish
            pass
        self.writing_to_display_currently = native_id
        self.oled.show()
        self.writing_to_display_currently = None
