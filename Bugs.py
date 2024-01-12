import math
import time
from random import randint

import pygame

pygame.init()

# Установка размеров окна
infoObject = pygame.display.Info()
win_width, win_height = infoObject.current_w, infoObject.current_h
# win_width, win_height = 1000, 1000
win = pygame.display.set_mode((win_width, win_height))

# Загрузка изображений персонажа
player_left = pygame.image.load('персонаж облаченный зеленый.png')  # сам спрайт (изночально персонаж повернут влево)
# player_left = pygame.transform.scale(player_left, (win_width//400*70, win_width//400*100))  # новые размеры персонажа
player_right = pygame.transform.flip(player_left, True, False)  # прриколы с поворотом
player = player_right

# Загрузка изображения заднего плана
# Загрузка изображения заднего плана
background = pygame.image.load('просто представление карты.png')
background = pygame.transform.scale(background, (win_width * 20, win_height * 20))  # новые размеры персонажа

bg_x, bg_y = -win_width * 9.6, -win_height * 9.1
bg_width, bg_height = background.get_size()

character_x, character_y = win_width // 2, win_height // 2  # где встанет персонаж
vel = 5  # хз, ща разберемся (может хп жука?)
character_hp = 100  # количество хп (жизней/здоровья)

# Установка параметров заднего плана
bg_x, bg_y = -win_width * 9.6, -win_height * 9.1
bg_width, bg_height = background.get_size()


class Bug:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
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

        self.x = new_x
        self.y = new_y
        return dist

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def pos_bg(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y


def soxrany_i_pomilui(vel_x, vel_y):
    for bug in bugs:
        bug.pos_bg(vel_x, vel_y)


# Создание жуков
bugs = [Bug(randint(0, win_width), randint(0, win_height), randint(1, 5))]
start = time.time()
x, y = 1, 1
wals = [(x, y)]
font = pygame.font.Font(None, 36)  # создаем обьект шрифта
bugs_count = 0
vyhod = True  # выход из игры после проигрыша
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

    if keys[pygame.K_a] and vyhod:
        new_character_x -= vel  # - Если клавиша `a` нажата и `a` равно True,
        # то значение `new_character_x` уменьшается на `vel`.
        # Затем переменные `player` и `position` присваиваются значение `player_right`.

        player = player_right
    if keys[pygame.K_d] and vyhod:
        new_character_x += vel  # - Если клавиша `d` нажата и `a` равно True,
        # то значение `new_character_x` увеличивается на `vel`.
        # Затем переменные `player` и `position` присваиваются значение `player_left`.

        player = player_left
    if keys[pygame.K_w] and vyhod:
        new_character_y -= vel  # - Если клавиша `w` нажата и `a` равно True,
        # то значение `new_character_y` уменьшается на `vel`.

    if keys[pygame.K_s] and vyhod:
        new_character_y += vel  # - Если клавиша `K_s` нажата и `a` равно True,
        # то значение `new_character_y` увеличивается на `vel`.

    if keys[pygame.K_DOWN] and vyhod:
        vel = 100  # - Если клавиша `K_DOWN` нажата и `a` равно True,
        # то значение `vel` устанавливается равным 100.
        # В противном случае, значение `vel` устанавливается равным 5.

    else:
        vel = 5

    # Проверка, не выходит ли персонаж за пределы окна или не врезается ли он в стены
    prov_bg = True
    vel_bg_x = 0
    vel_bg_y = 0
    if not (200 <= new_character_y <= win_height - 200) and not (200 <= new_character_x <= win_width - 200):
        if new_character_x > win_width - 200:
            bg_x -= vel
        else:
            bg_x += vel
        if new_character_y > win_height - 200:
            bg_y -= vel
            vel_bg_y = -vel
        else:
            bg_y += vel
            vel_bg_y = vel

        new_character_x = character_x
        new_character_y = character_y

        prov_bg = False

    if not (200 <= new_character_x <= win_width - 200):
        # Перемещение заднего плана, когда персонаж подходит к краю экрана
        if new_character_x > win_width - 200:
            bg_x -= vel
            vel_bg_x = -vel
        else:
            bg_x += vel
            vel_bg_x = vel

        character_y = new_character_y

        prov_bg = False

    if not (200 <= new_character_y <= win_height - 200):
        if new_character_y > win_height - 200:
            bg_y -= vel
            vel_bg_y = -vel
        else:
            bg_y += vel
            vel_bg_y = vel

        character_x = new_character_x

        prov_bg = False

    if prov_bg:
        character_x = new_character_x
        character_y = new_character_y

    soxrany_i_pomilui(vel_bg_x, vel_bg_y)

    if keys[pygame.K_SPACE]:  # Если нажата клавиша 'space', персонаж "бьет" жуков
        for bug in bugs:
            if math.sqrt((bug.x - character_x) ** 2 + (bug.y - character_y) ** 2) < 200:
                bug.hp -= 10
                print("Персонаж бьет жука!")

    win.fill((0, 0, 0))  # Заполняем окно черным цветом
    win.blit(background, (bg_x, bg_y))  # Рисуем задний план
    win.blit(player, (character_x, character_y))  # Рисуем персонажа

    for bug in bugs:
        dist = bug.move_towards(character_x, character_y)
        bug.draw(win)
        if dist < 50:
            character_hp -= 1
            print("Жук бьет персонажа!")
        if bug.hp <= 0:
            bugs_count += 1
            bugs.remove(bug)
            print("Жук убит!")

    hp_text = font.render(f"Здоровье: {character_hp}", True, (255, 255, 255))
    bugs_count_text = font.render(f"Количество убитых жуков: {bugs_count}, ЖИВОДЁР!", True, (255, 255, 255))
    if character_hp <= 0:
        hp_text = font.render(f"Вы умерли", True, (255, 255, 255))
        bugs = []
        start = time.time() + 10 * 10
        run = False
    win.blit(hp_text, (20, 20))
    win.blit(bugs_count_text, (750, 20))  # Отображаем здоровье персонажа

    pygame.display.update()  # Обновляем окно

pygame.quit()
