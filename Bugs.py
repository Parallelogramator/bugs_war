import time
from math import sqrt
from random import randint
import pygame

from move import Players, Bug
from unmove import Artifact, Weapon, Armor, Scales, Smiths


def soxrany_i_pomilui(vel_x, vel_y, bugs, artifacts, weapons, armors, scales, smits):
    for bug in bugs:
        bug.pos_bg(vel_x, vel_y)

    for artifact in artifacts:
        artifact.pos_bg(vel_x, vel_y)

    for weapon in weapons:
        weapon.pos_bg(vel_x, vel_y)

    for armor in armors:
        armor.pos_bg(vel_x, vel_y)

    for scale in scales:
        scale.pos_bg(vel_x, vel_y)

    smits.pos_bg(vel_x, vel_y)

def prov_game_objects(scales, weapons, armors, smits, win, character_x, character_y, player, key):
    for scale in scales:
        scale.draw(win)
        dist = scale.dist(character_x, character_y)
        if dist < 200:
            player.add_scale()
            scales.remove(scale)

    for weapon in weapons:
        weapon.draw(win)
        dist = weapon.dist(character_x, character_y)
        if dist < 200 and key[pygame.K_e]:
            a = player.add_weapon(weapon.get_char())
            weapons.remove(weapon)
            if a:
                weapons.append(Weapon(character_x, character_y,
                                      randint(0, 1), randint(100, 100),
                                      randint(100, 100)))
                weapons[-1].image = a
            break

    for armor in armors:
        armor.draw(win)
        dist = armor.dist(character_x, character_y)
        if dist < 200 and key[pygame.K_e]:
            player.add_armor(armor.get_char())
            armors.remove(armor)

    smits.draw(win)
class Button:
    def __init__(self, image, x, y, visible):
        self.image = image #получаем изображение
        self.x = x
        self.y = y
        self.visible = visible

    # Рисование текста
    def draw(self, screen):
        # Отрисовываем кнопку на экране, если она видима
        if self.visible:
            screen.blit(self.image, (self.x, self.y))
            #self.draw_button()




class Game:
    def __init__(self, background, level):
        pygame.init()

        self.level = level

        # Установка размеров окна
        infoObject = pygame.display.Info()
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h
        # self.win_width, self.win_height = 1000, 1000
        self.win = pygame.display.set_mode((self.win_width, self.win_height))

        # Загрузка изображений персонажа
        self.character_x, self.character_y = self.win_width // 2, self.win_height // 2  # где встанет персонаж

        self.player = Players(self.character_x, self.character_y, self.win_width, self.win_height)

        # Установка параметров заднего плана
        self.bg_x, self.bg_y = -self.win_width * 9.6, -self.win_height * 9.1
        self.bg_width, self.bg_height = background.get_size()

        # Создание жуков
        self.bugs = [Bug(randint(0, self.win_width), randint(0, self.win_height), randint(1, 5), self.level)]
        self.artifacts = [Artifact(randint(0, self.bg_width), randint(0, self.bg_height), 'артефакт1.png'),
                          Artifact(randint(0, self.bg_width), randint(0, self.bg_height), 'артефакт2.png'),
                          Artifact(randint(0, self.bg_width), randint(0, self.bg_height), 'артефакт3.png')]
        self.armors = []
        self.weapons = []
        self.scales = []
        self.smiths = Smiths(self.win_width // 2, self.win_height // 2, 'пустой_перс_всё_для_куздница/кузнец.png')

        x, y = 1, 1
        # self.walls = [(x, y)]
        self.bugs_count = 0
        self.background = background

        self.time = time.time()

    def open_trade_window(self, visible, count_):
        self.screen = self.win_width, self.win_height  # размеры экрана
        self.trade_window = Button(pygame.image.load('подложка_у_кузнеца.png'), self.win_width * 2 // 3,
                                   self.win_height // 3, True)  # создаем торговое окно
        self.close_button = Button(pygame.image.load('красная.png'), 0, 0, True)  # создаем кнопку закрытия
        self.trade_window.visible = visible
        self.close_button.visible = visible
        self.trade_window.image = pygame.transform.scale(self.trade_window.image, (
            self.win_width * 2 // 3, self.win_height // 3))  # изменяем размеры торгового окна
        self.close_button.x = self.trade_window.x + self.trade_window.image.get_width() - self.close_button.image.get_width()  # располагаем кнопку закрытия в правом верхнем углу торгового окна
        screen_surface = pygame.Surface(self.screen)
        self.close_button.draw(screen_surface)
        self.trade_window.draw(screen_surface)

    def game(self):
        live = 1
        res = self.level
        font = pygame.font.Font(None, 36)
        run = True
        start_bugs = time.time()
        time_change = time.time()
        clock = pygame.time.Clock()
        while run:
            clock.tick(24)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
            if time.time() - start_bugs > 5:
                self.bugs.append(
                    Bug(randint(0, self.win_width), randint(0, self.win_height), randint(1, 5), self.level))
                start_bugs = time.time()
                print("Bug")
            keys = pygame.key.get_pressed()

            if keys[pygame.K_c] and time.time() - time_change > 0.5:
                print(1)
                self.player.change_weapon()
                time_change = time.time()

            vel_bg_x, vel_bg_y, self.bg_x, self.bg_y = self.player.move(keys, self.bg_x, self.bg_y)

            soxrany_i_pomilui(vel_bg_x, vel_bg_y, self.bugs, self.artifacts, self.weapons, self.armors, self.scales, self.smiths)
            self.character_x, self.character_y = self.player.x, self.player.y

            if keys[pygame.K_SPACE]:  # Если нажата клавиша 'space', персонаж "бьет" жуков
                for bug in self.bugs:
                    if sqrt((bug.x - self.character_x) ** 2 + (bug.y - self.character_y) ** 2) < self.player.rang():
                        bug.hp -= self.player.attack()
                        print("Персонаж бьет жука!")

                # Если нажата клавиша 'space', персонаж взаимодействует" с кузнецом

                if sqrt((self.smiths.x - self.character_x) ** 2 + (self.smiths.y - self.character_y) ** 2) < self.player.rang():
                    print("Персонаж взаимодействует с кузнецом!")
                    self.open_trade_window(True, self.player.scale)



            self.win.fill((0, 0, 0))  # Заполняем окно черным цветом
            self.win.blit(self.background,
                          (self.bg_x, self.bg_y))  # Рисуем задний план
            self.player.draw(self.win)  # Рисуем персонажа

            for bug in self.bugs:
                dist = bug.move_towards(self.character_x, self.character_y)
                bug.draw(self.win)

                if dist < 200:
                    self.player.hp -= (1 * (1 / self.player.defence()))
                    print("Жук бьет персонажа!")

                if bug.hp <= 0:
                    print("Жук убит!")
                    self.bugs_count += 1
                    if randint(0, self.bugs_count) in (2, 5, 7, 10, 16, 29, 42, 58, 71, 84, 88, 90, 100):
                        self.scales.append(Scales(bug.x, bug.y,
                                                  'артефакт1.png'))

                    if randint(0, self.bugs_count) in (2, 5, 7, 10, 16, 29, 42, 58, 71, 84, 88, 90, 100):
                        self.weapons.append(Weapon(bug.x, bug.y,
                                                   randint(0, 1), randint(100, 100),
                                                   randint(100, 100)))
                    if randint(0, self.bugs_count) in (3, 5, 9, 11, 16, 29, 52, 58, 71, 84, 88, 90, 100):
                        self.armors.append(Armor(bug.x, bug.y, 'пустой_перс_всё_для_куздница/итем_брони.png',
                                                 randint(100, 100),
                                                 randint(100, 100)))

                    self.bugs.remove(bug)

            for artifact in self.artifacts:
                artifact.draw(self.win)
                dist = artifact.dist(self.character_x, self.character_y)
                if dist < 200:
                    self.player.add_artifact()
                    self.artifacts.remove(artifact)

            prov_game_objects(self.scales, self.weapons, self.armors, self.smiths, self.win, self.character_x, self.character_y,
                              self.player, keys)

            hp_text = font.render(f"Здоровье: {self.player.hp}", True, (255, 255, 255))
            bugs_count_text = font.render(f"Количество расчленённых жуков: {self.player.scale}, ЖИВОДЁР!", True,
                                          (255, 255, 255))
            if self.player.hp <= 0:
                hp_text = font.render(f"Вы умерли", True, (255, 255, 255))
                live = 0
                res = -1
                self.bugs = []
                start_bugs = time.time() + 10 * 10
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False

            elif self.player.artifact == 3:
                hp_text = font.render(f"Вы победили!", True, (255, 255, 255))
                res = self.level
                self.bugs = []
                start_bugs = time.time() + 10 * 10
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False
            self.win.blit(hp_text, (20, 20))
            self.win.blit(bugs_count_text, (750, 20))  # Отображаем здоровье персонажа
            mouse_pos = pygame.mouse.get_pos()
            x = 50
            self.player.all_weapon_sprites.draw(self.win)
            for n, i in enumerate(self.player.weapon):
                if n == self.player.current_weapon:
                    pygame.draw.rect(self.win, (0, 0, 255), pygame.Rect(50, x, 50, 50), 1)

                if pygame.Rect(50, x, 50, 50).collidepoint(mouse_pos):
                    # Отображение характеристик оружия
                    text = font.render(f'{i}', True, (0, 0, 0))
                    self.win.blit(text, mouse_pos)
                x += 51
            pygame.display.update()  # Обновляем окно

        print(type(self.background))
        print(type(self.player.player_left))
        return {'win': res, 'time': self.time, 'bugs': self.bugs_count, 'live': live, 'scale': self.player.scale}

    def __getstate__(self):
        print("123")
        self.player.player_left = pygame.image.tostring(self.player.player_left, "RGBA")
        self.player.player_right = ''
        self.player.image = ''
        self.player.all_weapon_sprites = []
        for i in self.player.all_weapon:
            i.image = pygame.image.tostring(i.image, "RGBA")

        print(type(self.background))
        bugs = []
        for bug in self.bugs:
            bugs.append([bug.x, bug.y, bug.speed])
        for artifacts in self.artifacts:
            artifacts.image = pygame.image.tostring(artifacts.image, "RGBA")

        '''self.player_left = pygame.image.load(
            'персонаж_броня_.png')  # сам спрайт (изначально персонаж повернут влево)
        # player_left = pygame.transform.scale(player_left, (win_width // 400 * 70, win_width // 400 * 100))
        self.player_right = pygame.transform.flip(self.player_left, True, False)  # приколы с поворотом

        self.image = self.player_left'''

        state = self.__dict__.copy()
        state['win'] = ''
        state['background'] = self.background
        print(type(state['background']))
        print(type(self.background))
        state['bugy'] = bugs
        state['bugs'] = []
        state['scales'] = []
        state['armors'] = []
        state['weapons'] = []

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        print(type(self.player.player_left))
        self.player.player_left = pygame.image.fromstring(self.player.player_left, (70, 100), "RGBA")
        self.player.player_right = pygame.transform.flip(self.player.player_left, True, False)  # приколы с поворотом

        self.player.all_weapon_sprites = pygame.sprite.Group()
        for i in self.player.all_weapon:
            i.image = pygame.image.fromstring(i.image, (50, 50), "RGBA")
            self.player.all_weapon_sprites.add(i)

        self.player.image = self.player.player_left
        bugs = []
        for bug in self.bugy:
            self.bugs.append(Bug(bug[0], bug[1], bug[2], self.level))

        # self.bugs = bugs
        for artifacts in self.artifacts:
            artifacts.image = pygame.image.fromstring(artifacts.image, (30, 30), "RGBA")
        print(type(self.background))
        self.background = pygame.image.fromstring(self.background, (self.win_width * 20, self.win_height * 20), 'RGBA')


if __name__ == "__main__":
    pygame.init()
    level = 1
    infoObject = pygame.display.Info()
    win_width, win_height = infoObject.current_w, infoObject.current_h
    # Загрузка изображения заднего плана
    background = pygame.image.load(f'задник_{level}.png')
    # background = pygame.transform.scale(background,
    # (win_width * 20, win_height * 20))  # новые размеры персонажа

    a = Game(background, level)

    '''with open("savegame.dat", "rb") as fp:
        a = pickle.load(fp)'''

    a.game()