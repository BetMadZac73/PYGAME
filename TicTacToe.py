# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:53:18 2020

Try to make a basic Noughts and Crosses Game - just for fun, it needs:-
    - To build a 3x3 grid of squares.  use a class for the squares to make them easier to process
    - it needs to highlight the square that we are currently hovering over
    - tell us whose go it is
    - check whether we have a winner or if all moves have been made, confirm the draw
    - keep a score 
    - provide a start/end by displaying "press space bar to start"

@author: carll
"""

import pygame               # we are using this library

pygame.font.init()          # we are going to use some fonts
WIDTH, HEIGHT = 750, 750    # set the size constants.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))      # Set the constant WIN to be the Name of the screen for playing board
pygame.display.set_caption("Noughts & Crosses")     # Give it a caption
plx , plo = 0, 0                # set the scores player X and player O score starts at Zero
playerX = True                  # we are going to toggle this to see whose go it is

# pygame.display.update()       # just used to test that it will display

class Square:
    # Here we are going to create the grid squares this enables us to create each of the 9 squares
    def __init__(self,x,y,size):
        self.x = x
        self.xpos = (x+1) * size            # this sets the coords up, because the x,y provided is 0,1,2 x 0,1,2
        self.y = y
        self.ypos = (y+1) * size            # this sets the coords up
        self.size = size
        self.selected = False               # this is for when the mouse is over
        self.empty = True                   # this tells us that the square is empty
        self.value = ""                     # this is the value either X or O or nothing
        
    def draw(self, window):
        # this is the function for drawing the square
        if self.selected:                   # we use this to change the color - when the mouse is over
            mycol = (255,255,255)           # make it bright white
        else:
            mycol = (155,155,155)           # make it standard light gray
        pygame.draw.rect(window, mycol, (self.xpos + 2, self.ypos + 2, self.size - 4, self.size - 4))   # position it
        
    def update(self, playerX):
        # pretty simple - if i have been clicked on, then update the value
        if playerX: 
            self.value = "X"
        else:
            self.value = "O"
        self.empty = False  # set the empty status to False so we do not try to write in here again. 
            

def is_win(counters):
    # this checks the array of where the counters are and if there is a winner then we return the winner value
    # if there is no winner we return None, because this means we can test it as a logical variable.
    for i in range(3):
        if counters[i][0] == counters[i][1] == counters[i][2]:
            return counters[i][1]
        if counters[0][i] == counters[1][i] == counters[2][i]:
            return counters[1][i]
    if counters[0][0] == counters[1][1] == counters[2][2]:
        return counters[1][1]
    if counters[2][0] == counters[1][1] == counters[0][2]:
        return counters[1][1]
    return None 



def main():
    # this is the main loop
    run = True                      # we are going to use this to keep running
    FPS = 30                        # Give ourselves a display speed
    main_font = pygame.font.SysFont("comicsans", 70)    # Set a Font
    counter_font = pygame.font.SysFont("comicsans", 150)    # This for the X and O counters
    win_font = pygame.font.SysFont("comicsans", 250)    # This for the X and O counters
    squares = []                    # create an array to hold the squares
    size = (HEIGHT // 4) * 0.8      # set a square size based on the size of the screen
    
    global playerX                  # we are going to toggle this to see whose go it is it's boolean, we use it as global because we want it to keep track across games
    moves = 0                       # let's count the moves 1 - 9, enables us to know when all squares have been filled
    
    counters = [ [ "0", "1", "2" ], [ "3", "4", "5" ], [ "6", "7", "8"] ]   # we set the counters array up and populate it this is where the Xs and Os are going to be placed
    result = None                   # handy to know when there is a result.
    
    global plx, plo                 # access the scores, these are global as they cover game to game. 
    
    clock = pygame.time.Clock()     # this enables us to control the speed of the game
    
    # build out the 3x3 grid - very simple way to build out our grid with 9 instances of the Square Class
    # and of course it keeps track of them by keeping them in an array.
    for x in range(3):
        for y in range(3):
            square = Square(x, y, size)
            squares.append(square)
    
    
    def redraw_window():
        # This is a callable function from within the main loop, to allow access to variables
        # This is what draws the screen every time it is called accoridng to the clock ticks
        pygame.draw.rect(WIN, (0,0,0), (0,0, WIDTH, HEIGHT))                # just draw the background black rectangle
        
        for square in squares:      # here we use the array of 9 squares to allow us to process each square each time
            square.draw(WIN)        # call the draw method of the square to draw it
            if not square.empty:    # if there is a value then we will need to draw that
                if square.value == "X": mylabel = counter_font.render("X",1,(0,255,0))  # create the label as GREEN
                if square.value == "O": mylabel = counter_font.render("O",1,(0,0,255))  # create the label as BLUE
                adjx = size/2 - mylabel.get_width() /2      # just so we can place the value in the centre of the square
                adjy = size/2 - mylabel.get_height() /2     # just so we can place the value in the centre of the square
                WIN.blit(mylabel, (square.xpos + adjx, square.ypos +adjy))   # place it
            
        if moves < 9:   # while we still have moves available - display whose turn it is
            if playerX:
                player_label = main_font.render("Player - X",1,(0,255,0))
            else:
                player_label = main_font.render("Player - O",1,(0,0,255))
            WIN.blit(player_label, (WIDTH/2 - player_label.get_width()/2 , size/3))    # place it
        
        if result:      # when we have a result value, use it and tell us who wins
            result_label = win_font.render(f"{result} - Wins", 1, (255,0,0))
            WIN.blit(result_label, (WIDTH/2 - result_label.get_width()/2 , HEIGHT/2 - result_label.get_height()/2 ))
        elif moves == 9: # or when we are out of available moves tell them it is a draw
            result_label = win_font.render("Draw", 1, (255,0,0))
            WIN.blit(result_label, (WIDTH/2 - result_label.get_width()/2 , HEIGHT/2 - result_label.get_height()/2 ))
            
        x_label = counter_font.render(str(plx), 1, (0,255,0))   #we are just going to place the scores top left and top right
        o_label = counter_font.render(str(plo), 1, (0,0,255))
        WIN.blit(x_label, (10, 10)) 
        WIN.blit(o_label, (WIDTH - 10 - o_label.get_width(), 10))           
        
        pygame.display.update()             # that's it, update the display
    
    
    while run:                      # This is the loop we are going to run
        clock.tick(FPS)             # the clock ticks at the FPS speed
        if result == 'X': plx += 1    # add to the score
        if result == 'O': plo += 1    # add to the score
        redraw_window()             # call the function to redraw the window

        if result or moves >= 9: run = False     # show the Space Bar to Start message
        
        for event in pygame.event.get():    # Check for any events that have happened
            if event.type == pygame.QUIT:   # being able to quit is helpful - click the x on the top of the window
                run = False
                quit()
            # when they hit the mousebutton, you are going to need to process it
            if event.type == pygame.MOUSEBUTTONDOWN and moves < 9 :         # we are looking for a click
                for square in squares:                                      # run through each square
                    if square.selected and square.empty:    # if the square is both selected and empty then do it
                        square.update(playerX)                              # update the value of the square
                        moves += 1                                          # keep count of the moves
                        if playerX:                                         # When we are player X
                            counters[square.x][square.y] = "X"              # set the value into the array
                            playerX = False                                 # switch the player
                        else:                                               # When we are player O
                            counters[square.x][square.y] = "O"              # set the value into the array
                            playerX = True                                  # switch the player
                result = is_win(counters)                                   # check if there is a win
                if result: moves = 9                                        # if there is a result max the moves counter
    
        mouse_x , mouse_y = pygame.mouse.get_pos()                          # keep track of where the mouse is
        for square in squares:                                              # check if the mouse is over each swaure
            square.selected = False                                         # make sure it starts as false
            if square.xpos < mouse_x and mouse_x < square.xpos + square.size:   # in horizontal range
                if square.ypos < mouse_y and mouse_y < square.ypos + square.size:   # in vertical range
                    square.selected = True                                  # set this one as selected


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
