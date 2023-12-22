import math
import time
from random import randint

import pygame

pygame.init()

# Чтение размеров экрана
infoObject = pygame.display.Info()#cоздаем объект infoObject типа pygame.display.Info(), содержит информацию об экране
win_width, win_height = infoObject.current_w, infoObject.current_h #win_width и win_height значения ширины и высоты окна соответственно

win = pygame.display.set_mode((win_width, win_height)) # Запуск окна размеров экрана#


character_x, character_y = win_width// 2, win_height //2# где встанет персонаж
vel = 5#хз, ща разберемся (может хп жука?)
character_hp = 100# количество хп (жизней/здоровья)

# работа с персонажем
player_left = pygame.image.load('персонаж облаченный зеленый.png')#сам спрайт (изночально персонаж повернут влево)
player_left = pygame.transform.scale(player_left, (win_width// 400 * 70, win_width// 400 * 100)) #новые размеры персонажа
position = player_left
player_right = pygame.transform.flip(player_left, True, False)#прриколы с поворотом
player = player_right

class Bug:#
    def __init__(self, x, y, speed):#
        self.x = x#
        self.y = y#
        self.speed = speed#
        self.image = pygame.image.load('жуг.png')#
        self.bugs_right = pygame.image.load('жуг.png')#
        self.bugs_left = pygame.transform.flip(self.bugs_right, True, False)#
        self.image = self.bugs_right#
        self.hp = 20#
#
    def move_towards(self, target_x, target_y):#
        dx = target_x - self.x#
        dy = target_y - self.y#
        dist = math.sqrt(dx ** 2 + dy ** 2)#
        dx /= dist#
        dy /= dist#
        new_x = self.x + dx * self.speed#
        if dx > 0:#
            self.image = self.bugs_left#
        else:#
            self.image = self.bugs_right#
        new_y = self.y + dy * self.speed#
        if 50 <= new_x <= win_width - 50 and 50 <= new_y <= win_height - 50:#
            self.x = new_x#
            self.y = new_y#
        return dist#
#
    def draw(self, win):#
        win.blit(self.image, (self.x, self.y))#
#
# Создание жуков#
bugs = [Bug(randint(0, win_width), randint(0, win_height), randint(1, 5))]#
start = time.time()#
x, y = 1, 1#
wals = [(x, y)]#
font = pygame.font.Font(None, 36)# создаем обьект шрифта
#
a = True
run = True
while run:#
    pygame.time.delay(100)#
#
    for event in pygame.event.get():#
        if event.type == pygame.QUIT:#
            run = False#
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:#
            run = False#
#
    if time.time() - start > 5:#
        bugs.append(Bug(randint(0, win_width), randint(0, win_height), randint(1, 5)))#
        start = time.time()#
        print("Bug")#

    keys = pygame.key.get_pressed()#

    new_character_x = character_x#
    new_character_y = character_y#




    if keys[pygame.K_a] and a:
        new_character_x -= vel#    - Если клавиша `a` нажата и `a` равно True, то значение `new_character_x` уменьшается на `vel`. Затем переменные `player` и `position` присваиваются значение `player_right`.

        player = player_right#
        position = player_right#
    if keys[pygame.K_d]and a:
        new_character_x += vel#    - Если клавиша `d` нажата и `a` равно True, то значение `new_character_x` увеличивается на `vel`. Затем переменные `player` и `position` присваиваются значение `player_left`.

        player = player_left#
        position = player_left#
    if keys[pygame.K_w]and a:
        new_character_y -= vel#     - Если клавиша `w` нажата и `a` равно True, то значение `new_character_y` уменьшается на `vel`. Затем переменная `player` присваивается повернутому изображению `position` на 0 градусов с помощью функции `pygame.transform.rotate`.

        player = pygame.transform.rotate(position, 0)#
    if keys[pygame.K_s]and a:
        new_character_y += vel#    - Если клавиша `K_s` нажата и `a` равно True, то значение `new_character_y` увеличивается на `vel`. Затем переменная `player` присваивается повернутому изображению `position` на 0 градусов с помощью функции `pygame.transform.rotate`.


        player = pygame.transform.rotate(position, 0)#
    if keys[pygame.K_DOWN]and a:
        vel = 100#    - Если клавиша `K_DOWN` нажата и `a` равно True, то значение `vel` устанавливается равным 100. В противном случае, значение `vel` устанавливается равным 5.

    else:#
        vel = 5#

    if 50 <= new_character_x <= win_width - 50 and 50 <= new_character_y <= win_height - 50 and (new_character_x,#
                                                                                                 new_character_y) not in wals:#
        character_x = new_character_x#
        character_y = new_character_y#

    if keys[pygame.K_SPACE]:#
        for bug in bugs:#
            if math.sqrt((bug.x - character_x) ** 2 + (bug.y - character_y) ** 2) < 50:#
                bug.hp -= 10#
                print("Персонаж бьет жука!")

    win.fill((0, 0, 0))#
    win.blit(player, (character_x, character_y))#

    for bug in bugs[:]:#
        dist = bug.move_towards(character_x, character_y)#
        bug.draw(win)#
        if dist < 50:#
            character_hp -= 1#
            print("Жук бьет персонажа!")
        if bug.hp <= 0:#
            bugs.remove(bug)#
            print("Жук убит!")


    hp_text = font.render(f"Здоровье: {character_hp}", True, (255, 255, 255))#
    if character_hp < 0:
        hp_text = font.render(f"Вы умерли", True, (255, 255, 255))#
        bugs = []#
        start = time.time() + 10 * 10#
        a = False#
    win.blit(hp_text, (20, 20))  # Отображаем здоровье персонажа

    pygame.display.update()# Обновляем окно
    pygame.display.update()#

pygame.quit()#
