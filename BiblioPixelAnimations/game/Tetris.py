# Based on: https://gist.github.com/kch42/565419

from random import randrange as rand
import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim


# The configuration
cols = 19
rows = 40
maxfps = 30

color_map = [
    (0, 0, 0),
    colors.Red,
    colors.Orange,
    colors.Yellow,
    colors.Green,
    colors.Blue,
    colors.Purple,
    colors.Violet,

    colors.Cyan,
    colors.SeaGreen,
    colors.Navy,
    colors.YellowGreen,
    colors.DarkRed,
    colors.Teal,
    colors.MediumVioletRed,
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]],

    [[8]],

    [[9, 0, 0],
     [9, 9, 0],
     [9, 9, 9]],

    [[10, 0, 10],
     [10, 10, 10]],

    [[0, 11, 0],
     [11, 11, 11],
     [0, 11, 0]],

    [[12, 0, 0],
     [12, 12, 12],
     [0, 0, 12]],

    [[13, 13, 13],
     [13, 0, 13],
     [13, 13, 13]],

    [[14, 0, 0],
     [14, 0, 0],
     [14, 14, 14]],
]


def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board


def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + off_y - 1	][cx + off_x] += val
    return mat1


def new_board():
    board = [[0 for x in range(cols)] for y in range(rows)]
    return board


class Tetris(BaseGameAnim):

    def __init__(self, layout, inputDev, evil=False):
        super(Tetris, self).__init__(layout, inputDev)

        if (self.width, self.height) != (25, 50):
            raise Exception(
                "Sorry, this was lazily written to only work on a 25x50 display :(")

        if hasattr(self._input_dev, "setLights") and hasattr(self._input_dev, "setLightsOff"):
            self._input_dev.setLightsOff(5)
            lights = {
                "Y": (0, 255, 0),
                "B": (0, 0, 0),
                "X": (0, 0, 0),
                "A": (255, 0, 0),
                "SELECT": (255, 0, 0)
            }
            self._input_dev.setLights(lights)

        self.setSpeed("drop", 5)
        self.rlim = cols
        self._evilMode = evil
        self._doEvil = False
        self.next_stone = self._getNextPiece()

        self.addKeyFunc("LEFT", lambda: self.move(-1), speed=3, hold=True)
        self.addKeyFunc("RIGHT", lambda: self.move(+1), speed=3, hold=True)
        self.addKeyFunc("DOWN", lambda: self.drop(True), speed=1, hold=True)
        self.addKeyFunc(["A"], self.rotate_stone, speed=1, hold=False)
        self.addKeyFunc(["B", "SELECT"], self.insta_drop, speed=1, hold=False)
        self.addKeyFunc("START", self.togglePause, speed=1, hold=False)
        self.init_game()

    def _getNextPiece(self):
        stop = len(tetris_shapes) if self._doEvil else 7
        return tetris_shapes[rand(0, stop)]

    def togglePause(self):
        self.paused = not self.paused

    def clearLevelUp(self):
        self.doStart = False
        if self.levelUp:
            self.paused = False
            self.levelUp = False

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = self._getNextPiece()
        self.stone_x = int(cols // 2 - len(self.stone[0]) // 2)
        self.stone_y = 0

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.lines_per_level = 6
        self.gameover = False
        self.win = False
        self.levelUp = True
        self.doStart = False
        self.paused = True
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0

    def disp_msg(self, msg, x, y):
        self.layout.drawText(msg, x, y, font_scale=1,
                             font='6x4', color=colors.White)

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    self.layout.set(off_x + x, off_y + y, color_map[val])

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        if n > 0 and self._evilMode and not self._doEvil:
            self._doEvil = True
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level * self.lines_per_level:
            self.level += 1
            self.levelUp = True
            self.paused = True
            s = self.getSpeed("drop")
            s -= 1
            if s <= 0:
                self.win = True
            else:
                self.setSpeed("drop", s)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                    self.board,
                    self.stone,
                    (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board):
                        if 0 not in row:
                            self.board = remove_row(
                                self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        self.doStart = False
        if self.gameover or self.win:
            self.init_game()
            self.gameover = False

    def step(self, amt=1):
        if (self.levelUp or self.gameover or self.win) and (self._lastKeys != self._keys) and any(v is True for v in self._keys.itervalues()):
            self.doStart = True
        if self.doStart:
            if not any(v is True for v in self._keys.itervalues()):
                if self.levelUp:
                    self.clearLevelUp()
                elif self.gameover or self.win:
                    self.start_game()
            else:
                return

        if not self.doStart:
            self.handleKeys()

        self.layout.all_off()
        if self.gameover:
            self.layout.all_off()
            self.layout.drawText("GAME", self.width // 2 - 11,
                                 self.height // 2 - 8, color=colors.Green)
            self.layout.drawText("OVER", self.width // 2 - 11,
                                 self.height // 2 + 1, color=colors.Green)
            s = "{}".format(self.score)
            self.layout.drawText(s, self.width // 2 - (len(s) * 4) //
                                 2 + 1, self.height // 2 + 9, font_scale=1, font='6x4', color=colors.Green)
        elif self.win:
            for x in range(self.width):
                c = colors.hue_helper(
                    self.width - x, self.width, self._speedStep * 2)
                self.layout.drawLine(self.width // 2, self.height // 2, x, 0, c)
                self.layout.drawLine(self.width // 2, self.height // 2,
                                     self.width - 1 - x, self.height - 1, c)
            for y in range(self.height):
                c = colors.hue_helper(y, self.height, self._speedStep * 2)
                self.layout.drawLine(self.width // 2, self.height // 2, 0, y, c)
                self.layout.drawLine(self.width // 2, self.height // 2,
                                     self.width - 1, self.height - 1 - y, c)

            self.layout.drawText("YOU", self.width // 2 - 9,
                                 self.height // 2 - 8, color=colors.Black, bg=None)
            self.layout.drawText("WIN!", self.width // 2 - 10,
                                 self.height // 2 + 1, color=colors.Black, bg=None)
        else:
            if self.paused:
                self.layout.all_off()
                if self.levelUp:
                    self.layout.drawText(
                        "LVL", self.width // 2 - 8, self.height // 2 - 8, color=colors.Green)
                    str_level = "{}".format(self.level)
                    self.layout.drawText(
                        str_level, self.width // 2 - (len(str_level) * 6) // 2 + 1, self.height // 2 + 1, color=colors.Green)
                else:
                    x = self.width // 2 - 2
                    y = 1
                    self.layout.drawText("P", x, y + 0, color=colors.White)
                    self.layout.drawText("A", x, y + 8, color=colors.White)
                    self.layout.drawText("U", x, y + 16, color=colors.White)
                    self.layout.drawText("S", x, y + 24, color=colors.White)
                    self.layout.drawText("E", x, y + 32, color=colors.White)
                    self.layout.drawText("D", x, y + 40, color=colors.White)

            else:
                self.disp_msg("{}".format(self.score), 1, 1)

                lines_left = self.level * self.lines_per_level - self.lines
                for l in range(lines_left):
                    self.layout.set(0, self.height - 1 - l * 2, colors.Red)

                # draw rainbow border
                self.layout.drawLine(2, 8, cols + 3, 8,
                                     colorFunc=lambda pos: colors.hue_helper(pos, cols + 2, self._speedStep * 2))
                self.layout.drawLine(2, self.height - 1, cols + 3, self.height - 1,
                                     colorFunc=lambda pos: colors.hue_helper(cols + 2 - pos, cols + 2, self._speedStep * 2))
                self.layout.drawLine(2, 9, 2, self.height - 2,
                                     colorFunc=lambda pos: colors.hue_helper(rows + 2 - pos, rows, self._speedStep * 2))
                self.layout.drawLine(cols + 3, 9, cols + 3, self.height - 2,
                                     colorFunc=lambda pos: colors.hue_helper(pos, rows, self._speedStep * 2))

                # draw current board state
                self.draw_matrix(self.board, (3, 9))
                # draw current block
                self.draw_matrix(
                    self.stone, (self.stone_x + 3, self.stone_y + 9))
                # draw next block
                self.draw_matrix(self.next_stone, (self.width - 6, 1))
                # drop block
                if self.checkSpeed("drop"):
                    self.drop(False)

        self._step += amt
