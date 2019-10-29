import numpy as np
import pygame
import queue

from blocks import *
from board import *

class Player:
    def __init__(self):
        self.board = TetrisBoard()
        self.active_block = None

    def new_block(self, block_type=None):
        if self.active_block is not None:
            self.board.add_block(self.active_block)
        if block_type is None:
            block_type = np.random.choice(Block.get_random_block())
        rand_block = block_type(3)
        self.active_block = rand_block
        return block_type

    def _move(self, axis, step):
        curr = getattr(self.active_block, axis)
        setattr(self.active_block, axis, curr + step)
        if not self.board.valid_move(self.active_block):
            setattr(self.active_block, axis, curr)
            return False
        else:
            return True

    def left(self):
        return self._move('x', -1)

    def right(self):
        return self._move('x', +1)

    def down(self):
        return self._move('y', +1)

    def up(self):
        return self._move('y', -1)

    def rotate(self):
        self.active_block.rotate()
        # We try a horizontal wall-kick
        # if not self.board.valid_move(self.active_block):
        #     self.active_block.x += 1
        # if not self.board.valid_move(self.active_block):
        #     self.active_block.x -= 2
        if not self.board.valid_move(self.active_block):
            # self.active_block.x += 1
            self.active_block.inv_rotate()

    def add_lines(self, n=1):
        for _ in range(n):
            if self.board.upper_row_contains_block():
                return True
            self.board.add_line()
            while not self.board.valid_move(self.active_block):
                if not self.up():
                    return True
        return False

    def game_over(self):
        return not self.board.valid_move(self.active_block)

    def clear_lines(self):
        return self.board.clear_lines()

    def drop(self):
        while self.down():
            pass


class TetrisBattle:
    color_map = {
        1: (0, 255, 0),
        2: (255, 0, 0),
        3: (0, 255, 255),
        4: (255, 255, 0),
        5: (255, 165, 0),
        6: (0, 0, 255),
        7: (128, 0, 128),
        8: (128, 128, 128),
        9: (255, 192, 203),
    }
    line_adds = {
        0: 0,
        1: 0,
        2: 1,
        3: 2,
        4: 4
    }

    def __init__(self, width, height):
        self.players = [Player(), Player()]
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((self.width, self.height))
        self.board_width = self.width // 2
        block_size_x = self.width // (2 * self.players[0].board.width)
        block_size_y = self.height // self.players[0].board.height
        self.block_size = min(block_size_x, block_size_y)

        block_type = self.players[0].new_block()
        self.players[1].new_block(block_type)
        self.block_queues = [queue.Queue(), queue.Queue()]

    def _draw_grid(self):
        for pix, player in enumerate(self.players):
            sx = pix * self.board_width
            for i in range(len(player.board.board)):
                pygame.draw.line(
                    self.window,
                    (255, 255, 255),
                    (sx, i*self.block_size),
                    (sx + self.board_width, i*self.block_size)
                )
                for j in range(len(player.board.board[i]) + 1):
                    pygame.draw.line(
                        self.window,
                        (255, 255, 255),
                        (sx + j*self.block_size, 0),
                        (sx + j*self.block_size, self.height)
                    )

    def _draw_board(self):
        for pix, player in enumerate(self.players):
            sx = pix * self.board_width
            for i in range(len(player.board.board)):
                for j in range(len(player.board.board[i])):
                    if player.board.board[i][j] > 0:
                        pygame.draw.rect(
                            self.window, 
                            TetrisBattle.color_map[player.board.board[i][j]],
                            (sx + j*self.block_size, i*self.block_size,
                             self.block_size, self.block_size),
                            0
                        )

    def _draw_piece(self):
        for pix, player in enumerate(self.players):
            sx = pix * self.board_width
            c = TetrisBattle.color_map[np.max(player.active_block.block)]
            for i in range(player.active_block.block.shape[0]):
                for j in range(player.active_block.block.shape[1]):
                    if (player.active_block.x + j >= 0 and 
                        player.active_block.y + i >= 0 and 
                        player.active_block.block[i][j] > 0):
                        pygame.draw.rect(
                            self.window, c,
                            (sx + (player.active_block.x + j)*self.block_size,
                             (player.active_block.y + i)*self.block_size,
                             self.block_size, self.block_size),
                            0
                        )

    def draw(self):
        self.window.fill((0, 0, 0))
        self._draw_board()
        self._draw_piece()
        self._draw_grid()

    def play(self):
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.5
        run = True
        while run:
            fall_time += clock.get_rawtime()
            clock.tick()
            change_piece = [False, False]

            if fall_time/1000 > fall_speed:
               fall_time = 0
               for pix, player in enumerate(self.players):
                   if not player.down():
                       change_piece[pix] = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.players[0].left()
                    if event.key == pygame.K_RIGHT:
                        self.players[0].right()
                    if event.key == pygame.K_DOWN:
                        change_piece[0] = not self.players[0].down()
                    if event.key == pygame.K_UP:
                        self.players[0].rotate()
                    if event.key == pygame.K_RCTRL:
                        self.players[0].drop()
                        change_piece[0] = True

                    if event.key == pygame.K_a:
                        self.players[1].left()
                    if event.key == pygame.K_d:
                        self.players[1].right()
                    if event.key == pygame.K_s:
                        change_piece[1] = not self.players[1].down()
                    if event.key == pygame.K_w:
                        self.players[1].rotate()
                    if event.key == pygame.K_SPACE:
                        self.players[1].drop()
                        change_piece[1] = True

            for pix, player in enumerate(self.players):
                if change_piece[pix]:
                    if self.block_queues[pix].empty():
                        self.block_queues[1 - pix].put(self.players[pix].new_block())
                    else:
                        self.players[pix].new_block(self.block_queues[pix].get())

                    nr_lines = self.players[pix].clear_lines()
                    run = not self.players[1-pix].add_lines(TetrisBattle.line_adds[nr_lines])
                    run = not self.players[pix].game_over()

            self.draw()
            pygame.display.update()

        input()

TetrisBattle(720, 600).play()