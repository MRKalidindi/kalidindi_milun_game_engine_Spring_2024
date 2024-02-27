# This file was created by: Milun Kalidindi

# importing libraries
import pygame as pg 
from settings import *
from random import randint  
from sprites import *
import sys 
from os import path


#pg.init()


# initialize class
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
        self.running = True
        # later on we'll store game info here
        self.load_data()
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
                print(self.map_data)
        # method for creating a new game
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.potions = pg.sprite.Group()
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
                if tile == 'C':
                    Coin(self, col, row)
        


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
         self.all_sprites.update()  
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
        #
            for event in pg.event.get():
                # when you hit the red x the window closes the game ends
                if event.type == pg.QUIT:
                    self.quit()
                    print("The game has ended")
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

    def show_start_screen(self):
        pass 
    def show_go_screen(self):
        pass   

############################### Instantiate Game....##################################
g = Game()
# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
