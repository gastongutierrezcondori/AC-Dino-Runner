import random

import pygame

from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:

    def __init__(self):
        self.obstacles = [] # lista de obstaculos


    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))

            elif random.randint(0, 2) == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS))

            elif random.randint(0, 2) == 2:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            # acceder al dinosaurio
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:

                    pygame.time.delay(500)
                # detener el siclo
                    game.playing = False
                    game.death_count +=1
                    game.previus_points = game.points
                    game.points = 0
                    break
                else:
                    self.obstacles.remove(obstacle)


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []