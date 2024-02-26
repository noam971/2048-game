import numpy as np
import board as Board
import random


def mcst_move(search_per_move, search_len, board_values):
    board = board_values.board
    moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    scores = np.zeros(4)

    for first_index in range(4):
        c_board = np.copy(board)
        first_board = Board.Board(0)
        first_board.board = c_board
        first_board.take_turn(moves[first_index])
        scores[first_index] += first_board.score

        for later_move in range(search_per_move):
            move_number = 1
            search_board = Board.Board(0)
            search_board.board = np.copy(first_board.board)
            search_board.score = first_board.score

            while search_board.check_valid_move() and move_number < search_len:
                turn = random.randint(0, 3)
                search_board.take_turn(moves[turn])
                scores[first_index] += search_board.score
                move_number += 1

            del search_board

        del c_board, first_board

    best_move_index = np.argmax(scores)
    if scores[best_move_index] == 0:
        best_move_index = random.randint(0, 3)

    best_move = moves[best_move_index]
    return best_move





