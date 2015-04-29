Strip Animations
=====================

Animations that inherit from BaseStripAnim

## Alternates ##
This animation alternates colours on every other pixel and then animates them flipping between the default colours White and Off.

### Usage ###
Alternates has 3 optional properties

* max_led - int the number of pixels you want used
* color1 - (int, int, int) the color you want the odd pixels to be
* color2 - (int, int, int) the color you want the even pixels to be

In code:

	from Alternates import Alternates
	...
	anim = Alternates(led, max_led=10, color1=(255, 0, 0), color2=(0, 0, 255))

Best run in the region of 5-10 FPS

## PixelPingPong ##
This animation runs 1 or many pixels from one end of a strip to the other.

### Usage ###
Alternates has 3 optional properties

* max_led - int the number of pixels you want used
* color - (int, int, int) the color you want the pixels to be
* additional_pixels - int the number of pixels you want to ping pong

In code:

	from PixelPingPong import PixelPingPong
	...
	anim = PixelPingPong(led, max_led=30, color=(0, 0, 255), additional_pixels=5)

Best run in the region of 5-200 FPS
