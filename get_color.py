import numpy as np
import pyautogui
import cv2

# The following link may provide a faster solution
# https://stackoverflow.com/questions/3800458/quickly-getting-the-color-of-some-pixels-on-the-screen-in-python-on-windows-7

# Because the current solution, we do this in many steps
# capture screen -> convert into numpy array -> convert into cvtColor

def get_color(mon,lower):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image2 = image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        # cv2.imwrite('output.png',image2)
        if [a for a in image2[5, 5]] == lower:
                return True
        return False
# print(not get_color([970, 10, 1262, 10], [0,0,0]))