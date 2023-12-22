import math
import time
from random import randint

import pygame

pygame.init()

# Чтение размеров экрана
infoObject = pygame.display.Info()
win_width, win_height = infoObject.current_w, infoObject.current_h

# Запуск окна размеров экрана
win = pygame.display.set_mode((win_width, win_height))

# Установка параметров персонажа
character_x, character_y = 50, 50
vel = 5
character_hp = 100

# Загрузка изображений персонажа
character_left = pygame.image.load('персонаж облаченный зеленый.png')
position = character_left
character_right = pygame.transform.flip(character_left, True, False)
character_up = pygame.transform.rotate(position, 0)
character_down = pygame.transform.rotate(position, 0)
character = character_right

class Bug:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load('жуг.png')
        self.bugs_right = pygame.image.load('жуг.png')
        self.bugs_left = pygame.transform.flip(self.bugs_right, True, False)
        self.image = self.bugs_right
        self.hp = 20

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        dx /= dist
        dy /= dist
        new_x = self.x + dx * self.speed
        if dx > 0:
            self.image = self.bugs_left
        else:
            self.image = self.bugs_right
        new_y = self.y + dy * self.speed
        if 50 <= new_x <= win_width - 50 and 50 <= new_y <= win_height - 50:
            self.x = new_x
            self.y = new_y
        return dist

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

# Создание жуков
bugs = [Bug(randint(0, win_width), randint(0, win_height), randint(1, 5))]
start = time.time()
x, y = 1, 1
wals = [(x, y)]
font = pygame.font.Font(None, 36)

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False

    if time.time() - start > 5:
        bugs.append(Bug(randint(0, win_width), randint(0, win_height), randint(1, 5)))
        start = time.time()
        print("Bug")

    keys = pygame.key.get_pressed()

    new_character_x = character_x
    new_character_y = character_y

    if keys[pygame.K_a]:
        new_character_x -= vel
        character = character_right
        position = character_right
    if keys[pygame.K_d]:
        new_character_x += vel
        character = character_left
        position = character_left
    if keys[pygame.K_w]:
        new_character_y -= vel
        character = pygame.transform.rotate(position, 0)
    if keys[pygame.K_s]:
        new_character_y += vel
        character = pygame.transform.rotate(position, 0)
    if keys[pygame.K_DOWN]:
        vel = 100
    else:
        vel = 5

    if 50 <= new_character_x <= win_width - 50 and 50 <= new_character_y <= win_height - 50 and (new_character_x,
                                                                                                 new_character_y) not in wals:
        character_x = new_character_x
        character_y = new_character_y

    if keys[pygame.K_SPACE]:
        for bug in bugs:
            if math.sqrt((bug.x - character_x) ** 2 + (bug.y - character_y) ** 2) < 50:
                bug.hp -= 10
                print("Персонаж бьет жука!")

    win.fill((0, 0, 0))
    win.blit(character, (character_x, character_y))

    for bug in bugs[:]:
        dist = bug.move_towards(character_x, character_y)
        bug.draw(win)
        if dist < 50:
            character_hp -= 1
            print("Жук бьет персонажа!")
        if bug.hp <= 0:
            bugs.remove(bug)
            print("Жук убит!")


    hp_text = font.render(f"Здоровье: {character_hp}", True, (255, 255, 255))
    if character_hp < 0:
        hp_text = font.render(f"Вы умерли", True, (255, 255, 255))
        bugs = []
        start = time.time() + 10 * 10
    win.blit(hp_text, (20, 20))  # Отображаем здоровье персонажа

    pygame.display.update()  # Обновляем окно
    if character_hp < 0:
        a = True
        while a:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                a = False
            pass
    pygame.display.update()

pygame.quit()
