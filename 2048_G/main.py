# 2048 game :)
from game import Game
# import pygame
# import random
# import numpy as np
#
# pygame.init()
#
# # Initial setup
# WIDTH = 400
# HEIGHT = 500
# screen = pygame.display.set_mode([WIDTH, HEIGHT])
# pygame.display.set_caption('2048 :)')
# timer = pygame.time.Clock()
# fps = 60
# font = pygame.font.Font('freesansbold.ttf', 24)
#
# # 2048 color library
# colors = {0: (204, 192, 179),
#           2: (238, 228, 218),
#           4: (237, 224, 200),
#           8: (242, 177, 121),
#           16: (245, 149, 99),
#           32: (246, 124, 95),
#           64: (246, 94, 59),
#           128: (237, 207, 114),
#           256: (237, 204, 97),
#           512: (237, 200, 80),
#           1024: (237, 197, 63),
#           2048: (237, 194, 46),
#           4096: (32, 172, 47),
#           8192: (255, 50, 70),
#           'light text': (249, 246, 242),
#           'dark text': (119, 110, 101),
#           'other': (0, 0, 0),
#           'bg': (187, 173, 160)}
#
# # game variables initialize
# board_values = np.zeros((4, 4), int)
# game_over = False
# spawn_new = True
# init_count = 0
# direction = ''
# score = 0
# file = open('high_score', 'r')
# init_high = int(file.readline())
# file.close()
# high_score = init_high
#
#
# # draw game over and restart text
# def draw_over():
#
#     pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
#     game_over_text1 = font.render('Game Over :(', True, 'white')
#     game_over_text2 = font.render('Press Enter To Restart', True, 'white')
#     screen.blit(game_over_text1, (130, 65))
#     screen.blit(game_over_text2, (70, 105))
#
#
# # take turn for RIGHT and DOWN
# def take_turn_R_D(board, R):
#
#     global score
#     # squeezing the numbers right
#     board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in board], int)
#     # adding the needed numbers
#     merged = np.full((4, 4), False)
#     for ix, iy in np.ndindex(board.shape):
#         if iy < 3:
#             if not(board[ix][iy] == 0) and board[ix][iy + 1] == board[ix][iy] and not merged[ix][iy] \
#                     and not merged[ix][iy + 1]:
#                 board[ix][iy + 1] *= 2
#                 score += board[ix][iy + 1]
#                 board[ix][iy] = 0
#                 merged[ix][iy + 1] = True
#
#     board = np.array([np.concatenate((col[col == 0], col[col != 0])) for col in board], int)
#     if R:
#         board = board.T
#     return board
#
#
# # take turn for LEFT and UP
# def take_turn_L_U(board, U):
#
#     global score
#     # squeezing the numbers left
#     board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in board], int)
#     # adding the needed numbers
#     merged = np.full((4, 4), False)
#     for ix, iy in np.ndindex(board.shape):
#         if iy > 0:
#             if not(board[ix][iy] == 0) and board[ix][iy] == board[ix][iy - 1] and not merged[ix][iy - 1] \
#                     and not merged[ix][iy]:
#                 board[ix][iy - 1] *= 2
#                 score += board[ix][iy - 1]
#                 board[ix][iy] = 0
#                 merged[ix][iy - 1] = True
#
#     board = np.array([np.concatenate((col[col != 0], col[col == 0])) for col in board], int)
#     if U:
#         board = board.T
#     return board
#
#
# # take turn base on direction
# def take_turn(direc, board):
#
#     if direc == 'UP':
#         board = take_turn_L_U(board.T, True)
#     elif direc == 'DOWN':
#         board = take_turn_R_D(board.T, True)
#     elif direc == 'RIGHT':
#         board = take_turn_R_D(board, False)
#     elif direc == 'LEFT':
#         board = take_turn_L_U(board, False)
#
#     return board
#
#
# # spawn in new pieces randomly when turns start
# def new_pieces(board):
#
#     full = False
#     board_zeros = np.argwhere(board == 0)
#     if len(board_zeros) != 0:
#         rnd = random.randint(0, len(board_zeros) - 1)
#         if random.randint(1, 10) == 4:
#             board[board_zeros[rnd][0]][board_zeros[rnd][1]] = 4
#         else:
#             board[board_zeros[rnd][0]][board_zeros[rnd][1]] = 2
#     else:
#         full = True
#     return board, full
#
#
# def draw_board():
#
#     pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
#     score_text = font.render(f'Score: {score}', True, 'black')
#     high_score_text = font.render(f'High Score: {high_score}', True, 'black')
#     screen.blit(score_text, (10, 410))
#     screen.blit(high_score_text, (10, 450))
#
#
# def draw_pieces(board):
#
#     for idx, tile in np.ndenumerate(board):
#         value = tile
#         if value > 8:
#             value_color = colors['light text']
#         else:
#             value_color = colors['dark text']
#         if value <= 8192:
#             color = colors[value]
#         else:
#             color = colors['other']
#         pygame.draw.rect(screen, color, [idx[1] * 95 + 20, idx[0] * 95 + 20, 75, 75], 0, 5)
#         if value > 0:
#             value_len = len(str(value))
#             font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
#             value_text = font.render(str(value), True, value_color)
#             text_rect = value_text.get_rect(center=(idx[1] * 95 + 57, idx[0] * 95 + 57))
#             screen.blit(value_text, text_rect)
#             pygame.draw.rect(screen, 'black', [idx[1] * 95 + 20, idx[0] * 95 + 20, 75, 75], 2, 5)
#
#
# # Main game
# run = True
# while run:
#     timer.tick(fps)
#     screen.fill('grey')
#     draw_board()
#     draw_pieces(board_values)
#     perv_turn = None
#     if spawn_new or init_count < 2:
#         board_values, game_over = new_pieces(board_values)
#         spawn_new = False
#         init_count += 1
#     if direction != '':
#         perv_board = board_values
#         board_values = take_turn(direction, board_values)
#         if not np.array_equal(perv_board, board_values):
#             direction = ''
#             spawn_new = True
#         else:
#             direction = ''
#             continue
#
#     if game_over:
#         draw_over()
#         if high_score > init_high:
#             file = open('high_score', 'w')
#             file.write(f'{high_score}')
#             file.close()
#             init_high = high_score
#
#     for event in pygame.event.get([pygame.QUIT, pygame.KEYUP]):
#         if event.type == pygame.QUIT:
#             run = False
#         if event.type == pygame.KEYUP:
#             if not game_over:
#                 if event.key == pygame.K_UP:
#                     direction = 'UP'
#                 elif event.key == pygame.K_DOWN:
#                     direction = "DOWN"
#                 elif event.key == pygame.K_RIGHT:
#                     direction = 'RIGHT'
#                 elif event.key == pygame.K_LEFT:
#                     direction = 'LEFT'
#
#             if game_over:
#                 if score > high_score:
#                     high_score = score
#                 if event.key == pygame.K_RETURN:
#                     board_values = np.zeros((4, 4), int)
#                     spawn_new = True
#                     init_count = 0
#                     score = 0
#                     direction = ''
#                     game_over = False
#                     continue
#
#     pygame.display.flip()
# pygame.quit()
if __name__ == "__main__":
    game = Game()
    game.run_game()
