import pygame
import math
import time
from random import randint
pygame.init()

# Установка размеров окна
infoObject = pygame.display.Info()
win_width, win_height = infoObject.current_w, infoObject.current_h
win = pygame.display.set_mode((win_width, win_height))

# Загрузка изображений персонажа
character_right = pygame.image.load('персонаж облаченный зеленый.png')
character_left = pygame.transform.flip(character_right, True, False)

# Загрузка изображения заднего плана
background = pygame.image.load('задник.png')

# Загрузка изображений персонажа и жука
character = character_right

# Установка параметров персонажа
character_x, character_y = 50, 50
vel = 5
character_hp = 100

# Установка параметров заднего плана
bg_x, bg_y = 0, 0
bg_width, bg_height = background.get_size()

class Bug:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load('жуг.png')
        self.hp = 20

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        dx /= dist
        dy /= dist
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if 50 <= new_x <= win_width - 50 and 50 <= new_y <= win_height - 50:  # Проверка, не выходит ли жук за пределы окна или не врезается ли он в стены
            self.x = new_x
            self.y = new_y
        return dist

    def draw(self, win):
        win.blit(self.image, (self.x - bg_x, self.y - bg_y))

# Создание жуков
bugs = [Bug(randint(0, 800), randint(0, 600), randint(1, 5))]
start = time.time()

font = pygame.font.Font(None, 36)  # Шрифт для отображения здоровья

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if time.time() - start > 5:
        bugs.append(Bug(randint(0, 800), randint(0, 600), randint(1, 5)))
        start = time.time()
        print("Bug")
    keys = pygame.key.get_pressed()

    new_character_x = character_x
    new_character_y = character_y

    if keys[pygame.K_a]:  # Если нажата клавиша 'a', персонаж движется влево
        new_character_x -= vel
        character = character_right  # Персонаж поворачивается влево
    if keys[pygame.K_d]:  # Если нажата клавиша 'd', персонаж движется вправо
        new_character_x += vel
        character = character_left  # Персонаж поворачивается вправо
    if keys[pygame.K_w]:  # Если нажата клавиша 'w', персонаж движется вверх
        new_character_y -= vel
    if keys[pygame.K_s]:  # Если нажата клавиша 's', персонаж движется вниз
        new_character_y += vel
    if keys[pygame.K_DOWN]:  # Если нажата клавиша 'shift', персонаж движется вниз
        vel = 100
    else:
        vel = 5

    # Проверка, не выходит ли персонаж за пределы окна или не врезается ли он в стены


    # Перемещение заднего плана, когда персонаж подходит к краю экрана
    if new_character_x > win_width-50:
        bg_x = (new_character_x - win_width + 50 )
        new_character_x = character_x
    if new_character_y > win_height - 50:
        bg_y = (new_character_y - win_height + 50)
        new_character_y = character_y
    if new_character_x < bg_width - win_width - 50:
        bg_x = - (bg_width - win_width - new_character_x)
        new_character_x = character_x
    if new_character_y < bg_height - win_height - 50:
        bg_y = - (bg_height - win_height - new_character_y)
        new_character_y = character_y

    if 50 <= new_character_x <= win_width - 50 and 50 <= new_character_y <= win_height - 50 or 1:
            character_x = new_character_x
            character_y = new_character_y

    if keys[pygame.K_SPACE]:  # Если нажата клавиша 'space', персонаж "бьет" жуков
        for bug in bugs:
            if math.sqrt((bug.x - character_x) ** 2 + (bug.y - character_y) ** 2) < 50:
                bug.hp -= 10
                print("Персонаж бьет жука!")

    win.fill((0, 0, 0))  # Заполняем окно черным цветом
    win.blit(background, (bg_x, bg_y))  # Рисуем задний план
    win.blit(character, (character_x, character_y))  # Рисуем персонажа

    for bug in bugs[:]:
        dist = bug.move_towards(character_x, character_y)
        bug.draw(win)
        if dist < 50:
            character_hp -= 1
            print("Жук бьет персонажа!")
        if bug.hp <= 0:
            bugs.remove(bug)
            print("Жук убит!")

    hp_text = font.render(f"Здоровье: {character_hp}", True, (255, 255, 255))
    if character_hp < 0:
        hp_text = font.render(f"Вы умерли", True, (255, 255, 255))
        bugs = []
        start = time.time() + 10*10
    win.blit(hp_text, (20, 20))  # Отображаем здоровье персонажа

    pygame.display.update()  # Обновляем окно
    if character_hp < 0:
        time.sleep(20)
        run = False

pygame.quit()
