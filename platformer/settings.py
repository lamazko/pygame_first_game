import pygame as pg
vec = pg.math.Vector2
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (60, 160, 70)
BGREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "testing"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


WALL_IMG = 'tile_69.png'
COLLECTABLE = 'tile_237.png'

# player settings

PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 200 #degré / sec
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(25,10)

#mob settings

MOB_IMG = 'zombie.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 35, 35)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Gun Settings

BULLET_IMG = 'bullet.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BULLET_HIT_RECT = pg.Rect(0,0,6,6)
GUN_SPREAD  = 5
BULLET_DAMAGE = 10

#effects

MUZZLE_FLASHES = ['whitePuff15.png','whitePuff16.png','whitePuff17.png','whitePuff18.png']
FLASH_DURATION = 40

#layers

WALL_LAYER =1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1


#items

ITEM_IMAGES = {'health_pack': 'medical-kit-sprite-1.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 10
BOB_SPEED = 0.3



# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav'}