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

velocity_x = resistance_model (key_left, key_right, velocity_x, velocitymini_x, velocitymax_x, resistance_x)