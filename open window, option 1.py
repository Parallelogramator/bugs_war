import pygame
import pygame_menu
import sqlite3
from random import randint

from Bugs import Game
#Экран + меню
class Start_Window():
    def __init__(self):
        pygame.init()
        self.name_gamer = ''
        self.connection = sqlite3.connect('bugs_war_database.sqlite')
        infoObject = pygame.display.Info()
        font = pygame_menu.font.FONT_MUNRO
        self.win_width, self.win_height = infoObject.current_w, infoObject.current_h
        mytheme = pygame_menu.themes.Theme(title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
                                            background_color=(200, 255, 100, 100),
                                              title_background_color=(4, 47, 126), 
                                              title_font=font, title_font_color=(250, 200, 200),
                                              title_font_size=70, title_offset=(self.win_width // 2 - 70, 0), 
                                              widget_font_color=(211, 50, 40), widget_font_size=60, 
                                              widget_font=font)
        surface = pygame.display.set_mode((self.win_width, self.win_height), pygame.FULLSCREEN)
        self.menu = pygame_menu.Menu('Bags War', self.win_width, self.win_height,
                       theme=mytheme)
        # Кнопки
        self.message = None
        self.menu.add.text_input('Name :', default='', onchange=self.check_name)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Settings', self.show_settings)
        self.menu.add.button('Statistics', self.show_statistics)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.center_content()
        self.menu.mainloop(surface)
    
    def check_name(self, name):
        self.name_gamer = name

    def start_the_game(self): # начать игру
        if self.name_gamer != '':

            if (self.name_gamer, ) not in self.connection.cursor().execute("""SELECT name_gamer FROM Gamers""").fetchall():
                self.connection.cursor().execute("""INSERT INTO Gamers(ip_address, name_gamer) VALUES(?, ?)""", (11, self.name_gamer))
            background = pygame.image.load('задник.png')
            background = pygame.transform.scale(background,
                                    (self.win_width * 20, self.win_height * 20))  # новые размеры персонажа
            a = Game(background)
            a.game()
        elif self.message is None:
            self.message = self.menu.add.label('Put name')
    def show_statistics(self): # показать статистику
        pass
    def show_settings(self): # показать настройки
        pass

if __name__ == "__main__": 
    Start_Window()
