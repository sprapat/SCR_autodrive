import numpy as np
import cv2

def get_color(image, mon, lower):
        # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image2 = image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        # cv2.imwrite('output.png',image2)
        if [a for a in image2[5, 5]] == lower:
                return True
        return False
# print(not get_color([970, 10, 1262, 10], [0,0,0]))