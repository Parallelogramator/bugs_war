import pygame
import pickle
import time
import threading
import sqlite3
import sys

from Bugs import Game

# Рисование текста

def draw_text(surface, text, x, y, font=None, font_size=60, color=(255, 255, 255)):
    myFont = pygame.font.SysFont(font, font_size)
    new_text = myFont.render(text, 1, color)
    surface.blit(new_text, (x, y))

def save(self, time, user_id):
    self.background = pygame.image.tostring(self.background, "RGBA")
    вот тут надо вставить загрузку файла в бд
    with open(f"data/{time}.dat", "wb") as fp:
        pickle.dump(self, fp)

class Start_Window():

    # Инициализация
    def __init__(self, name_gamer=''):
        pygame.init()

        # Размеры окна
        infoObject = pygame.display.Info()
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h

        # Настройка окна
        screen = pygame.display.set_mode((self.win_width, self.win_height), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))
        '''big_sky = pygame.image.load("sky.jpg")
        # масштабируем картинку под размер экрана
        sky = scale(big_sky, ((win_width, win_height))'''
        pygame.display.set_caption("Война жуков")

        # Подключение к базе данных
        self.connection = sqlite3.connect('bugs_war_database.sqlite')

        # Переменные
        self.name_gamer = name_gamer  # Имя игрока
        self.input_name = False  # Напоминание вести имя игрока
        self.common_x = self.win_width // 2 - 250
        self.koef_y = self.win_height // 10
        infoObject = pygame.display.Info()
        win_width, win_height = infoObject.current_w, infoObject.current_h
        # Загрузка изображения заднего плана
        background = pygame.image.load('задник.png')
        self.background = pygame.transform.scale(background,
                                                 (win_width * 20, win_height * 20))  # новые размеры персонажа

        # Создание кнопок
        start_button = Button(screen, self.common_x, self.koef_y * 2)
        continue_button = Button(screen, self.common_x, self.koef_y * 3)
        statistics_button = Button(screen, self.common_x, self.koef_y * 4)
        shop_button = Button(screen, self.common_x, self.koef_y * 5)
        information_button = Button(screen, self.common_x, self.koef_y * 6)
        quit_button = Button(screen, self.common_x, self.koef_y * 7)

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
                    if self.check_name(): # Если введено имя
                        if start_button.button.collidepoint(mouse_pos):
                            self.start_game()
                        if continue_button.button.collidepoint(mouse_pos):
                            self.continue_game()
                        if statistics_button.button.collidepoint(mouse_pos):
                            self.show_statistics()
                        if shop_button.button.collidepoint(mouse_pos):
                            self.show_shop()
                    if information_button.button.collidepoint(mouse_pos):
                        self.show_information()
                    if quit_button.button.collidepoint(mouse_pos):
                        pygame.quit()
                        save(self.game, time.time(), self.name_gamer)
                        self.connection.close()
                        sys.exit()

                # Добавление имени
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:  # Удаление последнего символа
                        self.name_gamer = self.name_gamer[:-1]
                    elif len(self.name_gamer) < 10: # Имя меньше 10 символов
                        self.name_gamer += event.unicode
                    self.input_name = False

            # Отрисовываем объекты
            screen.fill((0, 0, 0))
            '''big_sky = pygame.image.load("sky.jpg")
                    # масштабируем картинку под размер экрана
                    sky = scale(big_sky, ((win_width, win_height))'''
            draw_text(screen, 'Война жуков', self.common_x, self.koef_y,
                      font_size=100)
            start_button.text_button('Начать игру')
            continue_button.text_button('Продолжить игру')
            statistics_button.text_button('Статистика')
            information_button.text_button('Информация')
            shop_button.text_button('Магазин')
            quit_button.text_button('Выйти из игры')
            draw_text(screen, 'Имя:', self.common_x, self.koef_y * 8)
            draw_text(screen, self.name_gamer, self.common_x + 200, self.koef_y * 8)

            # Если не введено имя
            if self.input_name == True:
                draw_text(screen, 'Введите имя', self.common_x, self.koef_y * 9)
            pygame.display.flip()

    # Проверка на имя
    def check_name(self):
        if self.name_gamer != '':
            res = self.connection.cursor().execute("""SELECT name_gamer FROM Gamer""").fetchall()
            if (self.name_gamer,) not in res: # Если имени нет в БД, добавляем
                self.connection.cursor().execute(
                    """INSERT INTO Gamer(name_gamer, count_games, count_win, count_fail, all_dead_bugs, count_assistants, count_coins) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (self.name_gamer, 0, 0, 0, 0, 0, 0))
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
        pygame.quit()
        self.__init__(self.name_gamer)
    # Начать игру
    def start_game(self):
        self.game = Game(self.background)
        это_в_бд = self.game.game()
        '''
        thread = threading.Thread(target=self.game.save)
        thread.start()'''

    # Продолжить игру
    def continue_game(self):
        try:
            self.game.game()

        except Exception:
             нужно подтащить файл пути из бд

            with open(f"1705232418.5041902.dat", "rb") as fp:
                self.game = pickle.load(fp)
            это_в_бд = self.game.game()

    # Показать статистику
    def show_statistics(self):

        # Настройка окна
        statistics_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Статистика")
        statistics_screen.fill(((0, 0, 0)))

        # Информация об игроке
        information_gamer = self.connection.cursor().execute("""SELECT * FROM Gamer WHERE name_gamer=?""",
                                                             (self.name_gamer,)).fetchone()
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

            pygame.display.update()  # Обновляем окно

    # Показать магазин
    def show_shop(self):

        # Настройка окна
        shop_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Магазин")
        shop_screen.fill(((0, 0, 0)))

        # Кнопка "Назад"
        last = self.return_button(shop_screen)

        # Информация об игроке
        res = self.connection.cursor().execute("""SELECT count_assistants, count_coins FROM Gamer WHERE name_gamer=?""",
                                               (self.name_gamer,)).fetchone()
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
                        if res[1] >= 20: # Если денег хватает
                            self.connection.cursor().execute(f"""UPDATE SET count_assistants = {res[0] + 1} 
                            SET count_coins = {res[1] - 20} FROM Gamer WHERE name_gamer=?""", (self.name_gamer,))
                            self.connection.commit()
                        else:
                            draw_text(shop_screen, 'Не хватает денег', self.common_x, self.koef_y * 8)

            # Отрисовываем объекты
            shop_screen.fill(((0, 0, 0)))
            draw_text(shop_screen, 'Магазин', self.common_x, self.koef_y, font_size=100)
            draw_text(shop_screen, f'Кол-во жуков-помощников: {res[0]}', self.common_x, self.koef_y * 2)
            draw_text(shop_screen, f'Кол-во монет: {res[1]}', self.common_x, self.koef_y * 3)
            last.text_button('Назад')
            buy.text_button('Купить')
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
        text = '/n'.join([j.strip() for j in f])

        # Отрисовываем объекты
        draw_text(information_screen, text, self.common_x - 400, self.koef_y * 2)
        draw_text(information_screen, 'Информация', self.common_x, self.koef_y, font_size=100)

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
            draw_text(information_screen, text, self.common_x - 400, self.koef_y * 2)
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
