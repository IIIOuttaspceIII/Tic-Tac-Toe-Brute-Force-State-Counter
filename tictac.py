import math


class Noughts_Board:
    def __init__(self, board_state, depth):
        self.board = board_state
        self.current_depth = depth

    def get_player_id(self):
        return (self.current_depth % 2) + 1

    def get_empty_cells(self):
        empty_cells = []
        for i in range(9):
            if self.board[i] == 0:
                empty_cells.append(i)
        return empty_cells

    def boardspace_to_arrayspace(self, x, y):
        return x + y * 3

    def arrayspace_to_boardspace(self, index):
        return math.floor(index / 3), index % 3

    def get_player_at_space(self, x, y):
        return self.board[boardspace_to_arrayspace(x, y)]

    def has_finished(self):
        if self.has_won():
            return True
        elif 0 not in self.board:
            return True
        else:
            return False

    def has_won(self):
        for i in range(3):
            if self.check_row_for_win(i):
                return True
            if self.check_column_for_win(i):
                return True
        for i in range(2):
            if self.check_diagonal_for_win(i):
                return True
        return False

    def check_row_for_win(self, row):
        """ Correctly checks rows """
        if (self.board[row * 3] == 0):
            return False
        elif(len(set(self.board[row * 3:row * 3 + 3])) is not 1):
            return False
        return True

    def check_column_for_win(self, column):
        """ Correctly checks columns """
        if (self.board[column] == 0):
            return False
        elif(len(set(self.board[column:9:3])) is not 1):
            return False
        return True

    def check_diagonal_for_win(self, diagonal):
        """ Probably Works """
        cells = [0, 4, 8] if diagonal == 0 else [2, 4, 6]
        values = []
        for cell in cells:
            values.append(self.board[cell])
        if values[0] == 0:
            return False
        elif(len(set(values)) is not 1):
            return False
        return True

    def try_move(self, cell):
        """ returns new board state """
        if self.has_finished():
            return None

        if (self.board[cell] == 0):
            new_board = self.board.copy()

            new_board[cell] = self.get_player_id()
            return Noughts_Board(new_board, self.current_depth + 1)
        else:
            return None

    def permutate_board(self, order):
        new_board_array = []
        for permutation in order:
            new_board_array.append(self.board[permutation])
        new_board = Noughts_Board(new_board_array, self.current_depth)
        return new_board

    def get_rotated_board(self):
        perms = [2, 5, 8, 1, 4, 7, 0, 3, 6]
        return self.permutate_board(perms)

    def get_flipped_board(self):
        perms = [2, 1, 0, 5, 4, 3, 8, 7, 6]
        return self.permutate_board(perms)


class Noughts_Solver:
    def __init__(self, ignore_wins=True, ignore_start=True, ignore_rotations=True, ignore_flips=True):
        self.ignore_wins = ignore_wins
        self.ignore_start = ignore_start
        self.ignore_rotations = ignore_rotations
        self.ignore_flips = ignore_flips
        self.states = []

    def solve(self):
        starting_board = Noughts_Board([0] * 9, 0)
        if not self.ignore_start:
            self.try_add_new_state(starting_board)
        self.try_all_moves(starting_board)
        print(
            f"Found {len(self.states)} states or {math.ceil(math.log2(len(self.states)))} ({math.log2(len(self.states))}) bits")

    def try_all_moves(self, board):
        for i in range(9):
            self.try_move(board, i)

    def try_move(self, board, cell):
        new_board = board.try_move(cell)
        if new_board:
            self.try_add_new_state(new_board)
            self.try_all_moves(new_board)

    def is_board_saved(self, board):
        if board.board in self.states:
            return True

        if self.ignore_flips:  # Try to check if a flip exists
            flipped_board = board.get_flipped_board()
            if flipped_board.board in self.states:
                return True

        if self.ignore_rotations:  # Try check if a rotation exists
            rotated_board = board.get_rotated_board()
            for i in range(2):
                if rotated_board.board in self.states:
                    return True
                if self.ignore_flips:  # Try to check if a flip exists
                    flipped_board = rotated_board.get_flipped_board()
                    if flipped_board.board in self.states:
                        return True
                rotated_board = rotated_board.get_rotated_board()
        return False

    def try_add_new_state(self, board):
        if self.ignore_wins and board.has_won():
            return
        if not self.is_board_saved(board):
            self.states.append(board.board)
            if len(self.states) % 100 == 0:
                print(
                    f"{len(self.states)} or {math.ceil(math.log2(len(self.states)))} bits")


if __name__ == "__main__":
    noughts = Noughts_Solver()

    noughts.solve()
