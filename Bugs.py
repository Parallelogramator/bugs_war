import time
from math import sqrt
from random import randint
import pickle
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


class Game:
    def __init__(self, background):
        pygame.init()

        # Установка размеров окна
        infoObject = pygame.display.Info()
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h
        # self.win_width, self.win_height = 1000, 1000
        self.win = pygame.image.tostring(pygame.display.set_mode((self.win_width, self.win_height)), "RGBA")

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
        self.font = pygame.font.Font(None, 36)  # создаем объект шрифта
        self.bugs_count = 0
        self.background = pygame.image.tostring(background, "RGBA")

    def game(self):
        win = pygame.image.fromstring(self.win, (self.win_width, self.win_height), "RGBA")
        run = True
        start = time.time()
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
            if time.time() - start > 5:
                self.bugs.append(Bug(randint(0, 800), randint(0, win_height), randint(1, 5)))
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

            win.fill((0, 0, 0))  # Заполняем окно черным цветом
            win.blit(pygame.image.fromstring(self.background, (self.bg_width, self.bg_height), "RGBA"),
                     (self.bg_x, self.bg_y))  # Рисуем задний план
            self.player.draw(win)  # Рисуем персонажа

            for bug in self.bugs:
                dist = bug.move_towards(self.character_x, self.character_y)
                bug.draw(win)

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

            prov_game_objects(self.artifacts, self.weapons, self.armors, win, self.character_x, self.character_y,
                              self.player)

            hp_text = self.font.render(f"Здоровье: {self.player.hp}", True, (255, 255, 255))
            self.bugs_count_text = self.font.render(f"Количество убитых жуков: {self.bugs_count}, ЖИВОДЁР!", True,
                                                    (255, 255, 255))
            if self.player.hp <= 0:
                hp_text = self.font.render(f"Вы умерли", True, (255, 255, 255))
                self.bugs = []
                start = time.time() + 10 * 10
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False

            elif self.player.artifact == 3:
                hp_text = self.font.render(f"Вы победили!", True, (255, 255, 255))
                self.bugs = []
                start = time.time() + 10 * 10
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False
            win.blit(hp_text, (20, 20))
            win.blit(self.bugs_count_text, (750, 20))  # Отображаем здоровье персонажа

            pygame.display.update()  # Обновляем окно

        with open("savegame.dat", "wb") as fp:
            pickle.dump(a, fp)


    def __getstate__(self):
        print(self.__dict__.copy())
        state = self.__dict__.copy()

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)



if __name__ == "__main__":
    pygame.init()
    infoObject = pygame.display.Info()
    win_width, win_height = infoObject.current_w, infoObject.current_h
    # Загрузка изображения заднего плана
    background = pygame.image.load('задник.png')
    background = pygame.transform.scale(background,
                                        (win_width * 20, win_height * 20))  # новые размеры персонажа

    a = Game(background)


    a.game()
