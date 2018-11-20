from bibliopixel.animation.strip import Strip


class ColorFill(Strip):
    """Fill the dots progressively along the strip."""
    # DEPRECATED - use bibliopixel.animation.fill

    def __init__(self, layout, color, **kwds):
        super().__init__(layout, **kwds)
        self._color = color

    def step(self, amt=1):
        self.layout.fill(self._color)
