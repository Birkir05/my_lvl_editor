import pygame as py
from settings import *


""
class Lvl_maker:

    def __init__(self, editor):
        self.e = editor
        self.running = False

        self.clicked = False
        self.right_clicking = False
        self.rect_selected = False
        self.selected_tile = 0

        self.camera = Camera(self)
        self.chunk = Chunk_system(self)

    def load_maker(self, file):
        self.tile_sheet = file[0]
        self.tile_img = py.transform.scale(self.tile_sheet, (IMG_SHEET_W*4, IMG_SHEET_H*4))
        self.tile_positions = file[1]
        self.rect_objects()

        # Gets all tile images from personal sprite_sheet
        # in same index order as self.tile_positions
        self.tile_images = [self.e.get_image(self.tile_sheet, p[0], p[1], p[2], p[3])
                             for p in self.tile_positions]

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

        self.visible_chunks = self.chunk.get_current_chunks()

        if self.within_tile_sheet():
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(self.mx, self.my):
                    if self.clicked:
                        print("click")
                        self.rect_selected = True
                        self.selected_tile = self.select_rect(i)

        elif not self.within_tile_sheet():
            if self.clicked:
                if self.rect_selected:
                    cr_chunk_and_tile = self.get_pos_chunk_and_tile()
                    self.place_or_delete(cr_chunk_and_tile)

    def within_tile_sheet(self):
        return self.tile_sheet_rect.collidepoint(self.mx, self.my)

    def draw(self):
        screen = self.e.screen
        
        self.chunk.render(self.visible_chunks)

        screen.blit(self.tile_sheet_surf, (LVL_E_W*0.75, 0))

        if self.rect_selected:
            screen.blit(self.selected_tile[1], (self.mx, self.my))
    
    def rect_objects(self):
        self.tile_sheet_surf = py.Surface((IMG_SHEET_W*4, IMG_SHEET_H*4))
        self.tile_sheet_surf.blit(self.tile_img, (0,0))

        self.tile_sheet_rect = py.Rect(LVL_E_W*0.75, 0, IMG_SHEET_W*4, IMG_SHEET_H*4)

        self.rects=[py.Rect(p[0]*4,p[1]*4,p[2]*4,p[3]*4) for p in self.tile_positions]

        for x in self.rects:
            py.draw.rect(self.tile_sheet_surf, BLUE, x, 1)

        self.rects=[rect.move(int(LVL_E_W*0.75), 0) for rect in self.rects]


    def select_rect(self, index_of_rect):
        selected_tile = py.transform.scale(self.tile_images[index_of_rect], (48, 48))
        return index_of_rect, selected_tile

    def get_pos_chunk_and_tile(self):
        scroll = self.camera.scroll

        curr_chunk_x = (self.mx - scroll[0]) // 384  # Hver upscaled chunk er 384x384
        curr_chunk_y = (self.my - scroll[1]) // 384

        # How much the mouse has traveled into the current chunk
        travel_dist_x = (self.mx - (curr_chunk_x*384))/6 # þar sem hver chunk var stækkaður um 6x
        travel_dist_y = (self.my - (curr_chunk_y*384))/6 # vegna (320x180) pixel resolution
        
        # Current tile within the current chunk
        curr_tile_x = travel_dist_x // 8 # Hver unscaled chunk er 64x64
        curr_tile_y = travel_dist_y // 8 
        
        print(self.chunk.level_map)
        return curr_tile_x, curr_tile_y, curr_chunk_x, curr_chunk_y
    
    def place_or_delete(self, pos):
        tile_x = pos[0]
        tile_y = pos[1]

        i_cr_tile_in_chunk = int(tile_x + tile_y*8) # one dimensional array

        chunk_x = pos[2]
        chunk_y = pos[3]

        chunk_key = f"{chunk_x};{chunk_y}"
        cr_chunk_data = self.chunk.level_map[chunk_key]

        tile_type = self.selected_tile[0]
        cr_chunk_data[i_cr_tile_in_chunk][1] = tile_type


class Chunk_system:
    def __init__(self, level_data):
        self.level_data = level_data
        self.level_map = {}
        self.load_data()
        
    def load_data(self):
        self.grid_img = self.level_data.e.chunk_grid
        self.scroll = self.level_data.camera.scroll
        self.screen = self.level_data.e.screen
    
    def generate_chunk(self):
        tile_type = 0
        chunk_data = []
        #chunk_x = chunk_pos[0]
        #chunk_y = chunk_pos[1]
        for y_pos in range(CHUNK_SIZE): 
            for x_pos in range(CHUNK_SIZE): 
                #target_x = chunk_x*CHUNK_SIZE + x_pos
                #target_y = chunk_y*CHUNK_SIZE + y_pos

                # real position of each tile on the level map
                # added real pos of tile and the type (air)
                chunk_data.append([[x_pos, y_pos], tile_type])

                #chunk_data.append([[target_x, target_y], tile_type])
        
        return chunk_data
        
    def get_current_chunks(self):
        visible_chunks = []
        vertical_chunks = 3 # Það komast 3 chunks lóðrétt á skjáinn (180 pixlar)
        horizontal_chunks = 5 # Það komast 5 chunks lárétt á skjáinn (320 pixlar)
        for y in range(vertical_chunks):
            for x in range(horizontal_chunks):
                target_x = x + int(self.scroll[0]/(CHUNK_SIZE*TILE_SIZE))
                target_y = y + int(self.scroll[1]/(CHUNK_SIZE*TILE_SIZE))
                target_chunk = f"{target_x};{target_y}" # pos of chunk

                # add an empty chunk to level map if it doesnt exist already.
                if target_chunk not in self.level_map:
                    self.level_map[target_chunk] = self.generate_chunk()
                # adds current chunk that is visible on screen
                visible_chunks.append([target_x, target_y])

        return visible_chunks # This variable goes into render method

    def render(self, chunks_pos):
        screen_surf = py.Surface((EDITOR_W, EDITOR_H)) # (320x180) pixlar
        chunk_height = CHUNK_SIZE*TILE_SIZE
        chunk_width = CHUNK_SIZE*TILE_SIZE

        for chunk_x, chunk_y in chunks_pos:
            chunk_key = f"{chunk_x};{chunk_y}"
            chunk_x = chunk_x*384 # maybe clearer to call this variable true_chunk_x
            chunk_y = chunk_y*384
            chunk_surf = py.Surface((chunk_width, chunk_height)) # (64x64) 
            deco_chunk_surf = py.Surface((chunk_width, chunk_height)) # VANTAR py.SRCALPHA ??
            tile_chunk_surf = py.Surface((chunk_width, chunk_height))
            for tile in self.level_map[chunk_key]:

                # destination of tile on current chunk
                tile_destination = tile[0][0]*TILE_SIZE-self.scroll[0], tile[0][1]*TILE_SIZE-self.scroll[1]

                if tile[1] > 0: # ef það er tile (þá á líka er það líka sprite)
                    tile_chunk_surf.blit(self.level_data.tile_images[tile[1]], tile_destination)
                elif tile[1] < 0: # ef það er decoration (f.e. tree)
                    deco_chunk_surf.blit(self.level_data.tile_images[tile[1]], tile_destination)

                chunk_surf.blit(deco_chunk_surf, (0,0))
                chunk_surf.blit(tile_chunk_surf, (0,0))
            
            chunk_surf = py.transform.scale(chunk_surf, (384, 384))

            ###---------- LAGA HÉRNA ----------####
            self.screen.blit(chunk_surf, (chunk_x, chunk_y))
            self.screen.blit(self.grid_img, (chunk_x, chunk_y))
                    


class Camera:
    def __init__(self, level_data):
        self.level_data = level_data
        self.scroll = [0,0]

    def pan(self):
        pass

    def zoom(self):
        pass 