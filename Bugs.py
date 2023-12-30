import time
from random import randint
from math import sqrt

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
    artifacts = [Artifact(randint(0, bg_width), randint(0, bg_height), 'Инфа.png'),
                 Artifact(randint(0, bg_width), randint(0, bg_height), 'Инфа.png'),
                 Artifact(randint(0, bg_width), randint(0, bg_height), 'Инфа.png')]
    armors = []
    weapons = []

    start = time.time()
    x, y = 1, 1
    # walls = [(x, y)]
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
                if sqrt((bug.x - character_x) ** 2 + (bug.y - character_y) ** 2) < player.rang():
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
                if randint(0, bugs_count) == 5:
                    armors.append(Armor(bug.x, bug.y,
                                        'Инфа.png', randint(1, 10),
                                        randint(1, 10)))
                if randint(0, bugs_count) == 7:
                    weapons.append(Weapon(bug.x, bug.y,
                                          'Инфа.png', randint(1, 10),
                                          randint(1, 10)))
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
