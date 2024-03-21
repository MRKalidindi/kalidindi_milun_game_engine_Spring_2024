# This file was created by: Milun Kalidindi


'''
Sources:
kids can code: https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2001 


Game design truths:goals, rules, feedbaack, freedom, verb, sentence

Bosses
smoother enemies
Character with lasers
sword
allow for pausing
levels (different school with different maps)
map that moves with character


'''

# importing libraries
import pygame as pg 
from settings import *
from random import randint  
from sprites import *
import sys 
from os import path


#pg.init()


# initialize class
# cooldown class
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = float((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# Game Class
class Game:
    # method that defines function: __init__ 
    def __init__(self):
        pg.init()
        # set parameters for width and height (imported from setting)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #creates caption
        pg.display.set_caption("My First Video Game")
        # Clock(): class that tracks time using ticks
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        # later on we'll store game info here
        self.load_data()
        self.running = True
        self.paused = False
    def load_data(self): 
        # says location is the game folder
        game_folder = path.dirname(__file__)
        # will put map data in this empty list
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'Autobot Symbol.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        # opens that file map.txt and opens it as f
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

        # method for creating a new game
    def new(self):
        # create timer
        # self.test_timer = Cooldown()
        # print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.potions = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobs2 = pg.sprite.Group()
        self.health = pg.sprite.Group()
        for i in range (0,1):
            Coin(self, randint(0,30), randint(0,22)) 

        #self.player = Player(self, 10, 10)
        #self.all_sprites.add(self.player)
        #for x in range (10, 20):
         #  Wall(self, x, 5)
        # enumerate takes a list of things and enumerates them (says what it is)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'o':
                    Potions(self, col, row)
                # if tile == 'C':
                #     Coin(self, col, row) 
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'f':
                    Mob2(self, col, row)
                if tile == 'h':
                    Health(self, col, row)
    # call the function
        self.run()
#run method - responsible for running
    def run(self):
        self.playing = True
        while self.playing: 
            self.dt = self.clock.tick(FPS) / 1000
            # this is input
            self.events()
            # this is processing
            self.update()
            # this is output
            self.draw()


    def quit(self):
        pg.quit()
        sys.exit()
 # method (like functions but they are ties to a class) 
    def input(self): 
         pass
    def update(self):
        if not self.paused:
            # wws
            self.all_sprites.update()
            if self.player.hitpoints < 1:
                self.playing = False
            # if self.player.moneybag > 2:
                # self.change_level(LEVEL2)
    # draws the grid on the screen
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        pg.display.flip()
        
    def events(self):
        for event in pg.event.get():
            # when you hit the red x the window closes the game ends
            if event.type == pg.QUIT:
                self.quit()
                print("The game has ended")
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    if not self.paused:
                        self.paused = True
                    else:
                        self.paused = False
            # gets inputs from the key arrows and tells it what to do (move)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player.move(dx=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_d:
            #         self.player.move(dx=1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_w:
            #         self.player.move(dy=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_s:
            #         self.player.move(dy=1)
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 150, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any key to play", 150, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key() 
    

############################### Instantiate Game....##################################
g = Game()

g.show_go_screen()
while True:
    g.new()
    # g.run()
    g.show_start_screen()

