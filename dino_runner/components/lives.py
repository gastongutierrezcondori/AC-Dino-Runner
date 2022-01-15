import pygame

from dino_runner.utils.constants import HEART, LIST_LIVES, POSITION_LIVE_SCREEN, MAX_LIVES, ADD_LIVES
from pygame.sprite import Sprite


class Lives(Sprite):
    X_POS = 900
    Y_POS = 20

    def __init__(self):
        self.Image = HEART
        self.rect = self.Image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.lives = LIST_LIVES

    def check_status_live(self, game):

        if game.points % 200 == 0 and game.lives < MAX_LIVES:
            game.lives = game.lives + ADD_LIVES
            if len(game.live_list) > 0:
                self.get_live_last = game.live_list[len(game.live_list) - 1]
            else:
               self.get_live_last = 700

            game.live_list.append(self.get_live_last + POSITION_LIVE_SCREEN)

    def update(self, game):

        if game.lives > 0:
            game.lives -= 1
            self.take_life(game.lives, game)
            if game.lives == 200:
                game.lives += 1
        else:
            pygame.time.delay(500)
            game.playing = False
            game.death_count += 1
            game.previus_points = game.points

            game.points = 0

    def draw(self, screen, game):
        for live in game.live_list:
            self.rect.x = live
            screen.blit(self.Image, (self.rect.x, self.rect.y))

    def take_life(self, position, game):
        if len(game.live_list) != 0:
            game.live_list.pop(position)
