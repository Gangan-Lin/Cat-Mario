# 更新報告
    # 我懶得寫
    # 測試時拜託先切成英文


# 導入sys & pygame導入sys & pygame
import sys
import pygame
import math
import time
import os
import glob 
from pygame.locals import QUIT
# 初始化
pygame.init()
# 設定畫面邊界大小
width, height = 1280, 720
# 顏色
white = (255, 255, 255)
blue = (0, 0, 255 )
black = (0, 0, 0)
red = (255, 0, 0)
# 設定視窗大小
screen = pygame.display.set_mode((width,height))        # set_mode << 設定視窗大小
pygame.display.set_caption('超級瑪莉')      # set_caption('視窗名稱') << 設定視窗名稱
# 填滿視窗(顏色(R, G, B))
screen.fill(white)      #fill << 填滿
    # 設定各項數值
# 字體大小
font_size_v = 20                            # version字體大小
death_time_v = 60 
# 宣告 NAME = pygame.font.SysFont(字體,字體大小)     # SysFont << 設定字體(這裡只自體本身，如字體(新細明體, 標楷體)和字體大小
Test = pygame.font.SysFont(None,20)
Version = pygame.font.SysFont(None,font_size_v)
Death_time = pygame.font.SysFont(None, death_time_v)
# 版本(寫好玩的)
version = Version.render("V1.0.0.7", True, (0, 0, 0))     # 放在這裡純粹方便改 (V版本.大更新.小更新.測試版本)

# 各項參數 >> 方便知道什麼變數幹嘛用的
clock_hz = 60                                           # 就是clock(問題太多，先暫訂60就好)
    # 迴圈階段
loopstage = 0                              
gamestage = 0                              # 遊戲階段(關卡 暫停(-1) 主畫面 死亡)
pause = 0
    # 地圖x(以最左為0)
map_x = 0                                   
    # 腳色最左能到的距離
max_x = width // 2
    # 判定
collision_x = 0                             # 碰撞判定 x     1:碰撞點為角色右邊  0:無碰撞    -1:碰撞點為物體左邊
collision_y = 0                             # 碰撞判定 y     1:碰撞點為角色上方  0:無碰撞    -1:碰撞點為物體下方
collision_trap = 0
stand = 0                                   # 站立判定
jump = 0                                    
hold = 0                                    # 跳躍鍵按下時長判定
     # 變數
velocity_x = 0                              # x方向速度
velocity_y = 0                              # y方向速度
    # 遊戲常數
velocitymax_x = 4 * (60 / clock_hz)                     # x方向最大速度
velocitymini_x = 0.08 * (60 / clock_hz)                 # x方向最小速度
accelerationadd_x = 0.2 * (60 / clock_hz)* (60 / clock_hz)               # x方向操縱加速度
acceleration_penalty = 0.8                             # 空中速度懲罰倍率 (影響在空中時的x方向加速度) 
resistance_x = 0.3 * (60 / clock_hz)* (60 / clock_hz)                    # x方向基礎阻力 ( < accelerationadd_x/2)
jump_delay = 10 * (clock_hz / 60)                       # 長按大跳時長判定 (5~20就好)
jump_award = 0.6                                        # 大跳倍數(0.55約等於沒有，別問我為什麼會這樣，我想破頭都還沒想出來)
jump_second = 1                                         # 第二段跳倍數
jump_penalty = 1                                        # 第二段跳對x的速度懲罰(基本上就是在第二段跳時對當前速度影響的倍率)
jump_y = 5.05 * (60 / clock_hz)                                              # y方向跳躍加速度
gravitational_acceleration = 0.18 * (60 / clock_hz)* (60 / clock_hz)     # 重力加速度
    # 規則
real = 0 
double_jump = 1                             # 二段跳開關
# 圖片路徑
    # map image 路徑
map_0_image_path = '.\超級瑪利\image\map_0\map_0.png'
map_1_image_path = '.\超級瑪利\image\map_1\maptest1.png'
map_2_image_path = '.\超級瑪利\image\player\cat_right.png'
    # pause image 路徑
pause_image_path = '.\超級瑪利\image\pause\pause_image.png'
    # player image 路徑
player_image_right = '.\超級瑪利\image\player\cat_right.png'
player_image_left = '.\超級瑪利\image\player\cat_left.png'
player_image_mid = '.\超級瑪利\image\player\cat_mid.png'
    # nothing image path
nothing_image_path =  '.\超級瑪利\image\O\O.png'

button_push = 0 

class physics :
    
    def __init__(self, object_map, trap_map, player_sizex, player_sizey, player_x, player_y, map) :
        # player 基礎設置
        self.player_sizex = player_sizex
        self.player_sizey = player_sizey
        # player 判定
        self.collision_x = collision_x
        self.collision_y = collision_y
        self.collision_trap1 = collision_trap
        self.hold = hold
        self.stand = stand
        # player 變數
        self.player_x = player_x
        self.player_y = player_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        #player 常數
        self.velocitymax_x = velocitymax_x
        self.velocitymini_x = velocitymini_x
        self.accelerationadd_x = accelerationadd_x
        self.acceleration_penalty = acceleration_penalty
        self.jump_delay = jump_delay
        self.jump_award = jump_award                                        
        self.jump_second = jump_second                                         
        self.jump_penalty = jump_penalty                                        
        self.jump_y = jump_y                                             
        # 就是key寫成這樣方便調用而已
        self.key_left = 0
        self.key_right = 0
        self.key_up = 0
        # loopstage setting
        self.loopstage = loopstage
        # map 設定
        self.map_x = map_x 
        self.object_map = object_map # 腳色當下所在的地圖
        self.trap_map = trap_map
        self.map = map
        self.map_image = Map(map_0_image_path)
        self.trap_all = {}
        # 規則
        self.jump = jump
        self.real = real
        self.double_jump = double_jump
        self.max_x = max_x
        # 創建玩家精靈
        self.player = Player(self.player_x, self.player_y)
        # 紀錄死亡次數
        self.death_time = 0 
        # 終點
        self.end_x = 10000
    def keypress_model(self) :
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] :
            self.key_left = 1
            player_1.player.change_image(player_image_left)
        else :
            self.key_left = 0
        if keys[pygame.K_RIGHT] :
            self.key_right = 1
            player_1.player.change_image(player_image_right)
        else :
            self.key_right = 0
        if keys[pygame.K_UP] :
            self.key_up = 1
        else :
            self.key_up = 0
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] :
            player_1.player.change_image(player_image_mid)

    def keymove_model (self) : 
        acceleration_x = 0      
        acceleration_y = 0
        if key_1.key_left == 1 and key_1.key_right == 0 and self.velocity_x > self.velocitymax_x*-1 :     # 當向左鍵按下且向左速度數值 < 最大速度值
            if self.stand == 1 :
                acceleration_x = self.accelerationadd_x*-1                               # 加速度直設為 負的 accelerationadd_x << x方向操縱加速度
            else :
                acceleration_x -= self.accelerationadd_x*self.acceleration_penalty          # 在空中時乘上速度懲罰
        elif key_1.key_left == 1 and key_1.key_right == 0 :                                     # 當向左鍵按下且向左速度大於或等於最大速讀值
            self.velocity_x = self.velocitymax_x*-1                                           # 將速度設為 負的 velocitymax_x << x方向最大速度
        if key_1.key_right == 1 and key_1.key_left == 0 and self.velocity_x < self.velocitymax_x :        # 當向右鍵按下且向右速度數值 < 最大速度值
            if self.stand == 1 :
                acceleration_x = self.accelerationadd_x                                  # 加速度直設為 正的 accelerationadd_x << x方向操縱加速度
            else :
                acceleration_x = self.accelerationadd_x*self.acceleration_penalty             # 在空中時乘上速度懲罰
        elif key_1.key_right == 1 and key_1.key_left == 0 :                                     # 當向右鍵按下且向右速度大於或等於最大速讀值
            self.velocity_x = self.velocitymax_x                                              # 將速度設為 正的 velocitymax_x << x方向最大速度
        if key_1.key_up == 1 and self.hold >= 1 :                                              # 當向上鍵按下且 stand >= 1 << 跳躍鍵按下時長判定
            self.hold = self.hold - 1                                                         # 剩下的就是用 if 判斷式判斷第幾次跳躍及常按向上與方放開重案的二段跳
            if  self.hold == 2 and self.jump == 1:
                acceleration_y = self.jump_y*self.jump_award*-1                               # 乘上大跳獎勵
                self.jump = 0
                self.hold = 0
        elif self.jump == 1 :
            self.hold = 2
        elif self.jump == 2 and self.stand == 0 :
            self.jump = 1 
        if self.hold == 119  and self.jump == 2 :
            acceleration_y = self.jump_y*-1
            self.jump = 1
            self.hold = self.jump_delay + 2
        if self.hold == 1 and self.jump == 1 and self.double_jump == 1:
            self.velocity_y = 0
            self.velocity_x = self.velocity_x*jump_penalty
            acceleration_y = self.jump_y*self.jump_second*-1                                 # 乘上第二段跳倍數
            self.jump = 0
            self.hold = 0
        self.velocity_x = self.velocity_x + acceleration_x         # 將加速度導入速度
        self.velocity_y = self.velocity_y + acceleration_y + gravitational_acceleration

        # 阻力模組
    def resistance_model (self) :
        if self.real == 1 and self.stand == 0 :
            self.real = 1
        else :
            if self.velocity_x >= self.velocitymini_x :
                self.velocity_x = self.velocity_x - resistance_x*(abs(self.velocity_x)/(self.velocitymax_x))            # 線性調整阻力大小
                if key_1.key_right == 1 and key_1.key_left == 1 :
                    self.velocity_x = self.velocity_x - resistance_x*(abs(self.velocity_x)/(self.velocitymax_x*0.375))  # 煞車用的
                elif key_1.key_right == 1 :
                    self.velocity_x = self.velocity_x + resistance_x*(abs(self.velocity_x)/(self.velocitymax_x))
            if self.velocity_x <= self.velocitymini_x :
                self.velocity_x = self.velocity_x + resistance_x*(abs(self.velocity_x)/(self.velocitymax_x))
                if key_1.key_right == 1 and key_1.key_left == 1 :
                    self.velocity_x = self.velocity_x + resistance_x*(abs(self.velocity_x)/(self.velocitymax_x*0.375))
                elif key_1.key_left == 1 :
                    self.velocity_x = self.velocity_x - resistance_x*(abs(self.velocity_x)/(self.velocitymax_x))
            if self.velocity_x < self.velocitymini_x and self.velocity_x > self.velocitymini_x*-1 :
                self.velocity_x = 0
            if self.velocity_x > (self.velocitymax_x-self.velocitymini_x) :
                self.velocity_x = self.velocitymax_x
            if self.velocity_x < (self.velocitymax_x-self.velocitymini_x)*-1 :
                self.velocity_x = self.velocitymax_x*-1

        # 移動模組
    def move_model(self):
        if game_loopset.loopstage == 4 :
            if self.collision_x == 0 :
                self.player_x = self.player_x + math.copysign(0.01, self.velocity_x)
                if self.player_x + self.player_sizex > self.max_x :
                    self.player_x = self.player_x - math.copysign(0.01, self.velocity_x)
                    self.map_x = self.map_x + math.copysign(0.01, self.velocity_x)   
            elif self.collision_x == -1 or self.collision_x == 1 :
                self.velocity_x = 0 
        if game_loopset.loopstage == 5 :
            if self.collision_y == 0 :
                self.player_y = self.player_y + math.copysign(0.01, self.velocity_y)
            elif self.collision_y == -1 or self.collision_y == 1 :
                self.velocity_y = 0
        if self.collision_y == 0 or self.collision_y == 1 :
            self.stand = 0
        if self.collision_y == -1 :
            (self.hold, self.jump, self.stand) = (120, 2, 1)

        # 碰撞判斷模組                                                                                                      
    def collision_model (self) :
        create_time_map = len(self.object_map)
        if game_loopset.loopstage == 4 :
            player_x_here = self.player_x + math.copysign(0.01, self.velocity_x)
            for time_c in range(0, create_time_map,1) :
                player_collision_box = pygame.Rect(player_x_here, self.player_y, self.player_sizex, self.player_sizey) 
                if self.collision_x == 0 :
                    time_c_int = round(time_c, 0)
                    object_collision_box = pygame.Rect(self.object_map[time_c_int][0] - self.map_x, (height - self.object_map[time_c_int][1]), self.object_map[time_c_int][2], self.object_map[time_c_int][3])
                    if  player_collision_box.colliderect(object_collision_box) : # 碰撞(偵測x) >> 左右不影響
                        self.collision_x = 1
        if game_loopset.loopstage == 5 :
            player_y_here = self.player_y + math.copysign(0.01, self.velocity_y)
            for time_c in range(0, create_time_map,1) :   
                time_c_int = round(time_c, 0)
                player_collision_box = pygame.Rect(self.player_x, player_y_here, self.player_sizex, self.player_sizey)
                object_collision_box = pygame.Rect(self.object_map[time_c_int][0] - self.map_x, (height - self.object_map[time_c_int][1]), self.object_map[time_c_int][2], self.object_map[time_c_int][3])
                if collision_y == 0 :
                    if player_collision_box.colliderect(object_collision_box) and (player_y_here) < (height - self.object_map[time_c_int][1]) : # 碰撞(偵測y) >> 上(物體的)
                        self.collision_y = -1
                    elif player_collision_box.colliderect(object_collision_box) : # 碰撞(偵測y) >> 下(物體的)
                            self.collision_y = 1

        # 碰撞方塊繪製模組
    def collisionbox_draw_model (self) :
        create_time = len(self.object_map)
        for time_c in range(0, create_time, 1) :
            time_c_int = round(time_c, 0)
            pygame.draw.rect(screen, blue, (self.object_map[time_c_int][0] - self.map_x, (height - self.object_map[time_c_int][1]), self.object_map[time_c_int][2], self.object_map[time_c_int][3]), 2)

        # boundary
    def boundary (self) :
        import math
        floor = 1
        if game_loopset.loopstage == 4 :
            if self.player_x + math.copysign(0.01, self.velocity_x) >= 0 :
                self.collision_x = 0
            elif self.player_x + math.copysign(0.01, self.velocity_x) <= 0:
                self.collision_x = -1
        if game_loopset.loopstage == 5 and floor == 1:
            if self.player_y + math.copysign(0.01, self.velocity_y) <= (height - self.player_sizey) :
                self.collision_y = 0
            elif self.player_y + math.copysign(0.01, self.velocity_y) >= (height - self.player_sizey) :
                self.collision_y = -1

        # 陷阱建立模組
    def trap_create_model(self) :
        self.trap_all = {}
        map_trap = self.trap_map
        # 迴圈建立變數
        for i in range(0, len(map_trap)):
            trap_name = f"trap_{i}"
            if map_trap[i][0] == 1 :
                self.trap_all[trap_name] = Trap(map_trap[i][1], map_trap[i][2], map_trap[i][3], map_trap[i][4], map_trap[i][5], map_trap[i][6], map_trap[i][7], map_trap[i][8], map_trap[i][9], map_trap[i][10], map_trap[i][11], map_trap[i][12])
                all_sprites_trap.add(self.trap_all[trap_name])
            if map_trap[i][0] == 2 :
                self.trap_all[trap_name] = NPC_Trap(map_trap[i][1], map_trap[i][2], map_trap[i][3], map_trap[i][4], map_trap[i][5], map_trap[i][6], map_trap[i][7], map_trap[i][8])
                all_sprites_trap.add(self.trap_all[trap_name])
        # 陷阱碰撞判斷模組
    def collision_trap1_model(self) :
        collision_trap1_list = pygame.sprite.spritecollide(player_1.player, all_sprites_trap, False)
        if len(collision_trap1_list) >= 1 :
            self.collision_trap1 = 1 
            
        # 陷阱觸發箱繪製模組
    def trap_triggerbox_draw_model (self) :
        create_time = len(self.trap_map)
        for time_c in range(0, create_time, 1) :
            time_c_int = round(time_c, 0)
            if self.trap_map[time_c_int][0] == 1 :
                pygame.draw.rect(screen, red, (self.trap_map[time_c_int][3] - self.map_x, (height - self.trap_map[time_c_int][4]), self.trap_map[time_c_int][5], self.trap_map[time_c_int][6]), 2)
    
        # 地圖碰撞判斷
    def map_collision (self) :
        self.collision_x = 0
        self.collision_y = 0
        self.boundary()
        self.collision_model()
        self.collision_trap1_model()

        # 繪製玩家
    def player_draw (self) :
        pygame.draw.rect(screen, blue, (self.player_x, self.player_y, self.player_sizex, self.player_sizey), 2)

        # 玩家圖片位置更新&地圖片更新
    def image_update (self) :
        self.player.rect.x = self.player_x
        self.player.rect.y = self.player_y
        self.map_image.rect.x = self.map_x*-1
        for variable_name, variable_value in self.trap_all.items():
            variable_value.DO()
        if self.map == 0 :
            self.map_image.change_image(map_0_image_path)

        # 難度變更
    def change_difficulty (self, difficulty_mod) :
        if difficulty_mod == 0 :
            self.double_jump = 1
            self.real = 0
            self.acceleration_penalty = 0.8
        if difficulty_mod == 1 :
            self.double_jump = 0
            self.real = 0
            self.acceleration_penalty = 0.8
        if difficulty_mod == 2 :
            self.double_jump = 0
            self.real = 1
            self.acceleration_penalty = 0

        # 關卡更新
    def change_map (self, object_map, trap_map, player_x, player_y, map, difficulty_mod, end_x) :
        self.object_map = object_map
        self.trap_map = trap_map
        self.player_x = player_x
        self.player_y = player_y
        self.map = map
        self.map_x = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.collision_trap1 = 0
        self.end_x = end_x
        self.change_difficulty(difficulty_mod)

        # 腳色死亡動畫
    def Death_animation (self) :
        self.velocity_y = self.jump_y*-8
        self.velocity_x = self.velocity_x*5
        while self.player_y < (height + 200 ) :
            self.velocity_y += gravitational_acceleration*3
            self.collision_y = 0
            self.collision_x = 0
            game_loopset.loopstage = 4
            for time_v in range(0,int(abs(round(player_1.velocity_x, 2))*100)) :
                player_1.move_model()
            game_loopset.loopstage = 5
            for time_v in range(0,int(abs(round(player_1.velocity_y, 2))*100)) :
                player_1.move_model()
            screen.fill(white)     
            screen.blit(version, (width-80, height - font_size_v))
            player_1.image_update()
            sprites_updata_model()
            all_sprites_map.draw(screen)
            all_sprites_player.draw(screen)
            all_sprites_trap.draw(screen)
            player_1.player_draw() 
            player_1.collisionbox_draw_model() 
            pygame.display.flip()
            clock.tick(clock_hz)

    def map_end (self) :
        global gamestage
        if self.map_x - self.player_x >= self.end_x :
            gamestage = (gamestage + 1)*10
# 精靈群組
all_sprites_player = pygame.sprite.Group()
all_sprites_map = pygame.sprite.Group()
all_sprites_pause = pygame.sprite.Group()
all_sprites_trap = pygame.sprite.Group()
all_sprites_death = pygame.sprite.Group()
all_sprites_button = pygame.sprite.Group()
    # 玩家
class Player(pygame.sprite.Sprite) :
    def __init__(self, x, y):
        super().__init__()
        self.image_path = player_image_right
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, height - y)
    def change_image(self, new_image) :
        self.image = pygame.image.load(new_image).convert_alpha()

    # 地圖
class Map(pygame.sprite.Sprite) :
    def __init__(self, map_image) :
        super().__init__()
        self.image_path = map_image
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, height - 720 )
    def change_image(self,new_image) :
        self.image = pygame.image.load(new_image).convert_alpha()

    # 陷阱
class Trap(pygame.sprite.Sprite) :
    def __init__(self, x, y, trigger_box_x, trigger_box_y, trigger_size_x, trigger_size_y, vector_x, vector_y, velocity_trap, trap_image, physics_simulation, invisible) :
        super().__init__()
        self.image_path = trap_image
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, height - y)
        self.triggered = 0
        self.invisible = invisible
        self.trap_x = x
        self.trap_y = height - y

        self.trap_velocity_y = 0
        self.physics_simulation = physics_simulation

        self.velocity_trap = velocity_trap
        self.vector_x = vector_x
        self.vector_y = vector_y
        self.trigger_box_x = trigger_box_x
        self.trigger_box_y = trigger_box_y
        self.trigger_size_x = trigger_size_x
        self.trigger_size_y = trigger_size_y

    def DO (self) :
        self.rect.x = self.trap_x - player_1.map_x
        self.trigger_box_collision()
        self.move()
        self.physics_simulation_model()
    def trigger_box_collision (self) :
        if self.invisible == 1 and self.triggered == 0 :
            self.change_image(nothing_image_path)     
        map_x = player_1.map_x
        trigger_sprite = pygame.sprite.Sprite()
        trigger_sprite.rect = pygame.Rect((self.trigger_box_x - map_x), (height - self.trigger_box_y), self.trigger_size_x, self.trigger_box_y)
        if trigger_sprite.rect.colliderect(player_1.player.rect):
            self.triggered = 1
            self.change_image(self.image_path)
    def move(self) :
        if self.triggered == 1 and self.physics_simulation == 0 :
            self.trap_x += self.vector_x * self.velocity_trap
            self.rect.y += self.vector_y * self.velocity_trap
    def physics_simulation_model(self) :
        if self.rect.y < (height + 200) :
            if self.triggered  == 1 and self.physics_simulation == 1 :
                self.trap_velocity_y += gravitational_acceleration
                self.rect.y += self.trap_velocity_y
    def change_image(self,new_image) :
        self.image = pygame.image.load(new_image).convert_alpha()

class NPC_Trap(pygame.sprite.Sprite) :
    def __init__(self, x, y, range_left, range_right, velocity_trap, trap_image, trap_sizex, trap_sizey) :
        super().__init__()
        self.image_path = trap_image
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, height - y)
        self.triggered = 0
        self.trap_original_x = x
        self.trap_x = x
        self.trap_y = height - y
        self.velocity_trap = velocity_trap
        self.range_right = range_right
        self.range_left = range_left
        
        # 地圖設置
        self.object_map = player_1.object_map
        self.map_x = player_1.map_x

        # 移動設置
        self.trap_velocity_y = 0
        self.trap_velocity_x = self.velocity_trap
        self.collision_x = 0
        self.collision_y = 0

        self.trap_sizex = trap_sizex
        self.trap_sizey = trap_sizey
    def DO (self) :
        self.move()
        self.rect.y = self.trap_y 
        self.rect.x = self.trap_x - player_1.map_x
        pygame.draw.rect(screen, red, (self.trap_x , self.trap_y, self.trap_sizex, self.trap_sizey), 2)

    def move (self) :
        if self.trap_x < (self.range_left - map_x ) :
            self.trap_velocity_x = self.velocity_trap
        if self.trap_x > (self.range_right - map_x ) :
            self.trap_velocity_x = self.velocity_trap* -1
        self.trap_velocity_y += gravitational_acceleration   
        
        self.trap_x += self.trap_velocity_x
        # y 方向碰撞 + 移動
        n = int(abs(round(self.trap_velocity_y, 2))*10)  
        for time_v in range(0,n):
            game_loopset.loopstage = 5  # 迴圈第5階段
            self.collision_y = 0
            self.collision_model()
            self.move_model()

    def collision_model (self) :
        # 地圖設置
        object_map = player_1.object_map
        map_x = player_1.map_x

        create_time_map = len(self.object_map)
        # trap_collision_box = pygame.Rect(self.trap_x - map_x)
        if game_loopset.loopstage == 5 :
            for time_c in range(0, create_time_map,1) :   
                if self.collision_y == 0 :
                    time_c_int = round(time_c, 0)
                    if self.trap_y + math.copysign(0.1, self.trap_velocity_y) > (height - object_map[time_c_int][1] - self.trap_sizey) and (self.trap_y + self.trap_sizey) < (height - object_map[time_c_int][1]) and (self.trap_x) > (object_map[time_c_int][0] - map_x - self.trap_sizex) and (self.trap_x ) < (object_map[time_c_int][0] - map_x + object_map[time_c_int][2]): # 碰撞(偵測y) >> 上(物體的)
                        self.collision_y = 1
    
    def move_model(self):
        if self.collision_y == 0 and game_loopset.loopstage == 5:
            self.trap_y = self.trap_y + math.copysign(0.1, self.trap_velocity_y)
        elif self.collision_y == 1 :
            self.trap_velocity_y = 0




    # 死亡畫面
class Death_image(pygame.sprite.Sprite) :
    def __init__(self, x, y):
        super().__init__()
        self.image_path = player_image_right
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, height - y)
    def death(self, death_time) :
        global gamestage
        player_1.Death_animation ()
        for i in range(1, 60) :
            screen.fill(black)
            death_time_1 = Death_time.render("X", True, (white)) 
            screen.blit(death_time_1,(width // 2 , height // 2))
            death_time_2 = Death_time.render(f"{death_time}", True, (white)) 
            screen.blit(death_time_2,(width // 2 + 100 , height // 2))
            all_sprites_death.update()
            all_sprites_death.draw(screen)
            pygame.display.flip()
            clock.tick(clock_hz)
        gamestage = gamestage*10

class Button_image(pygame.sprite.Sprite) :
    def __init__(self, x, y, level, button_image):
        super().__init__()
        self.image_path = button_image
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.level = level 

collision_button_list = []
def button_collision() :
    global collision_button_list
    global button_push
    global pause
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    cursor_sprite = pygame.sprite.Sprite()
    cursor_sprite.rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
    collision_button_list = pygame.sprite.spritecollide(cursor_sprite, all_sprites_button, False)
    
    
    if event.type == pygame.MOUSEBUTTONDOWN  :
        if event.button == 1 :
            if collision_button_list and button_push == 0 :
                print(f"Cursor and sprite collided!{collision_button_list}")
                for sprite in collision_button_list:
                    print("精靈層級:", sprite.level)
                    if pause == 0   :
                        pause = 1
                        time.sleep(0.5)
                    else :
                        pause = 0 
                        time.sleep(0.5)
                button_push = 1
    else :
        button_push = 0

def button_create_model(Button) :
    for i in range(0, len(Button)):
        Button_name = Button[i][0]
        Button_name = Button_image(Button[i][1], Button[i][2], Button[i][3], Button[i][4])
        all_sprites_button.add(Button_name)

def sprites_updata_model() :
    all_sprites_map.update()
    all_sprites_player.update()
    all_sprites_pause.update()
    all_sprites_trap.update()
    all_sprites_button.update()
    all_sprites_death.update()
    # 測試
def game_test() :
    keys = pygame.key.get_pressed()
    global gamestage 
    global pause
    if keys[pygame.K_0] :
        gamestage = 0
        player_1.map = 0
        player_1.map_x = 0
    if keys[pygame.K_1] :
        gamestage = 10
        player_1.map = 1
    if keys[pygame.K_2] :
        gamestage = 20
        player_1.map = 2
    if pause == 0   :
        if keys[pygame.K_5] :
            pause = 1
            time.sleep(0.5)
    else :
        if keys[pygame.K_5] :
            pause = 0 
            time.sleep(0.5)
    if keys[pygame.K_6] :
        player_1.death_time += 1
        death_image.death(player_1.death_time)
    
        
# 建立 (位置以畫面左下角為(0, 0))
    # 按鈕 ["name", x, y, level, path]
Button = [
    ['PAUSE', 640, 100, 2, pause_image_path]
        
        
        
        ]
button_create_model(Button)

game_loopset =  physics(0, 0, 0, 0, 0, 0, 0)
key_1 = physics(0, 0, 0, 0, 0, 0, 0)      
# (地圖物件, 地圖陷阱, 腳色寬度, 腳色長度, 腳色出現位置_x, 腳色出現位置_y, 第幾關, 難度)   # 難度0 : 二段跳  # 難度1 : 關閉二段跳  # 難度2 : 關閉二段跳 + 踩地才能加速(反正我覺得這玩意兒不是給人玩的)
# 地圖檔
    # map_1
map_1_object = [
        [0,  20, 300000, 20 ],
        [400, 150, 300, 150 ],
        [1000,  110, 30, 30 ],
        [1200,  15, 300, 450 ]
       
    ]
    # (x, y, trigger_box_x, trigger_box_y, trigger_size_x, trigger_size_y, vector_x, vector_y, velocity_trap, trap_image, physics_simulation)
    # 觸發 [1, 起始位置_X, 起始位置_Y, 觸發箱_X, 觸發箱_y, 觸發箱寬, 觸發箱高,向量_X, 向量_Y, 移動速度, 陷阱圖片, 物理效果, 觸發前隱形]
    # NPC  [2, 起始位置_X, 起始位置_Y, 左極限, 右極限, 速度, NPC寬, NPC高]
map_1_trap = [
        [1, 100, 600, 100, 100, 100, 50, 0, 1, 10, player_image_left, 0, 1],
        [2, 500, 300, 0, 1000, 4, player_image_left, 30, 45]
    ]

    # map_2
map_2_object = [
        [0,  60, 300000, 20 ],
        [400, 90, 300, 30 ],
        [1000,  110, 30, 30 ],
        [1200,  110, 30, 300 ]
       
    ]
    # (x, y, trigger_box_x, trigger_box_y, trigger_size_x, trigger_size_y, vector_x, vector_y, velocity_trap, trap_image, physics_simulation)
    # 觸發 [起始位置_X, 起始位置_Y, 觸發箱_X, 觸發箱_y, 向量_X, 向量_Y, 移動速度, 陷阱圖片, 物理效果]
map_2_trap = [
        
    ]
# 建立腳色
player_1 = physics(map_1_object, map_1_trap, 30, 45, 1, 320, 0) 
all_sprites_player.add(player_1.player)
all_sprites_map.add(player_1.map_image)

# 建立暫停畫面
pause_image = Map(pause_image_path)
all_sprites_pause.add(pause_image)

# 建立死亡畫面
death_image = Death_image (width // 2 - 100, height // 2)
all_sprites_death.add(death_image)

# 遊戲clock
clock = pygame.time.Clock()

# 設定遊戲迴圈
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # 設定按鍵
    game_loopset.loopstage = 1       # 迴圈第1階段
    key_1.keypress_model()
    game_test()
    button_collision()
    #(key_1.key_left, key_1.key_right, key_1.key_up) 
    if gamestage >= 1 and pause == 0 :
    # 移動(加速度) & 二段跳躍設定 
        game_loopset.loopstage = 2       # 迴圈第2階段
        player_1.keymove_model ()

    # 移動阻力
        game_loopset.loopstage = 3  # 迴圈第3階段
        player_1.resistance_model()
    
    # x 方向碰撞 + 移動
        n = int(abs(round(player_1.velocity_x, 2))*100)  
        for time_v in range(0,n):
            game_loopset.loopstage = 4  # 迴圈第4階段
            player_1.map_collision()
            player_1.move_model()

    # y 方向碰撞 + 移動
        n = int(abs(round(player_1.velocity_y, 2))*100)  
        for time_v in range(0,n):
            game_loopset.loopstage = 5  # 迴圈第5階段
            player_1.map_collision()
            player_1.move_model()
    
    # 地圖判定
    game_loopset.loopstage = 6  # 迴圈第6階段      
    if gamestage == 10 :
        all_sprites_trap.empty()
        player_1.change_map(map_1_object, map_1_trap, 1, 410, 1, 0, 10000) # (地圖物件, 地圖陷阱, 腳色出現位置_x, 腳色出現位置_y, 第幾關, 難度)
        player_1.map_image.change_image(map_1_image_path)
        player_1.trap_create_model()
        gamestage = 1
    if gamestage == 20 :
        all_sprites_trap.empty()
        player_1.change_map(map_2_object, map_2_trap, 1, 410, 2, 2, 10000)
        player_1.map_image.change_image(map_2_image_path)
        player_1.trap_create_model()
        gamestage = 2
    
    # 死亡判定
    if player_1.collision_trap1 == 1 :
        player_1.death_time += 1
        death_image.death(player_1.death_time)
    # 終點判定
    if player_1.collision_trap1 == 0 :
        player_1.map_end()

    # 清空畫面
    screen.fill(white)      

    # 宣告head_font = pygame.font.SysFont(字體,字體大小)     # SysFont << 設定字體(這裡只自體本身，如字體(新細明體, 標楷體)和字體大小
    head_font = pygame.font.SysFont(None, 20) 

    # 宣告 NAME = NAME.render(f"文本{變數}", 平滑值, 文字顏色, 背景顏色)       # render << 設定文本     # f 是用來表示一個格式化字串（formatted string）的開頭
    test = Test.render(f" player_1.player_x: {player_1.player_x + player_1.map_x}  player_1.player_y: {player_1.player_y} collision_button_list: {collision_button_list} press the 'Number' key  0 >> Home screen  1 >> level1    2 >> level2    space >> pause " , True, (0,0,0))    # 顯示參數(方便測試Debug用)
    

    # 顯示版本
    screen.blit(version, (width-80, height - font_size_v))

    # 暫停的設置
    if pause == 0 :
        player_1.image_update()

    # 更新精靈群組
    sprites_updata_model()

    # 繪製地圖
    #all_sprites_map.draw(screen)
    all_sprites_button.draw(screen)

    if gamestage > 0 :
        # 繪製玩家與陷阱
        all_sprites_player.draw(screen)
        all_sprites_trap.draw(screen)
        # 繪製碰撞方塊
        player_1.player_draw() 
        player_1.collisionbox_draw_model() 
        player_1.trap_triggerbox_draw_model()
    # 繪製暫停畫面
    if pause == 1 :
        all_sprites_pause.draw(screen)
    # 顯示測試參數
    screen.blit(test,(10,10))
    # 更新畫面
    pygame.display.flip()
    
    # 控制遊戲迴圈速度
    clock.tick(clock_hz)
    