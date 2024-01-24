import os
import pickle
import sqlite3
import sys

import pygame

from Bugs import Game


# Рисование текста
def draw_text(surface, text, x, y, font=None, font_size=60, color=(255, 255, 255)):
    myFont = pygame.font.SysFont(font, font_size)
    new_text = myFont.render(text, 1, color)
    surface.blit(new_text, (x, y))


# Сохранение игры
def save(self, cursor, id_game):
    print('dddddddddd')
    print(id_game, os.listdir('data/'))
    self.background = pygame.image.tostring(self.background, "RGBA")
    file = cursor.execute("""SELECT path FROM Game WHERE id_game=?""", (id_game,)).fetchone()[0]
    print(file)
    with open(f"{file}.dat", "wb") as fp:
        pickle.dump(self, fp)


class Main_Window():

    # Инициализация
    def __init__(self, id_gamer=None):
        pygame.init()

        # Размеры окна
        infoObject = pygame.display.Info()
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h

        # Настройка окна
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        self.screen.fill((0, 0, 0))

        # Задний фон, если будет
        '''big_sky = pygame.image.load("sky.jpg")
        # масштабируем картинку под размер экрана
        sky = scale(big_sky, ((win_width, win_height))'''

        # Подключение к базе данных
        self.connection = sqlite3.connect('bugs_war_database.sqlite')
        self.cursor = self.connection.cursor()

        # Загрузка изображения заднего плана
        background = pygame.image.load('задник.png')
        self.background = pygame.transform.scale(background,
                                                 (self.win_width * 20, self.win_height * 20))  # новые размеры персонажа

        # Переменные
        self.id_gamer = id_gamer
        try:
            self.name_gamer = self.cursor.execute("""SELECT name_gamer FROM Gamer WHERE id_gamer=?""",
                                                  (self.id_gamer,)).fetchone()[0]  # Имя игрока
        except:
            self.name_gamer = ''
        self.input_name = False  # напоминание вести имя игрока
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

    # Закрытие приложения
    def close(self):
        pygame.quit()
        try:
            if self.game is not None:
                save(self.game, self.cursor, self.id_game)
        except Exception as e:
            print(e)
        self.cursor.close()
        self.connection.close()
        sys.exit()

    # Основной цикл главного окна
    def cycle(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
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
                        self.close()

                # Добавление имени
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:  # Удаление последнего символа
                        self.name_gamer = self.name_gamer[:-1]
                    elif len(self.name_gamer) < 10:  # Имя меньше 10 символов
                        self.name_gamer += event.unicode
                    self.input_name = False

            # Отрисовываем объекты
            self.screen.fill((0, 0, 0))
            draw_text(self.screen, 'Война жуков', self.common_x, self.koef_y,
                      font_size=100)
            self.start_button.text_button('Начать игру')
            self.continue_button.text_button('Продолжить игру')
            self.statistics_button.text_button('Статистика')
            self.information_button.text_button('Информация')
            self.shop_button.text_button('Магазин')
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
            res = self.cursor.execute("""SELECT name_gamer FROM Gamer""").fetchall()
            if (self.name_gamer,) not in res:  # Если имени нет в БД, добавляем
                self.cursor.execute("""INSERT INTO Gamer(name_gamer) VALUES(?)""", (self.name_gamer,))
                self.connection.commit()
            self.id_gamer = self.cursor.execute("""SELECT id_gamer FROM Gamer WHERE name_gamer=?""",
                                                (self.name_gamer,)).fetchone()[0]
            return True
        self.input_name = True
        return False

    # Кнопка "Назад"
    def return_button(self, screen):
        last = Button(screen, self.common_x, self.koef_y * 9)
        last.text_button('Назад')
        return last

    # Начать игру
    def start_game(self):

        # Создание строки в БД
        self.cursor.execute(
            """INSERT INTO Game(id_gamer, result, time, dead_bugs, hand_items, remaining_lives, path) VALUES(?, 0, 0, 0, 0, 0, 0)""",
            (self.id_gamer,))
        self.connection.commit()
        self.id_game = self.cursor.execute(""" SELECT MAX(id_game) FROM Game""").fetchone()[0]  # Сохранение id игры
        file_path = os.path.join('data/', str(self.id_game))  # Путь к папке
        self.cursor.execute(
            """UPDATE Game SET path=? WHERE id_game=?""", (file_path, self.id_game))
        self.connection.commit()

        # Создание игры
        self.game = Game(self.background, 0)
        to_end = self.game.game()

        print(to_end)

        # Сохранение данные по игре
        self.cursor.execute(
            """UPDATE Game SET result=?, time=?, dead_bugs=?, hand_items=?, remaining_lives=? WHERE id_game=?""",
            (to_end['win'], to_end['time'], to_end["bugs"], to_end["scale"], to_end["live"], self.id_game))
        information_gamer = self.cursor.execute("""SELECT * FROM Gamer WHERE id_gamer=?""",
                                                (self.id_gamer,)).fetchone()
        self.cursor.execute("""UPDATE Gamer SET count_games=?, all_dead_bugs=? WHERE id_gamer=?""",
                            (information_gamer[2] + 1, information_gamer[5] + to_end['bugs'], self.id_gamer))
        self.connection.commit()

        # Если игра завершилась поражением или победой
        if to_end['win'] == 3 or to_end['win'] == 0:
            self.game = None
            os.remove(f"{file_path}.dat")
            self.end_window(to_end)
        # Иначе сохраняем  данные по игре

    # Финальное окно
    def end_window(self, results):

        # Настройка окна
        end_screen = pygame.display.set_mode((self.win_width, self.win_height), pygame.FULLSCREEN)
        end_screen.fill((0, 0, 0))

        # Задний фон, если будет
        '''big_sky = pygame.image.load("sky.jpg")
        # масштабируем картинку под размер экрана
        sky = scale(big_sky, ((win_width, win_height))'''

        # Создание кнопки
        last_button = self.return_button(end_screen)

        # Переменные
        information_gamer = self.cursor.execute("""SELECT * FROM Gamer WHERE id_gamer=?""",
                                                (self.id_gamer,)).fetchone()
        if results['win'] == 3:
            win_or_fail = 'Победа'
            # Изменение общей статистики
            self.cursor.execute("""UPDATE Gamer SET count_win = ?
                                        WHERE id_gamer=?""", (information_gamer[3] + 1, self.id_gamer))
        else:
            win_or_fail = 'Поражение'
            # Изменение общей статистики
            self.cursor.execute("""UPDATE Gamer SET count_fail = ?
                                                    WHERE id_gamer=?""", (information_gamer[4] + 1, self.id_gamer))
        self.connection.commit()

        # Основной цикл финального окна
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cycle()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопки
                    if last_button.button.collidepoint(mouse_pos):
                        self.cycle()

            # Отрисовываем объекты
            end_screen.fill((0, 0, 0))
            draw_text(end_screen, 'Война жуков', self.common_x, self.koef_y,
                      font_size=100)
            draw_text(end_screen, win_or_fail, self.common_x + 70, self.koef_y * 3,
                      font_size=100)
            draw_text(end_screen, f'Время: {results["time"]}', self.common_x - 100, self.koef_y * 4)
            draw_text(end_screen, f'Кол-во убитых жуков: {results["bugs"]}', self.common_x - 100, self.koef_y * 5)
            draw_text(end_screen, f'Кол-во подобранных предметов: {results["scale"]}', self.common_x - 100,
                      self.koef_y * 6)
            draw_text(end_screen, f'Кол-во оставшихся жизней: {results["live"]}', self.common_x - 100, self.koef_y * 7)
            last_button.text_button('К главному меню')

            pygame.display.flip()

    # Продолжение игры
    def continue_game(self):
        try:
            self.game.game()
        except Exception:
            al = self.cursor.execute("""SELECT id_game, result FROM Game WHERE id_gamer=?""",
                                     (self.id_gamer,)).fetchall()
            self.id_game, result = max(al, key=lambda x: x[0])
            print(al, id, result)
            if result != -1:
                self.game = Game(self.background, result + 1)
            else:
                print(os.listdir('data/'))
                with open(f"data/{self.id_game}.dat", "rb") as fp:
                    self.game = pickle.load(fp)
            print(self.game.game())

    # Показать статистику
    def show_statistics(self):

        # Настройка окна
        statistics_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Статистика")
        statistics_screen.fill(((0, 0, 0)))

        # Информация об игроке
        information_gamer = self.cursor.execute("""SELECT * FROM Gamer WHERE id_gamer=?""",
                                                (self.id_gamer,)).fetchone()
        self.connection.commit()

        last = self.return_button(statistics_screen)

        # Отрисовываем объекты
        draw_text(statistics_screen, 'Статистика', self.common_x, self.koef_y, font_size=100)
        draw_text(statistics_screen, f"Имя: {information_gamer[1]}", self.common_x, self.koef_y * 2)
        draw_text(statistics_screen, f"Кол-во игр: {information_gamer[2]}", self.common_x, self.koef_y * 3)
        draw_text(statistics_screen, f"Кол-во побед: {information_gamer[3]}", self.common_x, self.koef_y * 4)
        draw_text(statistics_screen, f"Кол-во проигрышей: {information_gamer[4]}", self.common_x, self.koef_y * 5)
        draw_text(statistics_screen, f"Кол-во убитых жуков: {information_gamer[5]}", self.common_x, self.koef_y * 6)
        draw_text(statistics_screen, f"Кол-во жуков-помощников: {information_gamer[6]}", self.common_x,
                  self.koef_y * 7)
        draw_text(statistics_screen, f"Кол-во монет: {information_gamer[7]}", self.common_x, self.koef_y * 8)

        # Основной цикл
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cycle()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопок
                    if last.button.collidepoint(mouse_pos):
                        self.cycle()

            pygame.display.flip()

    # Показать магазин
    def show_shop(self):
        # Настройка окна
        shop_screen = pygame.display.set_mode((self.win_width, self.win_height))
        flag_not_money = False

        # Картинка
        image = pygame.image.load('жуг_бобрый.png').convert_alpha()
        image = pygame.transform.scale(image, (400, 300))

        # Кнопка "Назад"
        last = self.return_button(shop_screen)

        # Информация об игроке
        res = self.cursor.execute("""SELECT count_assistants, count_coins FROM Gamer WHERE id_gamer=?""",
                                  (self.id_gamer,)).fetchone()

        # Кнопка "Купить"
        buy = Button(shop_screen, self.common_x, self.koef_y * 7)

        # Основной цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cycle()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопок
                    if last.button.collidepoint(mouse_pos):
                        self.cycle()
                    if buy.button.collidepoint(mouse_pos):
                        if res[1] >= 1000:  # Если денег хватает
                            self.cursor.execute("""UPDATE Gamer SET count_assistants = ?
                            WHERE id_gamer=?""", (res[0] + 1, self.id_gamer))
                            self.cursor.execute("""UPDATE Gamer 
                                                        SET count_coins = ?
                                                        WHERE id_gamer=?""", (res[1] - 1000, self.id_gamer))
                            self.connection.commit()
                            flag_not_money = False
                        else:
                            flag_not_money = True

            # Отрисовываем объекты
            shop_screen.fill((0, 0, 0))
            shop_screen.blit(image, (self.common_x, self.koef_y * 4 - 40))
            res = self.cursor.execute(
                """SELECT count_assistants, count_coins FROM Gamer WHERE id_gamer=?""",
                (self.id_gamer,)).fetchone()
            if flag_not_money:
                draw_text(shop_screen, 'Не хватает денег', self.common_x, self.koef_y * 8)
            draw_text(shop_screen, 'Магазин', self.common_x, self.koef_y, font_size=100)
            draw_text(shop_screen, f'Кол-во жуков-помощников: {res[0]}', self.common_x, self.koef_y * 2)
            draw_text(shop_screen, f'Кол-во монет: {res[1]}', self.common_x, self.koef_y * 3)
            last.text_button('Назад')
            buy.text_button('Купить за 1000 монет')
            pygame.display.flip()

    def show_information(self):

        # Настройка окна
        information_screen = pygame.display.set_mode((self.win_width, self.win_height))

        # Кнопка "Назад"
        last = self.return_button(information_screen)

        # Информация из файла
        f = open('Information', encoding='UTF-8').readlines()
        text = [j.strip() for j in f]

        # Отрисовываем объекты
        for i in range(len(text)):
            draw_text(information_screen, text[i], 100, self.win_height // 15 * (i + 3))
        draw_text(information_screen, 'Информация', self.common_x, self.koef_y, font_size=100)

        # Основной цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cycle()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Проверка нажатия кнопок
                    if last.button.collidepoint(mouse_pos):
                        self.cycle()
            pygame.display.flip()


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
    def text_button(self, text, font=None, font_size=60, color=(255, 255, 255)):
        self.draw_button()
        draw_text(self.surface, text, self.x, self.y, font=font, font_size=font_size, color=color)


if __name__ == "__main__":
    Main_Window()
