import numpy as np
import random


class Board:

    # take turn base on direction
    @staticmethod
    def take_turn(direc, board, score):
        if direc == 'UP':
            return Board.take_turn_L_U(board.T, True, score)
        elif direc == 'DOWN':
            return Board.take_turn_R_D(board.T, True, score)
        elif direc == 'RIGHT':
            return Board.take_turn_R_D(board, False, score)
        elif direc == 'LEFT':
            return Board.take_turn_L_U(board, False, score)

    # take turn for RIGHT and DOWN
    @staticmethod
    def take_turn_R_D(board, R, score):
        # squeezing the numbers to the right
        board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in board], int)
        board, score = Board.merge(board, score, True)
        # squeezing the numbers to the right after merging the numbers
        board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in board], int)
        if R:
            board = board.T
        return board, score

    # take turn for LEFT and UP
    @staticmethod
    def take_turn_L_U(board, U, score):
        # squeezing the numbers to the left
        board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in board], int)
        board, score = Board.merge(board, score, False)
        # squeezing the numbers to the left after merging the numbers
        board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in board], int)
        if U:
            board = board.T
        return board, score

    # adding the needed numbers
    @staticmethod
    def merge(board, score, R_D):
        merged = np.full((4, 4), False)
        shift_direction = 1
        for ix, iy in np.ndindex(board.shape):
            if R_D:
                shift_direction = -1
                iy = 3 - iy
            if (iy > 0 and not R_D) or (R_D and iy < 3):
                if not (board[ix][iy] == 0) and board[ix][iy] == board[ix][iy - shift_direction] \
                        and not merged[ix][iy - shift_direction] and not merged[ix][iy]:
                    board[ix][iy - shift_direction] *= 2
                    score += board[ix][iy - shift_direction]
                    board[ix][iy] = 0
                    merged[ix][iy - shift_direction] = True
        return board, score

    @staticmethod
    def new_pieces(board):
        full = False
        board_zeros = np.argwhere(board == 0)
        if len(board_zeros) != 0:
            rnd = random.randint(0, len(board_zeros) - 1)
            if random.randint(1, 10) == 4:
                board[board_zeros[rnd][0]][board_zeros[rnd][1]] = 4
            else:
                board[board_zeros[rnd][0]][board_zeros[rnd][1]] = 2
        else:
            full = True
        return board, full
