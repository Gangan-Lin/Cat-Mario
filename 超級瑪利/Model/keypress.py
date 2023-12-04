    #按鍵偵測模組
def keypress()  :
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


(key_left, key_right, key_up) = (keypress()[0], keypress()[1], keypress()[2])
