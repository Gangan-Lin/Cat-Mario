#導入sys & pygame導入sys & pygame
import sys
import pygame
import math
import time
import os
import glob 
import MAP
from MAP import background
from MAP import map_1
from pygame.locals import QUIT
#初始化
pygame.init()


#偵測地圖檔
background_confirm = "./MAP/background"
map_1_confirm = "./map_1.py/"  
confirm_result = os.path.isdir(background_confirm)

head_font = pygame.font.SysFont(None,50)
confirm = head_font.render(f"background confirm: {confirm_result}",True,(0, 0, 0))


'''
# 使用 os 模組列出資料夾中的所有檔案
files_in_folder = os.listdir(folder_path)
# 使用 glob 模組篩選出資料夾中的所有檔案
files_with_path = glob.glob(os.path.join(folder_path, '*'))
# 打印檔案清單
print("Files using os.listdir:", files_in_folder)
print("Files using glob.glob:", files_with_path)
'''
#設定畫面邊界大小
width, height = 1280, 720
#設定視窗大小
screen = pygame.display.set_mode((width,height))        #set_mode << 設定視窗大小
pygame.display.set_caption('超級瑪莉')      #set_caption('視窗名稱') << 設定視窗名稱
#填滿視窗(顏色(R, G, B))
screen.fill((255,255,255))      #fill << 填滿
#顯示檔案確認結果
screen.blit(confirm,(width // 2-200, height // 2))
pygame.display.flip()
time.sleep(1)
    #設定各項數值
#顏色
white = (255,255,255)
blue = (0,0,255 )

#人物碰撞大小
player_sizex = 20
player_sizey = 20

#人物初始位置
player_x = 1
player_y = height - player_sizey - 10

#字體大小
font_size_v = 20                            #version字體大小

#宣告 NAME = pygame.font.SysFont(字體,字體大小)     #SysFont << 設定字體(這裡只自體本身，如字體(新細明體, 標楷體)和字體大小
head_font = pygame.font.SysFont(None,20)
Version = pygame.font.SysFont(None,font_size_v)

#版本(寫好玩的)
version = Version.render("V1.0.2", True, (0, 0, 0))     #放在這裡純粹方便改


#各項參數
    #變數
key_right = 0
key_left = 0
key_up = 0

round_vx = 0
round_vy = 0

map_x = 0                                   #地圖x(以最左為0)

pymunk_player_x = player_x
pymunk_player_y = 600 - player_y
collision_return = 0
collision_x = 0                             #碰撞判定 x     1:碰撞點為角色右邊  0:無碰撞    -1:碰撞點為物體左邊
collision_y = 0                             #碰撞判定 y
stand = 0                                   #站立判定
jump = 0                                    #跳躍次數判定
hold = 0                                    #跳躍鍵按下時長判定
velocity_x = 0                              #x方向速度
velocity_y = 0                              #y方向速度
acceleration_x = 0                          #x方向加速度
acceleration_y = 0                          #x方向加速度
    #遊戲常數
clock_hz = 60                                           #就是clock(問題太多，先暫訂60就好)
jump_delay = 12 * (clock_hz / 60)                       #長按大跳時長判定 (5~20就好)
jump_award = 0.6                                       #大跳倍數(0.55約等於沒有，別問我為什麼會這樣，我想破頭都還沒想出來)
jump_second = 1                                         #第二段跳倍數
jump_penalty = 1                                        #第二段跳對x的速度懲罰(基本上就是在第二段跳時對當前速度影響的倍率)
jump_y = 4                                              #y方向跳躍加速度
accelerationadd_x = 0.2 * (60 / clock_hz)               #x方向操縱加速度
acceleration_penalty = 0.8                              #空中速度懲罰倍率 (影響在空中時的x方向加速度)
resistance_x = 0.2 * (60 / clock_hz)                    #x方向基礎阻力 ( < accelerationadd_x/2)
velocitymax_x = 4 * (60 / clock_hz)                     #x方向最大速度
velocitymini_x = 0.08 * (60 / clock_hz)                 #x方向最小速度
gravitational_acceleration = 0.12 * (60 / clock_hz)     #重力加速度


#遊戲clock
clock = pygame.time.Clock()
#設定遊戲迴圈
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    

    #移動&二段跳躍設定
    #按鍵(上左右) >> 加速度
    #設定按鍵

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] :
        key_left = 1
    if keys[pygame.K_RIGHT] :
        key_right = 1
    if keys[pygame.K_UP] :
        key_up = 1
    
    if key_left == 1 and velocity_x > velocitymax_x*-1 :                    #當向左鍵按下且向左速度數值 < 最大速度值
        if stand == 1 :
            acceleration_x -= accelerationadd_x                             #加速度直設為 負的 accelerationadd_x << x方向操縱加速度
        else :
            acceleration_x -= accelerationadd_x*acceleration_penalty        #在空中時乘上速度懲罰
    elif key_left == 1 :                                                    #當向左鍵按下且向左速度大於或等於最大速讀值
        velocity_x = velocitymax_x*-1                                       #將速度設為 負的 velocitymax_x << x方向最大速度
    if key_right == 1 and velocity_x < velocitymax_x :                      #當向右鍵按下且向右速度數值 < 最大速度值
        if stand == 1 :
            acceleration_x += accelerationadd_x                             #加速度直設為 正的 accelerationadd_x << x方向操縱加速度
        else :
            acceleration_x += accelerationadd_x*acceleration_penalty        #在空中時乘上速度懲罰
    elif key_right == 1 :                                                   #當向右鍵按下且向右速度大於或等於最大速讀值
        velocity_x = velocitymax_x                                          #將速度設為 正的 velocitymax_x << x方向最大速度
    if key_up == 1 and hold >= 1 :                                          #當向上鍵按下且 stand >= 1 << 跳躍鍵按下時長判定
        hold = hold - 1                                                     #剩下的就是用 if 判斷式判斷第幾次跳躍及常按向上與方放開重案的二段跳
        if  hold == 2 and jump == 1:
            acceleration_y -= jump_y*jump_award                             #乘上大跳獎勵
            jump = 0
            hold = 0
    elif jump == 1 :
        hold = 2 
    if hold == 119  and jump == 2 :
        acceleration_y -= jump_y
        jump = 1
        hold = jump_delay + 2
    if hold == 1 and jump == 1:
        velocity_y = 0
        velocity_x = velocity_x*jump_penalty
        acceleration_y -= jump_y*jump_second                                #乘上第二段跳倍數
        jump = 0
        hold = 0

    #將加速度導入速度
    velocity_x = velocity_x + acceleration_x
    velocity_y = velocity_y + acceleration_y + gravitational_acceleration

    #阻力(x方向) >> 速度
    #x方向阻力
    if velocity_x >= velocitymini_x :
        velocity_x = velocity_x - resistance_x*(abs(velocity_x)/(velocitymax_x))            #線性調整阻力大小
        if key_right == 1 and key_left == 1 :
            velocity_x = velocity_x - resistance_x*(abs(velocity_x)/(velocitymax_x*0.375))  #煞車用的
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
    

    round_vx = round(velocity_x, 2)     #速度x取到小數點後第2位
    round_vy = round(velocity_y, 2)     #速度x取到小數點後第2位
    

    #x碰撞+移動
    n = int(abs(round_vx)*1000)  
    for time_v in range(1,n):
        collision_return = background.boundary(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x) #collision_x = 回傳的 return 值



        if collision_return == -1 or collision_return == 1 or collision_return == 0:            #return 值轉換 x 方向碰撞
            collision_x = 0
        if collision_return == -11 or collision_return == -10 or collision_return == -9:
            collision_x = -1
        if collision_return == 11 or collision_return == 10 or collision_return == 9:
            collision_x = 1

        if collision_x == 0 :
            player_x = player_x + math.copysign(0.001, velocity_x)
            if player_x + player_sizex >= width//2 :
                player_x = player_x - math.copysign(0.001, velocity_x)
                map_x = map_x + math.copysign(0.001, velocity_x)   
        elif collision_x == -1 or collision_x == 1 :
            velocity_x = 0 
    #y碰撞+移動
    n = int(abs(round_vy)*1000)  
    for time_v in range(1,n):
        collision_return = background.boundary(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x)

        if collision_return == -10 or collision_return == 0 or collision_return == 10:            #return 值轉換 x 方向碰撞
            collision_y = 0
        if collision_return == -11 or collision_return == -1 or collision_return == 9:
            collision_y = -1
        if collision_return == 11 or collision_return == 1 or collision_return == -9:
            collision_y = 1
        
        if collision_y == 0 :
            player_y = player_y + math.copysign(0.001, velocity_y)
        elif collision_y == -1 or collision_y == 1 :
            velocity_y = 0
    
    if collision_y == 0 or collision_y == 1 :
        stand = 0
    if collision_y == -1 :
        hold = 120
        jump = 2
        stand = 1

    #清空加速度數值
    acceleration_x = 0      
    acceleration_y = 0
    key_left = 0
    key_right = 0
    key_up = 0
    pymunk_player_x = player_x
    pymunk_player_y = height - player_y      
    # 清空畫面
    screen.fill(white)      #fill << 填滿

    # 畫出玩家  pygame.draw.rect(顯示於, 顏色(x座標, y座標, x方向大小, y方向大小))      #rect << 定位矩形空間
    pygame.draw.rect(screen, blue, (player_x, player_y, player_sizex, player_sizey))

    #宣告head_font = pygame.font.SysFont(字體,字體大小)     #SysFont << 設定字體(這裡只自體本身，如字體(新細明體, 標楷體)和字體大小
    head_font = pygame.font.SysFont(None,20)

    #宣告 NAME = NAME.render(f"文本{變數}", 平滑值, 文字顏色, 背景顏色)       #render << 設定文本     #f 是用來表示一個格式化字串（formatted string）的開頭
    test = head_font.render(f"confirm_result: {confirm_result} collision_x: {round(collision_x, 2)}  round_vx: {round_vx} stand: {stand}" ,True,(0,0,0))    #顯示參數(方便測試Debug用)
    #顯示測試參數
    screen.blit(test,(10,10))
    #顯示版本
    screen.blit(version,(width-80,height - font_size_v))
    
    
    # 更新畫面
    pygame.display.flip()

    # 控制遊戲迴圈速度
    clock.tick(clock_hz)