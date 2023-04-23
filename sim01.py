import pygame
from pygame.locals import *
from pygame.math import Vector2
from bacteria01 import Bacteria
from food import Food
import random

BG_COLOR = (0,0,0)
FPS = 100

class App:

    def __init__(self):
        self._running = True
        self._display = None
        self.size = self.width, self.heigth = 800,800
        self.objects = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.MAX_FOOD_TIMER = 1

    def on_init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self._display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._background = pygame.Surface(self._display.get_size())
        self._background.fill(BG_COLOR)
        self._display.blit(self._background, (0,0))
        pygame.display.set_caption('Sim 01')
        self._running = True
        self.food_timer = 0.0
        for i in range(0,10):
            self.objects.add( Bacteria(i,(random.randint(0, self.width),random.randint(0, self.heigth)),self._display) )
           # self.foods.add( Food((random.randint(0, self.width),random.randint(0, self.heigth)),100,self._display) )



    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                #get one random object
                o = self.objects.sprites()[random.randint(0,len(self.objects)-1)]
                self.objects.add(o.multiply())

    def on_loop(self):
        if len(self.objects) == 0:
            self._running = False

        self.objects.update(1./FPS, self.objects)
        self.foods.update()
        self.processObjectCollisions()
        self.processFoodCollisions()
        self.processFood()
        

    def on_render(self):
        #pygame.display.flip()
        #pygame.display.update()
        self.objects.clear(self._display, self._background)
        self.objects.draw(self._display)
        self.foods.clear(self._display, self._background)
        self.foods.draw(self._display)
        pygame.display.update()
        self.clock.tick(FPS)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running == False
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def circle_collision(self, left, right):
        if left != right:
            distance = Vector2(left.rect.center).distance_to(right.rect.center)
            return distance < left.radius
        else:
            return False
        
    def processObjectCollisions(self):
        collided_sprites = pygame.sprite.groupcollide(
            self.objects, self.objects, False, False,
            collided=self.circle_collision)
        for collided_sprite in collided_sprites:
            collided_sprite.collision(collided_sprites)

    def processFoodCollisions(self):
        collided_sprites = pygame.sprite.groupcollide(
            self.objects, self.foods, False, False,
            collided=self.circle_collision)
        for collided_sprite in collided_sprites:
            collided_sprite.foundFood(collided_sprites)

    def processFood(self):
        self.food_timer += 1./FPS
        if self.food_timer > 1.0:
            self.foods.add( Food((random.randint(5, self.width-5),random.randint(5, self.heigth-5)),random.randint(1,100),self._display))
            self.food_timer = 0.0

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()