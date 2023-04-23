import pygame
import random
import sys

FPS = 100



class Food(pygame.sprite.Sprite):
    def __init__(self, position, energy, surface):
        super(Food, self).__init__()
        self.radius = 10
        self.color = (0,255,0)
        self.position = list(position) or [0, 0]
        self.energy = energy
        
        self.display = surface
        #self.image = pygame.image.load(image_path)
        self.bounds = (self.display.get_size()[0] - self.radius,
                       self.display.get_size()[1] - self.radius)

        self.image = pygame.Surface(2*[self.radius*2])
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, 2*(self.radius,), self.radius)

    
    def update(self, dt, objects):
        super(Food, self).update()
        self.rect.center = self.position
        if self.energy <= 0:
            self.kill()