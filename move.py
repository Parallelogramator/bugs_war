import pygame
from math import sqrt
from unmove import Weapon


class Players:
    def __init__(self, x, y, win_width, win_height):
        self.x = x
        self.y = y
        self.speed = 5

        self.win_width = win_width
        self.win_height = win_height
        self.path = ['персонаж.png']
        self.player_left = pygame.image.load('пустой_перс_всё_для_куздница'+'_'.join(self.path))  # сам спрайт (изначально персонаж повернут влево)
        # player_left = pygame.transform.scale(player_left, (win_width // 400 * 70, win_width // 400 * 100))
        self.player_right = pygame.transform.flip(self.player_left, True, False)  # приколы с поворотом

        self.image = self.player_left
        self.hp = 100

        self.all_weapon = []
        self.all_weapon_sprites = pygame.sprite.Group()

        self.base_attack = 10
        self.current_weapon = 0
        self.artifact = 0
        self.weapon = [{'attack': 0, 'rang': 100}]
        self.armor = []
        self.scale = 0

        self.sprite = pygame.sprite.Sprite()
        # определим его вид
        self.sprite.image = pygame.transform.scale(self.image, (50, 50))
        self.sprite.rect = (50, 50, 50, 50)
        # добавим спрайт в группу
        self.all_weapon_sprites.add(self.sprite)

        self.all_weapon.append(self.sprite)

    def move(self, keys, bg_x, bg_y):
        new_character_x = self.x
        new_character_y = self.y

        # Обработка нажатий клавиш
        if keys[pygame.K_a]:
            new_character_x -= self.speed
            self.image = self.player_right
        if keys[pygame.K_d]:
            new_character_x += self.speed
            self.image = self.player_left
        if keys[pygame.K_w]:
            new_character_y -= self.speed
        if keys[pygame.K_s]:
            new_character_y += self.speed
        if keys[pygame.K_LSHIFT]:
            self.speed = 50
        else:
            self.speed = 10

        # Проверка, не выходит ли персонаж за пределы окна или не врезается ли он в стены
        vel_bg_x, vel_bg_y, bg_x, bg_y = self.check_character_bounds(new_character_x, new_character_y, bg_x, bg_y)

        return vel_bg_x, vel_bg_y, bg_x, bg_y

    def check_character_bounds(self, new_character_x, new_character_y, bg_x, bg_y):
        self.boundary = self.win_height// 2  #количество пикселей, формирующих прямоугольник в котором ходит персонаж
        vel_bg_x, vel_bg_y = 0, 0

        if not (self.boundary <= new_character_y + 300 and new_character_y  <= self.win_height - self.boundary): #проверяет что
            # персонаж не выходит из "невидимомго" прямоугольника по координатам У с учетом что спрайт персонажа имеет размеры
            bg_y, vel_bg_y, new_character_y = self.update_position(new_character_y, self.y, self.win_height, bg_y,
                                                                   self.speed)

        if not (self.boundary <= new_character_x + 210 and new_character_x <= self.win_width - self.boundary): # аналогично,
            #проверяет что персонаж не выходит из "невидимомго" прямоугольника по координатам Х с учетом что спрайт персонажа имеет размеры
            bg_x, vel_bg_x, new_character_x = self.update_position(new_character_x, self.x, self.win_width, bg_x,
                                                                   self.speed)

        self.x, self.y = new_character_x, new_character_y

        return vel_bg_x, vel_bg_y, bg_x, bg_y

    def update_position(self, new_character_pos, character_pos, win_size, bg_pos, speed):
        if new_character_pos > win_size - self.boundary:
            bg_pos -= speed
            vel_bg = -speed
        else:
            bg_pos += speed
            vel_bg = speed

        new_character_pos = character_pos

        return bg_pos, vel_bg, new_character_pos

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def add_artifact(self):
        self.artifact += 1
        print("Adding artifact")

    def add_weapon(self, char):
        self.sprite = pygame.sprite.Sprite()
        # определим его вид
        self.sprite.image = char.get('image')
        # и размеры
        a = False

        if len(self.weapon) == 2:
            self.sprite.rect = (50, 50+(51*(self.current_weapon)), 50, 50)
            # добавим спрайт в группу
            char.pop('image')
            self.all_weapon_sprites.remove(self.all_weapon[self.current_weapon])
            a = self.all_weapon[self.current_weapon].image
            self.all_weapon[self.current_weapon] = self.sprite
            print(dir(self.sprite.image))
            self.all_weapon_sprites.add(self.sprite)
            self.weapon[self.current_weapon] = char
        else:
            self.sprite.rect = (50, 101, 50, 50)
            # добавим спрайт в группу
            self.all_weapon_sprites.add(self.sprite)

            self.all_weapon.append(self.sprite)

            char.pop('image')
            self.weapon.append(char)
        print("Adding weapon")
        return a

    def change_weapon(self):
        self.current_weapon = (self.current_weapon+1) % 2

    def add_armor(self, char):
        self.armor.append(char)
        print("Adding armor")

    def add_scale(self):
        self.scale += 1
        print("Adding scale")

    def attack(self):
        return self.base_attack + self.weapon[self.current_weapon].get('attack')

    def defence(self):
        res = 1
        for i in self.armor:
            res += i['protection']
            i['strength'] -= 1
        return res

    def rang(self):
        return self.weapon[self.current_weapon].get('rang')


class Bug:
    def __init__(self, x, y, speed, level):
        self.x = x
        self.y = y
        self.speed = speed
        self.animation_frames = bugs_image[level]
        self.bug_right = self.animation_frames
        self.bug_left = [pygame.transform.flip(image, True, False) for image in self.bug_right]
        self.image = self.bug_right[0]
        self.current_frame = 0 #кадрик анимации
        self.hp = 20

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = sqrt(dx ** 2 + dy ** 2)
        dx /= dist
        dy /= dist
        new_x = self.x + dx * self.speed
        if dx > 0:
            self.image = self.bug_left[self.current_frame]
        else:
            self.image = self.bug_right[self.current_frame]
        new_y = self.y + dy * self.speed

        self.x = new_x
        self.y = new_y
        self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

        return dist

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def pos_bg(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y


bugs_image = [[pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг1.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг2.png'),
                                 pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг3.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг4.png'),
                                 pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг5.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг6.png'),
                                 pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг7.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг8.png'),
                                 pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг9.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг10.png'),
                                 pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг11.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг12.png'),
                                 pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг13.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг14.png'),
                                 pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг15.png'), pygame.image.load('анимация_самого_простотго_жука_зеленой/жуг16.png')], 'жук_фиолетовый.png']
