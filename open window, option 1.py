import pygame
import pygame_menu

#Экран + меню
class Start_Window():
    def __init__(self):
        pygame.init()
        infoObject = pygame.display.Info()
        font = pygame_menu.font.FONT_MUNRO
        win_width, win_height = infoObject.current_w, infoObject.current_h
        mytheme = pygame_menu.themes.Theme(title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
                                            background_color=(200, 255, 100, 100),
                                              title_background_color=(4, 47, 126), 
                                              title_font=font, title_font_color=(250, 200, 200),
                                              title_font_size=70, title_offset=(win_width // 2 - 70, 0), 
                                              widget_font_color=(211, 50, 40), widget_font_size=60, 
                                              widget_font=font)
        surface = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
        menu = pygame_menu.Menu('Bags War', win_width, win_height,
                       theme=mytheme)
        # Кнопки
        menu.add.text_input('Name :', default='')
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Settings', self.show_settings)
        menu.add.button('Statistics', self.show_statistics)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.center_content()
        menu.mainloop(surface)

    def start_the_game(): # начать игру
        pass
    def show_statistics(): # показать статистику
        pass
    def show_settings(): # показать настройки
        pass

if __name__ == "__main__": 
    Start_Window()
