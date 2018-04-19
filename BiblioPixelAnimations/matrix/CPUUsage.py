from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import colors

import psutil
from collections import deque


class CPUUsage(BaseMatrixAnim):

    def __init__(self, layout, onColor=colors.Red):
        super(CPUUsage, self).__init__(layout)
        self._onColor = onColor

        self._usage = deque(iterable=[0] * self.width, maxlen=self.width)

    def step(self, amt=1):
        self.internal_delay = 0.5
        self.layout.all_off()
        usage = psutil.cpu_percent()
        self._usage.append(int(usage // 100.0 * self.height))

        for x in range(self.width):
            if self._usage[x] > 0:
                self.layout.drawLine(x, self.height, x, self.height - 1 - self._usage[x], self._onColor)
