import pygame
import random

class Target(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("content/assets/images/balloon.png"), (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel_x = 2
        self.vel_y = 2

    def update(self, screen_width, screen_height):
        if random.randint(1, 50) == 1:
            self.vel_x = -self.vel_x
        if random.randint(1, 1000) == 1:
            self.vel_y = -self.vel_y

        if self.rect.right + self.vel_x > screen_width / 2 or self.rect.left + self.vel_x < 0:
            self.vel_x = - self.vel_x
        if self.rect.bottom + self.vel_y > screen_height or self.rect.top + self.vel_y < 0:
            self.vel_y = - self.vel_y
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def pop(self):
        self.image = pygame.image.load("content/assets/images/explosion.png")
