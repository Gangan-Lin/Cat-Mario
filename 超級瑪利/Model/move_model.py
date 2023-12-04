def move_model(player_x, player_y, player_sizex, velocity_x, velocity_y, collision_x, collision_y, map_x, max_x, loopstage):
    import math
    if loopstage == 4 :
        if collision_x == 0 :
            player_x = player_x + math.copysign(0.001, velocity_x)
            if player_x + player_sizex >= max_x :
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


return_move_model = move_model(player_x, player_y, player_sizex, velocity_x, velocity_y, collision_x, collision_y, map_x, max_x, loopstage)
(player_x, player_y, velocity_x, velocity_y, map_x) = (return_move_model[0], return_move_model[1], return_move_model[2], return_move_model[3], return_move_model[4])