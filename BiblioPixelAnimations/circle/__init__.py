from bibliopixel import colors
from . arc_rotate import ArcRotate
from . bloom import Bloom
from . fireflies import FireFlies
from . pinwheel import PinWheel
from . swirl import Swirl

rainbow = [colors.Red, colors.Orange, colors.Yellow,
           colors.Green, colors.Blue, colors.Purple]
MANIFEST = [
    {
        "class": ArcRotate,
        "controller": "circle",
        "desc": None,
        "display": "ArcRotate",
        "id": "ArcRotate",
        "params": [
            {
                "default": rainbow,
                "help": "",
                "id": "colors",
                "label": "Colors",
                "type": "multi",
                "controls": {
                    "help": None,
                    "label": "Color",
                    "type": "color"
                }
            },
            {
                "default": 180,
                "help": "Arc Angle to light up",
                "id": "arc",
                "label": "Arc Angle",
                "type": "int",
                "min": 1,
                "max": 359
            }
        ],
        "type": "animation"
    },
    {
        "class": Bloom,
        "controller": "circle",
        "desc": None,
        "display": "Bloom",
        "id": "Bloom",
        "params": [
            {
                "default": 1,
                "help": "",
                "id": "spread",
                "label": "Spread",
                "type": "int",
                "min": 1,
                "max": 32
            }
        ],
        "type": "animation"
    },
    {
        "class": FireFlies,
        "controller": "circle",
        "desc": None,
        "display": "FireFlies",
        "id": "FireFlies",
        "params": [
            {
                "default": rainbow,
                "help": "",
                "id": "colors",
                "label": "Colors",
                "type": "multi",
                "controls": {
                    "help": None,
                    "label": "Color",
                    "type": "color"
                }
            },
            {
                "default": 10,
                "help": "Total lit pixels in each frame",
                "id": "count",
                "label": "Pixel Count",
                "type": "int"
            }
        ],
        "type": "animation"
    },
    {
        "class": PinWheel,
        "controller": "circle",
        "desc": None,
        "display": "PinWheel",
        "id": "PinWheel",
        "params": [
            {
                "default": rainbow,
                "help": "",
                "id": "colors",
                "label": "Colors",
                "type": "multi",
                "controls": {
                    "help": None,
                    "label": "Color",
                    "type": "color"
                }
            }
        ],
        "type": "animation"
    },
    {
        "class": Swirl,
        "controller": "circle",
        "desc": None,
        "display": "Swirl",
        "id": "Swirl",
        "params": [
            {
                "default": 12,
                "help": "Degrees change per frame",
                "id": "angle",
                "label": "Angle Change",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
