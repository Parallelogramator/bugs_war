import math
import time
from random import randint

import pygame


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

            self.player = self.player_right
        if keys[pygame.K_d]:
            new_character_x += self.speed  # - Если клавиша `d` нажата и `a` равно True,
            # то значение `new_character_x` увеличивается на `self.speed`.
            # Затем переменные `player` и `position` присваиваются значение `player_left`.

            self.player = self.player_left
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


class game_object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def dist(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def pos_bg(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y


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


def soxrany_i_pomilui(vel_x, vel_y, bugs, artifacts, weapons, armors):
    for bug in bugs:
        bug.pos_bg(vel_x, vel_y)

    for artifact in artifacts:
        artifact.pos_bg(vel_x, vel_y)

    for weapon in weapons:
        weapon.pos_bg(vel_x, vel_y)

    for armor in armors:
        armor.pos_bg(vel_x, vel_y)


def prov_game_objects(artifacts, weapons, armors, win, character_x, character_y, player):
    for artifact in artifacts:
        artifact.draw(win)
        dist = artifact.dist(character_x, character_y)
        if dist < 50:
            player.add_artifact()
            artifacts.remove(artifact)

    for weapon in weapons:
        weapon.draw(win)
        dist = weapon.dist(character_x, character_y)
        if dist < 50:
            player.add_weapon(weapon.get_char())
            weapons.remove(weapon)

    for armor in armors:
        armor.draw(win)
        dist = armor.dist(character_x, character_y)
        if dist < 50:
            player.add_armor(armor.get_char())
            armors.remove(armor)


def game(background):
    pygame.init()

    # Установка размеров окна
    infoObject = pygame.display.Info()
    win_width, win_height = infoObject.current_w, infoObject.current_h
    # win_width, win_height = 1000, 1000
    win = pygame.display.set_mode((win_width, win_height))

    # Загрузка изображений персонажа
    character_x, character_y = win_width // 2, win_height // 2  # где встанет персонаж

    player = Players(character_x, character_y, win_width, win_height)

    # Установка параметров заднего плана
    bg_x, bg_y = 0, 0
    bg_width, bg_height = background.get_size()

    # Создание жуков
    bugs = [Bug(randint(0, win_width), randint(0, win_height), randint(1, 5))]
    artifacts = [Artifact(randint(0, bg_width), randint(0, bg_height), 'изображение_viber_2022-05-12_23-33-42-501.jpg'),
                 Artifact(randint(0, bg_width), randint(0, bg_height), 'изображение_viber_2022-05-12_23-33-42-501.jpg'),
                 Artifact(randint(0, bg_width), randint(0, bg_height), 'изображение_viber_2022-05-12_23-33-42-501.jpg')]
    armors = []
    weapons = []

    start = time.time()
    x, y = 1, 1
    # wals = [(x, y)]
    font = pygame.font.Font(None, 36)  # создаем объект шрифта
    bugs_count = 0
    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
        if time.time() - start > 5:
            x += 1
            bugs.append(Bug(randint(0, 800), randint(0, win_height), randint(1, 5)))
            start = time.time()
            print("Bug")
        keys = pygame.key.get_pressed()

        vel_bg_x, vel_bg_y, bg_x, bg_y = player.move(keys, bg_x, bg_y)

        soxrany_i_pomilui(vel_bg_x, vel_bg_y, bugs, artifacts, weapons, armors)
        character_x, character_y = player.x, player.y

        if keys[pygame.K_SPACE]:  # Если нажата клавиша 'space', персонаж "бьет" жуков
            for bug in bugs:
                if math.sqrt((bug.x - character_x) ** 2 + (bug.y - character_y) ** 2) < player.rang():
                    bug.hp -= player.attack()
                    print("Персонаж бьет жука!")

        win.fill((0, 0, 0))  # Заполняем окно черным цветом
        win.blit(background, (bg_x, bg_y))  # Рисуем задний план
        player.draw(win)  # Рисуем персонажа

        for bug in bugs:
            dist = bug.move_towards(character_x, character_y)
            bug.draw(win)

            if dist < 50:
                player.hp -= (1 * (1 / player.defence()))
                print("Жук бьет персонажа!")

            if bug.hp <= 0:
                print("Жук убит!")
                bugs_count += 1
                if randint(0, bugs_count) == 5 or 1:
                    armors.append(Armor(bug.x, bug.y,
                                        'изображение_viber_2022-05-12_23-33-42-501.jpg', randint(0, 10),
                                        randint(0, 10)))
                if randint(0, bugs_count) == 7 or 1:
                    weapons.append(Weapon(bug.x, bug.y,
                                          'изображение_viber_2022-05-12_23-33-42-501.jpg', randint(0, 10),
                                          randint(0, 10)))
                bugs.remove(bug)

        prov_game_objects(artifacts, weapons, armors, win, character_x, character_y, player)

        hp_text = font.render(f"Здоровье: {player.hp}", True, (255, 255, 255))
        bugs_count_text = font.render(f"Количество убитых жуков: {bugs_count}, ЖИВОДЁР!", True, (255, 255, 255))
        if player.hp <= 0:
            hp_text = font.render(f"Вы умерли", True, (255, 255, 255))
            bugs = []
            start = time.time() + 10 * 10
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        elif player.artifact == 3:
            hp_text = font.render(f"Вы победили!", True, (255, 255, 255))
            bugs = []
            start = time.time() + 10 * 10
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False
        win.blit(hp_text, (20, 20))
        win.blit(bugs_count_text, (750, 20))  # Отображаем здоровье персонажа

        pygame.display.update()  # Обновляем окно


if __name__ == "__main__":
    pygame.init()
    infoObject = pygame.display.Info()
    win_width, win_height = infoObject.current_w, infoObject.current_h
    # Загрузка изображения заднего плана
    background = pygame.image.load('задник.png')
    background = pygame.transform.scale(background,
                                        (win_width * 20, win_height * 20))  # новые размеры персонажа

    game(background)
