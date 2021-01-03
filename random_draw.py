# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:58:34 2020

We are just going to create a black canvas, and pop some coloured blobs on that are going to 
move around and draw onto the canvas.

Use ESCAPE key to exit
Use SPACE key to turn the trails on and off - try it you will see.

@author: carll
"""

import pygame
import random

# this bit is going to try and get the screen size will work for Windows Machine
# put it in a Try clause - hopefully will also work therefore on non-Windows
try:
    from win32api import GetSystemMetrics         # we want to get the screen size
    HEIGHT = GetSystemMetrics(1)
    WIDTH = GetSystemMetrics(0)
except:
    HEIGHT = 750
    WIDTH = 1500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))              # create the window
pygame.display.set_caption("Doodle")                        # give it the tittle
pygame.font.init()                                          # we are going to use some fonts

class Brush():
    # Create the Brush Class, they are going to be little squares
    def __init__(self):
        self.x = random.randint(WIDTH * 0.4//1, WIDTH * 0.6//1)     # we use // to make sure it is an Integer 
        self.y = random.randint(HEIGHT * 0.4//1, HEIGHT * 0.6//1)   # use // to get integer
        self.size = random.randint(1,6)                             # give a random size
        self.R = random.randint(30,255)                             # random colors
        self.G = random.randint(30,255)
        self.B = random.randint(30,255)
        
    def draw(self, window):
        # very simple draw method
        pygame.draw.rect(window, (self.R, self.G, self.B), (self.x, self.y, self.size, self.size))
    
    def move(self, posx, posy, clicked):
        # this moves the brush randomly
        self.x += random.randint(-12 + self.size, 12 - self.size)
        self.y += random.randint(-12 + self.size, 12 - self.size)
        if self.x < -50 or self.x > WIDTH + 50: self.x = WIDTH/2
        if self.y < -50 or self.y > HEIGHT + 50: self.y = HEIGHT/2
        if clicked:
            # If the mouse was clicked the we are going to chase the brushes away from the cursor position
            if self.x < posx - 50: self.x += -1
            if self.y < posy - 50: self.y += -1
            if self.x > posx + 50: self.x -= -1
            if self.y > posy + 50: self.y -= -1

def main():
    run = True                      # we use this to run for ever
    FPS = 30                        # this is the speed that we cycle at
    brushes = []                    # create an array to hold all our brushes in
    clock = pygame.time.Clock()     # make the clock so we can tick
    clicked = False                 # we use this in case using mouse to chase the brushes around
    trails_on = True                # this enables us to toggle whether trails are kept or cleared
    key_cool = 0                    # the key hit happens too fast, so we use this to cool down after a key hit
    main_font = pygame.font.SysFont("comicsans", 20)    # Set a Font
    
    for i in range(2500):           # We are going to create this many indiviudal brushes
        brush = Brush()             # create the brush
        brushes.append(brush)       # add it to the array so we can iterate them all
    
    # We are going to tell them how to control this program
    info = [f"Random v1.0 uses 2,500 brushes running at {FPS} FPS", "Press <esc> to exit", "Press <space> to toggle trails on/off", "Click Mouse to chase brushes"]
    n = 0
    for line in info:
        n += 1
        info_label = main_font.render(line,1,(255,255,255))
        WIN.blit(info_label, (10 , n * 15))
    
    def redraw_window():
        # when it's not trails then fill the background with a blank black rectangle
        if not trails_on:
            pygame.draw.rect(WIN, (0,0,0), (0,0, WIDTH, HEIGHT)) 
        # iterate through all the brushes, move them, and then draw them n
        for brush in brushes:
            brush.move(posx,posy,clicked)
            brush.draw(WIN)
        # update that display
        pygame.display.update()
 
    # Now let's hold it in the endless loop until we are ready to exit.           
    while run:
        clock.tick(FPS)                     # go at this speed
        posx, posy = pygame.mouse.get_pos() # check the position of the mouse
        redraw_window()                     # call the redraw function before we do anything else
       
        # now check for any events.
        for event in pygame.event.get():    # Check for any events that have happened
            if event.type == pygame.QUIT:   # being able to quit is helpful - click the x on the top of the window
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # We are looking for a mouse click on or off
                clicked = not clicked       # switch the value True or False

            keys = pygame.key.get_pressed() # check key presses
            if keys[pygame.K_ESCAPE]:       # it's nice to be able to exit
                run = False
                pygame.quit()
            if keys[pygame.K_SPACE] and key_cool == 0:  # Space Bar enables us to turn trails on and off
                trails_on = not trails_on
                key_cool = 3                # set the counter so we detect only one key press
            
            if key_cool > 0: key_cool -= 1  # decrement the cool down counter
       
main() 

        
        