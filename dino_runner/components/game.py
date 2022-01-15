import pygame

from dino_runner.components.lives import Lives
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.text_utils import get_score_element, get_centered_message
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, RUNNING, LIVES, CLOUD, \
    LIST_LIVES
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.dinosaur import Dinosaur


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = 300
        self.y_pos_cloud = 200

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.previus_points = 0
        self.points = 0
        self.death_count = 0
        self.running = True
        self.powerup_manager = PowerUpManager()
        self.heart = Lives()
        self.live_list = LIST_LIVES

    def init_lives(self):
        self.lives = LIVES
        self.live_list = [700]

    def run(self):
        self.game_speed = 20
        self.points = 0
        self.init_lives()

        self.create_components()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.heart.check_status_live(self)

    def create_components(self):
        self.obstacle_manager.reset_obstacles()
        self.powerup_manager.reset_power_ups(self.points)

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)

        self.powerup_manager.update(self.points, self.game_speed, self.player)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))

        self.draw_background()
        self.draw_cloud()

        self.player.draw(self.screen)
        self.heart.draw(self.screen, self)

        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.score()

        pygame.display.update()
        pygame.display.flip()

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1

        score, score_rect = get_score_element(self.points)
        self.screen.blit(score, score_rect)

        self.player.check_invincibility(self.screen)
        self.player.check_hammer(self.screen)

    def show_menu(self):
        self.running = True
        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.print_menu_elements(self.death_count)
        pygame.display.update()

        self.handle_key_events_on_menu()

    def print_menu_elements(self, death_count):

        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        self.screen.blit(RUNNING[0], (half_screen_width - 20, half_screen_height - 140))

        text, text_rect = get_centered_message('press any key to start the game')
        self.screen.blit(text, text_rect)

        text, text_rect = get_centered_message('Death : {}'.format(self.death_count), 550, 400)
        self.screen.blit(text, text_rect)

        text1, text_rect1 = get_centered_message('points : {}'.format(self.previus_points), 550, 450)
        self.screen.blit(text1, text_rect1)

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_cloud(self):
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))
        if self.x_pos_cloud <= -image_width:
            self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))
            self.x_pos_cloud = 1000

        self.x_pos_cloud -= self.game_speed
