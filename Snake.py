# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 11:34:37 2021

It's just a simple snake game.  You steer with WASD controls on the keyboard. 
and simply you collect the fruit as you go (Red and Blue Dots) and each time 
you eat one, the snake gets longer by 2 blocks. each ninth level it speeds up a bit. 

@author: carll
"""

import pygame
import random

# create a standard size for the board
WIDTH = 750
HEIGHT = 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Snake") 
pygame.font.init()          # we are going to use some fonts

# It's just the super class.  I don't think we relaly need it, but maybe one day we would 
class Square():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
        
# We need to draw in the game board square
class Board(Square):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)
        self.xpos = size + (self.x * self.size)
        self.ypos = 100 + (self.y * self.size)

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.xpos, self.ypos, self.size, self.size))
        
# snake squares implement the super class and adjust the size and position a little
# also the game will call the size and color details to adjust them as the snake piece ages.
class Snake(Square):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)
        self.xpos = 3 + size + (self.x * self.size)
        self.ypos = 103 + (self.y * self.size)
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.xpos, self.ypos, self.size - 6, self.size - 6))

# Fruit is actually going to be a circle, but it gets it's first position from the super class
class Fruit(Square):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)
        self.xpos = size + size/2 + (self.x * self.size)
        self.ypos = 100 + size/2 + (self.y * self.size)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.xpos, self.ypos), self.size/2.3)

# We need to test whether the square we intend to place either the next Snake or the Fruit
# is actually valid, i.e. not already occupied - we just return True or False
def is_valid(snakeX, snakeY, snakes, wide, high):
    if not 0 <= snakeX < wide: return False
    if not 0 <= snakeY < high: return False
    for snake in snakes:
        if snake.x == snakeX and snake.y == snakeY: return False
    return True

# We need to check if the square we plan to move the snake on to also occupies a fruit
# and simply return True or False
def is_fruit(snakeX, snakeY, fruits):
    for fruit in fruits:
        if fruit.x == snakeX and fruit.y == snakeY:
            return True
    return False


def main():
    # the main loop
    main_font = pygame.font.SysFont("comicsans", 70)    # Set a Font
    run = True                                          # this is how we run forever
    FPS = 30                                            # this is our frame speed
    clock = pygame.time.Clock()                         # we use this to time the speed
    COOLDOWN = 10                                       # this is the snake speed (10 frames)
    cooldown_counter = 0                                # we set this to COOLDOWN 
    gimme_fruit = 0                                     # it's a cooldown for next fruit
    size = 50                                           # This is the square size
    boards = []                                         # these are all the board squares
    wide, high = 13, 12                                 # this is the shape of the board
    snakes = []                                         # these are snake segments
    snakeX, snakeY = 7, 6                               # starting position
    adjX , adjY = 0, 0                                  # we use these for adjusting position
    snake_color = (0,255,160)                           # RGB color of the snake
    snake_len = 10                                      # This is the starting length
    fruits = []                                         # Hold the fruit array
    score = 0                                           # We need a scroe
    
    # Create the board squares
    for x in range(wide):
        for y in range(high):
            color = (155,155,155)
            if x % 2 == 0 and y % 2 == 0: color = (50,50,50)
            if x % 2 != 0 and y % 2 != 0: color = (50,50,50)
            board = Board(x, y, size, color)
            boards.append(board)
            
    # Createt he first Snake segmeent
    snake = Snake(snakeX, snakeY, size, snake_color)
    snakes.append(snake)
    
    # Each time we want to draw the board
    def redraw_window():
        pygame.draw.rect(WIN, (0,0,0), (0,0, WIDTH, HEIGHT))        # blank the screen
        for board in boards:                                        # draw the baord squares
            board.draw(WIN)
        for snake in snakes:                                        # draw the snake segments
            snake.draw(WIN)
        for fruit in fruits:                                        # draw the fruit
            fruit.draw(WIN)
        score_label = main_font.render(f"Score : {score}", 1, (255,255,255))
        WIN.blit(score_label, (10,10))                              # draw the score onto the screen
        length_label = main_font.render(f"Snake Length : {len(snakes)}", 1, (255,255,255))
        WIN.blit(length_label, (WIDTH - 10 - length_label.get_width(),10)) # tell them the snake length

        pygame.display.update()
    
    # Just keep doing this    
    while run:
        clock.tick(FPS)
        redraw_window()

        if cooldown_counter > 0: cooldown_counter -= 1              # decrement the cooldown
        
        for event in pygame.event.get():    # Check for any events that have happened
            if event.type == pygame.QUIT:   # being able to quit is helpful - click the x on the top of the window
                run = False
                pygame.quit()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and adjX != 1: adjX, adjY = -1, 0
        if keys[pygame.K_d] and adjX != -1: adjX, adjY = +1, 0
        if keys[pygame.K_w] and adjY != 1: adjX, adjY = 0, -1
        if keys[pygame.K_s] and adjY != -1: adjX, adjY = 0, +1

        if cooldown_counter == 0:
            cooldown_counter = COOLDOWN - (score // 9)      # we adjust the speed every 9th level
            snakeX += adjX
            snakeY += adjY
            if is_valid(snakeX, snakeY, snakes, wide, high):
                if is_fruit(snakeX, snakeY, fruits):
                    fruits = []
                    snake_len += 2
                    score += 1
                
                snake = Snake(snakeX, snakeY, size, snake_color)
                snakes.append(snake)
                snakes = snakes[-snake_len:]
                for snake in snakes:
                    if snake.color[1] > 50:
                        snake.color = (snake.color[0], snake.color[1] - 10, snake.color[2])
                    else:
                        snake.color = (snake.color[0] + 5, 200, snake.color[2])
                        if snake.size > 30:
                            snake.xpos += 1
                            snake.ypos += 1
                            snake.size -= 2

            elif len(snakes) > 1:
                run = False

        if gimme_fruit == 0 and len(fruits) == 0:
            fruitX = random.randint(0, wide-1)
            fruitY = random.randint(0, high-1)
            fruit_color = random.choice([(0,0,255),(255,0,0)])
            if is_valid(fruitX, fruitY, snakes, wide, high):
                fruit = Fruit(fruitX, fruitY, size, fruit_color)
                fruits.append(fruit)
                gimme_fruit = random.randint(1*FPS, 5*FPS)
        if gimme_fruit > 0: gimme_fruit -= 1

def main_menu():
    # Just the top level menu - does not do much.
    title_font = pygame.font.SysFont("ComisSans", 50)                       # we need this font
    title_label = title_font.render("Press Space Bar to start...", 1, (255,255,255)) # to make this label
    run = True                                                              # enable us to have na endless loop
    while run:
        # we are deliberately not wiping the whole screen, just placing our text over the top.
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()//2 , HEIGHT * 0.85)) # place it
        pygame.display.update()                                             # update the display
        for event in pygame.event.get():                                    # look for events
            if event.type == pygame.QUIT:                                   # it's nice to be able to quit
                run = False
            if event.type == pygame.KEYDOWN:                                # look for key press
                if event.key == pygame.K_SPACE:                             # when it is the space bar
                    main()                                                  # run the main program
    pygame.quit()
    
main_menu()

