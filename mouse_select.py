import pygame as py
import json
from os import path
from pygame.locals import *
from settings import *

class Spritesheet_croper:

    def __init__(self, editor):
        self.running = False
        self.e = editor

        self.cropped_imgs = []
        self.cropped_imgs_pos = {"positions": []}

        self.init_mx, self.init_my = 0, 0
        self.end_mx, self.end_my = 0, 0
        self.clicking = False
        self.right_clicking = False
        self.cropping = False
        

    def load_sheet(self, file):
        self.WIDTH = file.get_width()
        self.HEIGHT = file.get_height()
        # Redda þessari línu... 
        # passa að hafa alpha gildi þegar crop fallið er notað
        self.tile_img = py.transform.scale(file, (self.WIDTH*SCALE, self.HEIGHT*SCALE))
        self.unscaled_img = file

    def croper_events(self):
        for e in py.event.get():
            if e.type == py.QUIT:
                self.running = False
                self.e.running = False

            if e.type == py.KEYDOWN:
                if e.key == py.K_g:
                    grid_is_on = not grid_is_on

                if e.key == py.K_c:
                    self.cropping = not self.cropping

                if e.key == py.K_q:
                    self.running = False
                    self.e.running = False
                if e.key == py.K_ESCAPE:
                    self.running = False
                    self.e.menu.run_menu()
                if e.key == py.K_s: #and e.key == py.K_LCTRL:
                    self.save_img_sheet()

            if e.type == py.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.clicking = True
                    self.init_mx, self.init_my = e.pos[0]//SCALE, e.pos[1]//SCALE
                if e.button == 3:
                    self.right_clicking = True
            elif e.type == py.MOUSEBUTTONUP:
                if e.button == 1:
                    self.clicking = False
                    self.end_mx, self.end_my = e.pos[0]//SCALE, e.pos[1]//SCALE

                    # Þarft að halda inni hægri takka músarinnar 
                    # áður en maður sleppir vinstri
                    if self.right_clicking or self.cropping:  
                        self.crop()
                        print(self.cropped_imgs)
                        self.right_clicking = False


    def draw_croper(self):
        self.e.screen.blit(self.tile_img, (0,0))

        self.e.draw_text(self.e.screen, (self.mx, self.my), 25, WHITE, self.WIDTH-50, 50)
        self.e.draw_text(self.e.screen, (self.init_mx, self.init_my, self.end_mx, self.end_my), 25, WHITE, self.WIDTH-50, 100)
        self.select_box()
    

    def run(self, file):
        # Þarf að breyta þessu. betra að hlaða inn myndum við fyrsta tilvik klasans
        self.load_sheet(file) 
        self.running = True
        screen = py.display.set_mode
        self.e.screen = screen((self.WIDTH*SCALE, self.HEIGHT*SCALE))

        while self.running:
            self.mx, self.my = py.mouse.get_pos() 
            self.mx, self.my = self.mx//SCALE, self.my//SCALE
            
            # events
            self.croper_events()

            # Draw
            self.e.draw(self.e.screen, self.draw_croper)


    def select_box(self):
        if self.clicking:
            start_x = self.init_mx
            start_y = self.init_my
            current_x = self.mx
            current_y = self.my
            width = abs(current_x*SCALE - start_x*SCALE) + SCALE
            height = abs(current_y*SCALE - start_y*SCALE) + SCALE
            box = py.Rect(start_x*SCALE, start_y*SCALE, width, height)
            py.draw.rect(self.e.screen, BLUE, box, 2)
            self.e.draw_text(self.e.screen, str((width//SCALE, height//SCALE)), 25, BLUE, 45, 150)
        
    def crop(self):
        w = self.end_mx - self.init_mx+1 # remember to fix
        h = self.end_my - self.init_my+1 # 
        start_x = self.init_mx
        start_y = self.init_my

        image = py.Surface((w, h), py.SRCALPHA)
        
        # **** Ein leið *********
        #cropped_region = self.unscaled_img.subsurface((start_x, start_y, w, h))
        #image.blit(cropped_region, (0,0))
        
        # *********** Önnur leið ***********
        image.blit(self.unscaled_img, (0,0), (start_x, start_y, w, h))
        self.cropped_imgs.append(image)
        
    
    def save_img_sheet(self):
        blank_img = py.Surface((IMG_SHEET_W, IMG_SHEET_H))
        blank_img.fill(GRAY)
        x, y = 2,3

        for cr_img in self.cropped_imgs:
            blank_img.blit(cr_img, (x, y))

            img_length = cr_img.get_width()
            img_height = cr_img.get_height()
            self.cropped_imgs_pos["positions"].append([x, y, img_length, img_height])

            if x + img_length > 120:
                x = 2
                y = 3 + img_height+3
            else:
                x+= img_length+2
            

        
        # save the img via personal name of file
        dir_to_save = self.e.own_tile_img_dir
        file_name = input("Skrifaðu heitið á skránni þinni: ")
        file_path = f"{dir_to_save}\\{file_name}"
        py.image.save(blank_img, f"{file_path}.png")

        with open(f"{file_path}.json", 'w') as json_file:
            json.dump(self.cropped_imgs_pos, json_file)