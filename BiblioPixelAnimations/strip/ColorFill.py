from bibliopixel.animation import BaseStripAnim


class ColorFill(BaseStripAnim):
    """Fill the dots progressively along the strip."""
    # DEPRECATED - use bibliopixel.animation.fill

    def __init__(self, layout, color):
        super().__init__(layout)
        self._color = color

    def step(self, amt=1):
        self.layout.fill(self._color)
