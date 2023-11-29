import pygame as py
from settings import *


""
class Lvl_maker:

    def __init__(self, editor):
        self.e = editor
        self.running = False

        self.clicked = False
        self.clicking = False
        self.right_clicking = False
        self.middle_click = False
        self.rect_selected = False
        self.delete_is_active = False
        self.selected_tile = 0

        self.all_tile_types = {}
        self.all_tile_imgs = {}

        # save all tiles individually and there types
        sheet_data = self.e.lvl_maker_data
        current_type = 0
        for sheet_name in sheet_data.keys():
            tile_sheet = sheet_data[sheet_name][0]
            position_list = sheet_data[sheet_name][1]
            
            tile_types = tuple(type for type in range(current_type+1, len(position_list)+current_type+1))
            current_type += len(position_list)

            self.all_tile_types[tile_types] = sheet_name

            tile_imgs = [self.e.get_image(tile_sheet, p[0], p[1], p[2], p[3])
                             for p in position_list]
            
            self.all_tile_imgs[sheet_name] = tile_imgs

        print(self.all_tile_types)

        self.camera = Camera(self)
        self.chunk = Chunk_system(self)

    def load_maker(self, file, sheet_name):
        self.current_sheet = sheet_name
        self.tile_sheet = file[0]
        self.tile_img = py.transform.scale(self.tile_sheet, (IMG_SHEET_W*4, IMG_SHEET_H*4))
        self.tile_positions = file[1]
        self.rect_objects()


    #def load_maker(self, file):
    #    self.tile_sheet = file[0]
    #    self.tile_img = py.transform.scale(self.tile_sheet, (IMG_SHEET_W*4, IMG_SHEET_H*4))
    #    self.tile_positions = file[1]
    #    self.rect_objects()

    #    # Gets all tile images from personal sprite_sheet
    #    # in same index order as self.tile_positions
    #    self.tile_images = [self.e.get_image(self.tile_sheet, p[0], p[1], p[2], p[3])
    #                         for p in self.tile_positions]

        
    def run(self, file, selected_sheet):
        self.load_maker(file, selected_sheet)

        self.running = True 
        screen = py.display.set_mode
        self.e.screen = screen((LVL_E_W, LVL_E_H))
        
        while self.running:
            self.events()

            self.update()

            self.e.draw(self.e.screen, self.draw)

    def events(self):
        self.clicked = False
        self.middle_click = False
        for e in py.event.get():
            if e.type == py.QUIT:
                self.running = False
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    self.running = False
                    self.e.menu.run_menu()
                if e.key == py.K_d:
                    self.delete_is_active = True
                    self.rect_selected = False
                if e.key == py.K_s:
                    self.save_lvl()

            if e.type == py.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.clicking = True
                    self.clicked = True
                if e.button == 2:
                    self.middle_click = True
                    
                if e.button == 3:
                    self.right_clicking = True
            elif e.type == py.MOUSEBUTTONUP:
                if e.button == 1:
                    self.clicking = False
                
        
    def update(self):
        self.mx, self.my = py.mouse.get_pos()

        self.visible_chunks = self.chunk.get_current_chunks()

        if self.within_tile_sheet():

            if self.clicked:
                self.selected_tile = self.select_rect()

            #for i, rect in enumerate(self.rects): 
            #    if rect.collidepoint(self.mx, self.my):
            #        if self.clicked:
            #            self.rect_selected = True
            #            self.selected_tile = self.select_rect(i)

        elif not self.within_tile_sheet():
            if self.clicking:
                if self.rect_selected:
                    cr_chunk_and_tile = self.get_pos_chunk_and_tile()
                    self.place(cr_chunk_and_tile)
                elif self.delete_is_active:
                    cr_chunk_and_tile = self.get_pos_chunk_and_tile()
                    self.delete(cr_chunk_and_tile)

            elif self.middle_click:
                cr_chunk_and_tile = self.get_pos_chunk_and_tile()
                #self.selected_tile[0] = cr_chunk_and_tile[]
                #self.selected_tile[1] = 

    def within_tile_sheet(self):
        return self.tile_sheet_rect.collidepoint(self.mx, self.my)

    def draw(self):
        screen = self.e.screen
        
        self.chunk.render(self.visible_chunks)

        screen.blit(self.tile_sheet_surf, (LVL_E_W*0.75, 0))
    
    def rect_objects(self):
        self.tile_sheet_surf = py.Surface((IMG_SHEET_W*4, IMG_SHEET_H*4))
        self.tile_sheet_surf.blit(self.tile_img, (0,0))

        self.tile_sheet_rect = py.Rect(LVL_E_W*0.75, 0, IMG_SHEET_W*4, IMG_SHEET_H*4)

        self.rects=[py.Rect(p[0]*4,p[1]*4,p[2]*4,p[3]*4) for p in self.tile_positions]

        # Testing purpose
        for x in self.rects:
            py.draw.rect(self.tile_sheet_surf, BLUE, x, 1)

        self.rects=[rect.move(int(LVL_E_W*0.75), 0) for rect in self.rects]


    def select_rect(self):
        
        current_tile_type = [types[0] for types, sheet in self.all_tile_types.items()
                             if sheet == self.current_sheet]

        for i, rect in enumerate(self.rects): 
            if rect.collidepoint(self.mx, self.my):
                self.rect_selected = True

                tile_imgs = self.all_tile_imgs[self.current_sheet]
                
                selected_tile = py.transform.scale(tile_imgs[i], (48, 48))

                return i+current_tile_type[0], selected_tile

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
        
        return curr_tile_x, curr_tile_y, curr_chunk_x, curr_chunk_y
    
    def place(self, pos):
        
        tile_x = pos[0]
        tile_y = pos[1]

        i_cr_tile_in_chunk = int(tile_x + tile_y*8) # one dimensional array

        chunk_x = pos[2]
        chunk_y = pos[3]

        chunk_key = f"{chunk_x};{chunk_y}"
        cr_chunk_data = self.chunk.level_map[chunk_key]

        tile_type = self.selected_tile[0] # til þess að greina frá lofti (sem er 0)
        cr_chunk_data[i_cr_tile_in_chunk][1] = tile_type
    
    def delete(self, pos):

        tile_x = pos[0]
        tile_y = pos[1]
        
        i_cr_tile_in_chunk = int(tile_x + tile_y*8)

        chunk_x = pos[2]
        chunk_y = pos[3]

        chunk_key = f"{chunk_x};{chunk_y}"
        cr_chunk_data = self.chunk.level_map[chunk_key]

        tile_type = 0
        cr_chunk_data[i_cr_tile_in_chunk][1] = tile_type

    def save_lvl(self):
        pass
    
class Chunk_system:
    def __init__(self, level_data):
        self.level_data = level_data
        self.level_map = {}

        self.retrieve_data()
        
    def retrieve_data(self):
        self.grid_img = self.level_data.e.chunk_grid
        self.scroll = self.level_data.camera.scroll
        self.screen = self.level_data.e.screen
    
        self.all_tile_types = self.level_data.all_tile_types
        self.all_tile_imgs = self.level_data.all_tile_imgs
    
    def get_category(self, tile_type):
        for tile_types in self.all_tile_types.keys():
            if tile_type in tile_types:

                key_to_sheet = tile_types
                index_of_img = tile_types.index(tile_type)

                return self.all_tile_types[key_to_sheet], index_of_img # this is the sheet string

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
                tile_type = tile[1]
                

                # destination of tile on current chunk
                tile_destination = tile[0][0]*TILE_SIZE-self.scroll[0], tile[0][1]*TILE_SIZE-self.scroll[1]

                if tile_type > 0: # ef það er tile (þá á líka er það líka sprite)
                    sheet_type, index_of_img = self.get_category(tile_type)

                    tile_chunk_surf.blit(self.all_tile_imgs[sheet_type][index_of_img], tile_destination) # -1 to compensate right index in saved images
                elif tile_type < 0: # ef það er decoration (f.e. tree)
                    deco_chunk_surf.blit(self.all_tile_imgs[sheet_type][index_of_img], tile_destination)

                chunk_surf.blit(deco_chunk_surf, (0,0))
                chunk_surf.blit(tile_chunk_surf, (0,0))
            
            chunk_surf = py.transform.scale(chunk_surf, (384, 384))

            self.screen.blit(chunk_surf, (chunk_x, chunk_y))
            self.screen.blit(self.grid_img, (chunk_x, chunk_y))
        

    def render_safe(self, chunks_pos):
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
                    tile_chunk_surf.blit(self.level_data.tile_images[tile[1]-1], tile_destination) # -1 to compensate right index in saved images
                elif tile[1] < 0: # ef það er decoration (f.e. tree)
                    deco_chunk_surf.blit(self.level_data.tile_images[tile[1]], tile_destination)

                chunk_surf.blit(deco_chunk_surf, (0,0))
                chunk_surf.blit(tile_chunk_surf, (0,0))
            
            chunk_surf = py.transform.scale(chunk_surf, (384, 384))

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