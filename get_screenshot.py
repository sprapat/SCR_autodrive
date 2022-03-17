import pyautogui
import numpy as np
import cv2

def get_screenshot():
    return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)