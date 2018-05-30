#Programa simulando o jogo Pong, proveniente do videogame Atari.
#Autor: Paulo Gabriel Sena Comasetto
#E-mail: paulogscomasetto@gmail.com

from math import ceil
from random import randint
import pygame
from pygame.locals import *


class Playable:
    """
    Abstract class, represents both paddles and the ball.
    """

    def __init__(self, image, pos, color, screen_dim):
        self.image = image
        self.pos = pos
        self.color = color
        self.screen_dim = screen_dim

    def getRect(self):
        return self.rect
    
    def setRect(self, new_rect):
        self.rect = new_rect


class Paddle(Playable):
    """
    Paddles controlled by the player.
    As a player scores, the paddles' height gets smaller.
    """

    def __init__(self, image, pos, color, screen_dim, height, y_speed):
        super().__init__(image, pos, color, screen_dim)
        self.Y_SPEED = y_speed
        self.y_speed = y_speed
        self.HEIGHT = height
        self.height = height
        self._height2 = height
        self.WIDTH = 15

    def getHeight2(self):
        return self._height2

    def setHeight2(self, new_height2):
        self._height2 = new_height2        
    
    def stopMovement(self):
        self.y_speed = 0

    def resetMovement(self):
        self.y_speed = self.Y_SPEED

    def resetHeight(self):
        self.height = self.HEIGHT
        self._height2 = self.HEIGHT

    def willPassWall(self, top=False, bottom=False):
        if top:
            return self.pos[1] - 1 < 0
        if bottom:
            return (self.pos[1] + self.height + 1) > self.screen_dim[1]

    def getAboveOrBelowHit(self, ball):
        p_mid_y = self.getRect().y + self.height/2
        if ball.getRect().y < p_mid_y:
            return 0
        else:
            return 9
        
    def getHitSection(self, ball):
        b_mid_y = ball.getRect().y + ball.size/2
        section_h = self.height / 8
        
        if b_mid_y <=  self.getRect().y + section_h*1:
            return 1
        elif self.getRect().y + section_h*1 < b_mid_y \
             and b_mid_y <= self.getRect().y + section_h*2:
            return 2
        elif self.getRect().y + section_h*2 < b_mid_y \
             and b_mid_y <= self.getRect().y + section_h*3:
            return 3
        elif self.getRect().y + section_h*3 < b_mid_y \
             and b_mid_y <= self.getRect().y + section_h*4:
            return 4
        elif self.getRect().y + section_h*4 < b_mid_y \
             and b_mid_y <= self.getRect().y + section_h*5:
            return 5
        elif self.getRect().y + section_h*5 < b_mid_y \
             and b_mid_y <= self.getRect().y + section_h*6:
            return 6
        elif self.getRect().y + section_h*6 < b_mid_y \
             and b_mid_y <= self.getRect().y + section_h*7:
            return 7
        elif self.getRect().y + section_h*7 <= b_mid_y:
            return 8


class Ball(Playable):
    """
    Ball used in the game.
    As long as a player doesn't score, the ball's speed increases.
    increases. When a player scores, it resets to the default speed
    and starts increasing again.
    """

    def __init__(self, image, pos, color, screen_dim, size, speed, speed_add):
        super().__init__(image, pos, color, screen_dim)
        self.size = size
        self.POS = pos
        self.SPEED = tuple(speed)
        self.speed = speed
        self.SPEED_ADD = speed_add
        self.speed_add = speed_add

        self.sect_yspeed = {0:-650, 1:-500, 2:-350, 3:-200, 4:-50,
                            5:50, 6:200, 7:350, 8:500, 9:650}
        
    def resetPos(self):
        self.pos = self.POS

    def resetSpeed(self, left=False, right=False, top=False, bottom=False):
        if left:
            self.speed[0] = -abs(self.SPEED[0])
        if right:
            self.speed[0] = abs(self.SPEED[0])
        if top:
            self.speed[1] = -abs(self.SPEED[1])
        if bottom:
            self.speed[1] = abs(self.SPEED[1])

    def resetSpeedAdd(self):
        self.speed_add = self.SPEED_ADD

    def willPassWall(self, top=False, bottom=False, left=False, right=False):
        if top:
            return (self.pos[1] - 0.1) <= 0
        if bottom:
            return (self.pos[1] + self.size + 0.1) >= self.screen_dim[1]

        if left:
            return (self.pos[0] - 0.1) <= 0
        if right:
            return (self.pos[0] + self.size + 0.1) >= self.screen_dim[0]


class Message:
    """
    Class encompassing all texts in the game.
    Can be directly instantiated, or through the Scoreboard subclass.
    """

    def __init__(self, message, font_family, font_size, color, pos,
                 bold=False, italic=False):
        self.message = message
        self.font_family = font_family
        self.font_size = font_size
        self.color = color
        self.pos = pos
        self.bold = bold
        self.italic = italic


class Scoreboard(Message):
    """
    Scoreboard diplayed in the screen. One for each player.
    Goes from 0 to 10. When a player scores 10 points, the match ends.
    """

    def __init__(self, font_family, font_size, color, pos,
                 bold=False, italic=False, score=0, max_score=10):
        super().__init__(str(score), font_family, font_size, color, pos,
                         bold, italic)
        self._score = score
        self.max_score = max_score

    def getScore(self):
        return self._score

    def score(self):
        self._score += 1
        self.message = str(self.getScore())

    def reachedMaxScore(self):
        return self._score == self.max_score

    def resetScore(self):
        self._score = 0
        self.message = str(self.getScore())
        

##################################objects creation and initializing

#INIT
##pygame.mixer.pre_init(44100, -16, 2, 512)
##pygame.mixer.init()

pygame.init()

#CLOCK
clock = pygame.time.Clock()

#HIDE MOUSE
pygame.mouse.set_visible(False)

#SOUNDS
##ball_paddle_sd = pygame.mixer.Sound("Sounds/ball_paddle.ogg")
##ball_wall_sd = pygame.mixer.Sound("Sounds/ball_wall.ogg")
##score_sd = pygame.mixer.Sound("Sounds/score.ogg")

#BACKGROUND AND SCREEN
screen = pygame.display.set_mode((800, 600), 0, 32)
screen_bg = pygame.image.load("Images/background.png").convert()
pygame.display.set_caption("PONG")
icon_img = pygame.image.load("Images/pong_icon.png").convert_alpha()
pygame.display.set_icon(icon_img)

#PADDLES
p1_color = (randint(50, 255), randint(50, 255), randint(50, 255))

while True:
    p2_color0 = randint(50, 255)
    if abs(p1_color[0] - p2_color0) >= 50:
        break
while True:
    p2_color1 = randint(50, 255)
    if abs(p1_color[1] - p2_color1) >= 50:
        break
while True:
    p2_color2 = randint(50, 255)
    if abs(p1_color[2] - p2_color2) >= 50:
        break
p2_color = (p2_color0, p2_color1, p2_color2)

paddle1 = Paddle(pygame.image.load("Images/paddle100.png").convert_alpha(),
                 (50, 10), p1_color, screen.get_size(), 100, 850)
paddle2 = Paddle(pygame.image.load("Images/paddle100.png").convert_alpha(),
                 (735, 10), p2_color, screen.get_size(), 100, 850)

#BALL
b_img = pygame.image.load("Images/ball.png").convert_alpha()
ball = Ball(b_img, (400, 300), (255, 255, 255),
            screen.get_size(), 15, [500, 350], 1.00)

#SCOREBOARDS
scoreboard1 = Scoreboard("ubuntumono", 130, paddle1.color,
                         (285, 0), bold=True)
scoreboard2 = Scoreboard("ubuntumono", 130, paddle2.color,
                         (445, 0), bold=True)

scoreboard1.font = pygame.font.SysFont(scoreboard1.font_family,
                                        scoreboard1.font_size,
                                        scoreboard1.bold,
                                        scoreboard1.italic)
scoreboard2.font = pygame.font.SysFont(scoreboard2.font_family,
                                        scoreboard2.font_size,
                                        scoreboard2.bold,
                                        scoreboard2.italic)

#PLAY MESSAGE
play_msg = Message("Press      Spacebar", "ubuntumono",
                    50, (255, 255, 255), (200, 400), bold=True)
play_msg.font = pygame.font.SysFont(play_msg.font_family,
                                    play_msg.font_size,
                                    play_msg.bold, play_msg.italic)
play_msg.surface = play_msg.font.render(play_msg.message,
                                        True, play_msg.color)


#######################
msg = True
#main loop, repeats every time a new match starts
while True:

    paddle1.image = pygame.image.load("Images/paddle100.png").convert_alpha()
    paddle2.image = pygame.image.load("Images/paddle100.png").convert_alpha()
    
    paddle1.resetHeight()
    paddle2.resetHeight()
    
    if paddle1.pos[1] + paddle1.height > screen.get_size()[1]:
        paddle1.pos = (paddle1.pos[0],
                       screen.get_size()[1] - paddle1.height)
    if paddle2.pos[1] + paddle2.height > screen.get_size()[1]:
        paddle2.pos = (paddle2.pos[0],
                       screen.get_size()[1] - paddle2.height)

    scoreboard1.pos = (285, 0)

    scoreboard1.resetScore()
    scoreboard2.resetScore()

    scoreboard1.surface = scoreboard1.font.render(scoreboard1.message,
                                                  True, scoreboard1.color)
    scoreboard2.surface = scoreboard2.font.render(scoreboard2.message,
                                                  True, scoreboard2.color)

    ball.resetPos()
    ball.resetSpeed(right=True, bottom=True)
    ball.resetSpeedAdd()

    #pygame main loop        
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        screen.blit(screen_bg, (0,0))

        #time in seconds
        time_passed = clock.tick(60) / 1000 #fps

        #PADDLES
        pressed = pygame.key.get_pressed()
        #######1
        if pressed[K_a]:
            if paddle1.willPassWall(top=True):
                paddle1.stopMovement()
            else:
                paddle1.resetMovement()
            paddle1.pos = (paddle1.pos[0],
                           paddle1.pos[1] - paddle1.y_speed*time_passed)

        if pressed[K_z]:
            if paddle1.willPassWall(bottom=True):
                paddle1.stopMovement()
            else:
                paddle1.resetMovement()
            paddle1.pos = (paddle1.pos[0],
                           paddle1.pos[1] + paddle1.y_speed*time_passed)

        #######2
        if pressed[K_k]:
            if paddle2.willPassWall(top=True):
                paddle2.stopMovement()
            else:
                paddle2.resetMovement()

            paddle2.pos = (paddle2.pos[0],
                           paddle2.pos[1] - paddle2.y_speed*time_passed)

        if pressed[K_m]:
            if paddle2.willPassWall(bottom=True):
                paddle2.stopMovement()
            else:
                paddle2.resetMovement()

            paddle2.pos = (paddle2.pos[0],
                           paddle2.pos[1] + paddle2.y_speed*time_passed)

        paddle1.image.fill(paddle1.color)
        paddle2.image.fill(paddle2.color)

        screen.blit(paddle1.image, paddle1.pos)
        screen.blit(paddle2.image, paddle2.pos)

        #PLAY MSG
        if msg:
            screen.blit(play_msg.surface, play_msg.pos)
            if event.type == KEYDOWN and event.key == K_SPACE:
                msg = False

        #VICTORY
        if scoreboard1.reachedMaxScore() or scoreboard2.reachedMaxScore():
            if scoreboard1.reachedMaxScore():
                win_msg = Message("WIN", "ubuntumono", 90,
                                  paddle1.color, (200, 250), bold=True)
                scoreboard1.pos = (215, 0)
            else:
                win_msg = Message("WIN", "ubuntumono", 90,
                                  paddle2.color, (530, 250), bold=True)

            win_msg.font = pygame.font.SysFont(win_msg.font_family,
                                               win_msg.font_size,
                                               win_msg.bold,
                                               win_msg.italic)
            win_msg.surface = win_msg.font.render(win_msg.message,
                                                  True, win_msg.color)

            screen.blit(win_msg.surface, win_msg.pos)

            msg = True

            if event.type == KEYDOWN and event.key == K_SPACE:
                msg = False
                break

        #ESCAPE: quit a match
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            msg = True
            break

        #BALL
        elif not msg:

            ball_rect = pygame.Rect(ball.pos, (ball.size, ball.size))
            paddle1_rect = pygame.Rect(paddle1.pos,
                                       (paddle1.WIDTH, paddle1.height))
            paddle2_rect = pygame.Rect(paddle2.pos,
                                       (paddle2.WIDTH, paddle2.height))

            ball.setRect(ball_rect)
            paddle1.setRect(paddle1_rect)
            paddle2.setRect(paddle2_rect)

            if ball.willPassWall(top=True) or ball.willPassWall(bottom=True):
                ##ball_wall_sd.play(maxtime=100)                
                ball.speed[1] *= -1
                
            elif ball.getRect().colliderect(paddle1.getRect()) \
                 or ball.getRect().colliderect(paddle2.getRect()):
                ##ball_paddle_sd.play(maxtime=100)                
                ball.speed_add += 0.1
    
                if ball.getRect().colliderect(paddle1.getRect()):
                    ball.speed[0] = 350
                    
                    #check if ball hit above or below the paddle 1                    
                    if paddle1.getRect().x + paddle1.WIDTH \
                       - ball.getRect().x > 13:                        
                        sect = paddle1.getAboveOrBelowHit(ball)                 
                        ball.pos = (paddle1.getRect().x + paddle1.WIDTH,
                                    ball.pos[1])
                        
                    else: #ball hit in one of the 8 sections
                        sect = paddle1.getHitSection(ball)                        
                        
                elif ball.getRect().colliderect(paddle2.getRect()):
                    ball.speed[0] = -350
                    
                    #check if ball hit above or below the paddle 2
                    if ball.getRect().x + ball.size \
                       - paddle2.getRect().x > 13:                        
                        sect = paddle2.getAboveOrBelowHit(ball)
                        ball.pos = (paddle2.getRect().x - ball.size,
                                    ball.pos[1])
                        
                    else: #ball hit in one of the 8 sections                        
                        sect = paddle2.getHitSection(ball)

                ball.speed[1] = ball.sect_yspeed[sect]
                
                ball.speed[0] *= ball.speed_add
                ball.speed[1] *= ball.speed_add                
                
            elif ball.willPassWall(left=True) or ball.willPassWall(right=True):
                ##score_sd.play(maxtime=100)
                
                if ball.willPassWall(left=True):
                    scoreboard2.score()
                    scoreboard2.surface = scoreboard2.font.render(
                        scoreboard2.message, True, scoreboard2.color)

                    if paddle2.pos[1] + paddle2.height/2 \
                       <= screen.get_size()[1]/2:
                        ball.resetSpeed(right=True, top=True)
                    else:
                        ball.resetSpeed(right=True, bottom=True)

                elif ball.willPassWall(right=True):
                    scoreboard1.score()
                    scoreboard1.surface = scoreboard1.font.render(
                        scoreboard1.message, True, scoreboard1.color)

                    if paddle1.pos[1] + paddle1.height/2 \
                       <= screen.get_size()[1]/2:
                        ball.resetSpeed(left=True, top=True)
                    else:
                        ball.resetSpeed(left=True, bottom=True)

                ball.resetPos()
                ball.resetSpeedAdd()
                
                paddle1.setHeight2(paddle1._height2 - 2.5)
                paddle2.setHeight2(paddle2._height2 - 2.5)
                
                paddle1.height = ceil(paddle1.getHeight2())
                paddle2.height = ceil(paddle2.getHeight2())
                
                paddle1.image = pygame.image.load("Images/"
                    "paddle"+str(paddle1.height)+".png").convert_alpha()
                paddle2.image = pygame.image.load("Images/"
                    "paddle"+str(paddle2.height)+".png").convert_alpha()


            ball.pos = (ball.pos[0] + ball.speed[0]*time_passed,
                        ball.pos[1] + ball.speed[1]*time_passed)

            ball.image.fill(ball.color)
            screen.blit(ball.image, ball.pos)

        #SCOREBOARD
        screen.blit(scoreboard1.surface, scoreboard1.pos)
        screen.blit(scoreboard2.surface, scoreboard2.pos)

        #UPDATE
        pygame.display.update()
