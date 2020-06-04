#!/usr/bin/env python3

###############################################################################
# IMPORTS
###############################################################################

import pygame
from Paddle import Paddle
from Ball import Ball


###############################################################################
# CONSTANTS
###############################################################################

# Window dimensions
WIDTH     = 800
HEIGHT    = 600

# Paddle dimensions
PADDLE_TO_WALL = 20
PADDLE_WIDTH   = 10
PADDLE_HEIGHT  = 100

PADDLE_MOVE_DISTANCE = 8

BALL_SIZE = 30
NET_WIDTH = 8

# Define some colors
BLACK     = (0,0,0)
WHITE     = (255,255,255)
RED       = (255,0,0)
YELLOW    = (255,255,0)
GREEN     = (0,255,0)
BLUE      = (0,0,255)
ORANGE    = (255,100,0)


###############################################################################
# MAIN PROGRAM
###############################################################################

pygame.init()





# Open a new window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Amazing Pong Game")

# Create two Paddles
paddleA = Paddle(WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, HEIGHT-PADDLE_HEIGHT)
paddleA.rect.x = PADDLE_TO_WALL
paddleA.rect.y = (HEIGHT / 2) - (PADDLE_HEIGHT / 2)

paddleB = Paddle(WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, HEIGHT-PADDLE_HEIGHT)
paddleB.rect.x = WIDTH - PADDLE_WIDTH - PADDLE_TO_WALL
paddleB.rect.y = (HEIGHT / 2) - (PADDLE_HEIGHT / 2)

# Create a ball
center = [int(WIDTH/2), int(HEIGHT/2)]
ball = Ball(WHITE, BALL_SIZE, BALL_SIZE, center)
ball.reset()

# This will be a list that will contain all the sprites we intend to use in our game.
# sprite = graphic element that is seen on screen
all_sprites_list = pygame.sprite.Group()

# Add the paddles to the list of sprites
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will carry on until the user exit the game
# -> e.g. clicks the close button
carryOn = True

# Is the game currently paused?
pause = False

# Are we in the intro?
intro = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# background image
intro_image = pygame.image.load('pong_intro.png')

#Initialise player scores
scoreA = 0
scoreB = 0

# -----------------------------------------------------------------------------
# draw text on screen
# -----------------------------------------------------------------------------

def text_on_screen(screen, text, font_size, font_color, pos_x, pos_y):
     font = pygame.font.Font('freesansbold.ttf',font_size)
     text_surface = font.render(text, True, font_color)
     text_rectangle = text_surface.get_rect()
     text_rectangle.center = (pos_x,pos_y)
     screen.blit(text_surface, text_rectangle)



# -----------------------------------------------------------------------------
# Main Program Loop
# -----------------------------------------------------------------------------
while carryOn:

     # -------------------------------------------------------------------------
     # Intro
     # -------------------------------------------------------------------------

     # intro screen
     while intro:

          # define the surface (screen)
          screen.fill(GREEN)

          # draw (= render/blit) text on the surface (screen)
          text_on_screen(screen, "PONG", 100, BLACK, WIDTH/2, 100)
          text_on_screen(screen, "(C) Marcus Kossatz", 15, BLACK, WIDTH/2, HEIGHT-30)

          # draw image on the surface (screen)
          center = WIDTH/2 - intro_image.get_size()[0]/2
          bottom = HEIGHT - intro_image.get_size()[1] - 75
          screen.blit(intro_image,(center, bottom))

          pygame.display.update()
          clock.tick(15)

          # end intro on click on return key ("Enter")
          for event in pygame.event.get():
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                         intro = False
                    if event.key == pygame.K_x:
                         pygame.quit()

     # -------------------------------------------------------------------------
     # Main Event Loop
     # -------------------------------------------------------------------------

     # User did something
     for event in pygame.event.get():

          # If user clicked close
          # => End the game = exit this loop
          if event.type == pygame.QUIT:
               carryOn = False

          # If user clicked "x" Key
          # => End the game = exit this loop
          elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_RETURN:
                    intro = False
               if event.key == pygame.K_x:
                    carryOn = False
               if event.key == pygame.K_p:
                    pause = not pause
               if event.key == pygame.K_r:
                    ball.reset()
               if event.key == pygame.K_PLUS:
                    ball.speedup()
               if event.key == pygame.K_MINUS:
                    ball.speeddown()

     # only execute rest of the program if NOT paused
     if not pause:

          # React to keypresses
          keys = pygame.key.get_pressed()
          if keys[pygame.K_w]:
               paddleA.moveUp(PADDLE_MOVE_DISTANCE)
          if keys[pygame.K_s]:
               paddleA.moveDown(PADDLE_MOVE_DISTANCE)
          if keys[pygame.K_UP]:
               paddleB.moveUp(PADDLE_MOVE_DISTANCE)
          if keys[pygame.K_DOWN]:
               paddleB.moveDown(PADDLE_MOVE_DISTANCE)

          # --------------------------------------------------------------------
          # Game Logic!
          # --------------------------------------------------------------------

          all_sprites_list.update()

          #Check if the ball is bouncing against any of the 4 walls:

          # right wall: point for A
          if ball.rect.x > WIDTH - PADDLE_WIDTH - BALL_SIZE/2:
               scoreA += 1
               ball.reset()
               ball.bounce()

          # left wall: point for B
          if ball.rect.x < 0:
               scoreB += 1
               ball.reset()
               ball.bounce()

          # lower wall
          if ball.rect.y > HEIGHT - BALL_SIZE:
               ball.bounce_y()

          # upper wall
          if ball.rect.y < 0:
               ball.bounce_y()

          #Detect collisions between the ball and the paddles
          if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
               ball.bounce()

          # --------------------------------------------------------------------
          # Drawing the screen
          # --------------------------------------------------------------------

          # First, clear the screen to black.
          screen.fill(BLACK)

          # Draw the net
          pygame.draw.line(screen, WHITE, [(WIDTH/2)-(NET_WIDTH/2), 0], [(WIDTH/2)-(NET_WIDTH/2), HEIGHT], NET_WIDTH)

          # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
          all_sprites_list.draw(screen)

          # Display scores:
          font = pygame.font.Font(None, int(HEIGHT/8))
          scoreA_text = font.render(str(scoreA), 1, WHITE)
          scoreA_text_width = scoreA_text.get_size()[0]
          screen.blit(scoreA_text,(int(WIDTH*1/3)-scoreA_text_width/2,10))
          scoreB_text = font.render(str(scoreB), 1, WHITE)
          scoreB_text_width = scoreB_text.get_size()[0]
          screen.blit(scoreB_text,(int(WIDTH*2/3)-scoreB_text_width/2,10))

          # Go ahead and update the screen with what we've drawn.
          pygame.display.flip()

          # Limit to 60 frames per second
          clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
