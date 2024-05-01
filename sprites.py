# This file was created by Milun Kalidindi
# Appreciation to Chris Bradfield
import pygame as pg
from settings import *
from random import randint
from utils import *
from os import path

vec =pg.math.Vector2
# game_folder = path.dirname(__file__)
# img_folder = path.join(game_folder, 'images')

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y


# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        # self.groups = game.all_sprites
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.player_img
        # self.spritesheet = Spritesheet(path.join(img_folder, 'Autobot Symbol.png'))
        # self.load_images()
        # self.image.fill(GREEN)
        # self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE 
        self.y = y * TILESIZE
        self.speed = 300
        self.moneybag = 0
        self.status = ""
        self.hitpoints = 100
        self.pos = vec(0,0)
        self.dir = vec(0,0)
        self.current_frame = 0
        self.last_update = 0
        self.material = True

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Cheese":
                Cheese(self.game, randint(0,30), randint(0,22))
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Potions":
                print(hits[0].__class__.__name__)
                self.speed += 100
            if str(hits[0].__class__.__name__) == "Mob" or str(hits[0].__class__.__name__) == "Mob2":
                print(hits[0].__class__.__name__)
                self.game.new()
                print("Collided with mob")
                self.hitpoints -= 1
            if str(hits[0].__class__.__name__) == "Health":
                print(hits[0].__class__.__name__)
                print("Collided with Health Potion")
                self.hitpoints += 1
            if str(hits[0].__class__.__name__) == "Bush":
                print(hits[0].__class__.__name__)
                print("collided with bush")

                # if self.status == "Invincible":
                #     print("you can't hurt me")
    # def load_images(self):
    #     self.running_frames = [self.spritesheet.get_image(0,32, 32, 64), 
    #                             self.spritesheet.get_image(32,32, 64, 64),
    #                             self.spritesheet.get_image(64,32, 96,64),
    #                             self.spritesheet.get_image(32,32, 64, 64)]
    #     self.standing_frames = [self.spritesheet.get_image(0,0,32,0)]


    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if now - self.last_update > 350:
    #         self.last_update = now
    #         self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #         bottom = self.rect.bottom
    #         self.image = self.standing_frames[self.current_frame]
    #         self.rect = self.image.get_rect()
    #         self.rect.bottom = bottom

            


# old motion
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy  



# UPDATE THE UPDATE
    def update(self):
        #self.rect.x = self.x
        #self.rect.y = self.y
        # self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.collide_with_group(self.game.cheese, True)
        # if self.game.cooldown.cd < 1:
        #     self.cooling = False
        # if not self.cooling:
        self.collide_with_group(self.game.potions, True)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.health, True)
        
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        


# Objective: write a player class (write a wall class)
            
class Potions(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.potions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# coin class
class Cheese(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.cheese
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def move(self,x,y):
        self.x = x
        self.y = y

# triangular mob class
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        super().__init__(game.all_sprites, game.mobs)
        self.game = game
        self.image = self.create_triangular_image()
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = speed
# creating triangular mobs with triangular hit boxes
    def create_triangular_image(self):
        image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        pg.draw.polygon(image, ORANGE, [(TILESIZE // 2, 0), (0, TILESIZE), (TILESIZE, TILESIZE)])
        return image

    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        # self.image = pg.transform.rotate(self.image, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        # self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        # self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        # self.rect.center = self.hit_rect.center
        # if self.health <= 0:
        #     self.kill()
    # creating bush collide method
    def collide_with_bush(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.bush, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.bush, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def spawning(self, x, y):
        pass
        # NEED TO WORK HERE
        

class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        self.image = pg.Surface((2 * TILESIZE, 2 * TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        self.speed = 150
        # self.health = MOB_HEALTH

    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        # self.image = pg.transform.rotate(self.image, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        # self.rect.center = self.hit_rect.center
        # if self.health <= 0:
        #     self.kill()
    # creating bush collide method
    def collide_with_bush(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.bush, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.bush, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

class Health(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.health
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Bush(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        self.image = pg.Surface((3 *TILESIZE, 3 * TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        self.speed = 0
        # self.health = MOB_HEALTH
