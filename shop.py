import pygame
import random


class Button:
    def __init__(self, image, x, y):
        self.image = image#получаем изображение
        self.x = x
        self.y = y
        self.visible = True

    def draw(self, screen):
        # Отрисовываем кнопку на экране, если она видима
        if self.visible:
            screen.blit(self.image, (self.x, self.y))


class Start_Window:
    def __init__(self):
        pygame.init()
        infoObject = pygame.display.Info() # Получаем размер экрана пользователя
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h #запоминаем размеры экрана
        self.background = pygame.image.load('задник_магазина.png')# Загружаем изображение заднего плана и
        self.background = pygame.transform.scale(self.background,
                                                 (self.win_width, self.win_height))
        #                                         масштабируем изображение под размер экрана

        self.button_image = pygame.image.load('подложка_в_магазине.png')# Загружаем изображение кнопки

        # Вычисление координат кнопок и создание списока в который координаты будут положены
        self.button_x = self.win_width // 2.5  #Вычисление начальной координаты x для первой кнопки
        self.button_y = self.win_height // 8.1  #Вычисление начальной координаты y для первой кнопки
        self.button_width = 60 #ширина изображения кнопки
        self.button_height = 60 # высота изображения кнопки
        self.button_spacing_x = self.win_width // 85  # Вычисление горизонтального расстояние между кнопками
        self.button_spacing_y = self.win_height // 60  # Вычисление вертикального расстояние между кнопками
        self.num_buttons_col = 4  #количество кнопок в столбце
        self.num_buttons = self.num_buttons_col * 4  # количество столбцов
        self.last_button_x = self.button_x + (self.num_buttons_col - 1) * (
                    self.button_width + self.button_spacing_x)  # Вычисление координаты x последней кнопки в столбце
        self.last_button_y = self.button_y + (self.num_buttons - 1) * (
                    self.button_height + self.button_spacing_y)  # Вычисление координаты y последней кнопки в столбце
        self.button_coords = []  #список координат кнопок
        button_x = self.button_x  # для хранения текущей координаты x кнопки
        button_y = self.button_y  # для хранения текущей координаты y кнопки
        for i in range(self.num_buttons):
            self.button_coords.append((button_x, button_y))# Добавляем координаты текущей кнопки в список координат кнопок
            button_x += self.button_width + self.button_spacing_x  # Увеличиваем координату x текущей кнопки на ширину кнопки и горизонтальное расстояние между кнопками
            if (i + 1) % self.num_buttons_col == 0:  # Если текущая кнопка является последней в столбце
                button_x = self.button_x  # Сбрасываем координату x текущей кнопки к началу столбца
                button_y += self.button_height + self.button_spacing_y  # Увеличиваем координату y текущей кнопки на высоту кнопки и вертикальное расстояние между кнопками
        # Создаем список кнопок
        self.buttons = []
        for x, y in self.button_coords:
            self.buttons.append(Button(self.button_image, x,
                                       y))  # Создание элемента класса Button для каждой координаты в списке координат кнопок


    def run(self):
        # Создаем окно с заданным размером
        screen = pygame.display.set_mode((self.win_width, self.win_height))
        # Устанавливаем заголовок окна
        pygame.display.set_caption("Начальное окно")

        # Основной цикл
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, (button_x, button_y) in enumerate(self.button_coords):
                        if button_x < event.pos[0] < button_x + self.button_width and \
                                button_y < event.pos[1] < button_y + self.button_height:
                            self.buttons[i].visible = False# Если кнопка нажата, делаю её невидимой


            screen.blit(self.background, (0, 0))
            # Рисование всех видимых кнопкок на экране
            for button in self.buttons:
                if button.visible:
                    button.draw(screen)
            pygame.display.flip()# Обновляем экран
        pygame.quit()


if __name__ == "__main__":
    start_window = Start_Window()
    start_window.run()