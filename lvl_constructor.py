import pygame as py
from settings import *

class Lvl_maker:

    def __init__(self, editor):
        self.e = editor
        self.running = False

        self.clicked = False
        self.right_clicking = False
        self.rect_selected = False
        self.chunk = Chunk_system(self)

    def load_maker(self, file):
        tile_sheet = file[0]
        self.tile_img = py.transform.scale(tile_sheet, (IMG_SHEET_W*4, IMG_SHEET_H*4))
        self.tile_positions = file[1]
        self.rect_objects()

    def run(self, file):
        self.load_maker(file)

        self.running = True 
        screen = py.display.set_mode
        self.e.screen = screen((LVL_E_W, LVL_E_H))
        
        while self.running:
            self.events()

            self.update()

            self.e.draw(self.e.screen, self.draw)

    def events(self):
        self.clicked = False
        for e in py.event.get():
            if e.type == py.QUIT:
                self.running = False
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    self.running = False
                    self.e.menu.run_menu()
            if e.type == py.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.clicked = True
                    
                if e.button == 3:
                    self.right_clicking = True
            elif e.type == py.MOUSEBUTTONUP:
                pass
                
        
    def update(self):
        self.mx, self.my = py.mouse.get_pos()
        if self.tile_sheet_rect.collidepoint(self.mx, self.my):
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(self.mx, self.my):
                    print(f"kassi{i}")
                    if self.clicked:
                        self.select_rect(rect)
        
        #else:
            #print(False)

    def draw(self):
        screen = self.e.screen

        screen.blit(self.tile_sheet_surf, (LVL_E_W*0.75, 0))

        if self.rect_selected:
            screen.blit(self.selected_tile, (self.mx, self.my))
    
    def rect_objects(self):
        self.tile_sheet_surf = py.Surface((IMG_SHEET_W*4, IMG_SHEET_H*4))
        self.tile_sheet_surf.blit(self.tile_img, (0,0))

        self.tile_sheet_rect = py.Rect(LVL_E_W*0.75, 0, IMG_SHEET_W*4, IMG_SHEET_H*4)

        self.rects=[py.Rect(p[0]*4,p[1]*4,p[2]*4,p[3]*4) for p in self.tile_positions]

        for x in self.rects:
            py.draw.rect(self.tile_sheet_surf, BLUE, x, 1)

        self.rects=[rect.move(int(LVL_E_W*0.75), 0) for rect in self.rects]


    def select_rect(self, rect_pos):
        x, y = rect_pos[0], rect_pos[1]
        w = rect_pos[2]
        h = rect_pos[3]
        self.selected_tile = py.Surface((w,h), py.SRCALPHA)
        self.selected_tile.blit(self.tile_img, (0,0), (x, y, w, h))

        self.rect_selected = True
        return self.selected_tile


class Chunk_system:
    def __init__(self, level_data):
        self.level_data = level_data
        self.load_data()
        pass

    def load_data(self):
        grid_img = py.image.load(self.myndBjorn)
    

    def generate_chunk(self):
        pass

    def show_current_chunks(self):
        pass

