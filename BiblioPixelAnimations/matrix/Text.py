from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel import font


class ScrollText(BaseMatrixAnim):

    def __init__(self, layout, text='ScrollText', xPos=0, yPos=0,
                 color=colors.White, bgcolor=colors.Off,
                 font_name=font.default_font, font_scale=1):
        super(ScrollText, self).__init__(layout)
        self.bgcolor = bgcolor
        self.color = color
        self._text = text
        self.xPos = xPos
        self.orig_xPos = xPos
        self.yPos = yPos
        self.font_name = font_name
        self.font_scale = font_scale
        self._strW = font.str_dim(text, font_name, font_scale, True)[0]

    def pre_run(self):
        self.xPos = self.orig_xPos

    def step(self, amt=1):
        self.layout.all_off()
        self.layout.drawText(self._text, self.xPos, self.yPos,
                             color=self.color, bg=self.bgcolor, font=self.font_name, font_scale=self.font_scale)
        self.xPos -= amt
        if self.xPos + self._strW <= 0:
            self.xPos = self.width - 1
            self.animComplete = True

        self._step = 0


class BounceText(BaseMatrixAnim):

    def __init__(self, layout, text='BounceText', xPos=0, yPos=0, buffer=0, color=colors.White, bgcolor=colors.Off, font_name=font.default_font, font_scale=1):
        super(BounceText, self).__init__(layout)
        self.color = color
        self.bgcolor = bgcolor
        self._text = text
        self.xPos = xPos
        self.yPos = yPos
        self.font_name = font_name
        self.font_scale = font_scale
        self._strW = font.str_dim(text, font_name, font_scale, True)[0]
        self._dir = -1
        self._buffer = buffer

    def step(self, amt=1):
        self.layout.all_off()
        self.layout.drawText(self._text, self.xPos, self.yPos,
                             color=self.color, bg=self.bgcolor,
                             font=self.font_name, font_scale=self.font_scale)

        if self._strW < self.width:
            if self.xPos <= 0 + self._buffer and self._dir == -1:
                self._dir = 1
            elif self.xPos + self._strW > self.width - self._buffer and self._dir == 1:
                self._dir = -1
                self.animComplete = True
        else:
            if self.xPos + self._strW <= self.width - self._buffer and self._dir == -1:
                self._dir = 1
            elif self.xPos >= 0 + self._buffer and self._dir == 1:
                self._dir = -1
                self.animComplete = True

        self.xPos += amt * self._dir

        self._step = 0
