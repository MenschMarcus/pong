import pygame
from random import randint

BLACK = (0,0,0)

MAX_SPEED = 20
MIN_SPEED = 2
SPEEDUP_FACTOR = 1.5

class Ball(pygame.sprite.Sprite):
     #This class represents a ball. It derives from the "Sprite" class in Pygame.

     def __init__(self, color, width, height, center):
          # Call the parent class (Sprite) constructor
          super().__init__()

          # set members: center of screen
          self.center = center

          # Pass in the color of the ball, its width and height.
          # Set the background color and set it to be transparent
          self.image = pygame.Surface([width, height])
          self.image.fill(BLACK)
          self.image.set_colorkey(BLACK)

          self.velocity = [0, 0]

          # Draw the ball (a rectangle!)
          pygame.draw.rect(self.image, color, [0, 0, width, height])

          self.velocity = [randint(4,8),randint(-8,8)]

          # Fetch the rectangle object that has the dimensions of the image.
          self.rect = self.image.get_rect()

     def reset(self):
          self.rect.x = self.center[0]
          self.rect.y = self.center[1]

     def update(self):
          self.rect.x += self.velocity[0]
          self.rect.y += self.velocity[1]

     def bounce(self):
          self.velocity[0] = -self.velocity[0]
          self.velocity[1] = randint(-5,5)

     def bounce_y(self):
          self.velocity[1] = -self.velocity[1]

     def speedup(self):
          # calculate direction (y = m*x -> m = y/x)
          direction = self.velocity[1] / self.velocity[0]

          # increase speed in x-direction
          self.velocity[0] *= SPEEDUP_FACTOR

          # clip speed to max speed
          if self.velocity[0] > MAX_SPEED:
               self.velocity[0] = MAX_SPEED
          if self.velocity[0] < -MAX_SPEED:
               self.velocity[0] = -MAX_SPEED

          # maintain direction (y = m*x)
          self.velocity[1] = direction * self.velocity[0]

     def speeddown(self):
          # calculate direction (x/y relation)
          direction = self.velocity[1] / self.velocity[0]

          # increase speed in x-direction
          self.velocity[0] *= 1/SPEEDUP_FACTOR

          # clip speed to min / max speed
          # ensure that speed is never in between [-3 .. +3]
          if self.velocity[0] < MIN_SPEED and self.velocity[0] > 0:
               self.velocity[0] = MIN_SPEED
          if self.velocity[0] > -MIN_SPEED and self.velocity[0] < 0:
               self.velocity[0] = -MIN_SPEED

          # maintain direction (y = m*x)
          self.velocity[1] = direction * self.velocity[0]
