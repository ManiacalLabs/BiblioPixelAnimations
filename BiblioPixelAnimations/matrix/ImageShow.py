from bibliopixel.animation.matrix import Matrix
from bibliopixel.util.image import load_image
import os


class ImageShow(Matrix):

    def __init__(self, layout, imagePath=None, offset=(0, 0), **kwds):
        super().__init__(layout, **kwds)
        if imagePath is None:
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            imagePath = os.path.abspath(os.path.join(cur_dir, '../../Graphics/ml_logo.bmp'))
        self.img = imagePath
        self.offset = offset

    def pre_run(self):
        self.layout.setTexture(load_image.loadImage(self.layout, imagePath=self.img, offset=self.offset))

    def step(self, amt):
        self.layout.fillScreen()
