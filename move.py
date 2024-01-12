import pygame
from math import sqrt


class Players:
    def __init__(self, x, y, win_width, win_height):
        self.x = x
        self.y = y
        self.speed = 5

        self.win_width = win_width
        self.win_height = win_height
        self.player_left = pygame.image.load(
            'персонаж облаченный зеленый.png')  # сам спрайт (изначально персонаж повернут влево)
        # player_left = pygame.transform.scale(player_left, (win_width // 400 * 70, win_width // 400 * 100))
        self.player_right = pygame.transform.flip(self.player_left, True, False)  # приколы с поворотом

        self.image = self.player_left
        self.hp = 100

        self.base_attack = 10
        self.current_weapon = 0
        self.artifact = 0
        self.weapon = [{'attack': 0, 'rang': 100}]
        self.armor = []

    def move(self, keys, bg_x, bg_y):
        new_character_x = self.x
        new_character_y = self.y
        if keys[pygame.K_a]:
            new_character_x -= self.speed  # - Если клавиша `a` нажата и `a` равно True,
            # то значение `new_character_x` уменьшается на `self.speed`.
            # Затем переменные `player` и `position` присваиваются значение `player_right`.

            self.image = self.player_right
        if keys[pygame.K_d]:
            new_character_x += self.speed  # - Если клавиша `d` нажата и `a` равно True,
            # то значение `new_character_x` увеличивается на `self.speed`.
            # Затем переменные `player` и `position` присваиваются значение `player_left`.

            self.image = self.player_left
        if keys[pygame.K_w]:
            new_character_y -= self.speed  # - Если клавиша `w` нажата и `a` равно True,
            # то значение `new_character_y` уменьшается на `self.speed`.

        if keys[pygame.K_s]:
            new_character_y += self.speed  # - Если клавиша `K_s` нажата и `a` равно True,
            # то значение `new_character_y` увеличивается на `self.speed`.

        if keys[pygame.K_LSHIFT]:
            self.speed = 100  # - Если клавиша `K_DOWN` нажата и `a` равно True,
            # То значение `self.speed` устанавливается равным 100.
            # В противном случае значение `self.speed` устанавливается равным 5.

        else:
            self.speed = 5

            # Проверка, не выходит ли персонаж за пределы окна или не врезается ли он в стены
        prov_bg = True
        vel_bg_x = 0
        vel_bg_y = 0
        if not (200 <= new_character_y <= self.win_height - 200) and not (
                200 <= new_character_x <= self.win_width - 200):
            if new_character_x > self.win_width - 200:
                bg_x -= self.speed
            else:
                bg_x += self.speed
            if new_character_y > self.win_height - 200:
                bg_y -= self.speed
                vel_bg_y = -self.speed
            else:
                bg_y += self.speed
                vel_bg_y = self.speed

            new_character_x = self.x
            new_character_y = self.y

            prov_bg = False

        if not (200 <= new_character_x <= self.win_width - 200):
            # Перемещение заднего плана, когда персонаж подходит к краю экрана
            if new_character_x > self.win_width - 200:
                bg_x -= self.speed
                vel_bg_x = -self.speed
            else:
                bg_x += self.speed
                vel_bg_x = self.speed

            self.y = new_character_y

            prov_bg = False

        if not (200 <= new_character_y <= self.win_height - 200):
            if new_character_y > self.win_height - 200:
                bg_y -= self.speed
                vel_bg_y = -self.speed
            else:
                bg_y += self.speed
                vel_bg_y = self.speed

            self.x = new_character_x

            prov_bg = False

        if prov_bg:
            self.x = new_character_x
            self.y = new_character_y

        return vel_bg_x, vel_bg_y, bg_x, bg_y

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def add_artifact(self):
        self.artifact += 1
        print("Adding artifact")

    def add_weapon(self, char):
        self.weapon.append(char)
        print("Adding weapon")

    def add_armor(self, char):
        self.armor.append(char)
        print("Adding armor")

    def attack(self):
        return self.base_attack + self.weapon[self.current_weapon].get('attack')

    def defence(self):
        res = 1
        for i in self.armor:
            res += i['protection']
            i['strength'] -= 1
        return res

    def rang(self):
        return self.weapon[self.current_weapon].get('rang')


class Bug:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.bug_right = pygame.image.load('жуг.png')
        self.bug_left = pygame.transform.flip(self.bug_right, True, False)
        self.image = self.bug_right
        self.hp = 20

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = sqrt(dx ** 2 + dy ** 2)
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
