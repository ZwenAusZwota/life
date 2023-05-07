import pygame
from helper import SimConstants


class Food(pygame.sprite.Sprite):
    def __init__(self, position, energy, surface):
        super(Food, self).__init__()
        self.type = SimConstants.OTypeFood
        self.radius = 2
        self.color = (0,255,0)
        self.position = list(position) or [0, 0]
        self.energy = energy
        self.age = 0
        
        self.display = surface
        #self.image = pygame.image.load(image_path)
        self.bounds = (self.display.get_size()[0] - self.radius,
                       self.display.get_size()[1] - self.radius)

        self.image = pygame.Surface(2*[self.radius*2])
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, self.color, pygame.Rect(0,0,self.radius*2,self.radius*2))

    
    def update(self, dt, objects):
    #def update(self):
        super(Food, self).update()
        self.rect.center = self.position
        self.age += 1*dt
        if self.energy <= 0 or self.age > 100:
            self.kill()
            
    def decEnergy(self):
        self.energy = 0
        self.kill()

    def collision(self,sprites):
        keys = list(sprites.keys())
        #print("Food Collision")
        # 0 bin ist das hiesige Objekt, 1 das andere

        #if keys[0].energy > keys[1].energy:
        #    keys[0].energy +=1
        #    keys[1].energy -=2
        #sys.exit()