import pygame
from pygame.locals import *
from math import ceil
from random import randint

####TASKS
#colisão bola-palheta em 8 pontos
#reflexão da bola em 8 pontos da palheta
#sons do jogo
#trajetória inicial da bola

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
        self.WIDTH = 15

    def getHeight2(self):
        return self.height2

    def setHeight2(self, new_height2):
        self.height2 = new_height2        
    
    def stopMovement(self):
        self.y_speed = 0

    def resetMovement(self):
        self.y_speed = self.Y_SPEED

    def resetHeight(self):
        self.height = self.HEIGHT

    def willPassWall(self, top=False, bottom=False):
        if top:
            return self.pos[1] - 1 < 0
        if bottom:
            return (self.pos[1] + self.height + 1) > self.screen_dim[1]


class Ball(Playable):
    """
    Ball used in the game.
    As long as a player doesn't score, the ball's speed.
    increases. When a player scores, it resets to the default speed
    and starts increasing again.
    """

    def __init__(self, image, pos, color, screen_dim, size, speed):
        super().__init__(image, pos, color, screen_dim)
        self.size = size
        self.POS = pos
        self.pos = pos
        self.SPEED = tuple(speed)
        self.speed = speed
        
    def resetPos(self):
        self.pos = self.POS

    def resetSpeed(self):
        self.speed = list(self.SPEED)

    def willPassWall(self, top=False, bottom=False, left=False, right=False):
        if top:
            return (self.pos[1] - 1) < 0
        if bottom:
            return (self.pos[1] + self.size + 1) > self.screen_dim[1]

        if left:
            return (self.pos[0] - 1) < 0
        if right:
            return (self.pos[0] + self.size + 1) > self.screen_dim[0]


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

#########################################
#objects creation and initializing

pygame.init()

#CLOCK
clock = pygame.time.Clock()

#HIDE MOUSE
pygame.mouse.set_visible(False)

#BACKGROUND AND SCREEN
screen = pygame.display.set_mode((800, 600), 0, 32)
screen_bg = pygame.image.load("Images/background.png").convert()
pygame.display.set_caption("PONG")

#PADDLES
p1_color = (randint(50, 255), randint(50, 255), randint(50, 255))
while True:
    p2_color = (randint(50, 255), randint(50, 255), randint(50, 255))
    if abs(p1_color[0] - p2_color[0]) >= 50\
       and abs(p1_color[1] - p2_color[1]) >= 50\
       and abs(p1_color[2] - p2_color[2]) >= 50:
        break

print(p1_color, p2_color, sep=" -- ")

paddle1 = Paddle(pygame.image.load("Images/paddle100.png").convert_alpha(),
                 (50, 10), p1_color, screen.get_size(), 100, 850)
paddle2 = Paddle(pygame.image.load("Images/paddle100.png").convert_alpha(),
                 (735, 10), p2_color, screen.get_size(), 100, 850)

#BALL
img = pygame.image.load("Images/ball.png").convert_alpha()
ball = Ball(img, (400, 300), (255, 255, 255),
            screen.get_size(), 15, [500, 350])

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

#main loops
while True:
    msg = True
    win = False

    paddle1.image = pygame.image.load("Images/paddle100.png").convert_alpha()
    paddle1.resetHeight()
    paddle2.image = pygame.image.load("Images/paddle100.png").convert_alpha()
    paddle2.resetHeight()

    scoreboard1.pos = (285, 0)

    scoreboard1.resetScore()
    scoreboard2.resetScore()

    scoreboard1.surface = scoreboard1.font.render(scoreboard1.message,
                                                  True, scoreboard1.color)
    scoreboard2.surface = scoreboard2.font.render(scoreboard2.message,
                                                  True, scoreboard2.color)

    ball.resetPos()
    ball.resetSpeed()

    while not win:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        #time in seconds
        time_passed = clock.tick(60) / 1000 #60 fps

        screen.blit(screen_bg, (0,0))

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
                print("-"*10)
                win = True


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
                ball.speed[1] *= -1

            elif ball.getRect().colliderect(paddle1.getRect()) \
                 or ball.getRect().colliderect(paddle2.getRect()):
                ball.speed[0] *= -1
                ball.speed[0] *= 1.05
                #ball.speed[1] *= -1
                #if ball_rect.colliderect(paddle1_rect):
                    

            elif ball.willPassWall(left=True) or ball.willPassWall(right=True):
                if ball.willPassWall(left=True):
                    scoreboard2.score()
                    scoreboard2.surface = scoreboard2.font.render(
                        scoreboard2.message, True, scoreboard2.color)

                else:
                    scoreboard1.score()
                    scoreboard1.surface = scoreboard1.font.render(
                        scoreboard1.message, True, scoreboard1.color)

                ball.resetPos()
                ball.resetSpeed() #mudar depois
                
                paddle1.height -= 2.5
                paddle2.height -= 2.5
                
                paddle1.setHeight2(ceil(paddle1.height))
                paddle2.setHeight2(ceil(paddle2.height))
                
                paddle1.image = pygame.image.load("Images/"
                    "paddle"+str(paddle1.getHeight2())+".png").convert_alpha()
                paddle2.image = pygame.image.load("Images/"
                    "paddle"+str(paddle2.getHeight2())+".png").convert_alpha()


            ball.pos = (ball.pos[0] + ball.speed[0]*time_passed,
                        ball.pos[1] + ball.speed[1]*time_passed)

            ball.image.fill(ball.color)
            screen.blit(ball.image, ball.pos)

        #SCOREBOARD
        screen.blit(scoreboard1.surface, scoreboard1.pos)
        screen.blit(scoreboard2.surface, scoreboard2.pos)

        #UPDATE
        pygame.display.update()
