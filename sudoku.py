from board import Board
from dfs import dfs

# https://en.wikipedia.org/wiki/Sudoku
PROBLEM = (
    '53  7    \n'
    '6  195   \n'
    ' 98    6 \n'
    '8   6   3\n'
    '4  8 3  1\n'
    '7   2   6\n'
    ' 6    28 \n'
    '   419  5\n'
    '    8  79')
SOLUTION = (
    '534678912\n'
    '672195348\n'
    '198342567\n'
    '859761423\n'
    '426853791\n'
    '713924856\n'
    '961537284\n'
    '287419635\n'
    '345286179')

# https://www.websudoku.com/
EASY = (
    '7   91 35\n'
    ' 1   3   \n'
    '9 3 67   \n'
    '845 3 61 \n'
    '         \n'
    ' 36 5 487\n'
    '   47 9 8\n'
    '   9   6 \n'
    '65 31   4')
MEDIUM = (
    '12735    \n'
    '    7    \n'
    '  8 6  7 \n'
    '81 5    4\n'
    '2  7 4  1\n'
    '4    3 95\n'
    ' 9  2 6  \n'
    '    4    \n'
    '    31259')
HARD = (
    '  26  5  \n'
    '        3\n'
    '8  1  92 \n'
    ' 3  7   9\n'
    '27     54\n'
    '9   8  6 \n'
    ' 24  6  7\n'
    '3        \n'
    '  5  26  ')
EVIL = (
    ' 18 6    \n'
    '3    9   \n'
    '  9  34  \n'
    ' 9 1    5\n'
    ' 42   71 \n'
    '5    2 8 \n'
    '  45  6  \n'
    '   8    7\n'
    '    7 84 ')


class SearchProblem:
    '''探索問題を定義する抽象クラス'''
    def get_start_state(self):
        '''初期状態を返す関数'''
        raise NotImplementedError

    def next_states(self, state):
        '''与えられた状態 state から遷移できる状態のリストを返す関数'''
        raise NotImplementedError

    def is_goal(self, state):
        '''与えられた状態 state がゴールかどうかを True/False で返す関数'''
        raise NotImplementedError


class Sudoku(SearchProblem):
    def __init__(self, board):
        self.board = board
        #self.

    def get_start_state(self):
        return self.board

    def is_goal(self, board):
        return board.filled() and board.verify()

    def next_states(self, board):
        import copy

        #候補表
        allowed_digits_table = [[0 for i in range(9)] for j in range(9)]
        for (x, y) in [(i // 9, i % 9) for i in range(9 * 9)]:
            allowed_digits_table[x][y] = board.get_allowed_digits(x, y)

        #消去法
        while True: #do-while

            #更新前
            allowed_digits_table_b = copy.deepcopy(allowed_digits_table)
            
            #候補が1つのセルの座標リストの表
            confirmed_cell = []
            for (x, y) in [(i // 9, i % 9) for i in range(9 * 9)]:
                if len(allowed_digits_table[x][y]) == 1:
                    confirmed_cell += [(x, y)]

            #候補の除外
            for x, y in confirmed_cell: #(x, y): 候補が1つのセルの座標
                #エリア
                for (gx, gy) in [(3 * (x // 3) + (i // 3), 3 * (y // 3) + (i % 3)) for i in range(3 * 3)]:
                    if (gx, gy) != (x, y):
                        allowed_digits_table[gx][gy] = list(set(allowed_digits_table[gx][gy]) - set(allowed_digits_table[x][y]))
                
                for index in range(0, 9):
                    #行
                    if (x, index) != (x, y):
                        allowed_digits_table[x][index] = list(set(allowed_digits_table[x][index]) - set(allowed_digits_table[x][y]))
                    #列
                    if (index, y) != (x, y):
                        allowed_digits_table[index][y] = list(set(allowed_digits_table[index][y]) - set(allowed_digits_table[x][y]))
            
            if not(allowed_digits_table_b != allowed_digits_table):
                break

        #NakedPair法
        while True:

            #更新前
            allowed_digits_table_b = copy.deepcopy(allowed_digits_table)

            #エリア

            if not(allowed_digits_table_b != allowed_digits_table):
                break


        
        #インスタンス生成
        next_boards = []
        for (x, y) in [(i // 9, i % 9) for i in range(9 * 9)]:
            for n in allowed_digits_table[x][y]:
                if board.data[x][y] == 0:
                    #背理法
                    candidate_state = board.move(x, y, n)
                    noContradiction = True
                    for (x, y) in [(i // 9, i % 9) for i in range(9 * 9)]:
                        noContradiction &= not(candidate_state.data[x][y] == 0 and len(candidate_state.get_allowed_digits(x, y)) == 0)
                    if noContradiction:
                        next_boards += [candidate_state]

        return next_boards


def text_to_data(text):
    data = []
    for line in text.splitlines():
        assert len(line) == 9
        data.append(list(map(int, line.replace(' ', '0'))))
    return data

def test(title, problem):
    print('\nTesting %s problem...' % title)
    board = Board(text_to_data(problem))
    sudoku = Sudoku(board)
    boards = dfs(sudoku)
    print('%d Board objects instantiated' % Board.num_objects)
    assert boards[-1].verify()


if __name__ == '__main__':
    board = Board(text_to_data(MEDIUM))
    sudoku = Sudoku(board)
    boards = dfs(sudoku)
    for i, board in enumerate(boards):
        print('\nSTEP %d' % i)
        print(board)
    print('%d Board objects instantiated' % Board.num_objects)
    #assert boards[-1].data == text_to_data(SOLUTION)

    test('easy', EASY)
    test('medium', MEDIUM)
    test('hard', HARD)
    test('evil', EVIL)