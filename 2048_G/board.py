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


    @staticmethod
    def take_turn_R_D(board, R, score):
        # squeezing the numbers right
        board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in board], int)
        # adding the needed numbers
        merged = np.full((4, 4), False)
        for ix, iy in np.ndindex(board.shape):
            if iy < 3:
                if not (board[ix][iy] == 0) and board[ix][iy + 1] == board[ix][iy] and not merged[ix][iy] \
                        and not merged[ix][iy + 1]:
                    board[ix][iy + 1] *= 2
                    score += board[ix][iy + 1]
                    board[ix][iy] = 0
                    merged[ix][iy + 1] = True

        board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in board], int)
        if R:
            board = board.T
        return board, score

    # take turn for LEFT and UP
    @staticmethod
    def take_turn_L_U(board, U, score):
        # squeezing the numbers left
        board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in board], int)
        # adding the needed numbers
        merged = np.full((4, 4), False)
        for ix, iy in np.ndindex(board.shape):
            if iy > 0:
                if not (board[ix][iy] == 0) and board[ix][iy] == board[ix][iy - 1] and not merged[ix][iy - 1] \
                        and not merged[ix][iy]:
                    board[ix][iy - 1] *= 2
                    score += board[ix][iy - 1]
                    board[ix][iy] = 0
                    merged[ix][iy - 1] = True

        board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in board], int)
        if U:
            board = board.T
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
