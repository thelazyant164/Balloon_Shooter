import pygame
import math

class Projectile(pygame.sprite.Sprite):
    missed_shots = 0
    screen_width = 0
    screen_height = 0

    def __init__(self, pos, direction):
        super().__init__()
        offset_x = direction[0] - pos[0]
        offset_y = direction[1] - pos[1]
        rot = -math.atan2(offset_y, offset_x) * 180 / math.pi
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("content/assets/images/bullet.png"), (60, 30)), rot)

        self.rect = self.image.get_rect()
        self.rect.center = pos

        #Evaluate speed in individual axis, then enforce consistent speed
        ratio = offset_x/offset_y
        base_vel = 10
        if abs(ratio) > 1:
            self.vel_x = base_vel * (offset_x/abs(offset_x))
            self.vel_y = self.vel_x/ratio
        elif abs(ratio) < 1:
            self.vel_y = base_vel * (offset_y/abs(offset_y))
            self.vel_x = self.vel_y * ratio
        else:
            self.vel_x = base_vel
            self.vel_y = base_vel

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.has_missed():
            Projectile.missed_shots += 1
            self.kill()

    def has_missed(self):
        overflow_horizontally = self.rect.right < 0 or self.rect.left > Projectile.screen_width
        overflow_vertically = self.rect.top < 0 or self.rect.bottom > Projectile.screen_height
        return overflow_horizontally or overflow_vertically

    @classmethod
    def reset_missed_shots(cls):
        cls.missed_shots = 0

    @classmethod
    def initialize_screen_dimension(cls, screen_width, screen_height):
        cls.missed_shots = 0
        cls.screen_width = screen_width
        cls.screen_height = screen_height

    @classmethod
    def setup(cls, screen_width, screen_height):
        Projectile.reset_missed_shots()
        Projectile.initialize_screen_dimension(screen_width, screen_height)
