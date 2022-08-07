import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.original_img = pygame.transform.scale(
            pygame.image.load("content/assets/images/canon.png"), (300, 120))
        self.image = pygame.transform.rotate(self.original_img, 168)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = 4

    def update(self, screen_width, screen_height):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left - self.vel > 0:
            self.rect.x -= self.vel
        if key[pygame.K_RIGHT] and self.rect.right + self.vel < screen_width:
            self.rect.x += self.vel
        if key[pygame.K_DOWN] and self.rect.bottom + self.vel < screen_height:
            self.rect.y += self.vel
        if key[pygame.K_UP] and self.rect.top - self.vel > 0:
            self.rect.y -= self.vel

    def rotate_to_mouse(self):
        direction = pygame.mouse.get_pos()
        pos = self.rect.center
        offset_x = direction[0] - pos[0]
        offset_y = direction[1] - pos[1]
        rot = -math.atan2(offset_y, offset_x) * 180 / math.pi
        self.image = pygame.transform.rotate(self.original_img, rot + 168)
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.center = pos
