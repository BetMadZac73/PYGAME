# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:04:48 2020

@author: carll
"""

import pygame
import os
import time
import random
import winsound

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - tute")


# load images
asset_dir = "{}\\assets".format(os.path.dirname(__file__))

RED_SPACE_SHIP = pygame.image.load(os.path.join(asset_dir, "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join(asset_dir, "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join(asset_dir, "pixel_ship_blue_small.png"))

# player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join(asset_dir, "pixel_ship_yellow.png"))

# lasers
RED_LASER = pygame.image.load(os.path.join(asset_dir, "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join(asset_dir, "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join(asset_dir, "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join(asset_dir, "pixel_laser_yellow.png"))

# BG image
BG = RED_LASER = pygame.transform.scale(pygame.image.load(os.path.join(asset_dir, "background-black.png")), (WIDTH, HEIGHT))

# lets create the laser class will be used for inheriting 
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        
    def move(self, vel):
        self.y += vel
        
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(obj, self)



# lets create a class for ships will be used for ingeriting from
class Ship:
    COOLDOWN = 30
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y 
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0 
    
    def draw(self, window):
        # pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50 ), 0)   # used for testing
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1 
            
            
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)    # this is using the super init method from Ship 
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        score = 0
        for laser in self.lasers:
            laser.move(vel*2)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        score += obj.get_score()
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        return score

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
        
    def shoot(self):
        super().shoot()
        if self.cool_down_counter == 1: 
            winsound.Beep(2500, 150)     # frequency Mhz, duration mS        

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
        


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
        }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)    # inherith using the super Ship class
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        
    def move(self, vel):
        self.y += vel
        
    def get_score(self):
        return (HEIGHT - self.y) // 50
        

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    if obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None:
        winsound.Beep(450, 100)
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None  # (will return x,y of the collision point)


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    small_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("comicsans", 70)
    score = 0

    enemies = []
    wave_length = 5 
    enemy_vel = 1
    
    lost = False
    lost_count = 0
    
    new_level = False

    player_vel = 5    # player velocity
    laser_vel = 4    # laser speed
    
    
    player = Player(300, 600)
    
    
    clock = pygame.time.Clock()
    
    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text 
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,0,0))
        level_label = main_font.render(f"Level: {level}", 1, (255,0,0))
        score_label = main_font.render(f"Score: {score}", 1, (190,190,190))

        
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (10,40))

        enemy_lab = ""
        for enemy in enemies:
            enemy.draw(WIN)
            enemy_lab += "* "
        enemy_label = small_font.render(enemy_lab, 1, (255,255,255))
        WIN.blit(enemy_label, (WIDTH - enemy_label.get_width() - 10,40))
        
        player.draw(WIN)
        
        if lost:
            lost_label = lost_font.render(f"Game Over! - Score : {score} ", 1, (0, 255, 0))
            WIN.blit(lost_label, ((WIDTH/2 - lost_label.get_width()/2), 350))

        if new_level:
#            new_level = False
            level_label = main_font.render(f"Level : {level}", 1, (255,0,255))
            WIN.blit(level_label, ((WIDTH/2 - level_label.get_width()/2), 350))
            pygame.display.update()
            time.sleep(1.4)
        
        pygame.display.update()
        
    
    
    while run: 
        clock.tick(FPS)

        if player.health <= 0:
            lives -= 1
            player.health = player.max_health

        redraw_window()

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost: 
            if lost_count > FPS * 5:
                run = False
            else:
                continue
        
        new_level = False
        if len(enemies) == 0:
            level += 1
            new_level = True
            wave_length += 6 
            # enemy_vel += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]) )
                enemies.append(enemy)



        #check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 12 < HEIGHT: # down
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(0, FPS*4)  == 1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10
                score += enemy.get_score()      # add in score function call
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                player.health = player.max_health
                enemies.remove(enemy)

        score += player.move_lasers(-laser_vel, enemies)
                
        
def main_menu():
    title_font = pygame.font.SysFont("ComisSans", 50)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press mouse button to start...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()//2 , 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
        

        
main_menu()