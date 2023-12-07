import pygame
from pygame.locals import *
width, height = 1280, 720
screen = pygame.display.set_mode((width,height))

#陷阱機關
class trap :
    species = "for trap create"
    def __init__(self, trap_x, trap_y, image_name, player_x, player_y, map_x, height) :
        self.trap_x = trap_x
        self.trap_y = trap_y
        self.image_name = image_name
        self.player_x = player_x
        self.player_y = player_y
        self.map_x = map_x
        # 加載圖片(.convert_alpha() << 背景透明化用的)
        self.image_trap = pygame.image.load(image_name).convert_alpha()
        # 獲取圖像矩形對象
        self.rect_trap = self.image_trap.get_rect()
        # 獲取圖像初始位置
        self.rect_trap.topleft = (trap_x - map_x, height - trap_y)
        # 創建精靈
        self.sprite_trap = pygame.sprite.Sprite()

        # 精靈碰撞
    def trap_collision(self) :
        if pygame.sprite.collide_mask(self.sprite_trap):
            print("還沒做，不要吵")
       
        # 繪製圖片
    def trap_draw (self) :
        screen.blit(self.image_trap, self.rect_trap.topleft)
    
        # 更新與繪製精靈
    def sprite_draw (self) :
        sprite = pygame.sprite.Group(self.sprite_trap)
        sprite.update()
        sprite.draw(screen)


import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('.\Cat-Mario\超級瑪利\cat.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('.\Cat-Mario\超級瑪利\cat.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

all_sprites = pygame.sprite.Group()
player = Player(50, 50)
obstacle = Obstacle(200, 200)
all_sprites.add(player, obstacle)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()

    # 碰撞检测
    collisions = pygame.sprite.spritecollide(player, [obstacle], False, pygame.sprite.collide_mask)
    if collisions:
        print("像素级碰撞发生！")

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)


        


