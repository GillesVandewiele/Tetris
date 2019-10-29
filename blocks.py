import numpy as np


class Block:
    def __init__(self, x, y):
        """
        Parameters
        ----------
        x: int
            The column of the upper-left pixel of the block.
        y: int
            The row of the upper-left pixel of the block.
        """
        self.x = x
        self.y = y
        self.rotation = 0

    @property
    def block(self):
        return self.blocks[self.rotation]

    @property
    def h(self):
        return self.block.shape[0]

    @property
    def w(self):
        return self.block.shape[1]

    def rotate(self):
        self.rotation = (self.rotation + 1) % self.blocks.shape[0]

    def inv_rotate(self):
        self.rotation = (self.rotation - 1) % self.blocks.shape[0]

    @staticmethod
    def get_random_block():
        return list(Block.__subclasses__())


class BlockI(Block):
    def __init__(self, x, y=-2):
        super(BlockI, self).__init__(x, y)
        self.blocks = np.array([
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0]],

            [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]]], dtype=int
        )


class BlockJ(Block):
    def __init__(self, x, y=-1):
        super(BlockJ, self).__init__(x, y)
        self.blocks = np.array([
            [[0, 0, 0],
             [2, 2, 2],
             [0, 0, 2]],

            [[0, 2, 0],
             [0, 2, 0],
             [2, 2, 0]],

            [[2, 0, 0],
             [2, 2, 2],
             [0, 0, 0]],

            [[0, 2, 2],
             [0, 2, 0],
             [0, 2, 0]]], dtype=int
        )


class BlockL(Block):
    def __init__(self, x, y=-1):
        super(BlockL, self).__init__(x, y)
        self.blocks = np.array([
            [[0, 0, 0],
             [3, 3, 3],
             [3, 0, 0]],

            [[3, 3, 0],
             [0, 3, 0],
             [0, 3, 0]],

            [[0, 0, 3],
             [3, 3, 3],
             [0, 0, 0]],

            [[0, 3, 0],
             [0, 3, 0],
             [0, 3, 3]]], dtype=int
        )


class BlockO(Block):
    def __init__(self, x, y=-1):
        super(BlockO, self).__init__(x, y)
        self.blocks = np.array([
            [[0, 0, 0, 0],
             [0, 4, 4, 0],
             [0, 4, 4, 0],
             [0, 0, 0, 0]]], dtype=int
        )


class BlockS(Block):
    def __init__(self, x, y=-1):
        super(BlockS, self).__init__(x, y)
        self.blocks = np.array([
            [[0, 0, 0],
             [0, 5, 5],
             [5, 5, 0]],

            [[0, 5, 0],
             [0, 5, 5],
             [0, 0, 5]]], dtype=int
        )


class BlockZ(Block):
    def __init__(self, x, y=-1):
        super(BlockZ, self).__init__(x, y)
        self.blocks = np.array([
            [[0, 0, 0],
             [6, 6, 0],
             [0, 6, 6]],

            [[0, 0, 6],
             [0, 6, 6],
             [0, 6, 0]]], dtype=int
        )


class BlockT(Block):
    def __init__(self, x, y=-1):
        super(BlockT, self).__init__(x, y)
        self.blocks = np.array([
            [[0, 0, 0],
             [7, 7, 7],
             [0, 7, 0]],

            [[0, 7, 0],
             [7, 7, 0],
             [0, 7, 0]],

            [[0, 7, 0],
             [7, 7, 7],
             [0, 0, 0]],

            [[0, 7, 0],
             [0, 7, 7],
             [0, 7, 0]]], dtype=int
        )