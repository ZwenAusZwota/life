import pygame
import random
import sys
import math
from genome import Genome
from neat import NEAT
from helper import SimConstants
from pprint import pprint

FPS = 100
WeightMutationChance = 0.8
AddNodeChance = 0.03
AddConnectionChance = 0.05


class Bacteria(pygame.sprite.Sprite):
    def __init__(self, id, position, surface, genome, energy=45, color=(255,0,0)):
        super(Bacteria, self).__init__()
        self.id = str(id)
        self.type = SimConstants.oTypeLife
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
        pygame.draw.circle(self.image, self.color, 2*(self.radius,), self.radius, 1)

        #Attribute, die das Verhalten steuern
        #Input:Age, Speed, Energy, posX, posy, nearest_object_x, noby, nobtype, nobenergy
        #Output: directionX, directionY, speed, split
        self.genome = genome
        self.neat = NEAT(self.genome)
        #print(f'Neurons:{len(genome.nodeList)}, Connections{len(genome.connectionKeys)}')

        #die fetten sind die Werte, die innerhalb einer GEneration fix sind
        self.speed = 100 #<- das muss pro Individuum ein fixer wert seinm der am anfang zufällig sein kann
        self.MAX_ENERGY = 100
        self.MAX_SPEED = 100
        self.SPLIT_TIMER = 2 #Days
        self.MIN_SPLIT_ENERGY = 25
        self.SPLIT_ENERGY_MULTIPLIKATOR = 0.5
        self.EPOCHS = 150


        #die folgenden Attribute sind diejenigen, die dem Objekt selbst gehören
        self.health = 100
        self.energy = energy
        self.lastSplit = 0
        self.children = 0
        self.age = 0
        self.moveTimer = 0
        self.input = None
        self.output = None

        
        #self.velocity = [random.randint(0,100),random.randint(0,100)]
        self.direction = [random.randint(0 + self.radius, self.bounds[0]), random.randint(0 + self.radius, self.bounds[1])]
        #self.direction = self.position
        self.updateVelocity()

    
    def update(self, dt, objects):
        super(Bacteria, self).update()
        self.age += 1*dt
        nearestObject = self.detectOthers(objects)
        #self.detectFood(food)
        sumEnergy = 100
        if nearestObject:
            self.input = [
                self.age, self.speed, self.energy,
                int(self.position[0]), int(self.position[1]),
                int(nearestObject.position[0]), int(nearestObject.position[1]), nearestObject.type, nearestObject.energy
            ]
            self.output = self.neat.getOutput(self.input)
            self.direction[0] = int(self.output[0])
            self.direction[1] = int(self.output[1])
            self.speed = self.output[2]
            if self.speed > self.MAX_SPEED:
                self.speed = self.MAX_SPEED
            # print(input)
            # print(output)
            # print('------------------------------------------')
            self.updateVelocity()
            mt = 0
            for i in [0, 1]:
                sumEnergy += abs(self.velocity[i])
                mt += abs(self.velocity[i])
                self.position[i] += self.velocity[i] * dt

                if self.position[i] < self.radius:
                    self.position[i] = self.radius
                    self.velocity[i] *= -1

                elif self.position[i] > self.bounds[i]:
                    self.position[i] = self.bounds[i]
                    self.velocity[i] *= -1
                
            if mt == 0:
                self.moveTimer += 1
            else:
                self.moveTimer = 0
            if self.canMultiply(objects, int(self.output[3]) ):
                objects.add(self.multiply())
        
        
        
        self.rect.center = self.position
        # #TExt
        # text = self.font.render(f'{int(self.energy)}', True, (0,255,0), (0,0,255))
        # textRect = text.get_rect()
        # textRect.center = self.position
        # self.image.blit(text,textRect)
        # #text ende
        self.energy -= sumEnergy/100*dt
        #self.color = (int(self.energy),0,0)
        if self.energy <= 1 or self.moveTimer == 1000 or self.age > 100 :
            #print(f'{self.id} died at age {self.age}')
            #pprint(vars(self))
           # if self.age > 90:
            with open(f'{len(self.genome.nodeList)}-{len(self.genome.connectionKeys)}-{self.id}.json', 'w') as fp:
                fp.write(self.genome.toJSON())
            self.kill()

    def collision(self,sprites):
        keys = list(sprites.keys())
        # 0 bin ist das hiesige Objekt, 1 das andere
        for s in sprites:
            if s == self:
                pass
            elif s.type == SimConstants.OTypeFood:
                oe = self.energy
                energy = s.energy
                self.addEnergy( energy )
                #print(f'{self.id}: {oe} -> {self.energy}')
                s.decEnergy( )
                #wenn futter gefunden wurde, dann den letzten output und input verwenden um das Netz mittels Backpropagation zu stärken
                self.train()
            elif s.type == SimConstants.oTypeLife:
                if self.age < 5 or s.age < 5:
                    continue
                # if self.id[0] == s.id[0]: #eigene Familie wird nicht gefressen
                #     continue
                if s.energy < self.energy: #ich zuerst
                    diff = ( self.energy - s.energy )/2
                    self.addEnergy(diff)
                    s.addEnergy(-diff)
                else:
                    diff = ( s.energy - self.energy )/2
                    self.addEnergy(-diff)
                    s.addEnergy(diff)
            
                
        #sys.exit()
    def train(self):
        pass

    def canMultiply(self, objects, split=0):
        list = [e for e in objects if e.type == SimConstants.oTypeLife]
        #if (self.energy > self.MIN_SPLIT_ENERGY and self.age > (self.lastSplit + self.SPLIT_TIMER or split>0)):
        if (self.energy > self.MIN_SPLIT_ENERGY and len( list )<200 and self.age > self.lastSplit+self.SPLIT_TIMER):# or split > 0):
            return True
        return False

    def multiply(self):
        #voraussetzunge zur Vermehrung prüfen
        #if ...
        self.lastSplit = self.age
        self.children += 1
        energy = self.SPLIT_ENERGY_MULTIPLIKATOR * self.energy
        self.energy -= energy
        #mutate my genome
        r = random.random()
        if r < WeightMutationChance:
            self.genome.mutate(r)
        elif r < WeightMutationChance + AddNodeChance:
            self.genome.addNodeMutation()
        elif r < WeightMutationChance + AddNodeChance + AddConnectionChance:
            self.genome.addConnectionMutation()
        return Bacteria(self.id+"_"+str(self.children), self.position, self.display,self.genome, energy=energy, color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    
    # def foundFood(self,sprites):
    #     keys = list(sprites.keys()) #Bakterie
    #     items = list(sprites.items()) #Futter
    #     food = items[0][1][0]
    #     #energy = min(food.energy,5)
    #     energy = food.energy
    #     self.addEnergy( energy )
    #     food.decEnergy( )
    #     #print(f'{self.id}: {int(self.energy)}')
        

    # def detectFood(self,objects):
    #     foodList = [e for e in objects if e.type == SimConstants.OTypeFood]
    #     foodList.sort(key=lambda e: pow(e.rect.x-self.rect.x, 2) + pow(e.rect.y-self.rect.y, 2))
    #     if len(foodList) > 0:
    #         self.direction = foodList[0].position
    #         self.updateVelocity()
    #     #food = min(
    #     #    [e for e in objects if e.type == "FOOD"], 
    #     #    key=lambda e: pow(e.rect.x-self.rect.x, 2) + pow(e.rect.y-self.rect.y, 2))
    
    def detectOthers(self,objects):
        list = [e for e in objects]
        list.sort(key=lambda e: pow(e.rect.x-self.rect.x, 2) + pow(e.rect.y-self.rect.y, 2))
        if len(list)>1:
            return list[1]
        return None
            

    def addEnergy(self,energy):
        self.energy += energy
        if self.energy > self.MAX_ENERGY:
            self.energy = self.MAX_ENERGY

    def updateVelocity(self):
        dx = self.direction[0] - self.position[0]
        dy = self.direction[1] - self.position[1]
        if dx > self.bounds[0]:
            dx = self.bounds[0]
        if dy > self.bounds[1]:
            dy = self.bounds[1]
        if dx != 0 and dy != 0:
            d = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
            vx = int(self.speed/d*dx)
            vy = int(self.speed/d*dy)
            self.velocity = [vx,vy]
        else:
            self.velocity = [0,0]
    
