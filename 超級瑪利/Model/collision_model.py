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


def_return = collision_model(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y, object_map)