from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import image
import os


class ImageShow(BaseMatrixAnim):

    def __init__(self, layout, imagePath=None, offset=(0, 0)):
        super(ImageShow, self).__init__(layout)
        if imagePath is None:
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            imagePath = os.path.abspath(os.path.join(cur_dir, '../../Graphics/ml_logo.bmp'))
        self.img = imagePath
        self.offset = offset

    def pre_run(self):
        self.layout.setTexture(image.loadImage(self.layout, imagePath=self.img, offset=self.offset))

    def step(self, amt):
        self.layout.fillScreen()
