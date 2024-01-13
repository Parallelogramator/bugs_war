import pygame
from math import sqrt

class game_object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def dist(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        return sqrt(dx ** 2 + dy ** 2)

    def pos_bg(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y


class Artifact(game_object):
    def __init__(self, x, y, image_path):
        super().__init__(x, y)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))


class Armor(game_object):
    def __init__(self, x, y, image_path, protection, strength):
        super().__init__(x, y)

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.protection = protection
        self.strength = strength

    def get_char(self):
        return {'protection': self.protection, 'strength': self.strength}


class Weapon(game_object):
    def __init__(self, x, y, image_path, rang, damage):
        super().__init__(x, y)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rang, self.damage = rang, damage

    def get_char(self):
        return {'rang': self.rang, 'damage': self.damage}
