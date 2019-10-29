import numpy as np


class TetrisBoard:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height

        # We are adding some extra lines to avoid pesky out-of-bounds errors
        self.__board = np.zeros((self.height + 4, self.width + 4), dtype=int)
        self.__board[:2, :] = 0
        self.__board[-2:, :] = 9
        self.__board[:, :2] = 9
        self.__board[:, -2:] = 9

    @property
    def board(self):
        """Cut off the extra lines when a user accesses the board"""
        return self.__board[2:-2, 2:-2]

    def add_block(self, block):
        """Adds the provided block to the board"""
        # We add +2 since we count from -2
        x, y = block.x + 2, block.y + 2
        self.__board[y:y + block.h,
                     x:x + block.w] += block.block

    def valid_move(self, block):
        """Checks whether block is on a valid position"""
        # We add +2 since we count from -2
        x, y = block.x + 2, block.y + 2
        if x < 0 or y < 0:
            return False

        mask = block.block > 0
        masked_board = np.multiply(
            mask,
            self.__board[y:y + block.h,
                         x:x + block.w]
        )
        return np.sum(masked_board) == 0    

    def clear_lines(self):
        """Clear the full lines from the board"""
        mask = np.all(self.board > 0, axis=1)
        full_lines = np.arange(self.board.shape[0])[mask]
        for line in full_lines:
            self.board[line, :] = 0
            self.board[1:line + 1] = self.board[:line]
            self.board[0, :] = 0
        return len(full_lines)

    def upper_row_contains_block(self):
        """Checks if the upper row of the board contains a filled cell"""
        return np.sum(self.board[0, :]) > 0

    def add_line(self):
        """Add a random line with a gap to the board"""
        line = np.ones(self.width) * 8
        gap = np.random.choice(range(2, self.width))
        line[gap] = 0
        self.board[:-1, :] = self.board[1:, :]
        self.board[-1, :] = line

    def __str__(self):
        return np.array2string(self.board,
                               max_line_width=2*self.width,
                               separator='')
