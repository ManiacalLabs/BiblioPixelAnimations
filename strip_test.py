from bibliopixel import *
from bibliopixel.drivers.visualizer import *
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)
import bibliopixel.colors as colors


driver = DriverVisualizer(num=256, stayTop=True)
led = LEDStrip(driver, threadedUpdate=True)

from  strip.RGBClock import RGBClock
anim = RGBClock(led, 0, 10, 11, 20, 21, 30)
anim.run(fps=1, max_steps = 5)

from strip.Wave import Wave, WaveMove
anim = Wave(led, colors.Red, 2, start=0, end=-1)
anim.run(max_steps=100)

anim = WaveMove(led, colors.Red, 2, start=0, end=-1)
anim.run(max_steps=100)

from strip.Larson import LarsonScanner, LarsonRainbow
anim = LarsonScanner(led, colors.Red, tail=2, start=0, end=-1)
anim.run(max_steps=100)

anim = LarsonRainbow(led, tail=2, start=0, end=-1)
anim.run(max_steps=100)

from strip.FireFlies import FireFlies
anim = FireFlies(led, [colors.Red, colors.Green, colors.Blue], width=1, count=1, start=0, end=-1)
anim.run(max_steps=100)

from strip.PartyMode import PartyMode
anim = PartyMode(led, [colors.Red, colors.Green, colors.Blue], start=0, end=-1)
anim.run(max_steps=100)

from strip.ColorChase import ColorChase
anim = ColorChase(led, colors.Red, width=1, start=0, end=-1)
anim.run(max_steps=100)

from strip.ColorFade import ColorFade
anim = ColorFade(led, [colors.Red, colors.Blue], step=5, start=0, end=-1)
anim.run(max_steps=100)

from strip.ColorWipe import ColorWipe
anim = ColorWipe(led, colors.Red, start=0, end=-1)
anim.run(max_steps=100)

from strip.ColorPattern import ColorPattern
anim = ColorPattern(led, [colors.Red, colors.Green], 10, dir=True, start=0, end=-1)
anim.run(max_steps=100)

from strip.Rainbow import Rainbow, RainbowCycle
anim = Rainbow(led, start=0, end=-1)
anim.run(max_steps=100)

anim = RainbowCycle(led, start=0, end=-1)
anim.run(max_steps=100)
