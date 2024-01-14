import time
from math import sqrt
from random import randint
import pickle
import asyncio
import pygame

from move import Players, Bug
from unmove import Artifact, Weapon, Armor


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


def save(self):
    with open(f"{time.time()}.dat", "wb") as fp:
        pickle.dump(self, fp)


class Game:
    def __init__(self, background):
        pygame.init()

        # Установка размеров окна
        infoObject = pygame.display.Info()
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h
        # self.win_width, self.win_height = 1000, 1000
        self.win = pygame.display.set_mode((self.win_width, self.win_height))

        # Загрузка изображений персонажа
        self.character_x, self.character_y = self.win_width // 2, self.win_height // 2  # где встанет персонаж

        self.player = Players(self.character_x, self.character_y, self.win_width, self.win_height)

        # Установка параметров заднего плана
        self.bg_x, self.bg_y = 0, 0
        self.bg_width, self.bg_height = background.get_size()

        # Создание жуков
        self.bugs = [Bug(randint(0, self.win_width), randint(0, self.win_height), randint(1, 5))]
        self.artifacts = [Artifact(randint(0, self.bg_width), randint(0, self.bg_height), 'Инфа.png'),
                          Artifact(randint(0, self.bg_width), randint(0, self.bg_height), 'Инфа.png'),
                          Artifact(randint(0, self.bg_width), randint(0, self.bg_height), 'Инфа.png')]
        self.armors = []
        self.weapons = []

        x, y = 1, 1
        # self.walls = [(x, y)]
        self.bugs_count = 0
        self.background = background

    def game(self):
        font = pygame.font.Font(None, 36)
        run = True
        start = time.time()
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
            if time.time() - start > 5:
                self.bugs.append(Bug(randint(0, self.win_width), randint(0, self.win_height), randint(1, 5)))
                start = time.time()
                print("Bug")
            keys = pygame.key.get_pressed()

            vel_bg_x, vel_bg_y, self.bg_x, self.bg_y = self.player.move(keys, self.bg_x, self.bg_y)

            soxrany_i_pomilui(vel_bg_x, vel_bg_y, self.bugs, self.artifacts, self.weapons, self.armors)
            self.character_x, self.character_y = self.player.x, self.player.y

            if keys[pygame.K_SPACE]:  # Если нажата клавиша 'space', персонаж "бьет" жуков
                for bug in self.bugs:
                    if sqrt((bug.x - self.character_x) ** 2 + (bug.y - self.character_y) ** 2) < self.player.rang():
                        bug.hp -= self.player.attack()
                        print("Персонаж бьет жука!")

            self.win.fill((0, 0, 0))  # Заполняем окно черным цветом
            self.win.blit(self.background,
                     (self.bg_x, self.bg_y))  # Рисуем задний план
            self.player.draw(self.win)  # Рисуем персонажа

            for bug in self.bugs:
                dist = bug.move_towards(self.character_x, self.character_y)
                bug.draw(self.win)

                if dist < 50:
                    self.player.hp -= (1 * (1 / self.player.defence()))
                    print("Жук бьет персонажа!")

                if bug.hp <= 0:
                    print("Жук убит!")
                    self.bugs_count += 1
                    if randint(0, self.bugs_count) == 5:
                        self.armors.append(Armor(bug.x, bug.y,
                                                 'Инфа.png', randint(1, 10),
                                                 randint(1, 10)))
                    if randint(0, self.bugs_count) == 7:
                        self.weapons.append(Weapon(bug.x, bug.y,
                                                   'Инфа.png', randint(1, 10),
                                                   randint(1, 10)))
                    self.bugs.remove(bug)

            prov_game_objects(self.artifacts, self.weapons, self.armors, self.win, self.character_x, self.character_y,
                              self.player)

            hp_text = font.render(f"Здоровье: {self.player.hp}", True, (255, 255, 255))
            bugs_count_text = font.render(f"Количество убитых жуков: {self.bugs_count}, ЖИВОДЁР!", True,
                                                    (255, 255, 255))
            if self.player.hp <= 0:
                hp_text = font.render(f"Вы умерли", True, (255, 255, 255))
                self.bugs = []
                start = time.time() + 10 * 10
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False

            elif self.player.artifact == 3:
                hp_text = font.render(f"Вы победили!", True, (255, 255, 255))
                self.bugs = []
                start = time.time() + 10 * 10
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False
            self.win.blit(hp_text, (20, 20))
            self.win.blit(bugs_count_text, (750, 20))  # Отображаем здоровье персонажа

            pygame.display.update()  # Обновляем окно

        print(type(self.background))
        print(type(self.player.player_left))

    def __getstate__(self):
        print("123")
        self.player.player_left = pygame.image.tostring(self.player.player_left, "RGBA")
        self.player.player_right = ''
        self.player.image = ''
        bugs = []
        for bug in self.bugs:
            bugs.append([bug.x, bug.y, bug.speed])
        for artifacts in self.artifacts:
            artifacts.image = pygame.image.tostring(artifacts.image, "RGBA")

        '''self.player_left = pygame.image.load(
            'персонаж облаченный зеленый.png')  # сам спрайт (изначально персонаж повернут влево)
        # player_left = pygame.transform.scale(player_left, (win_width // 400 * 70, win_width // 400 * 100))
        self.player_right = pygame.transform.flip(self.player_left, True, False)  # приколы с поворотом

        self.image = self.player_left'''

        state = self.__dict__.copy()
        state['win'] = ''
        state['background'] = self.background
        state['bugy'] = bugs
        state['bugs'] = []
        state['armors'] = []
        state['weapons'] = []

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        print(type(self.player.player_left))
        self.player.player_left = pygame.image.fromstring(self.player.player_left, (70, 100), "RGBA")
        self.player.player_right = pygame.transform.flip(self.player.player_left, True, False)  # приколы с поворотом

        self.player.image = self.player.player_left
        bugs = []
        for bug in self.bugy:
            self.bugs.append(Bug(bug[0], bug[1], bug[2]))

        #self.bugs = bugs
        for artifacts in self.artifacts:
            artifacts.image = pygame.image.fromstring(artifacts.image, (30, 30), "RGBA")
        print(type(self.background))
        self.background = pygame.image.fromstring(self.background, (self.win_width * 20, self.win_height * 20), 'RGBA')


if __name__ == "__main__":
    pygame.init()
    infoObject = pygame.display.Info()
    win_width, win_height = infoObject.current_w, infoObject.current_h
    # Загрузка изображения заднего плана
    background = pygame.image.load('задник.png')
    #background = pygame.transform.scale(background,
                                        #(win_width * 20, win_height * 20))  # новые размеры персонажа

    a = Game(background)

    '''with open("savegame.dat", "rb") as fp:
        a = pickle.load(fp)'''

    a.game()
