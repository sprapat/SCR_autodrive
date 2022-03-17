import numpy as np
import cv2

def get_current_speed(image, top_speed):
    mon = [933, 90, 906, 1]
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image2 = image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
    # cv2.imshow('image',image2)
    # cv2.waitKey()
    # cv2.imwrite('output.png',image2)
    sought = [85,176,0]
    return round(np.count_nonzero(np.all(image2==sought,axis=2)) * (top_speed/90))
