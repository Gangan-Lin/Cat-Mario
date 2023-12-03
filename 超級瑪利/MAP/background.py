# background.py
def boundary (player_x, velocity_x, player_y, velocity_y, height, player_sizey, map_x) :
    import math
    collision_x = 0
    collision_y = 0
    if player_x + math.copysign(0.001, velocity_x) >= 0 :
        collision_x = 0
    elif player_x + math.copysign(0.001, velocity_x) <= 0:
        collision_x = -1
    if player_y + math.copysign(0.001, velocity_y) <= (height - player_sizey) :
        collision_y = 0
    elif player_y + math.copysign(0.001, velocity_y) >= (height - player_sizey) :
        collision_y = -1
    return (collision_x*10 + collision_y) 