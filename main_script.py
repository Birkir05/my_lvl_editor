import pygame as py
from settings import *
from menu import Menu

class Editor:

    def __init__(self):
        py.init()
        self.clock = py.time.Clock()
        self.screen = py.display.set_mode((menu_width, menu_height))
        self.running = True

        self.font_name = py.font.match_font("arial")
        self.menu = Menu(self)
    
    def load_data(self):
        pass

    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
    
    def draw(self, draw_method): # potentially possible to use kwargs here
        self.screen.fill(BLACK)
        draw_method()
        py.display.flip()

    def draw_text(self, surf, text, size, color, x, y):
        font = py.font.Font(self.font_name, size) 
        text_surface = font.render(str(text), True, color) 
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surf.blit(text_surface, text_rect)

editor = Editor()
editor.menu.run_menu()