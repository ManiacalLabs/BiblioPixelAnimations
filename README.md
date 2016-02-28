BiblioPixelAnimations
=====================

User created animations for BiblioPixel.

## Installation ##
You can always just download the code directly from here, but it's much easier to use the repository when it's installed, so the animations are available in your python path. But this is not a normal repository, so making it available in PyPi makes no sense. It's always in flux and normal version numbers and releases would be too hard to keep up with, since it's not a typical library. It's just a place for awesome BiblioPixel animations to live. To install *or upgrade* the repository, just run the following command:

```
pip install https://github.com/ManiacalLabs/BiblioPixelAnimations/archive/master.zip --upgrade
```

This will clone the latest code from GitHub and install it to your python path.

## Using Animations ##

A simple example of how to use the animations in this repo. 

```
from bibliopixel.drivers.serial_driver import *
from bibliopixel import LEDStrip
#import the module you'd like to use
from BiblioPixelAnimations.strip import Rainbows

#init driver with the type and count of LEDs you're using
driver = DriverSerial(type=LEDTYPE.WS2812B, num=10)

#init controller
led = LEDStrip(driver)

#init animation; replace with whichever animation you'd like to use
anim = Rainbows.RainbowCycle(led)

try:
    #run the animation
    anim.run()
except KeyboardInterrupt:
    #Ctrl+C will exit the animation and turn the LEDs offs
    led.all_off()
    led.update()
```

## PixelWeb ##

For information on how to make your animation PixelWeb ready, checkout the PixelWeb wikie: https://github.com/ManiacalLabs/PixelWeb/wiki/Manifests

## Submit ##

To submit, please post to our [forum](http://forum.maniacallabs.com/forumdisplay.php?fid=6). We will add them to this repository as we have time. Or, if you would like to help, fork this repository, add your animation as a new file under /matrix or /strip and submit a pull request.

Please include author information in a comment block at the top of your file. By submitting, you agree to provide your animations under the included MIT license.

## Style Guide ##

Please follow the [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/) coding guidelines. Please upload one animtion per file unless multiple files are required and consider reusability by other developers.

##Modules##

If your animation is big enough to require multiple files please build this in to a standalone module and place it in it's own folder.
