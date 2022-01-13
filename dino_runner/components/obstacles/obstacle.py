from pygame.sprite import Sprite
from dino_runner.utils.constants import LARGE_CACTUS, SCREEN_WIDTH


class Obstacle(Sprite):

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[type].get_rect()
        self.rect.x = SCREEN_WIDTH

    # metodos

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed # es para que el obstaculo se mueva a la misma velocidad que la imagen
        if self.rect.x < -self.rect.width:
            obstacles.pop() # remueve un elemento de una lista



    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

