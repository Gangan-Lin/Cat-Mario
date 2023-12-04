def collisionbox_draw_model (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y, object_map, screen, blue) :
    import pygame
    if loopstage == 9 :
        create_time = len(object)
        for time_c in range(0, create_time, 1) :
            time_c_int = round(time_c, 0)
            pygame.draw.rect(screen, blue, (object[time_c_int][0] - map_x, (height - object[time_c_int][1]), object[time_c_int][2], object[time_c_int][3]))

collisionbox_draw_model(player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x, loopstage, collision_x, collision_y, object_map, screen, blue)
