import pygame as py
from os import path
from pygame.locals import *
#from main_script import *
from settings import *

py.init()
font_name = py.font.match_font("arial")
init_mx, init_my = 0, 0
end_mx, end_my = 0, 0

def draw_text(surf, text, size, color, x, y):
    font = py.font.Font(font_name, size) 
    text_surface = font.render(str(text), True, color) 
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x,y)
    surf.blit(text_surface, text_rect)

def draw_grid():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            py.draw.line(screen, GRAY, (x*SCALE,y*SCALE), (x*SCALE, HEIGHT*SCALE))
            py.draw.line(screen, GRAY, (x*SCALE,y*SCALE), (WIDTH*SCALE, y*SCALE))
grid_is_on = False

def select_box(surf, color, start_pos, current_pos, is_clicking):
    if is_clicking:
        start_x = start_pos[0]
        start_y = start_pos[1]
        current_x = current_pos[0]
        current_y = current_pos[1]
        width = abs(current_x*SCALE - start_x*SCALE) + SCALE
        height = abs(current_y*SCALE - start_y*SCALE) + SCALE
        box = py.Rect(start_x*SCALE, start_y*SCALE, width, height)
        py.draw.rect(surf, color, box, 1)
        draw_text(surf, str((width//SCALE, height//SCALE)), 25, color, 45, 150)


main_dir = path.dirname(__file__)
img_dir = path.join(main_dir, "tiles_img")


grass_tile_img = py.image.load(path.join(img_dir, "GrassTiles.png"))
WIDTH = grass_tile_img.get_width()
HEIGHT = grass_tile_img.get_height()
grass_tile_img = py.transform.scale(grass_tile_img, (WIDTH*SCALE, HEIGHT*SCALE))

clock = py.time.Clock()
FPS = 60
screen = py.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE)) #py.FULLSCREEN|py.SCALED

clicking = False
running = True

while running:
    mx, my = py.mouse.get_pos()
    mx, my = mx//SCALE, my//SCALE

    for e in py.event.get():
        if e.type == py.QUIT:
            running = False
        if e.type == py.KEYDOWN:
            if e.key == py.K_g:
                grid_is_on = not grid_is_on
            if e.key == py.K_q:
                running = False
        if e.type == py.MOUSEBUTTONDOWN:
            if e.button == 1:
                clicking = True
                init_mx, init_my = e.pos[0]//SCALE, e.pos[1]//SCALE
        elif e.type == py.MOUSEBUTTONUP:
            if e.button == 1:
                clicking = False
                end_mx, end_my = e.pos[0]//SCALE, e.pos[1]//SCALE
                
    
    screen.fill(BLACK)
    screen.blit(grass_tile_img, (0,0))

    if grid_is_on:
        draw_grid()
    draw_text(screen, (mx, my), 25, WHITE, WIDTH-50, 50)
    draw_text(screen, (init_mx, init_my, end_mx, end_my), 25, WHITE, WIDTH-50, 100)
    select_box(screen, BLUE, [init_mx, init_my], [mx, my], clicking)

    clock.tick(FPS)
    py.display.flip()
    
    