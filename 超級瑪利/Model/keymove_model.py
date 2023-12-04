    #移動(按鍵操控)模組
def acceleration (key_left, key_right, key_up, velocity_x, velocity_y, velocitymax_x, accelerationadd_x, acceleration_penalty, stand, jump, jump_y, jump_delay, jump_award, jump_second, jump_penalty, hold, gravitational_acceleration) : 
    acceleration_x = 0      
    acceleration_y = 0
    if key_left == 1 and velocity_x > velocitymax_x*-1 :                    # 當向左鍵按下且向左速度數值 < 最大速度值
        if stand == 1 :
            acceleration_x = accelerationadd_x*-1                             # 加速度直設為 負的 accelerationadd_x << x方向操縱加速度
        else :
            acceleration_x = accelerationadd_x*acceleration_penalty*-1        # 在空中時乘上速度懲罰
    elif key_left == 1 :                                                    # 當向左鍵按下且向左速度大於或等於最大速讀值
        velocity_x = velocitymax_x*-1                                       # 將速度設為 負的 velocitymax_x << x方向最大速度
    if key_right == 1 and velocity_x < velocitymax_x :                      # 當向右鍵按下且向右速度數值 < 最大速度值
        if stand == 1 :
            acceleration_x = accelerationadd_x                             # 加速度直設為 正的 accelerationadd_x << x方向操縱加速度
        else :
            acceleration_x = accelerationadd_x*acceleration_penalty        # 在空中時乘上速度懲罰
    elif key_right == 1 :                                                   # 當向右鍵按下且向右速度大於或等於最大速讀值
        velocity_x = velocitymax_x                                          # 將速度設為 正的 velocitymax_x << x方向最大速度
    if key_up == 1 and hold >= 1 :                                          # 當向上鍵按下且 stand >= 1 << 跳躍鍵按下時長判定
        hold = hold - 1                                                     # 剩下的就是用 if 判斷式判斷第幾次跳躍及常按向上與方放開重案的二段跳
        if  hold == 2 and jump == 1:
            acceleration_y = jump_y*jump_award*-1                             # 乘上大跳獎勵
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
        acceleration_y = jump_y*jump_second*-1                                # 乘上第二段跳倍數
        jump = 0
        hold = 0
    # 將加速度導入速度
    velocity_x = velocity_x + acceleration_x
    velocity_y = velocity_y + acceleration_y + gravitational_acceleration

    return [velocity_x, velocity_y, jump, hold, stand]

return_move = acceleration(key_left, key_right, key_up, velocity_x, velocity_y, velocitymax_x, accelerationadd_x, acceleration_penalty, stand, jump, jump_y, jump_delay, jump_award, jump_second, jump_penalty, hold, gravitational_acceleration)
(velocity_x, velocity_y, jump, hold, stand) = (return_move[0], return_move[1], return_move[2], return_move[3], return_move[4])