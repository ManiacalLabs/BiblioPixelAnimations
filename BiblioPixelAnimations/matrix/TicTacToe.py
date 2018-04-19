# much of the code below borrowed from http://cwoebker.com/posts/tic-tac-toe
import random
from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors


class Tic(object):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('X-win', 'Draw', 'O-win')

    def __init__(self, squares=[]):
        if len(squares) == 0:
            self.clearBoard()
        else:
            self.squares = squares

    def clearBoard(self):
        self.squares = [None for i in range(9)]

    def available_moves(self):
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player):
        """what combos are available?"""
        return self.available_moves() + self.get_squares(player)

    def complete(self):
        """is the game over?"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() is not None:
            return True
        return False

    def X_won(self):
        return self.winner() == 'X'

    def O_won(self):
        return self.winner() == 'O'

    def tied(self):
        return self.complete() and self.winner() is None

    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                        break
                if win:
                    return player
        return None

    def winningCombo(self, player):
        positions = self.get_squares(player)
        winCombo = None
        for combo in self.winning_combos:
            win = True
            for pos in combo:
                if pos not in positions:
                    win = False
                    break
            if win:
                winCombo = combo
                break

        return winCombo

    def get_squares(self, player=None):
        """squares that belong to a player"""
        if player:
            return [k for k, v in enumerate(self.squares) if v == player]
        else:
            return self.squares

    def get_enemy(self, player):
        if player == 'X':
            return 'O'
        return 'X'

    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            result = 0
            if node.X_won():
                result = 1
            elif node.tied():
                result = 0
            elif node.O_won():
                result = -1
            if player == 'O':
                result = result * -1
            return result

        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, self.get_enemy(player), alpha, beta)
            node.make_move(move, None)
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta


class TicTacToe(BaseMatrixAnim):
    def __init__(self, layout):
        super(TicTacToe, self).__init__(layout)

        self._showWinCount = 0

    def pre_run(self):
        self._board = Tic()
        self._player = 'O'
        self._nextPlayer = 'O'

    def determine(self, board, player):
        a = -2
        choices = []
        if len(board.available_moves()) == 9:
            return random.randint(0, 8)
        for move in board.available_moves():
            board.make_move(move, player)
            val = board.alphabeta(board, self._board.get_enemy(player), -2, 2)
            board.make_move(move, None)
            if val > a:
                a = val
                choices = [move]
            elif val == a:
                choices.append(move)
        return random.choice(choices)

    def drawMove(self, index, player):
        x = index % 3
        y = index // 3
        cx = 3 + (x * 8)
        cy = 3 + (y * 8)

        if player == 'X':
            self.layout.drawLine(cx - 2, cy - 2, cx + 2, cy + 2, colors.Green)
            self.layout.drawLine(cx - 2, cy + 2, cx + 2, cy - 2, colors.Green)
        elif player == 'O':
            self.layout.drawCircle(cx, cy, 2, colors.Blue)

    def step(self, amt=1):
        winner = None
        winCombo = None
        complete = self._board.complete()

        if complete:
            winner = self._board.winner()
            if winner:
                winCombo = self._board.winningCombo(winner)

        self.layout.all_off()

        # right now just assuming 24x24, don't feel like doing the math for dynamic
        self.layout.drawLine(7, 0, 7, 22, colors.Red)
        self.layout.drawLine(15, 0, 15, 22, colors.Red)
        self.layout.drawLine(0, 7, 22, 7, colors.Red)
        self.layout.drawLine(0, 15, 22, 15, colors.Red)

        for i in range(9):
            self.drawMove(i, self._board.get_squares()[i])

        if winCombo:
            i = winCombo[0]
            x1 = ((i % 3) * 8) + 3
            y1 = ((i // 3) * 8) + 3
            i = winCombo[2]
            x2 = ((i % 3) * 8) + 3
            y2 = ((i // 3) * 8) + 3
            self.layout.drawLine(x1, y1, x2, y2, colors.White)

        self._step = 0

        if complete and self._showWinCount > 2:
            self._showWinCount = 0
            self._board.clearBoard()
            self._player = self._nextPlayer
            self._nextPlayer = self._board.get_enemy(self._nextPlayer)
            self.animComplete = True
        elif complete:
            self._showWinCount += 1

        if not complete:
            new_move = self.determine(self._board, self._player)
            self._board.make_move(new_move, self._player)
            self._player = self._board.get_enemy(self._player)
