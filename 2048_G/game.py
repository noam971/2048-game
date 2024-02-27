import pygame
import numpy as np
from board import Board
from mcst import mcst_move
pygame.init()
pygame.display.set_caption('2048 :)')


class Game:

    WIDTH = 400
    HEIGHT = 500

    def __init__(self):
        self.board_values = Board(0)
        self.game_over = False
        self.spawn_new = True
        self.init_count = 0
        self.direction = ''
        self.init_high = Game.get_high_score()
        self.high_score = self.init_high
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 24)

    @staticmethod
    def get_high_score():
        file = open('high_score', 'r')
        init_high = int(file.readline())
        file.close()
        return init_high

    @staticmethod
    def set_high_score(high_score):
        file = open('high_score', 'w')
        file.write(f'{high_score}')
        file.close()

    def draw_over(self):
        pygame.draw.rect(self.screen, 'black', [50, 50, 300, 100], 0, 10)
        game_over_text1 = self.font.render('Game Over :(', True, 'white')
        game_over_text2 = self.font.render('Press Enter To Restart', True, 'white')
        self.screen.blit(game_over_text1, (130, 65))
        self.screen.blit(game_over_text2, (70, 105))

    def draw_window(self):
        self.screen.fill('grey')
        self.board_values.draw_board(self.screen, self.high_score)
        self.board_values.draw_pieces(self.screen)

    # Main game
    def run_game(self, mcst=False):
        run = True
        while run:
            self.timer.tick(self.fps)
            self.draw_window()

            if self.spawn_new or self.init_count < 2:
                self.game_over = self.board_values.new_pieces()
                self.spawn_new = False
                self.init_count += 1

            if self.direction != '':
                perv_board = self.board_values.board.copy()
                self.board_values.take_turn(self.direction)
                if not np.array_equal(perv_board, self.board_values.board):
                    self.direction = ''
                    self.spawn_new = True
                    del perv_board
                else:
                    self.direction = ''
                    if len(np.argwhere(self.board_values.board == 0)) == 0:
                        if not self.board_values.check_valid_move():
                            self.game_over = True
                    del perv_board
                    continue

            if self.game_over:
                self.draw_over()
                if self.high_score > self.init_high:
                    Game.set_high_score(self.high_score)
                    self.init_high = self.high_score

            for event in pygame.event.get([pygame.QUIT, pygame.KEYUP]):
                if event.type == pygame.QUIT:
                    run = False
                if not mcst:
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
                            elif event.key == pygame.K_SPACE:
                                move = mcst_move(30, 10, self.board_values)
                                self.direction = move

                        if self.game_over:
                            if self.board_values.score > self.high_score:
                                self.high_score = self.board_values.score
                            if event.key == pygame.K_RETURN:
                                self.board_values = Board(0)
                                self.spawn_new = True
                                self.init_count = 0
                                self.direction = ''
                                self.game_over = False
                                continue

            if mcst:
                move = mcst_move(30, 10, self.board_values)
                self.direction = move

                if self.game_over:
                    self.draw_over()
                    if self.high_score > self.init_high:
                        Game.set_high_score(self.high_score)
                        self.init_high = self.high_score

                    for event in pygame.event.get([pygame.QUIT, pygame.KEYUP]):
                        if event.type == pygame.QUIT:
                            run = False
                        if self.board_values.score > self.high_score:
                            self.high_score = self.board_values.score
                        if event.key == pygame.K_RETURN:
                            self.board_values = Board(0)
                            self.spawn_new = True
                            self.init_count = 0
                            self.direction = ''
                            self.game_over = False
                            continue

            pygame.display.flip()
        pygame.quit()
