from bibliopixel.animation.cube import BaseCubeAnim
import bibliopixel.colors as colors


class cuby(BaseCubeAnim):

    def __init__(self, led, color_list=[colors.Red]):
        super(cuby, self).__init__(led)
        self.colors = color_list
        self.color_index = 0
        self.max = max([self.x, self.y, self.z]) + 1

    def step(self, amt=1):
        self._led.all_off()

        for x in range(self._step):
            for y in range(self._step):
                for z in range(self._step):
                    self._led.set(x, y, z, self.colors[x % len(self.colors)])

        self._step += amt
        if(self._step >= self.max):
            self._step = 0
            self.color_index += 1
            if self.color_index >= len(self.colors):
                self.color_index = 0
