import pygame as py
import json
from os import path
from settings import *
from menu import Menu
from mouse_select import Spritesheet_croper
from lvl_constructor import Lvl_maker

class Editor:

    def __init__(self):
        py.init()
        self.clock = py.time.Clock()
        self.screen = py.display.set_mode((menu_width, menu_height))
        self.running = True
        self.trans_color = GRAY
        self.load_data()

        self.font_name = py.font.match_font("arial")
        self.menu = Menu(self)
        self.sprite_croper = Spritesheet_croper(self)
        self.lvl_maker = Lvl_maker(self)
        self.menu.run_menu()
    
    def load_data(self):
        
        self.main_dir = path.dirname(__file__)
        self.croper_tiles_img_dir = path.join(self.main_dir, "crop_tiles_img")
        self.croper_deco_img_dir = path.join(self.main_dir, "crop_deco_img")

        self.own_tile_img_dir = path.join(self.main_dir, "tile_img")
        self.own_deco_img_dir = path.join(self.main_dir, "deco_img")

        # Spritesheet Croper data
        self.croper_data = {
            "GrassTiles": py.image.load(path.join(self.croper_tiles_img_dir, "GrassTiles.png")).convert_alpha(),
            "Skytile": py.image.load(path.join(self.croper_tiles_img_dir, "Tileset.png")).convert_alpha()
        }

        # data for level editor
        self.chunk_grid = py.image.load("chunk_grid.png").convert()
        self.chunk_grid.set_colorkey(BLACK)
        personal_sheets = ["gras", "virkar"]
        self.lvl_maker_data = {}

        for sheet in personal_sheets:
            img=py.image.load(path.join(self.own_tile_img_dir, f"{sheet}.png")).convert() # Athuga hér
            img.set_colorkey(self.trans_color)

            file = f"{self.own_tile_img_dir}\\{sheet}"
            with open(f"{file}.json", "r") as json_file:
                positions_data = json.load(json_file)
            positions_list = positions_data["positions"]

            self.lvl_maker_data[f"{sheet}"] = [img, positions_list]


    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
    
    def draw(self, surf, draw_method): # potentially possible to use kwargs here
        
        surf.fill(BLACK)
        draw_method()
        py.display.flip()

        self.clock.tick(FPS)

    def draw_text(self, surf, text, size, color, x, y):
        font = py.font.Font(self.font_name, size) 
        text_surface = font.render(str(text), True, color) 
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surf.blit(text_surface, text_rect)
    
    def get_image(self, spritesheet, x, y, w, h):
        image = py.Surface((w, h), py.SRCALPHA) # Tómur strigi
        # Lita hluta af spritesheet á strigann
        image.blit(spritesheet, (0, 0), (x, y, w, h))
        return image    # skila striga

editor = Editor()
editor.menu.run_menu()

py.quit()