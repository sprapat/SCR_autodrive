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
        return 'yes'

    def get_color(self, mon, color):
        cropped_image = self.image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        # cv2.imwrite('output.png',cropped_image)
        if [a for a in cropped_image[5, 5]] == color:
                return True
        return False

    # def OCR(self, mon, thresh, not_int = False, filter_result = True):
    #     cropped_image = self.image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
    #     hsv=cv2.cvtColor(cropped_image,cv2.COLOR_BGR2HSV)
    #     mask=cv2.inRange(hsv,np.array([0,0,255]),np.array([255,255,255]))
    #     cropped_image[mask>0]=(255,255,255)
    #     im_bw = cv2.threshold(cropped_image, thresh, 255, cv2.THRESH_BINARY)[1]
    #     cv2.imshow('image',cropped_image)
    #     cv2.waitKey()
    #     if not_int == False:
    #         result = pytesseract.image_to_string(im_bw, config='--psm 6 digits')
    #         if filter_result == True:
    #             result = ' '.join([s for s in result.split() if s.isdigit()])
    #             if result == ' ' or result == '(0)':
    #                 result = 0
    #     else:
    #         result = pytesseract.image_to_string(im_bw)
    #         # print(result)
    #     return result

    def compare_to_existing_image(self,old_image,mon):
        thresh = 50
        mon = mon
        cropped_new_image = self.image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        old_bw_image = cv2.threshold(old_image, thresh, 255, cv2.THRESH_BINARY)[1]
        new_bw_image = cv2.threshold(cropped_new_image, thresh, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow('image',new_bw_image)
        # cv2.waitKey()
        # cv2.imshow('o',old_bw_image)
        # cv2.waitKey()
        err = np.sum((new_bw_image.astype('float') - old_bw_image.astype('float')) ** 2)
        err /= float(new_bw_image.shape[0] * old_bw_image.shape[1])
        return err
        # return (old_bw_image == new_bw_image).all()

    def is_required_AWS_acknowledge(self):
        if 'is_required_AWS_acknowledge' not in self.cache:
            self.cache['is_required_AWS_acknowledge'] = not self.get_color([970, 10, 1262, 10], [0,0,0])
        return self.cache['is_required_AWS_acknowledge']

    #one use
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
        if 'is_approaching_station' not in self.cache:
            distance = self.get_distance_till_next_station1()
            print(distance)
            return (distance is not False) and (distance <= 0.2)
        return self.cache['is_approaching_station']

    #one use
    def is_at_station(self):
        return (type(self.get_distance_till_next_station1()) == float) and (self.get_distance_till_next_station1() == 0.0)

    # def get_distance_till_next_station(self):
    #     if 'distance_till_next_station' not in self.cache:
    #         ocr = self.OCR([990,30,680,30],100,filter_result = False)[:5]
    #         if ocr.replace('.','',1).replace('m','',1).strip().isnumeric():
    #             distance = float(ocr.replace('m','',1).strip())            
    #             self.cache['distance_till_next_station'] = distance     
    #         else:
    #             self.cache['distance_till_next_station'] = 0
    #     return self.cache['distance_till_next_station']

    # def get_loading_advisory_message(self):
    #     if 'loading_advisory_message' not in self.cache:
    #         self.cache['loading_advisory_message'] = self.OCR([820,30,830,300],50,True)
    #     return self.cache['loading_advisory_message']
    def get_distance_till_next_station1(self):
        if 'distance_till_next_station' not in self.cache:
            #[990,30,690,10]
            distance = 0
            distance += 0.1*self.get_min_of_values([990,30,691,8])[0]
            if distance >= 0.2:
                distance += self.get_min_of_values([990,30,678,8])[0]
                if distance >= 0.2:
                    distance += self.get_min_of_values([990,30,667,8])[0]
                    if distance <= 0.2:
                        distance = False
                else:
                    distance = False
            else:
                distance = False
            #change to 10th digit
            print(distance)
            self.cache['distance_till_next_station'] = distance
        return self.cache['distance_till_next_station']
    def get_min_of_values(self,mon):
        min = [0,100000000]
        for num in range(10):
            result = self.compare_to_existing_image(cv2.imread(f'distance_num/{num}.png'),mon)
            if result < min[1]:
                min = [num,float(result)]
        return min

            
        

    #one use
    def need_load_passenger_action(self):
        mon = [820,30,830,300]
        # ocr = self.get_loading_advisory_message()
        return ((self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/ready_to_load1.png'),mon) < 1000) or (self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/ready_to_load2.png'),mon)) < 1000)
        # return ('Press T to open' in ocr) or  ('Press T to begin' in ocr)

    #one use
    def need_close_door(self, under_signal_restriction):
        mon = [820,30,830,300]
        # ocr = self.get_loading_advisory_message()
        return ((self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/close_doors1.png'),mon) < 1000) or (self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/close_doors2.png'),mon)) < 1000)
        # return (('Press T to close doors' in ocr) or ('Doors closing' in ocr)) and (under_signal_restriction != 'red')
    
    #one use
    def get_speed_limit(self):
        if 'speed_limit' not in self.cache:
            min = [0,100000000]
            for speed_limit in [15,30,45,50,60,65,75,90,100,110,125]:
                result = self.compare_to_existing_image(cv2.imread(f'speed_limits/{speed_limit}.png'),[970, 20, 950, 30])
                if result < min[1]:
                    min = [speed_limit,float(result)]
        self.cache['speed_limit'] = min[0]
        return self.cache['speed_limit']

    #one use
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