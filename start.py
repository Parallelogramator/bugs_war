import pickle
import sqlite3
import sys
import time

import pygame

from Bugs import Game


# Рисование текста

def draw_text(surface, text, x, y, font=None, font_size=60, color=(255, 255, 255)):
    myFont = pygame.font.SysFont(font, font_size)
    new_text = myFont.render(text, 1, color)
    surface.blit(new_text, (x, y))


def save(self, id_gamer, connection):
    self.background = pygame.image.tostring(self.background, "RGBA")
    вот тут надо вставить сохранение по id игры
    file = connection.cursor().execute("""SELECT path FROM Game WHERE id_gamer=?""", (id_gamer,)).fetchone()
    with open(f"data/{file}.dat", "wb") as fp:
        pickle.dump(self, fp)


class Start_Window():

    # Инициализация
    def __init__(self, id_gamer=None):
        pygame.init()

        # Размеры окна
        infoObject = pygame.display.Info()
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h

        # Настройка окна
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        self.screen.fill((0, 0, 0))
        '''big_sky = pygame.image.load("sky.jpg")
        # масштабируем картинку под размер экрана
        sky = scale(big_sky, ((win_width, win_height))'''
        pygame.display.set_caption("Война жуков")

        # Подключение к базе данных
        self.connection = sqlite3.connect('bugs_war_database.sqlite')

        # Загрузка изображения заднего плана
        background = pygame.image.load('задник.png')
        self.background = pygame.transform.scale(background,
                                                 (self.win_width * 20, self.win_height * 20))  # новые размеры персонажа

        # Переменные
        self.id_gamer = id_gamer
        try:
            self.name_gamer = self.connection.cursor().execute("""SELECT name_gamer FROM Gamer WHERE id_gamer=?""",
                                                               (self.id_gamer,)).fetchone()[0]  # Имя игрока
        except:
            self.name_gamer = ''
        self.input_name = False  # Напоминание вести имя игрока
        self.common_x = self.win_width // 2 - 250
        self.koef_y = self.win_height // 10

        # Создание кнопок
        self.start_button = Button(self.screen, self.common_x, self.koef_y * 2)
        self.continue_button = Button(self.screen, self.common_x, self.koef_y * 3)
        self.statistics_button = Button(self.screen, self.common_x, self.koef_y * 4)
        self.shop_button = Button(self.screen, self.common_x, self.koef_y * 5)
        self.information_button = Button(self.screen, self.common_x, self.koef_y * 6)
        self.quit_button = Button(self.screen, self.common_x, self.koef_y * 7)

        self.cycle()


    def cycle(self):
        # Основной цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.connection.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопок
                    if self.check_name():  # Если введено имя
                        if self.start_button.button.collidepoint(mouse_pos):
                            self.start_game()
                        if self.continue_button.button.collidepoint(mouse_pos):
                            self.continue_game()
                        if self.statistics_button.button.collidepoint(mouse_pos):
                            self.show_statistics()
                        if self.shop_button.button.collidepoint(mouse_pos):
                            self.show_shop()
                    if self.information_button.button.collidepoint(mouse_pos):
                        self.show_information()

                    if self.quit_button.button.collidepoint(mouse_pos):
                        pygame.quit()
                        if self.game:
                            save(self.game, self.id_gamer, self.connection)
                        self.connection.close()
                        sys.exit()

                # Добавление имени
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:  # Удаление последнего символа
                        self.name_gamer = self.name_gamer[:-1]
                    elif len(self.name_gamer) < 10:  # Имя меньше 10 символов
                        self.name_gamer += event.unicode
                    self.input_name = False

            # Отрисовываем объекты
            self.screen.fill((0, 0, 0))
            '''big_sky = pygame.image.load("sky.jpg")
                    # масштабируем картинку под размер экрана
                    sky = scale(big_sky, ((win_width, win_height))'''
            draw_text(self.screen, 'Война жуков', self.common_x, self.koef_y,
                      font_size=100)
            self.start_button.text_button('Начать игру')
            self.continue_button.text_button('Продолжить игру')
            self.statistics_button.text_button('Статистика')
            self.information_button.text_button('Информация')
            self. shop_button.text_button('Магазин')
            self.quit_button.text_button('Выйти из игры')
            draw_text(self.screen, 'Имя:', self.common_x, self.koef_y * 8)
            draw_text(self.screen, self.name_gamer, self.common_x + 200, self.koef_y * 8)

            # Если не введено имя
            if self.input_name == True:
                draw_text(self.screen, 'Введите имя', self.common_x, self.koef_y * 9)
            pygame.display.flip()


    # Проверка на имя
    def check_name(self):
        if self.name_gamer != '':
            res = self.connection.cursor().execute("""SELECT name_gamer FROM Gamer""").fetchall()
            if (self.name_gamer,) not in res:  # Если имени нет в БД, добавляем
                self.connection.cursor().execute("""INSERT INTO Gamer(name_gamer) VALUES(?)""", (self.name_gamer,))
                self.id_gamer = self.connection.cursor().execute("""SELECT id_gamer FROM Gamer WHERE name_gamer=?""",
                                                                 (self.name_gamer,)).fetchone()[0]
                self.connection.commit()
            return True
        self.input_name = True
        return False

    # Кнопка "Назад"
    def return_button(self, screen):
        last = Button(screen, self.common_x, self.koef_y * 9)
        last.text_button('Назад')
        return last

    # Возвращение к меню
    def to_menu(self):
        self.cycle()

    # Начать игру
    def start_game(self):
        self.game = Game(self.background, 0)
        self.game.game()
        '''
        thread = threading.Thread(target=self.game.save)
        thread.start()'''

    # Продолжить игру
    def continue_game(self):
        # Нужна проверка на существование последней игры
        try:
            self.game.game()
            print(1)
        except Exception:
            # Подтащила время из БД
            резулт это уровень игры, время замени на id игры
            id, result = self.connection.cursor().execute("""SELECT time, result FROM Game WHERE id_gamer=?""",
                                                   (self.id_gamer)).fetchone()

            if result is not None:
                self.game = Game(self.background, result+1)
            else:
                with open(f"data/{id}.dat", "rb") as fp:
                    self.game = pickle.load(fp)
            self.game.game()

    # Показать статистику
    def show_statistics(self):

        # Настройка окна
        statistics_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Статистика")
        statistics_screen.fill(((0, 0, 0)))

        # Информация об игроке
        information_gamer = self.connection.cursor().execute("""SELECT * FROM Gamer WHERE id_gamer=?""",
                                                             (self.id_gamer,)).fetchone()
        self.connection.commit()

        last = self.return_button(statistics_screen)

        # Основной цикл
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.to_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопок
                    if last.button.collidepoint(mouse_pos):
                        self.to_menu()
            # Отрисовываем объекты
            statistics_screen.fill(((0, 0, 0)))
            draw_text(statistics_screen, 'Статистика', self.common_x, self.koef_y, font_size=100)
            draw_text(statistics_screen, f"Имя: {information_gamer[1]}", self.common_x, self.koef_y * 2)
            draw_text(statistics_screen, f"Кол-во игр: {information_gamer[2]}", self.common_x, self.koef_y * 3)
            draw_text(statistics_screen, f"Кол-во побед: {information_gamer[3]}", self.common_x, self.koef_y * 4)
            draw_text(statistics_screen, f"Кол-во проигрышей: {information_gamer[5]}", self.common_x, self.koef_y * 5)
            draw_text(statistics_screen, f"Кол-во убитых жуков: {information_gamer[5]}", self.common_x, self.koef_y * 6)
            draw_text(statistics_screen, f"Кол-во жуков-помощников: {information_gamer[6]}", self.common_x,
                      self.koef_y * 7)
            draw_text(statistics_screen, f"Кол-во монет: {information_gamer[7]}", self.common_x, self.koef_y * 8)

            # Кнопка "Назад"
            last.text_button('Назад')

            pygame.display.update()  # Обновляем окно

    # Показать магазин
    def show_shop(self):

        # Настройка окна
        shop_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Магазин")
        shop_screen.fill(((0, 0, 0)))
        flag_not_money = False

        # Картинка
        '''assistent = pygame.image.load('задник.png')
        self.background = pygame.transform.scale(background,
                                                 (self.win_width * 20, self.win_height * 20)) # новые размеры персонажа
        assistent = pygame.image.tostring(assistent, "RGBA")'''

        # Кнопка "Назад"
        last = self.return_button(shop_screen)

        # Информация об игроке
        res = self.connection.cursor().execute("""SELECT count_assistants, count_coins FROM Gamer WHERE id_gamer=?""",
                                               (self.id_gamer,)).fetchone()
        self.connection.commit()

        # Кнопка "Купить"
        buy = Button(shop_screen, self.common_x, self.koef_y * 7)

        # Основной цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.to_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопок
                    if last.button.collidepoint(mouse_pos):
                        self.to_menu()
                    if buy.button.collidepoint(mouse_pos):
                        print(res)
                        if res[1] >= 1000:  # Если денег хватает
                            self.connection.cursor().execute(f"""UPDATE SET count_assistants = {res[0] + 1} 
                            SET count_coins = {res[1] - 1000} FROM Gamer WHERE id_gamer=?""", (self.id_gamer,))
                            self.connection.commit()
                            flag_not_money = False
                        else:
                            flag_not_money = True

            # Отрисовываем объекты
            shop_screen.fill(((0, 0, 0)))
            if flag_not_money:
                draw_text(shop_screen, 'Не хватает денег', self.common_x, self.koef_y * 8)
            ''' assistent = pygame.image.tostring(assistent, "RGBA")'''
            draw_text(shop_screen, 'Магазин', self.common_x, self.koef_y, font_size=100)
            draw_text(shop_screen, f'Кол-во жуков-помощников: {res[0]}', self.common_x, self.koef_y * 2)
            draw_text(shop_screen, f'Кол-во монет: {res[1]}', self.common_x, self.koef_y * 3)
            last.text_button('Назад')
            buy.text_button('Купить за 1000 монет')
            pygame.display.flip()

    def show_information(self):

        # Настройка окна
        information_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Информация")
        information_screen.fill(((0, 0, 0)))

        # Кнопка "Назад"
        last = self.return_button(information_screen)

        # Информация из файла
        f = open('Information', encoding='UTF-8').readlines()
        text = [j.strip() for j in f]


        # Основной цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.to_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопок
                    if last.button.collidepoint(mouse_pos):
                        self.to_menu()

            # Отрисовываем объекты
            for i in range(len(text)):
                draw_text(information_screen, text[i], self.common_x -500, self.win_height // 15 * (i + 3), font_size=40)
            draw_text(information_screen, 'Информация', self.common_x, self.koef_y, font_size=100)
            pygame.display.update()  # Обновляем окно


# Класс для создания кнопок
class Button:

    # Инициализация
    def __init__(self, surface, x, y, color_button='green'):
        pygame.init()
        self.surface = surface
        self.x = x
        self.y = y
        self.color_button = color_button
        self.draw_button()

    # Рисование кнопки
    def draw_button(self):
        self.button = pygame.draw.rect(self.surface, self.color_button, (self.x, self.y, 450, 45))

    # Рисование текста
    def text_button(self, text, font=None, font_size=70, color=(255, 255, 255)):
        self.draw_button()
        draw_text(self.surface, text, self.x, self.y, font=None, font_size=60, color=(255, 255, 255))


if __name__ == "__main__":
    Start_Window()
