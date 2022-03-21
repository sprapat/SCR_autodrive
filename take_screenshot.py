import cv2
import pyautogui
import numpy as np
# thresh = 50
mon = [990,30,711,6]
cropped_new_image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
# new_bw_image = cv2.threshold(cropped_new_image, thresh, 255, cv2.THRESH_BINARY)[1]
# cv2.imwrite('no_tens_digit.png',cropped_new_image)