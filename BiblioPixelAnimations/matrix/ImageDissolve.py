from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import image
from random import shuffle
import os


class ImageDissolve(BaseMatrixAnim):

    def __init__(self, layout, imageFiles=None, pixelRate=10, waitFrames=30):
        super(ImageDissolve, self).__init__(layout)
        self.pixelRate = pixelRate
        if imageFiles is None:
            imageFiles = []
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            imageFiles.append(os.path.abspath(os.path.join(cur_dir, '../../Graphics/ml_logo.bmp')))
            imageFiles.append(os.path.abspath(os.path.join(cur_dir, '../../Graphics/rainbow.jpg')))
        self.imageFiles = imageFiles
        self.imgIndex = 0
        self.waitFrames = waitFrames
        self.waitCount = 0

    def pre_run(self):
        self.resetAndLoad()
        self.imgIndex = 0
        self.waitCount = 0

    def resetAndLoad(self):
        self.layout.setTexture(image.loadImage(self.layout, imagePath=self.imageFiles[self.imgIndex]))
        self.map = [(x, y) for x in range(self.width) for y in range(self.height)]
        shuffle(self.map)

    def step(self, amt):
        if self.waitCount == 0:
            for i in range(self.pixelRate):
                x, y = self.map.pop()
                self.layout.set(x, y)
                if len(self.map) == 0:
                    if len(self.imageFiles) == 1:
                        self.layout.all_off()
                        self.animComplete = True
                    else:
                        self.imgIndex += 1
                        if self.imgIndex >= len(self.imageFiles):
                            self.animComplete = True
                            self.imgIndex = 0
                    self.waitCount = self.waitFrames
                    self.resetAndLoad()
                    break
        else:
            self.waitCount -= 1
