import pygame
import random
import sys

FPS = 100



class Bacteria(pygame.sprite.Sprite):
    def __init__(self, id, position, surface, color=(255,0,0)):
        super(Bacteria, self).__init__()
        self.id = str(id)
        self.type = "LF"
        self.radius = 10
        self.color = color
        self.position = list(position) or [0, 0]
        self.direction = [0, 0]
        #self.font = pygame.font.Font('freesansbold.ttf', 10)
        
        self.display = surface
        #self.image = pygame.image.load(image_path)
        self.bounds = (self.display.get_size()[0] - self.radius,
                       self.display.get_size()[1] - self.radius)

        self.image = pygame.Surface(2*[self.radius*2])
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, 2*(self.radius,), self.radius)

        #Attribute, die das Verhalten steuern
        #die fetten sind die Werte, die innerhalb einer GEneration fix sind
        self.SPEED = 100 #<- das muss pro Individuum ein fixer wert seinm der am anfang zufällig sein kann
        self.MAX_ENERGY = 100
        self.SPLIT_ENERGY_MULTIPLIKATOR = 0.5
        self.SPLIT_TIMER = 5 #Days
        self.MIN_SPLIT_ENERGY = 50


        #die folgenden Attribute sind diejenigen, die dem Objekt selbst gehören
        self.health = 100
        self.energy = self.MAX_ENERGY
        self.lastSplit = 0
        self.children = 0
        self.age = 0

        self.VEL = [random.randint(-self.SPEED, self.SPEED), random.randint(-self.SPEED, self.SPEED)] #das ist ein Fester Wert pro Individuum
        self.velocity = self.VEL
        self.direction = [random.randint(0 + self.radius, self.bounds[0]), random.randint(0 + self.radius, self.bounds[1])]
    
    def update(self, dt, objects):
        super(Bacteria, self).update()
        self.age += 1*dt
        self.detectFood(objects)
        if self.canMultiply():
            objects.add(self.multiply())
        
        sumEnergy = 0
        for i in [0, 1]:
            sumEnergy += self.velocity[i]
            self.position[i] += self.velocity[i] * dt

            if self.position[i] < self.radius:
                self.position[i] = self.radius
                self.velocity[i] *= -1

            elif self.position[i] > self.bounds[i]:
                self.position[i] = self.bounds[i]
                self.velocity[i] *= -1

        self.rect.center = self.position
        # #TExt
        # text = self.font.render(f'{int(self.energy)}', True, (0,255,0), (0,0,255))
        # textRect = text.get_rect()
        # textRect.center = self.position
        # self.image.blit(text,textRect)
        # #text ende
        self.energy -= sumEnergy/10*dt
        #self.color = (int(self.energy),0,0)
        if self.energy <= 0:
            #print(f'{self.id} died at age {self.age}')
            self.kill()

    def collision(self,sprites):
        keys = list(sprites.keys())
        # 0 bin ist das hiesige Objekt, 1 das andere
        if len(keys) == 2:
            if keys[0].energy > keys[1].energy:
                keys[0].addEnergy(1)
                keys[1].addEnergy(-1)
        #sys.exit()

    def canMultiply(self):
        if self.energy >= self.MIN_SPLIT_ENERGY and self.age > (self.lastSplit + self.SPLIT_TIMER):
            return True
        return False

    def multiply(self):
        #voraussetzunge zur Vermehrung prüfen
        #if ...
        self.lastSplit = self.age
        self.children += 1
        return Bacteria(self.id+"_"+str(self.children), self.position, self.display, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    
    def foundFood(self,sprites):
        keys = list(sprites.keys()) #Bakterie
        items = list(sprites.items()) #Futter
        food = items[0][1][0]
        energy = min(food.energy,5)
        self.addEnergy( energy )
        food.decEnergy( energy )
        #print(f'{self.id}: {int(self.energy)}')
        self.updateVelocity()

    def detectFood(self,objects):
        foodList = [e for e in objects if e.type == "FOOD"]
        foodList.sort(key=lambda e: pow(e.rect.x-self.rect.x, 2) + pow(e.rect.y-self.rect.y, 2))
        #if len(foodList) > 0:
        #food = min(
        #    [e for e in objects if e.type == "FOOD"], 
        #    key=lambda e: pow(e.rect.x-self.rect.x, 2) + pow(e.rect.y-self.rect.y, 2))
    
    def addEnergy(self,energy):
        self.energy += energy

    def updateVelocity(self):
        dx = self.direction[0] - self.position[0]
        dy = self.direction[1] - self.position[1]
        self.velocity = [dx,dy]
    
