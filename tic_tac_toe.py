import random

FIGURES = ['x', 'o']

class player():

    def move(self, board):
        success = False
        while not success:
            try:
                print('your turn')
                i, j = map(int, input('enter row and col >> ').split())
                board.put(i, j)
                success = True
            except (IndexError, RuntimeError, ValueError) as e:
                print(e)

class bot(player):

    def __init__(self, first):
        super().__init__()
        self.first = first

    def move(self, board):
        print("computer's move")
        moves = {0: [], 1: [], -1:[]}
        if len(board.get_free_positions()) == board.n**2:
            board.put(1, 1) # fist move is a center
            return
        for pos in board.get_free_positions():
            board.put(*pos)
            score = self.minimax(board, not self.first)
            moves[score].append(pos)
            board.remove(*pos)
        if self.first:
            if moves[1]:
                bm = random.choice(moves[1])
            elif moves[0]:
                bm = random.choice(moves[0])
            else:
                bm = random.choice(moves[-1])
        else:
            if moves[-1]:
                bm = random.choice(moves[-1])
            elif moves[0]:
                bm = random.choice(moves[0])
            else:
                bm = random.choice(moves[1])
        board.put(*bm)


    def minimax(self, board, maximizing, depth = 0):
        '''
        let first player be maximizing player
        '''
        if (status := board.game_status()) != board.blank or board.occupied == board.n ** 2:
            if status == board.blank:
                return 0
            elif status == FIGURES[0]:
                return 1 # return 1 if the first player have won
            else:
                return -1
            
        elif maximizing:
            max_eval = float('-inf')
            for pos in board.get_free_positions():
                board.put(*pos)
                eval = self.minimax(board, False, depth + 1)
                board.remove(*pos)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for pos in board.get_free_positions():
                board.put(*pos)
                eval = self.minimax(board, True, depth + 1)
                board.remove(*pos)
                min_eval = min(min_eval, eval)
            return min_eval


class board():

    def __init__(self, n = 3):
        self.figures = FIGURES
        self.idx = 0
        self.blank = ' '
        self.n = n
        self.occupied = 0
        self.b = [[self.blank] * n for _ in range(n)]
        self.free_positions = set([(i, j) for i in range(self.n) for j in range(self.n)])

    def put(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            raise IndexError(f'({i, j}) is out of bounds')
        if self.b[i][j] != self.blank:
            raise RuntimeError(f'({i, j}) is already occupied')
        self.b[i][j] = self.figures[self.idx]
        self.idx = not self.idx
        self.occupied += 1
        self.free_positions.remove((i, j))

    def remove(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            raise IndexError(f'({i, j}) is out of bounds')
        self.b[i][j] = self.blank
        self.idx = not self.idx
        self.occupied -= 1
        self.free_positions.add((i, j))

    def get_diagonal(self, anti = False):
        if anti:
            return [self.b[i][self.n - i - 1] for i in range(self.n)]
        return [self.b[i][i] for i in range(self.n)]
    
    def get_line(self, axis, number):
        if axis not in (0, 1) or number < 0 or number >= self.n:
            raise IndexError(f'cant get list from this position {axis=}, {number=}')
        if axis == 0:
            return self.b[number]
        else:
            return [self.b[i][number] for i in range(self.n)]

    def is_line_finished(self, line):
        return all(map(lambda x: x == line[0] and x != self.blank, line))

    def get_free_positions(self):
        return self.free_positions
    
    def game_status(self):
        d1, d2 = self.get_diagonal(), self.get_diagonal(anti = True)
        if self.is_line_finished(d1):
            return d1[0]
        elif self.is_line_finished(d2):
            return d2[0]
        for i in range(self.n):
            line1 = self.get_line(0, i)
            line2 = self.get_line(1, i)
            if self.is_line_finished(line1):
                return line1[0]
            if self.is_line_finished(line2):
                return line2[0]
        return self.blank

    def __str__(self):
        return '\n'.join(('|'.join(self.b[i]) for i in range(self.n)))
        

class game():

    def __init__(self, p1, p2, board):
        self.players = [p1, p2]
        self.counter = 0
        self.player = self.players[0]
        self.board = board

    def next_player(self):
        return self.players[self.counter % 2]

    def play(self):
        while (not(status := self.board.game_status()) != self.board.blank
            and self.board.occupied < self.board.n ** 2):
            print(self.board)
            print('-'*10)
            self.player.move(self.board)
            self.counter += 1
            self.player = self.next_player()
        print(self.board)
        if status != self.board.blank:
            print('congratulations to', status)
        else:
            print('draw')

if __name__ == '__main__':
    while (choose := input(f'select from {FIGURES} >> ')) not in FIGURES:
        ...
    if choose == 'x':
        p1, p2 =  player(), bot(first = False)
    else:
        p1, p2 =  bot(first = True), player()
    print('rows and cols are numbered from 0')
    b = board()
    g = game(p1, p2, b)
    g.play()