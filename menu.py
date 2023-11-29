import pygame as py 
from settings import *
from mouse_select import Spritesheet_croper
class Menu:
    def __init__(self, editor):
        self.e = editor
        self.active = False
        self.current_menu = "LvL Editor"

        self.main_opts = ["LvL Editor", 
                          "Spritesheet croper", 
                          "Spritesheet combiner", 
                          "Spritesheet view", 
                          "Quit"]
        
        # fyrir framtíð
        self.submenu_opts = [list(self.e.lvl_maker_data.keys()), 
                             list(self.e.croper_data.keys()),
                             0, 
                             0,]

        self.entered = False
        self.submenu_entered = False

        self.curr_mainopt = 0
        self.curr_subopt = 0

        self.opt_posx = menu_width//2 - 80
        self.opt_posy = 60


    def menu_events(self):
        self.entered = False
        for event in py.event.get():
            if event.type == py.QUIT:
                self.active = False
                self.e.running = False

            if event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    move = -1
                    self.moving_selection(move)
                elif event.key == py.K_DOWN:
                    move = 1
                    self.moving_selection(move)
                if event.key == py.K_ESCAPE:
                    self.submenu_entered = not self.submenu_entered
                    self.curr_subopt = 0
                if event.key == py.K_RETURN:
                    self.current_submenu = self.submenu_opts[self.curr_mainopt]
                    self.entered = True


    def main_menu(self):
        separation = 60
        self.opt_pos = [self.opt_posx, self.opt_posy*self.curr_mainopt+60]
        for i, opt in enumerate(self.main_opts):
            self.e.draw_text(self.e.screen, opt, 25, WHITE, menu_width//2-60, i*separation+60)

        self.select_sheet_to_use()
        self.open_submenu()

        self.e.draw_text(self.e.screen, ">", 22, ORANGE, self.opt_pos[0], self.opt_pos[1])

    def select_sheet_to_use(self):
        if self.submenu_entered and self.entered:
            self.active = False

            if self.current_menu == "Spritesheet croper":
                file = self.e.croper_data[self.curr_sheet]
                self.e.sprite_croper.run(file)
            elif self.current_menu == "LvL Editor":
                file = self.e.lvl_maker_data[self.curr_sheet]
                self.e.lvl_maker.run(file, self.curr_sheet)

        if self.entered:
            self.submenu_entered = not self.submenu_entered
    
    def open_submenu(self):
        if self.submenu_entered:
            self.curr_sheet = self.current_submenu[self.curr_subopt]
            self.e.draw_text(self.e.screen, self.curr_sheet, 25, DARK_BLUE, menu_width//2+130, (self.curr_mainopt + 1)*60)

    def run_menu(self):
        screen = py.display.set_mode
        self.e.screen = screen((menu_width, menu_height))
        self.active = True

        while self.active:
            self.menu_events()

            self.e.draw(self.e.screen, self.main_menu)

    def moving_selection(self, move_amont):
        if self.submenu_entered:
            self.curr_subopt = (self.curr_subopt+move_amont) % len(self.current_submenu)
        else:
            self.curr_mainopt = (self.curr_mainopt+move_amont) % len(self.main_opts)
            self.current_menu = self.main_opts[self.curr_mainopt]