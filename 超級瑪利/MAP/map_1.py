#map_1.py
def map_1 (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x) :
    import math 
    import pygame 
    #設定變數
    collision_x = 0
    collision_y = 0
import pygame
import sys

pygame.init()

# 设置窗口大小
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("碰撞事件示例")

# 定义三角形的三个顶点
triangle_points = [(150, 50), (100, 150), (200, 150)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 渲染
    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (0, 0, 255), triangle_points)

    # 检测鼠标点击事件
    if pygame.mouse.get_pressed()[0]:  # 左键点击
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # 使用点和多边形的碰撞检测
        if pygame.Rect(*triangle_points[0], 1, 1).collidepoint(mouse_x, mouse_y) or \
           pygame.Rect(*triangle_points[1], 1, 1).collidepoint(mouse_x, mouse_y) or \
           pygame.Rect(*triangle_points[2], 1, 1).collidepoint(mouse_x, mouse_y):
            print("碰撞发生！")

    pygame.display.flip()

