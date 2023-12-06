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
version = Version.render("V1.0.4", True, (0, 0, 0))     # 放在這裡純粹方便改


# 各項參數 >> 方便知道什麼變數幹嘛用的
    # 人物碰撞大小
player_sizex = 10
player_sizey = 10

    # 人物初始位置
player_x = 1
player_y = height - player_sizey - 100

    # 迴圈階段
loopstage = 0                              
gamestage = 0                              # 遊戲階段(關卡 暫停(-1) 主畫面 死亡)

    # 按鍵
key_right = 0
key_left = 0
key_up = 0


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
    # 速度
velocity_x = 0                              # x方向速度
velocity_y = 0                              # y方向速度
    # 加速度
acceleration_x = 0                          # x方向加速度
acceleration_y = 0                          # x方向加速度
    # 遊戲常數
clock_hz = 120                                           # 就是clock(問題太多，先暫訂60就好)
jump_delay = 12 * (clock_hz / 60)                       # 長按大跳時長判定 (5~20就好)
jump_award = 0.6                                        # 大跳倍數(0.55約等於沒有，別問我為什麼會這樣，我想破頭都還沒想出來)
jump_second = 1                                         # 第二段跳倍數
jump_penalty = 1                                        # 第二段跳對x的速度懲罰(基本上就是在第二段跳時對當前速度影響的倍率)
jump_y = 4 * (60 / clock_hz)                                              # y方向跳躍加速度
accelerationadd_x = 0.2 * (60 / clock_hz)* (60 / clock_hz)               # x方向操縱加速度
acceleration_penalty = 0.8                              # 空中速度懲罰倍率 (影響在空中時的x方向加速度) << 目前有問題先不使用
resistance_x = 0.3 * (60 / clock_hz)* (60 / clock_hz)                    # x方向基礎阻力 ( < accelerationadd_x/2)
velocitymax_x = 4 * (60 / clock_hz)                     # x方向最大速度
velocitymini_x = 0.08 * (60 / clock_hz)                 # x方向最小速度
gravitational_acceleration = 0.12 * (60 / clock_hz)* (60 / clock_hz)     # 重力加速度

# 模組
    #按鍵偵測模組
def keypress_model()  :
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] :
        key_left = 1
    else :
        key_left = 0
    if keys[pygame.K_RIGHT] :
        key_right = 1
    else :
        key_right = 0
    if keys[pygame.K_UP] :
        key_up = 1
    else :
        key_up = 0
    keypress_return = [key_left, key_right, key_up]
    return keypress_return

    #移動(按鍵操控)模組
def keymove_model (key_left, key_right, key_up, velocity_x, velocity_y, velocitymax_x, accelerationadd_x, acceleration_penalty, stand, jump, jump_y, jump_delay, jump_award, jump_second, jump_penalty, hold, gravitational_acceleration) : 
    acceleration_x = 0      
    acceleration_y = 0
    if key_left == 1 and key_right == 0 and velocity_x > velocitymax_x*-1 :     # 當向左鍵按下且向左速度數值 < 最大速度值
        if stand == 1 :
            acceleration_x = accelerationadd_x*-1                               # 加速度直設為 負的 accelerationadd_x << x方向操縱加速度
        else :
            acceleration_x -= accelerationadd_x#*acceleration_penalty          # 在空中時乘上速度懲罰
    elif key_left == 1 and key_right == 0 :                                     # 當向左鍵按下且向左速度大於或等於最大速讀值
        velocity_x = velocitymax_x*-1                                           # 將速度設為 負的 velocitymax_x << x方向最大速度
    if key_right == 1 and key_left == 0 and velocity_x < velocitymax_x :        # 當向右鍵按下且向右速度數值 < 最大速度值
        if stand == 1 :
            acceleration_x = accelerationadd_x                                  # 加速度直設為 正的 accelerationadd_x << x方向操縱加速度
        else :
            acceleration_x = accelerationadd_x#*acceleration_penalty             # 在空中時乘上速度懲罰
    elif key_right == 1 and key_left == 0 :                                     # 當向右鍵按下且向右速度大於或等於最大速讀值
        velocity_x = velocitymax_x                                              # 將速度設為 正的 velocitymax_x << x方向最大速度
    if key_up == 1 and hold >= 1 :                                              # 當向上鍵按下且 stand >= 1 << 跳躍鍵按下時長判定
        hold = hold - 1                                                         # 剩下的就是用 if 判斷式判斷第幾次跳躍及常按向上與方放開重案的二段跳
        if  hold == 2 and jump == 1:
            acceleration_y = jump_y*jump_award*-1                               # 乘上大跳獎勵
            jump = 0
            hold = 0
    elif jump == 1 :
        hold = 2 
    if hold == 119  and jump == 2 :
        acceleration_y = jump_y*-1
        jump = 1
        hold = jump_delay + 2
    if hold == 1 and jump == 1:
        velocity_y = 0
        velocity_x = velocity_x*jump_penalty
        acceleration_y = jump_y*jump_second*-1                                 # 乘上第二段跳倍數
        jump = 0
        hold = 0
    velocity_x = velocity_x + acceleration_x         # 將加速度導入速度
    velocity_y = velocity_y + acceleration_y + gravitational_acceleration
    return [velocity_x, velocity_y, jump, hold, stand]      # 回傳

    # 阻力模組
def resistance_model (key_left, key_right, velocity_x, velocitymini_x, velocitymax_x, resistance_x) :
    if velocity_x >= velocitymini_x :
        velocity_x = velocity_x - resistance_x*(abs(velocity_x)/(velocitymax_x))            # 線性調整阻力大小
        if key_right == 1 and key_left == 1 :
            velocity_x = velocity_x - resistance_x*(abs(velocity_x)/(velocitymax_x*0.375))  # 煞車用的
        elif key_right == 1 :
            velocity_x = velocity_x + resistance_x*(abs(velocity_x)/(velocitymax_x))
    if velocity_x <= velocitymini_x :
        velocity_x = velocity_x + resistance_x*(abs(velocity_x)/(velocitymax_x))
        if key_right == 1 and key_left == 1 :
            velocity_x = velocity_x + resistance_x*(abs(velocity_x)/(velocitymax_x*0.375))
        elif key_left == 1 :
            velocity_x = velocity_x - resistance_x*(abs(velocity_x)/(velocitymax_x))
    if velocity_x < velocitymini_x and velocity_x > velocitymini_x*-1 :
        velocity_x = 0
    if velocity_x > (velocitymax_x-velocitymini_x) :
        velocity_x = velocitymax_x
    if velocity_x < (velocitymax_x-velocitymini_x)*-1 :
        velocity_x = velocitymax_x*-1
    return velocity_x

    # 移動模組
def move_model(player_x, player_y, player_sizex, velocity_x, velocity_y, collision_x, collision_y, map_x, max_x, loopstage):
    import math
    if loopstage == 4 :
        if collision_x == 0 :
            player_x = player_x + math.copysign(0.001, velocity_x)
            if player_x + player_sizex > max_x :
                player_x = player_x - math.copysign(0.001, velocity_x)
                map_x = map_x + math.copysign(0.001, velocity_x)   
        elif collision_x == -1 or collision_x == 1 :
            velocity_x = 0 
    if loopstage == 5 :
        if collision_y == 0 :
            player_y = player_y + math.copysign(0.001, velocity_y)
        elif collision_y == -1 or collision_y == 1 :
            velocity_y = 0
    return [player_x, player_y, velocity_x, velocity_y, map_x] 


    # 碰撞判斷模組
def collision_model (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y, object_map) :
    create_time = len(object_map)

    if loopstage == 4 :
        player_x = player_x + math.copysign(0.001, velocity_x)
        for time_c in range(0, create_time,1) : 
            time_c_int = round(time_c, 0)
            player_collision_box = pygame.Rect(player_x, player_y, player_sizex, player_sizey)
            object_collision_box = pygame.Rect(object_map[time_c_int][0] - map_x, (height - object_map[time_c_int][1]), object_map[time_c_int][2], object_map[time_c_int][3])
            if collision_x == 0 :
                if  player_collision_box.colliderect(object_collision_box) : # 碰撞(偵測x) >> 左右不影響
                    collision_x = 1
    
    if loopstage == 5 :
        player_y = player_y + math.copysign(0.001, velocity_y)
        for time_c in range(0, create_time,1) :   
            time_c_int = round(time_c, 0)
            player_collision_box = pygame.Rect(player_x, player_y, player_sizex, player_sizey)
            object_collision_box = pygame.Rect(object_map[time_c_int][0] - map_x, (height - object_map[time_c_int][1]), object_map[time_c_int][2], object_map[time_c_int][3])
            if collision_y == 0 :
                if player_collision_box.colliderect(object_collision_box) and (player_y) < (height - object_map[time_c_int][1]) : # 碰撞(偵測y) >> 上(物體的)
                    collision_y = -1
                elif player_collision_box.colliderect(object_collision_box) : # 碰撞(偵測y) >> 下(物體的)
                        collision_y = 1

    def_return = [collision_x , collision_y]
    return def_return

    # 碰撞方塊繪製模組
def collisionbox_draw_model (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y, object_map, screen, blue) :
    if loopstage == 9 :
        create_time = len(object_map)
        for time_c in range(0, create_time, 1) :
            time_c_int = round(time_c, 0)
            pygame.draw.rect(screen, blue, (object_map[time_c_int][0] - map_x, (height - object_map[time_c_int][1]), object_map[time_c_int][2], object_map[time_c_int][3]))

    # boundary
def boundary (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y) :
    import math
    floor = 1
    if loopstage == 4 :
        if player_x + math.copysign(0.001, velocity_x) >= 0 :
            collision_x = 0
        elif player_x + math.copysign(0.001, velocity_x) <= 0:
            collision_x = -1
    if loopstage == 5 and floor == 1:
        if player_y + math.copysign(0.001, velocity_y) <= (height - player_sizey) :
            collision_y = 0
        elif player_y + math.copysign(0.001, velocity_y) >= (height - player_sizey) :
            collision_y = -1
    def_return = [collision_x , collision_y]
    return def_return

# 地圖檔
    # map_1
def map_1 (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y) :
    object_map = [
        [0,  20, 30, 20 ],
        [400, 90, 300, 30 ],
        [1000,  110, 30, 30 ],
        [1200,  110, 30, 300 ]
       
    ]
    def_return = collision_model(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y, object_map)
    collisionbox_draw_model(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y, object_map, screen, blue)
    return def_return       # 回傳碰撞結果
    # map_2

# 遊戲clock
clock = pygame.time.Clock()
# 設定遊戲迴圈
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # 設定按鍵
    loopstage = 1       # 迴圈第1階段
    (key_left, key_right, key_up) = (keypress_model()[0], keypress_model()[1], keypress_model()[2])
    if gamestage >= 0 :
    # 移動(加速度) & 二段跳躍設定 
        loopstage = 2       # 迴圈第2階段
        return_move = keymove_model(key_left, key_right, key_up, velocity_x, velocity_y, velocitymax_x, accelerationadd_x, acceleration_penalty, stand, jump, jump_y, jump_delay, jump_award, jump_second, jump_penalty, hold, gravitational_acceleration)
        (velocity_x, velocity_y, jump, hold, stand) = (return_move[0], return_move[1], return_move[2], return_move[3], return_move[4])

    # 移動阻力
        loopstage = 3  # 迴圈第3階段
        velocity_x = resistance_model (key_left, key_right, velocity_x, velocitymini_x, velocitymax_x, resistance_x)

    # x 方向碰撞 + 移動
        n = int(abs(round(velocity_x, 2))*1000)  
        for time_v in range(0,n):
            loopstage = 4  # 迴圈第4階段
            collision_x = 0
            collision_x = boundary(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y)[0] 
            collision_x = map_1 (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y)[0]
            return_move_model = move_model(player_x, player_y, player_sizex, velocity_x, velocity_y, collision_x, collision_y, map_x, max_x, loopstage)
            (player_x, player_y, velocity_x, velocity_y, map_x) = (return_move_model[0], return_move_model[1], return_move_model[2], return_move_model[3], return_move_model[4])

    # y 方向碰撞 + 移動
        n = int(abs(round(velocity_y, 2))*1000)  
        for time_v in range(0,n):
            loopstage = 5  # 迴圈第5階段
            collision_y = 0
            collision_y = boundary(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y)[1]
            collision_y = map_1 (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y)[1]
            return_move_model = move_model(player_x, player_y, player_sizex, velocity_x, velocity_y, collision_x, collision_y, map_x, max_x, loopstage)
            (player_x, player_y, velocity_x, velocity_y, map_x) = (return_move_model[0], return_move_model[1], return_move_model[2], return_move_model[3], return_move_model[4])
    
        if collision_y == 0 or collision_y == 1 :
            stand = 0
        if collision_y == -1 :
            (hold, jump, stand) = (120, 2, 1)

    
        loopstage = 6  # 迴圈第6階段      
    # 清空畫面
    loopstage = 7  # 迴圈第7階段
    screen.fill(white)      # fill << 填滿

    # 畫出玩家碰撞方塊  pygame.draw.rect(顯示於, 顏色(x座標, y座標, x方向大小, y方向大小))      # rect << 定位矩形空間
    loopstage == 8  # 迴圈第8階段
    pygame.draw.rect(screen, blue, (player_x, player_y, player_sizex, player_sizey))


    # 畫出地圖碰撞方塊
    loopstage = 9  # 迴圈第9階段
    map_1 (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y) 

    
    
    # 宣告head_font = pygame.font.SysFont(字體,字體大小)     # SysFont << 設定字體(這裡只自體本身，如字體(新細明體, 標楷體)和字體大小
    head_font = pygame.font.SysFont(None,20)

    # 宣告 NAME = NAME.render(f"文本{變數}", 平滑值, 文字顏色, 背景顏色)       # render << 設定文本     # f 是用來表示一個格式化字串（formatted string）的開頭
    test = Test.render(f" key_left: {key_left}  key_right: {key_right} stand: {stand}" ,True,(0,0,0))    # 顯示參數(方便測試Debug用)
    # 顯示測試參數
    screen.blit(test,(10,10))
    # 顯示版本
    screen.blit(version,(width-80,height - font_size_v))
    
    #time.sleep(0.1) << 拿來Debug用的
    # 更新畫面
    pygame.display.flip()
    # 控制遊戲迴圈速度
    clock.tick(clock_hz)