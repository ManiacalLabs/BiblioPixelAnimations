import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim
from random import randint
import bibliopixel.util as util


class Snake(BaseGameAnim):

    def __init__(self, layout, inputDev):
        super(Snake, self).__init__(layout, inputDev)
        self._growLen = 4
        self._lives = 4
        self._level = 1
        self._apCount = 0
        self._apGoal = 6
        self._lastKeys = None
        self._apple = (-1, -1)
        self._gameOver = False
        self._gameOverCount = 0
        self._levelUp = True
        self._growCount = 0
        self._directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        self.doStart = False

        self.setSpeed("move", 4)

        if hasattr(self._input_dev, "setLights") and hasattr(self._input_dev, "setLightsOff"):
            self._input_dev.setLightsOff(5)
            lights = {
                "A": (0, 0, 0),
                "B": (0, 0, 0),
                "X": (0, 0, 0),
                "Y": (0, 0, 0),
                "START": (0, 0, 0)
            }
            self._input_dev.setLights(lights)

        self.addKeyFunc("UP", lambda: self.changeDir(0), speed=1, hold=False)
        self.addKeyFunc("DOWN", lambda: self.changeDir(1), speed=1, hold=False)
        self.addKeyFunc("RIGHT", lambda: self.changeDir(2),
                        speed=1, hold=False)
        self.addKeyFunc("LEFT", lambda: self.changeDir(3), speed=1, hold=False)

        self.resetBody()
        self.placeApple()

    def drawBody(self):
        body_len = len(self._body)
        i = 0
        for b in self._body:
            c = colors.hue_helper(i, body_len, 1)
            x, y = b
            self.layout.set(x, y, c)
            i += 1

    def drawLives(self):
        for i in range(self._lives):
            self.layout.set(self.width - 1 - i * 2, 0, colors.Red)

    def drawApplesLeft(self):
        for i in range(self._apGoal - self._apCount):
            self.layout.set(i * 2, 0, colors.Green)

    def drawApple(self):
        x, y = self._apple
        self.layout.set(x, y, colors.Green)

    def resetBody(self):
        dx, dy = self._dir = self._directions[0]  # randint(0,3)]
        dx, dy = dx * -1, dy * -1
        x, y = self._pos = (self.layout.width // 2, self.layout.height // 2)
        self._body = []
        for i in range(self._growLen):
            self._body.append(((x + (i * dx)), (y + (i * dy))))
        self._newDir = None

    def gameOver(self):
        self._gameOver = True
        self._gameOverCount = 0
        self._levelUp = True
        self._level = 1
        self.setSpeed("move", 4)
        self._lives = 4

    def dead(self):
        self._apCount = 0
        self._lives -= 1
        self._levelUp = True
        if self._lives <= 0:
            self.gameOver()

    def nextLevel(self):
        self._apCount = 0
        self._levelUp = True
        self._level += 1
        self._growLen += 1
        s = self.getSpeed("move") - 1
        if s < 1:
            s = 1
        self.setSpeed("move", s)
        # self._speed += self._speedGrow
        self.resetBody()

    def move(self):
        if self.checkSpeed("move"):
            x, y = self._pos = util.tuple_add(self._dir, self._pos)
            self._body.insert(0, (x, y))
            if (x, y) == self._apple:
                self._growCount = self._growLen
                self._apCount += 1
                self.placeApple()

            if self._growCount == 0:
                del self._body[-1]
            else:
                self._growCount -= 1

            if self._newDir:
                self._dir = self._newDir
                self._newDir = None

            if(x < 0 or x >= self.width or y < 1 or y >= self.height) or (x, y) in self._body[1:]:
                self.dead()
            else:
                if self._apCount >= self._apGoal:
                    self.nextLevel()

    def placeApple(self):
        while True:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            if (x, y) not in self._body:
                break
        self._apple = (x, y)

    def changeDir(self, newDir):
        self._pos = self._body[0]
        if newDir == 0 and self._dir[1] == 0:
            self._newDir = self._directions[0]
        if newDir == 1 and self._dir[1] == 0:
            self._newDir = self._directions[1]
        if newDir == 2 and self._dir[0] == 0:
            self._newDir = self._directions[2]
        if newDir == 3 and self._dir[0] == 0:
            self._newDir = self._directions[3]

    def step(self, amt=1):

        if (self._levelUp or self._gameOver) and (self._lastKeys != self._keys) and any(v is True for v in self._keys.itervalues()):
            self.doStart = True
        if self.doStart:
            if not any(v is True for v in self._keys.itervalues()):
                if self._levelUp:
                    self.doStart = False
                    self._levelUp = False
                    self.resetBody()
                    self.placeApple()
                elif self._gameOver:
                    self.doStart = False
                    self._gameOver = False
                    self.resetBody()
                    self.placeApple()
            else:
                return
        else:
            self.handleKeys()

        if self._gameOver:
            self.layout.all_off()
            self.layout.drawText("GAME", self.width // 2 - 11,
                                 self.height // 2 - 8, color=colors.Red)
            self.layout.drawText("OVER", self.width // 2 - 11,
                                 self.height // 2 + 1, color=colors.Red)
            # self._gameOverCount += 1
            # if self._gameOverCount > 45:
            #     self.resetBody()
            #     self.placeApple()
            #     self._gameOver = False
        elif self._levelUp:
            self.layout.all_off()
            self.layout.drawText("LVL", self.width // 2 - 8,
                                 self.height // 2 - 8, color=colors.Red)
            lvl = "{}".format(self._level)
            w = len(lvl) * 6

            self.layout.drawText(lvl, self.width // 2 - (w // 2),
                                 self.height // 2 + 1, color=colors.Red)
            # if self._keys.FIRE:#any(v > 0 for v in self._keys.itervalues()):
            #     self._levelUp = False
            #     self.resetBody()
            #     self.placeApple()
            #     self._lastKeys = None
        else:

            self.move()
            self.layout.all_off()
            self.drawBody()
            self.drawApple()
            self.drawApplesLeft()
            self.drawLives()
