import pygame as py
from os import path
from settings import *
from menu import Menu
from mouse_select import Spritesheet_croper

class Editor:

    def __init__(self):
        py.init()
        self.clock = py.time.Clock()
        self.screen = py.display.set_mode((menu_width, menu_height))
        self.running = True
        self.load_data()

        self.font_name = py.font.match_font("arial")
        self.menu = Menu(self)
        self.sprite_croper = Spritesheet_croper(self)
        self.menu.run_menu()
    
    def load_data(self):
        
        main_dir = path.dirname(__file__)
        tiles_img_dir = path.join(main_dir, "tiles_img")
        deco_img_dir = path.join(main_dir, "deco_img")

        # Spritesheet Croper data
        self.grass_tileset = py.image.load(path.join(tiles_img_dir, "GrassTiles.png")).convert_alpha()
        self.sky_tileset = py.image.load(path.join(tiles_img_dir, "Tileset.png")).convert_alpha()

    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
    
    def draw(self, surf, draw_method): # potentially possible to use kwargs here
        surf.fill(BLACK)
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

py.quit()