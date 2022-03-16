import pytesseract
import mss
import mss.tools
import numpy as np
import pyautogui
import cv2
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def OCR(mon, thresh, not_int = False, filter_result = True):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image2 = image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        hsv=cv2.cvtColor(image2,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,np.array([0,0,255]),np.array([255,255,255]))
        image2[mask>0]=(255,255,255)
        im_bw = cv2.threshold(image2, thresh, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow('image',image2)
        # cv2.waitKey()
        if not_int == False:
            result = pytesseract.image_to_string(im_bw, config='--psm 6 digits')
            if filter_result == True:
                result = ' '.join([s for s in result.split() if s.isdigit()])
                if result == ' ' or result == '(0)':
                    result = 0
        else:
            result = pytesseract.image_to_string(im_bw)
            print(result)
        return result

# print(OCR([820,30,830,300],150,True))