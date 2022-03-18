import pyautogui
import numpy as np
import cv2
import pytesseract

class ScreenShot:
    """This class represents screen shot and we can ask information from screen shot"""
    def __init__(self):
        self.image = None
        # cache - keep all cache values
        self.cache = {}
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    def remove_all_cache(self):
        self.cache = {}

    def capture(self):
        self.image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        self.remove_all_cache()

    def get_color(self, mon, color):
        # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cropped_image = self.image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        # cv2.imwrite('output.png',cropped_image)
        if [a for a in cropped_image[5, 5]] == color:
                return True
        return False

    def OCR(self, mon, thresh, not_int = False, filter_result = True):
        # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cropped_image = self.image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        hsv=cv2.cvtColor(cropped_image,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,np.array([0,0,255]),np.array([255,255,255]))
        cropped_image[mask>0]=(255,255,255)
        im_bw = cv2.threshold(cropped_image, thresh, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow('image',cropped_image)
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

    def is_required_AWS_acknowledge(self):
        if 'is_required_AWS_acknowledge' not in self.cache:
            self.cache['is_required_AWS_acknowledge'] = not self.get_color([970, 10, 1262, 10], [0,0,0])
        return self.cache['is_required_AWS_acknowledge']

    def get_signal_aspect(self):
        """Return signal aspect as string"""
        if self.get_color([940, 10, 1302, 10], [0, 190, 255]):
            return 'double yellow'
        elif self.get_color([980, 10, 1302, 10], [0, 190, 255]):
            return 'yellow'
        elif self.get_color([1000, 10, 1302, 10], [0, 0, 255]):
            return 'red'
        elif self.get_color([960, 10, 1300, 10], [0,255,0]):
            return 'green'
        elif self.get_color([960, 10, 1300, 10], [255,255,255]):
            return 'white'
        return 'out'

    def is_approaching_station(self):
        distance = self.get_distance_till_next_station()
        return (distance is not None) and (distance <= 0.2)

    def is_at_station(self):
        return (self.get_distance_till_next_station() == 0.0)

    def get_distance_till_next_station(self):
        if 'distance_till_next_station' not in self.cache:
            ocr = self.OCR([990,100,680,60],100,filter_result = False)[:5]
            if ocr.replace('.','',1).replace('m','',1).strip().isnumeric():
                distance = float(ocr.replace('m','',1).strip())            
            self.cache['distance_till_next_station'] = distance        
        return self.cache['distance_till_next_station']

    def get_loading_advisory_message(self):
        if 'loading_advisory_message' not in self.cache:
            self.cache['loading_advisory_message'] = self.OCR([820,30,830,300],50,True)
        return self.cache['loading_advisory_message']

    def need_load_passenger_action(self):
        ocr = self.get_loading_advisory_message()
        return ('Press T to open' in ocr) or  ('Press T to begin' in ocr)

    def need_close_door(self, under_signal_restriction):
        ocr = self.get_loading_advisory_message()
        return (('Press T to close doors' in ocr) or ('Doors closing' in ocr)) and (under_signal_restriction != 'red')
        
    def get_speed_limit(self):
        if 'speed_limit' not in self.cache:        
            result = self.OCR([970, 20, 950, 30],150)
            try:
                result = int(result)
            except Exception:
                result = None
            self.cache['speed_limit'] = result
        return self.cache['speed_limit']

    def get_current_speed(self, top_speed):
        if 'current_speed' not in self.cache:
            mon = [933, 90, 906, 1]
            image2 = self.image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
            sought = [85,176,0]
            result = round(np.count_nonzero(np.all(image2==sought,axis=2)) * (top_speed/90))
            try:
                result = int(result)
            except Exception:
                result = None
            self.cache['current_speed'] = result
        return self.cache['current_speed']