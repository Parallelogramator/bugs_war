<<<<<<< Updated upstream
import sqlite3
import sys

import pygame

from start import draw_text, Button, Start_Window


class End_Window:

    # Инициализация
    def __init__(self, id_game):
        pygame.init()

        # Размеры окна
        infoObject = pygame.display.Info()
        win_width, win_height = infoObject.current_w, infoObject.current_h

        # Настройка окна
        end_screen = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
        end_screen.fill((0, 0, 0))
        '''big_sky = pygame.image.load("sky.jpg")
        # масштабируем картинку под размер экрана
        sky = scale(big_sky, ((win_width, win_height))'''
        pygame.display.set_caption("Война жуков")

        # Переменные
        self.common_x = win_width // 2 - 250
        self.koef_y = win_height // 10
        id_gamer = 0

        # Подключение к базе данных
        self.connection = sqlite3.connect('bugs_war_database.sqlite')

        # Создание кнопок
        last_button = Button(end_screen, self.common_x, self.koef_y * 9)

        # Данные из БД (скорее всего всё будет в списке) из id game
        result = 0
        if result == 0:
            result = 'Поражение'
        else:
            result = 'Победа'
        time = 0
        dead_bugs = 0
        selected_items = 0
        remaining_lives = 0
        if dead_bugs != 0:
            ver = round((selected_items / dead_bugs * 100), 2)
        else:
            ver = 0

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
                    if last_button.button.collidepoint(mouse_pos):
                        self.connection.close()
                        Start_Window.__init__(self, id_gamer=id_gamer)
                        sys.exit()

            end_screen.fill((0, 0, 0))
            '''big_sky = pygame.image.load("sky.jpg")
                    # масштабируем картинку под размер экрана
                    sky = scale(big_sky, ((win_width, win_height))'''
            draw_text(end_screen, 'Война жуков', self.common_x, self.koef_y,
                      font_size=100)
            draw_text(end_screen, result, self.common_x + 70, self.koef_y * 3,
                      font_size=100)
            draw_text(end_screen, f'Время: {time}', self.common_x - 100, self.koef_y * 4)
            draw_text(end_screen, f'Кол-во убитых жуков: {dead_bugs}', self.common_x- 100, self.koef_y * 5)
            draw_text(end_screen, f'Кол-во выпавших предметов: {selected_items}', self.common_x- 100, self.koef_y * 6)
            draw_text(end_screen, f'Кол-во оставшихся жизней: {remaining_lives}', self.common_x- 100, self.koef_y * 7)
            draw_text(end_screen, f'Вероятность выпадания предметов: {ver}', self.common_x- 100, self.koef_y * 8)
            last_button.text_button('К главному меню')
            pygame.display.flip()


if __name__ == "__main__":
    End_Window(0)
=======
import sqlite3
import sys

import pygame

from start import draw_text, Button, Start_Window

class End_Window:

    # Инициализация
    def __init__(self, id_game):
        pygame.init()

        # Размеры окна
        infoObject = pygame.display.Info()
        win_width, win_height = infoObject.current_w, infoObject.current_h

        # Настройка окна
        end_screen = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
        end_screen.fill((0, 0, 0))
        '''big_sky = pygame.image.load("sky.jpg")
        # масштабируем картинку под размер экрана
        sky = scale(big_sky, ((win_width, win_height))'''
        pygame.display.set_caption("Война жуков")

        # Переменные
        self.common_x = win_width // 2 - 250
        self.koef_y = win_height // 10
        id_gamer = 0

        # Подключение к базе данных
        self.connection = sqlite3.connect('bugs_war_database.sqlite')

        # Создание кнопок
        last_button = Button(end_screen, self.common_x, self.koef_y * 9)

        # Данные из БД (скорее всего всё будет в списке) из id game
        result = 0
        if result == 0:
            result = 'Поражение'
        else:
            result = 'Победа'
        time = 0
        dead_bugs = 0
        selected_items = 0
        remaining_lives = 0
        if dead_bugs != 0:
            ver = round((selected_items / dead_bugs * 100), 2)
        else:
            ver = 0

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
                    if last_button.button.collidepoint(mouse_pos):
                        self.connection.close()
                        Start_Window.__init__(self, id_gamer=id_gamer)
                        sys.exit()

            end_screen.fill((0, 0, 0))
            '''big_sky = pygame.image.load("sky.jpg")
                    # масштабируем картинку под размер экрана
                    sky = scale(big_sky, ((win_width, win_height))'''
            draw_text(end_screen, 'Война жуков', self.common_x, self.koef_y,
                      font_size=100)
            draw_text(end_screen, result, self.common_x + 70, self.koef_y * 3,
                      font_size=100)
            draw_text(end_screen, f'Время: {time}', self.common_x - 100, self.koef_y * 4)
            draw_text(end_screen, f'Кол-во убитых жуков: {dead_bugs}', self.common_x- 100, self.koef_y * 5)
            draw_text(end_screen, f'Кол-во выпавших предметов: {selected_items}', self.common_x- 100, self.koef_y * 6)
            draw_text(end_screen, f'Кол-во оставшихся жизней: {remaining_lives}', self.common_x- 100, self.koef_y * 7)
            draw_text(end_screen, f'Вероятность выпадания предметов: {ver}', self.common_x- 100, self.koef_y * 8)
            last_button.text_button('К главному меню')
            pygame.display.flip()

if __name__ == "__main__":
    End_Window(0)
>>>>>>> Stashed changes
