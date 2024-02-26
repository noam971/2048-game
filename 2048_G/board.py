import numpy as np
import random
import pygame


class Board:


    pygame.init()
    # 2048 color library
    colors = {0: (204, 192, 179),
              2: (238, 228, 218),
              4: (237, 224, 200),
              8: (242, 177, 121),
              16: (245, 149, 99),
              32: (246, 124, 95),
              64: (246, 94, 59),
              128: (237, 207, 114),
              256: (237, 204, 97),
              512: (237, 200, 80),
              1024: (237, 197, 63),
              2048: (237, 194, 46),
              4096: (32, 172, 47),
              8192: (255, 50, 70),
              'light text': (249, 246, 242),
              'dark text': (119, 110, 101),
              'other': (0, 0, 0),
              'bg': (187, 173, 160)}

    def __init__(self, score):
        self.score = score
        self.board = np.zeros((4, 4), int)
        self.font = pygame.font.Font('freesansbold.ttf', 24)

    def draw_board(self, screen, high_score):
        pygame.draw.rect(screen, self.colors['bg'], [0, 0, 400, 400], 0, 10)
        score_text = self.font.render(f'Score: {self.score}', True, 'black')
        high_score_text = self.font.render(f'High Score: {high_score}', True, 'black')
        screen.blit(score_text, (10, 410))
        screen.blit(high_score_text, (10, 450))

    def draw_pieces(self, screen):
        for idx, tile in np.ndenumerate(self.board):
            value = tile
            if value > 8:
                value_color = self.colors['light text']
            else:
                value_color = self.colors['dark text']
            if value <= 8192:
                color = self.colors[value]
            else:
                color = self.colors['other']
            pygame.draw.rect(screen, color, [idx[1] * 95 + 20, idx[0] * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(idx[1] * 95 + 57, idx[0] * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [idx[1] * 95 + 20, idx[0] * 95 + 20, 75, 75], 2, 5)

    # take turn base on direction
    def take_turn(self, direc):
        if direc == 'UP':
            self.take_turn_L_U(True)
        elif direc == 'DOWN':
            self.take_turn_R_D(True)
        elif direc == 'RIGHT':
            self.take_turn_R_D(False)
        elif direc == 'LEFT':
            self.take_turn_L_U(False)

    # take turn for RIGHT and DOWN
    def take_turn_R_D(self, R):
        if R:
            self.board = self.board.T
        # squeezing the numbers to the right
        self.board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in self.board], int)
        self.merge(True)
        # squeezing the numbers to the right after merging the numbers
        self.board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in self.board], int)
        if R:
            self.board = self.board.T

    # take turn for LEFT and UP
    def take_turn_L_U(self, U):
        if U:
            self.board = self.board.T
        # squeezing the numbers to the left
        self.board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in self.board], int)
        self.merge(False)
        # squeezing the numbers to the left after merging the numbers
        self.board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in self.board], int)
        if U:
            self.board = self.board.T

    # adding the needed numbers
    def merge(self, R_D):
        merged = np.full((4, 4), False)
        shift_direction = 1
        for ix, iy in np.ndindex(self.board.shape):
            if R_D:
                shift_direction = -1
                iy = 3 - iy
            if (iy > 0 and not R_D) or (R_D and iy < 3):
                if not (self.board[ix][iy] == 0) and self.board[ix][iy] == self.board[ix][iy - shift_direction] \
                        and not merged[ix][iy - shift_direction] and not merged[ix][iy]:
                    self.board[ix][iy - shift_direction] *= 2
                    self.score += self.board[ix][iy - shift_direction]
                    self.board[ix][iy] = 0
                    merged[ix][iy - shift_direction] = True

    def check_valid_move(self):
        if not np.any(self.board):
            return True
        else:
            for ix, iy in np.ndindex(self.board.shape):
                if ix < 3:
                    if self.board[ix][iy] == self.board[ix + 1][iy]:
                        return True
                if iy < 3:
                    if self.board[ix][iy] == self.board[ix][iy + 1]:
                        return True
        return False

    def new_pieces(self):
        full = False
        board_zeros = np.argwhere(self.board == 0)
        if len(board_zeros) != 0:
            rnd = random.randint(0, len(board_zeros) - 1)
            if random.randint(1, 10) == 4:
                self.board[board_zeros[rnd][0]][board_zeros[rnd][1]] = 4
            else:
                self.board[board_zeros[rnd][0]][board_zeros[rnd][1]] = 2
        else:
            full = True
        return full
