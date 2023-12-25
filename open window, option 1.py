import pygame
import pygame_menu

#Экран + меню

pygame.init()
surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

def start_the_game():
    pass

def show_statistics():
    pass

def show_settings():
    pass


menu = pygame_menu.Menu('Жуки?', 1920, 1080,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='')
menu.add.button('Play', start_the_game)
menu.add.button('Settings', show_settings)
menu.add.button('Statistics', show_statistics)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
