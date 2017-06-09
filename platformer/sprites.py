import pygame as pg
from settings import *
from random import uniform,randint,choice,random
from tilemap import collide_hit_rect,collide_hit_rect_bis
from os import path
import pytweening as tween
vec = pg.math.Vector2


def collide_with_walls(sprite,group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print("hit the wall x")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print("hit the wall y")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_with_walls_delete(sprite,group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print(hits)
            sprite.kill()
            print("hit the wall x")
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print(hits)
            sprite.kill()
            print("hit the wall y")


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                dir = vec(1,0).rotate(-self.rot)
                Bullet(self.game,pos,dir)
                choice(self.game.weapons_sounds['gun']).play()
                MuzzleFlash(self.game,pos)


    def collide_with_collectable(self):
        hits = pg.sprite.spritecollide(self, self.game.collectable, True,collide_hit_rect)
        if hits:
            print("white collected")
            print(len(hits))

    def add_health(self,amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self,self.game.walls,'y')
        self.collide_with_collectable()
        self.rect.center = self.hit_rect.center

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image =  pg.image.load(path.join(img_folder,WALL_IMG)).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self._layer = WALL_LAYER
        self.groups =  game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y



class Collectable(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.groups = game.all_sprites, game.collectable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image =  pg.image.load(path.join(img_folder,COLLECTABLE)).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mobs(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        self._layer = MOB_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image =  game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.target = game.player

    def draw_health(self):
        if self.health > 60:
            col = BGREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0,0,width, 10)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image,col,self.health_bar)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS:
                    self.acc += dist.normalize()


    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = (target_dist).angle_to(vec(1,0))
            self.rect = self.image.get_rect()
            self.acc = vec(1,0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(MOB_SPEED)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self,self.game.walls,'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self,self.game.walls,'y')
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            choice(self.game.zombie_hit_sounds).play()
            self.game.map_img.blit(self.game.splat_green,self.pos - vec(32,32))

class Bullet(pg.sprite.Sprite):
        def __init__(self, game, pos, dir):
                game_folder = path.dirname(__file__)
                img_folder = path.join(game_folder, 'img')
                self._layer = BULLET_LAYER
                self.groups = game.all_sprites, game.bullets
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.baseimage = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
                self.image = self.baseimage
                self.pos = vec(pos)
                self.rect = self.image.get_rect()
                self.rect.center = pos
                self.hit_rect = BULLET_HIT_RECT.copy()
                self.hit_rect.center = self.rect.center
                spread = uniform(-GUN_SPREAD,GUN_SPREAD)
                self.vel = dir.rotate(spread) * BULLET_SPEED
                self.spawn_time = pg.time.get_ticks()
                self.ignored = 0

        def update(self):
                self.pos += self.vel * self.game.dt
                self.hit_rect.centerx = self.pos.x
                collide_with_walls_delete(self,self.game.walls,'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls_delete(self, self.game.walls, 'y')
                self.rect.center = self.hit_rect.center
                if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
                    self.kill()


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self,game,pos):
        self.groups = game.all_sprites
        self._layer = EFFECTS_LAYER
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        size = randint(20,50)
        self.image = pg.transform.scale(choice(game.gun_flashes),(size,size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class Item(pg.sprite.Sprite):
    def __init__(self,game,pos,type):
        self.groups = game.all_sprites,game.items
        self._layer = ITEMS_LAYER
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
