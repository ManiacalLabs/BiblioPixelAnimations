from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.image import loadImage, showImage
from random import randint, shuffle

class ImageDissolve(BaseMatrixAnim):

    def __init__(self, led, imageFiles, pixelRate=10, waitFrames = 30):
        super(ImageDissolve, self).__init__(led)
        if not isinstance(imageFiles, list) or len(imageFiles) == 0:
            raise ValueError("imageFiles must be a list of file paths.")
        self.pixelRate = pixelRate
        self.imageFiles = imageFiles
        self.imgIndex = 0
        self.waitFrames = waitFrames
        self.waitCount = 0

    def preRun(self):
        self.resetAndLoad()
        self.imgIndex = 0
        self.waitCount = 0

    def resetAndLoad(self):
        self._led.setTexture(loadImage(self._led, imagePath=self.imageFiles[self.imgIndex]))
        self.map = [(x,y) for x in range(self.width) for y in range(self.height)]
        shuffle(self.map)

    def step(self, amt):
        if self.waitCount == 0:
            for i in range(self.pixelRate):
                x,y = self.map.pop()
                self._led.set(x,y)
                if len(self.map) == 0:
                    if len(self.imageFiles) == 1:
                        self._led.all_off()
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


MANIFEST = [
    {
        "class": ImageDissolve,
        "controller": "matrix",
        "desc": "Dissolve betwen images",
        "display": "Image Dissolve",
        "id": "ImageDissolve",
        "params": [{
            "id": "imageFiles",
            "label": "Files",
            "type": "str_multi",
            "default": [],
            "help":"Image files to load.",
            "replace": {"\\":"/"}
        },{
            "id": "pixelRate",
            "label": "Pixel Rate",
            "type": "int",
            "default": 10,
            "min": 1,
            "help":"Number of pixels to add per frame.",
        },{
            "id": "waitFrames",
            "label": "Wait Frames",
            "type": "int",
            "default": 30,
            "min": 0,
            "help":"Number of frames between end of dissolve and start of next image",
        }],
        "type": "animation"
    }
]
