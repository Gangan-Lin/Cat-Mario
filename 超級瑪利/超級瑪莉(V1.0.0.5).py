# 更新報告
    # 將物理模擬模組化

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
# 設定視窗大小
screen = pygame.display.set_mode((width,height))        # set_mode << 設定視窗大小
pygame.display.set_caption('超級瑪莉')      # set_caption('視窗名稱') << 設定視窗名稱
# 填滿視窗(顏色(R, G, B))
screen.fill((255,255,255))      #fill << 填滿
    # 設定各項數值
# 顏色
white = (255,255,255)
blue = (0,0,255 )

# 字體大小
font_size_v = 20                            # version字體大小

# 宣告 NAME = pygame.font.SysFont(字體,字體大小)     # SysFont << 設定字體(這裡只自體本身，如字體(新細明體, 標楷體)和字體大小
Test = pygame.font.SysFont(None,20)
Version = pygame.font.SysFont(None,font_size_v)

# 版本(寫好玩的)
version = Version.render("V1.0.0.5", True, (0, 0, 0))     # 放在這裡純粹方便改

# 各項參數 >> 方便知道什麼變數幹嘛用的
clock_hz = 60                                           # 就是clock(問題太多，先暫訂60就好)
    # 迴圈階段
loopstage = 0                              
gamestage = 0                              # 遊戲階段(關卡 暫停(-1) 主畫面 死亡)
    # 地圖x(以最左為0)
map_x = 0                                   
    # 腳色最左能到的距離
max_x = width // 2
    # 判定
collision_x = 0                             # 碰撞判定 x     1:碰撞點為角色右邊  0:無碰撞    -1:碰撞點為物體左邊
collision_y = 0                             # 碰撞判定 y     1:碰撞點為角色上方  0:無碰撞    -1:碰撞點為物體下方
stand = 0                                   # 站立判定
jump = 0                                    # 跳躍次數判定
hold = 0                                    # 跳躍鍵按下時長判定
     # 變數
velocity_x = 0                              # x方向速度
velocity_y = 0                              # y方向速度
    # 遊戲常數
velocitymax_x = 4 * (60 / clock_hz)                     # x方向最大速度
velocitymini_x = 0.08 * (60 / clock_hz)                 # x方向最小速度
accelerationadd_x = 0.2 * (60 / clock_hz)* (60 / clock_hz)               # x方向操縱加速度
acceleration_penalty = 0.8                              # 空中速度懲罰倍率 (影響在空中時的x方向加速度) << 目前有問題先不使用
resistance_x = 0.3 * (60 / clock_hz)* (60 / clock_hz)                    # x方向基礎阻力 ( < accelerationadd_x/2)
jump_delay = 12 * (clock_hz / 60)                       # 長按大跳時長判定 (5~20就好)
jump_award = 0.6                                        # 大跳倍數(0.55約等於沒有，別問我為什麼會這樣，我想破頭都還沒想出來)
jump_second = 1                                         # 第二段跳倍數
jump_penalty = 1                                        # 第二段跳對x的速度懲罰(基本上就是在第二段跳時對當前速度影響的倍率)
jump_y = 4 * (60 / clock_hz)                                              # y方向跳躍加速度

gravitational_acceleration = 0.12 * (60 / clock_hz)* (60 / clock_hz)     # 重力加速度

class physics :
    
    def __init__(self, object_map, player_sizex, player_sizey, player_x, player_y) :
        # player 基礎設置
        self.player_sizex = player_sizex
        self.player_sizey = player_sizey
        # player 判定
        self.collision_x = collision_x
        self.collision_y = collision_y
        self.jump = jump
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
        self.max_x = max_x
        self.map_x = map_x 
        self.object_map = object_map # 腳色當下所在的地圖


    def keypress_model(self) :
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] :
            self.key_left = 1
        else :
            self.key_left = 0
        if keys[pygame.K_RIGHT] :
            self.key_right = 1
        else :
            self.key_right = 0
        if keys[pygame.K_UP] :
            self.key_up = 1
        else :
            self.key_up = 0

    def keymove_model (self) : 
        acceleration_x = 0      
        acceleration_y = 0
        if key_1.key_left == 1 and key_1.key_right == 0 and self.velocity_x > self.velocitymax_x*-1 :     # 當向左鍵按下且向左速度數值 < 最大速度值
            if self.stand == 1 :
                acceleration_x = self.accelerationadd_x*-1                               # 加速度直設為 負的 accelerationadd_x << x方向操縱加速度
            else :
                acceleration_x -= self.accelerationadd_x#*self.acceleration_penalty          # 在空中時乘上速度懲罰
        elif key_1.key_left == 1 and key_1.key_right == 0 :                                     # 當向左鍵按下且向左速度大於或等於最大速讀值
            self.velocity_x = self.velocitymax_x*-1                                           # 將速度設為 負的 velocitymax_x << x方向最大速度
        if key_1.key_right == 1 and key_1.key_left == 0 and self.velocity_x < self.velocitymax_x :        # 當向右鍵按下且向右速度數值 < 最大速度值
            if self.stand == 1 :
                acceleration_x = self.accelerationadd_x                                  # 加速度直設為 正的 accelerationadd_x << x方向操縱加速度
            else :
                acceleration_x = self.accelerationadd_x#*self.acceleration_penalty             # 在空中時乘上速度懲罰
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
        if self.hold == 119  and self.jump == 2 :
            acceleration_y = self.jump_y*-1
            self.jump = 1
            self.hold = self.jump_delay + 2
        if self.hold == 1 and self.jump == 1:
            self.velocity_y = 0
            self.velocity_x = self.velocity_x*jump_penalty
            acceleration_y = self.jump_y*self.jump_second*-1                                 # 乘上第二段跳倍數
            self.jump = 0
            self.hold = 0
        self.velocity_x = self.velocity_x + acceleration_x         # 將加速度導入速度
        self.velocity_y = self.velocity_y + acceleration_y + gravitational_acceleration

        # 阻力模組
    def resistance_model (self) :
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
        import math
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
        create_time = len(self.object_map)

        if game_loopset.loopstage == 4 :
            player_x_here = self.player_x + math.copysign(0.01, self.velocity_x)
            for time_c in range(0, create_time,1) : 
                time_c_int = round(time_c, 0)
                player_collision_box = pygame.Rect(player_x_here, self.player_y, self.player_sizex, self.player_sizey)
                object_collision_box = pygame.Rect(self.object_map[time_c_int][0] - self.map_x, (height - self.object_map[time_c_int][1]), self.object_map[time_c_int][2], self.object_map[time_c_int][3])
                if self.collision_x == 0 :
                    if  player_collision_box.colliderect(object_collision_box) : # 碰撞(偵測x) >> 左右不影響
                        self.collision_x = 1
        
        if game_loopset.loopstage == 5 :
            player_y_here = self.player_y + math.copysign(0.01, self.velocity_y)
            for time_c in range(0, create_time,1) :   
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
        if game_loopset.loopstage == 9 :
            create_time = len(self.object_map)
            for time_c in range(0, create_time, 1) :
                time_c_int = round(time_c, 0)
                pygame.draw.rect(screen, blue, (self.object_map[time_c_int][0] - self.map_x, (height - self.object_map[time_c_int][1]), self.object_map[time_c_int][2], self.object_map[time_c_int][3]))

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
        
    
    def map_collision (self) :
        self.collision_x = 0
        self.collision_y = 0
        self.boundary()
        self.collision_model()
    
    def player_draw (self) :
        pygame.draw.rect(screen, blue, (self.player_x, self.player_y, self.player_sizex, self.player_sizey))

# 建立
game_loopset =  physics(0, 0, 0, 0, 0)
# 地圖檔
    # map_1
map_1_object = [
        [0,  20, 300000, 20 ],
        [400, 90, 300, 30 ],
        [1000,  110, 30, 30 ],
        [1200,  110, 30, 300 ]
       
    ]
    # map_2

key_1 = physics(0, 0, 0, 0, 0)      #(object_map=map_1_object, player_sizex=10, player_sizey=10, player_x=1, player_y=(height - 110)) 
player_1 = physics(map_1_object, 10, 20, 1, 610) 



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
    #(key_1.key_left, key_1.key_right, key_1.key_up) 
    if gamestage >= 0 :
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
    
        

    
    game_loopset.loopstage = 6  # 迴圈第6階段      
    # 清空畫面
    game_loopset.loopstage = 7  # 迴圈第7階段
    screen.fill(white)      # fill << 填滿

    # 畫出玩家碰撞方塊  pygame.draw.rect(顯示於, 顏色(x座標, y座標, x方向大小, y方向大小))      # rect << 定位矩形空間
    game_loopset.loopstage == 8  # 迴圈第8階段
    player_1.player_draw()


    # 畫出地圖碰撞方塊
    game_loopset.loopstage = 9  # 迴圈第9階段
    player_1.collisionbox_draw_model()


    
    
    # 宣告head_font = pygame.font.SysFont(字體,字體大小)     # SysFont << 設定字體(這裡只自體本身，如字體(新細明體, 標楷體)和字體大小
    head_font = pygame.font.SysFont(None,20)

    # 宣告 NAME = NAME.render(f"文本{變數}", 平滑值, 文字顏色, 背景顏色)       # render << 設定文本     # f 是用來表示一個格式化字串（formatted string）的開頭
    test = Test.render(f" player_1.collision_y: {player_1.collision_y}  player_1.collision_x: {player_1.collision_x} stand: {key_1.stand}" ,True,(0,0,0))    # 顯示參數(方便測試Debug用)
    # 顯示測試參數
    screen.blit(test,(10,10))
    # 顯示版本
    screen.blit(version,(width-80,height - font_size_v))
    
    #time.sleep(0.1) << 拿來Debug用的
    # 更新畫面
    pygame.display.flip()
    # 控制遊戲迴圈速度
    clock.tick(clock_hz)