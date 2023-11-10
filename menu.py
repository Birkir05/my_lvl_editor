import pygame as py 
from settings import *
from mouse_select import Spritesheet_croper
class Menu:
    def __init__(self, editor):
        self.editor = editor
        self.active = False
        self.current_menu = "Lvl Editor"

        self.main_opts = ["LvL Editor", 
                          "Spritesheet croper", 
                          "Spritesheet combiner", 
                          "Spritesheet view", 
                          "Quit"]
        
        self.current_opt = 0
        self.opt_posx = menu_width//2 - 80
        self.opt_posy = 60


    def menu_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.active = False
                self.editor.running = False

            if event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    move = -1
                    self.moving_selection(move)
                elif event.key == py.K_DOWN:
                    move = 1
                    self.moving_selection(move)
                if event.key == py.K_RETURN:
                    if self.current_opt == 1:
                        self.active = False
                        self.editor.sprite_croper.run_croper()
                
    def main_menu(self):
        separation = 60
        for i, opt in enumerate(self.main_opts):
            self.editor.draw_text(self.screen, opt, 25, WHITE, menu_width//2-60, i*separation+60)
        self.editor.draw_text(self.screen, ">", 22, ORANGE, self.opt_posx, self.opt_posy*self.current_opt+60)
        
    def run_menu(self):
        self.active = True
        self.screen = self.editor.screen((menu_width, menu_height))

        while self.active:
            self.menu_events()

            self.editor.draw(self.screen, self.main_menu)

    def moving_selection(self, move_amont):
        self.current_opt = (self.current_opt+move_amont) % len(self.main_opts)