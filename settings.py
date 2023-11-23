menu_width, menu_height = 700, 800

LVL_E_W, LVL_E_H = 1920, 1080

EDITOR_W, EDITOR_H = 320, 180
# dimensions for box around edit area 3/4 of 1920 and 1080
EDITOR_BOX_Y, EDITOR_BOX_X = 320 * 0.75, 180 * 0.75

TILE_SIZE = 8
TILE_Y = EDITOR_H//TILE_SIZE
TILE_X = EDITOR_W//TILE_SIZE

# unscaled dimension for saving own spritesheet 
# 120 * 135
IMG_SHEET_W, IMG_SHEET_H = LVL_E_W//16, LVL_E_H//8


WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 128, 128)
ORANGE = (255, 127, 39)

FPS = 10

SCALE = 8