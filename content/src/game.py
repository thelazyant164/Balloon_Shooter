import pygame
from .player import Player
from .target import Target
from .projectile import Projectile


class Game:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.canon_and_balloon = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.canon = Player((self.width * 3 / 4, self.height // 2))
        self.balloon = Target((self.width // 4, self.height // 2))
        self.canon_and_balloon.add(self.canon)
        self.canon_and_balloon.add(self.balloon)
        self.explode_sound = pygame.mixer.Sound(
            "content/assets/sound/explode.mp3")
        self.fire_sound = pygame.mixer.Sound("content/assets/sound/fire.mp3")
        self.game_over = False
        self.quit_game = False
        Projectile.setup(screen_width, screen_height)

        # Setup custom cursor
        pygame.mouse.set_visible(False)
        self.cursor_img = pygame.transform.scale(
            pygame.image.load("content/assets/images/crosshair.png"), (120, 100))
        self.cursor_img_rect = self.cursor_img.get_rect()

    def display_missed_shots(self):
        missed_shots_count_font = pygame.font.Font(
            'content/resources/fonts/game_over.ttf', 64)
        missed_shots_count_text = missed_shots_count_font.render(
            f"Missed shots: {Projectile.missed_shots}",
            True, (0, 0, 0))
        self.screen.blit(missed_shots_count_text, (0, 0))

    def end_game(self):
        self.game_over = True
        self.explode_sound.play()
        self.balloon.vel_x = 0
        self.balloon.vel_y = 0
        self.canon.vel = 0
        self.balloon.pop()
        for bullet in self.bullets:
            bullet.vel_x = 0
            bullet.vel_y = 0
            bullet.kill()

    def display_game_over(self):
        game_over_font = pygame.font.Font(
            'content/resources/fonts/game_over.ttf', 128)
        game_over_text = game_over_font.render(
            "GAME OVER", True, (0, 0, 0))
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (self.width // 2, self.height // 2)

        play_again_font = pygame.font.Font(
            'content/resources/fonts/game_over.ttf', 64)
        play_again_text = play_again_font.render(
            "Press ENTER to replay", True, (0, 0, 0))
        play_again_text_rect = play_again_text.get_rect()
        play_again_text_rect.center = (self.width // 2, self.height // 2 + 50)

        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(play_again_text, play_again_text_rect)

    def start_game(self):
        clock = pygame.time.Clock()
        while not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        new_bullet = Projectile(
                            self.canon.rect.center, pygame.mouse.get_pos())
                        self.bullets.add(new_bullet)
                        self.fire_sound.play()
                    if event.key == pygame.K_RETURN and self.game_over:
                        self.__init__(self.width, self.height)

            self.canon.rotate_to_mouse()
            self.canon_and_balloon.update(self.width, self.height)
            self.bullets.update()
            self.screen.fill((255, 255, 255))
            self.display_missed_shots()
            self.canon_and_balloon.draw(self.screen)
            self.bullets.draw(self.screen)
            self.cursor_img_rect.center = pygame.mouse.get_pos()
            self.screen.blit(self.cursor_img, self.cursor_img_rect)

            if pygame.sprite.spritecollideany(self.balloon, self.bullets) and not self.game_over:
                self.end_game()

            if self.game_over:
                self.display_game_over()

            pygame.display.update()
            clock.tick(60)
