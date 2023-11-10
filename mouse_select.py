import pygame as py
from pygame.locals import *
from settings import *

class Spritesheet_croper:

    def __init__(self, editor):
        self.running = False
        self.editor = editor

        self.init_mx, self.init_my = 0, 0
        self.end_mx, self.end_my = 0, 0
        self.clicking = False
        
        self.load_sheet()

    def load_sheet(self):
        self.WIDTH = self.editor.grass_tile_img.get_width()
        self.HEIGHT = self.editor.grass_tile_img.get_height()
        self.tile_img = py.transform.scale(self.editor.grass_tile_img, (self.WIDTH*SCALE, self.HEIGHT*SCALE))

    def croper_events(self):
        for e in py.event.get():
            if e.type == py.QUIT:
                self.running = False
                self.editor.running = False

            if e.type == py.KEYDOWN:
                if e.key == py.K_g:
                    grid_is_on = not grid_is_on
                if e.key == py.K_q:
                    self.running = False
                    self.editor.running = False
                if e.key == py.K_ESCAPE:
                    self.running = False
                    self.editor.menu.run_menu()

            if e.type == py.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.clicking = True
                    self.init_mx, self.init_my = e.pos[0]//SCALE, e.pos[1]//SCALE
            elif e.type == py.MOUSEBUTTONUP:
                if e.button == 1:
                    self.clicking = False
                    self.end_mx, self.end_my = e.pos[0]//SCALE, e.pos[1]//SCALE

    def draw_croper(self):
        self.editor.screen.blit(self.tile_img, (0,0))

        self.editor.draw_text(self.editor.screen, (self.mx, self.my), 25, WHITE, self.WIDTH-50, 50)
        self.editor.draw_text(self.editor.screen, (self.init_mx, self.init_my, self.end_mx, self.end_my), 25, WHITE, self.WIDTH-50, 100)
        self.select_box()


    def run_croper(self):
        self.running = True
        self.editor.screen = py.display.set_mode((self.WIDTH*SCALE, self.HEIGHT*SCALE))

        while self.running:
            self.mx, self.my = py.mouse.get_pos() 
            self.mx, self.my = self.mx//SCALE, self.my//SCALE
            
            # events
            self.croper_events()

            # Draw
            self.editor.draw(self.draw_croper)


    def select_box(self):
        if self.clicking:
            start_x = self.init_mx
            start_y = self.init_my
            current_x = self.mx
            current_y = self.my
            width = abs(current_x*SCALE - start_x*SCALE) + SCALE
            height = abs(current_y*SCALE - start_y*SCALE) + SCALE
            box = py.Rect(start_x*SCALE, start_y*SCALE, width, height)
            py.draw.rect(self.editor.screen, BLUE, box, 1)
            self.editor.draw_text(self.editor.screen, str((width//SCALE, height//SCALE)), 25, BLUE, 45, 150)