# Set value to True to work on a machine without SCR program
PAPA_MACHINE = True

if not PAPA_MACHINE:
    import pyautogui

import numpy as np
import cv2
from collections import namedtuple

# constant
YELLOW = [0,190,255]
RED = [0,0,255]
GREEN = [0,255,0]
WHITE = [255,255,255]
BLACK = [0,0,0]

SIMILARITY_THRESHOLD = 1000

"""
Utility codes
=============
may extract to another file later but at the moment
we only use these functions in ScreenShot class
"""
def compare_image_similarity(img1, img2) -> float:
    """compare 2 images as numpy array and return mean square error
       assume that both images are the same size
    """
    result = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
    result /= float(img1.shape[0] * img1.shape[1])
    return result

def convert_to_BW_image(img, threshold):
    """return binary image"""
    return cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]

# Define Pos as namedtuple
# numpy array is in this format [height, width] = [y,x]
# Pos(100,20) means position at y=100, x=20
Pos = namedtuple("Pos", "y x")

class ScreenShot:
    """This class represents screen shot and we can ask information from screen shot"""
    def __init__(self):
        self.image = None
        # cache - keep all cache values
        self.cache = {}
        # cache digit image
        self.digit_image = [cv2.imread(f'distance_num/{num}.png') for num in range(10)]+[cv2.imread(f'distance_num/no_tens_digit.png')]
        # cache speed limit image
        self.speed_limit_image = {speed_limit:cv2.imread(f'speed_limits/{speed_limit}.png') for speed_limit in [15,30,45,50,60,65,75,80,90,100,110,125]} 
        # cache other images for comparison
        self.ready_to_load1_image = cv2.imread('need_to_load_passenger_or_close_doors/ready_to_load1.png')
        self.ready_to_load2_image = cv2.imread('need_to_load_passenger_or_close_doors/ready_to_load2.png')
        self.close_doors1_image = cv2.imread('need_to_load_passenger_or_close_doors/close_doors1.png')
        self.close_doors2_image = cv2.imread('need_to_load_passenger_or_close_doors/close_doors2.png')
    
    def remove_all_cache(self):
        self.cache = {}

    def capture(self):
        if PAPA_MACHINE:
            self.image = cv2.imread('screenshot/Screenshot 2022-03-22 11-40-10.png')
        else:
            self.image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        self.remove_all_cache()

    def is_same_color(self, pos, color):
        """return True if color at pos is the same as color in the parameter"""
        return np.array_equal(self.image[pos.y, pos.x], color)

    def compare_to_existing_image(self,old_image, mon, thresh):
        cropped_new_image = self.image[mon[0]:mon[0]+mon[1], mon[2]:mon[2]+mon[3]]
        old_bw_image = convert_to_BW_image(old_image, thresh)
        new_bw_image = convert_to_BW_image(cropped_new_image, thresh)
        return compare_image_similarity(old_bw_image, new_bw_image)

    def is_required_AWS_acknowledge(self):
        if 'is_required_AWS_acknowledge' not in self.cache:
            self.cache['is_required_AWS_acknowledge'] = not self.is_same_color(Pos(975, 1267), BLACK)
        return self.cache['is_required_AWS_acknowledge']

    #one use
    def get_signal_aspect(self):
        """Return signal aspect as string"""
        if self.is_same_color(Pos(945, 1307), YELLOW):
            return 'double yellow'
        if self.is_same_color(Pos(985, 1307), YELLOW):
            return 'yellow'
        if self.is_same_color(Pos(1005, 1307), RED):
            return 'red'
        if self.is_same_color(Pos(965, 1305), GREEN):
            return 'green'
        if self.is_same_color(Pos(965, 1305), WHITE):
            return 'white'
        return 'out'            

    def is_approaching_station(self):
        if 'is_approaching_station' not in self.cache:
            distance = self.get_distance_till_next_station()
            print(distance)
            self.cache['is_approaching_station'] = (distance is not False) and (distance <= 0.2)
        return self.cache['is_approaching_station']

    #one use
    def is_at_station(self):
        return (self.get_distance_till_next_station() is not False) and (self.get_distance_till_next_station() == 0.0)

    def get_loading_advisory_message(self):
        if 'loading_advisory_message' not in self.cache:
            self.cache['loading_advisory_message'] = self.OCR([820,30,830,300],50,True)
        return self.cache['loading_advisory_message']

    def get_distance_till_next_station(self):
        if 'distance_till_next_station' not in self.cache:
            #with no tens digit [990,30,693,6] [990,30,680,6]
            #with tens digit [990,30,711,6] [990,30,702,6] [990,30,689,6] [990,30,680,6] 
            distance = 0
            #if the distance is x.xx instead of xx.xx
            if self.get_min_of_values([990,30,711,6])[0] == 'no_tens_digit':
                # check the x.Xx
                print(.1)
                distance += 0.1*self.get_min_of_values([990,30,693,6])[0]
                if distance <= 0.2:
                    # check the X.xx
                    print(1)
                    distance += self.get_min_of_values([990,30,680,6])[0]
                    if distance <= 0.2:
                        #check the x.xX
                        distance += 0.01*self.get_min_of_values([990,30,702,6])[0]
                        if distance > 0.2:
                            distance = False
                    else:
                        distance = False
                else:
                    distance = False
            else:
                # check the xx.Xx
                print(.1)
                distance += 0.1*self.get_min_of_values([990,30,702,6])[0]
                if distance <= 0.2:
                    # check the xX.xx
                    print(1)
                    distance += self.get_min_of_values([990,30,689,6])[0]
                    if distance <= 0.2:
                        # check the Xx.xx
                        print(10)
                        distance += 10*self.get_min_of_values([990,30,680,6])[0]
                        if distance <= 0.2:
                            # check the xx.xX
                            distance += 0.01*self.get_min_of_values([990,30,711,6])[0]
                            if distance > 0.2:
                                distance = False
                        else:
                            distance = False
                    else:
                        distance = False
                else:
                    distance = False
            #change to tens digit
            print(distance)
            self.cache['distance_till_next_station'] = distance
        return self.cache['distance_till_next_station']

    def get_min_of_values(self,mon):
        min = [0,100000000]
        for num in range(11):
            result = self.compare_to_existing_image(self.digit_image[num],mon,50)

            if result < min[1]:
                if num == 10: 
                    num = 'no_tens_digit'
                min = [num,float(result)]
        print(min)
        return min

    #one use
    def need_load_passenger_action(self):
        mon = [820,30,830,300]
        return ((self.compare_to_existing_image(self.ready_to_load1_image, mon, 200) < SIMILARITY_THRESHOLD) or \
            (self.compare_to_existing_image(self.ready_to_load2_image,mon, 200)) < SIMILARITY_THRESHOLD)

    #one use
    def need_close_door(self, under_signal_restriction):
        mon = [820,30,830,300]
        return under_signal_restriction != 'red' and \
            ((self.compare_to_existing_image(self.close_doors1_image, mon, 200) < 5000) or \
            (self.compare_to_existing_image(self.close_doors2_image, mon, 200)) < 5000)
    
    #one use
    def get_speed_limit(self):
        if 'speed_limit' not in self.cache:
            min = 100000000
            for speed_limit in self.speed_limit_image:
                similarity_score = self.compare_to_existing_image(self.speed_limit_image[speed_limit],[970, 20, 950, 30], 200)
                if similarity_score < min:
                    min = similarity_score
                    self.cache['speed_limit'] = speed_limit
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