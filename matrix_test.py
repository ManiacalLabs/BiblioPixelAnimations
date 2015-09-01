from bibliopixel import LEDMatrix
import bibliopixel.colors as colors
from bibliopixel.drivers.visualizer import *
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

driver = DriverVisualizer(width=24, height=24, stayTop=True)
led = LEDMatrix(driver, threadedUpdate=True)

# from matrix.Text import ScrollText, BounceText
# anim = ScrollText(led, "Scroll Text", xPos=0, yPos=0, color=colors.White, bgcolor=colors.Off, size=1)
# anim.run(max_steps=100)
#
# anim = BounceText(led, "Bounce Text", xPos=0, yPos=0, buffer=0, color=colors.White, bgcolor=colors.Off, size=1)
# anim.run(max_steps=100)
#
# from matrix.SpiningTriangle import SpiningTriangle
# anim = SpiningTriangle(led, led.width/2, led.height/2, led.width/3)
# anim.run(max_steps=100)
#
# from matrix.MatrixRain import MatrixRain, MatrixRainBow
# anim = MatrixRain(led, rain_colors=[colors.Green], tail=4, growthRate=4)
# anim.run(max_steps=100)
#
# anim = MatrixRainBow(led, tail=4, growthRate=4)
# anim.run(max_steps=100)
#
# from matrix.AnalogClock import AnalogClock, RGBAnalogClock
# anim = AnalogClock(led)
# anim.run(fps=1, max_steps=5)
#
# anim = RGBAnalogClock(led)
# anim.run(fps=1, max_steps=5)
#
# from matrix.TicTacToe import TicTacToe
# anim = TicTacToe(led)
# anim.run(max_steps=100)
#
# from matrix.opencv_video import OpenCVVideo
# anim = OpenCVVideo(led, videoSource=None, mirror=True, offset=0.0, crop=True, useVidFPS=False)
# anim.run(max_steps=100)

from BiblioPixelAnimations.matrix.LangtonsAnt import LangtonsAnt
anim = LangtonsAnt(led, antColor=colors.Green, pathColor=colors.Red)
anim.run(fps=20)
anim.run(max_steps=200)

# from matrix.GameOfLife import GameOfLife, GameOfLifeRGB
# anim = GameOfLifeRGB(led, toroidal=True)
# anim.run(max_steps=100)
#
# anim = GameOfLife(led, color=colors.Red, bg=colors.Off, toroidal=False)
# anim.run(max_steps=100)
#
# from matrix.CPUUsage import CPUUsage
# anim = CPUUsage(led, colors.Red)
# anim.run(max_steps=10)
#
# from matrix.bloom import Bloom
# anim = Bloom(led, dir=True)
# anim.run(max_steps=100)
