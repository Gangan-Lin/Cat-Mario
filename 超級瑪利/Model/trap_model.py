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



        