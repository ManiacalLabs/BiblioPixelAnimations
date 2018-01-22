from bibliopixel.animation import BaseAnimation


class Fill(BaseAnimation):
    def __init__(self, *args, color, **kwds):
        super().__init__(*args, preclear=False, **kwds)
        self.color = color

    def pre_run(self):
        if hasattr(self.color_list, 'dtype'):
            self.color_list[:None] = self.color
        else:
            self.color_list[:] = [tuple(self.color)] * len(self.color_list)

    def step(self, amt=1):
        pass
