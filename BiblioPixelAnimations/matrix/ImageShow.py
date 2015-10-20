from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.image import loadImage

class ImageShow(BaseMatrixAnim):

    def __init__(self, led, imagePath, offset = (0,0)):
        super(ImageShow, self).__init__(led)
        self.img = imagePath
        self.offset = offset

    def preRun(self):
        self._led.setTexture(loadImage(self._led, imagePath=self.img, offset=self.offset))

    def step(self, amt):
        self._led.fillScreen()


MANIFEST = [
    {
        "class": ImageShow,
        "controller": "matrix",
        "desc": "Show static image",
        "display": "Image Show",
        "id": "ImageShow",
        "params": [{
            "id": "imagePath",
            "label": "Image File",
            "type": "str",
            "default": [],
            "help":"Image file to load.",
            "replace": {"\\":"/"}
        },{
            "default": [0,0],
            "help": "Image placement offset",
            "id": "offset",
            "label": "Offset",
            "type": "multi_tuple",
            "controls": [{
                "label": "X",
                "type": "int",
                "default": 0
            },{
                "label": "Y",
                "type": "int",
                "default": 0
            }]
        }],
        "type": "animation"
    }
]
