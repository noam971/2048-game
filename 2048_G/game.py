import pygame
import numpy as np
from board import Board


class Game:
    # Initial setup
    board_values = np.zeros((4, 4), int)
    game_over = False
    spawn_new = True
    init_count = 0
    direction = ''
    score = 0
    file = open('high_score', 'r')
    init_high = int(file.readline())
    file.close()
    high_score = init_high

    pygame.init()
    WIDTH = 400
    HEIGHT = 500
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('2048 :)')
    timer = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('freesansbold.ttf', 24)

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

    def draw_over(self):
        pygame.draw.rect(self.screen, 'black', [50, 50, 300, 100], 0, 10)
        game_over_text1 = self.font.render('Game Over :(', True, 'white')
        game_over_text2 = self.font.render('Press Enter To Restart', True, 'white')
        self.screen.blit(game_over_text1, (130, 65))
        self.screen.blit(game_over_text2, (70, 105))


    def draw_board(self):
        pygame.draw.rect(self.screen, self.colors['bg'], [0, 0, 400, 400], 0, 10)
        score_text = self.font.render(f'Score: {self.score}', True, 'black')
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, 'black')
        self.screen.blit(score_text, (10, 410))
        self.screen.blit(high_score_text, (10, 450))


    def draw_pieces(self, board):
        for idx, tile in np.ndenumerate(board):
            value = tile
            if value > 8:
                value_color = self.colors['light text']
            else:
                value_color = self.colors['dark text']
            if value <= 8192:
                color = self.colors[value]
            else:
                color = self.colors['other']
            pygame.draw.rect(self.screen, color, [idx[1] * 95 + 20, idx[0] * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(idx[1] * 95 + 57, idx[0] * 95 + 57))
                self.screen.blit(value_text, text_rect)
                pygame.draw.rect(self.screen, 'black', [idx[1] * 95 + 20, idx[0] * 95 + 20, 75, 75], 2, 5)

    # Main game
    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            self.screen.fill('grey')
            self.draw_board()
            self.draw_pieces(self.board_values)
            if self.spawn_new or self.init_count < 2:
                self.board_values, self.game_over = Board.new_pieces(self.board_values)
                self.spawn_new = False
                self.init_count += 1
            if self.direction != '':
                perv_board = self.board_values
                self.board_values, self.score = Board.take_turn(self.direction, self.board_values, self.score)
                if not np.array_equal(perv_board, self.board_values):
                    self.direction = ''
                    self.spawn_new = True
                else:
                    self.direction = ''
                    if len(np.argwhere(self.board_values == 0)) == 0:
                        self.game_over = True
                    continue

            if self.game_over:
                self.draw_over()
                if self.high_score > self.init_high:
                    self.file = open('high_score', 'w')
                    self.file.write(f'{self.high_score}')
                    self.file.close()
                    self.init_high = self.high_score

            for event in pygame.event.get([pygame.QUIT, pygame.KEYUP]):
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYUP:
                    if not self.game_over:
                        if event.key == pygame.K_UP:
                            self.direction = 'UP'
                        elif event.key == pygame.K_DOWN:
                            self.direction = "DOWN"
                        elif event.key == pygame.K_RIGHT:
                            self.direction = 'RIGHT'
                        elif event.key == pygame.K_LEFT:
                            self.direction = 'LEFT'

                    if self.game_over:
                        if self.score > self.high_score:
                            self.high_score = self.score
                        if event.key == pygame.K_RETURN:
                            self.board_values = np.zeros((4, 4), int)
                            self.spawn_new = True
                            self.init_count = 0
                            self.score = 0
                            self.direction = ''
                            self.game_over = False
                            continue

            pygame.display.flip()
        pygame.quit()
