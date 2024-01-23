'''
import pygame

class Bug:
    def __init__(self, x, y, speed, level):
        self.x = x
        self.y = y
        self.speed = speed
        self.bug_right = pygame.image.load(bugs_image[level])
        self.bug_left = pygame.transform.flip(self.bug_right, True, False)
        self.image = self.bug_right
        self.hp = 20

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx ** 2 + dy ** 2)**0.5
        dx /= dist
        dy /= dist
        new_x = self.x + dx * self.speed
        if dx > 0:
            self.image = self.bug_left
        else:
            self.image = self.bug_right
        new_y = self.y + dy * self.speed

        self.x = new_x
        self.y = new_y
        return dist

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def pos_bg(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y


bugs_image = ['жуг.png', 'жук_фиолетовый.png']
'''

