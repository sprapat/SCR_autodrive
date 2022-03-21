import pyautogui
import numpy as np
import cv2

# constant
YELLOW = [0, 190, 255]
RED = [0, 0, 255]
GREEN = [0,255,0]
WHITE = [255,255,255]

class ScreenShot:
    """This class represents screen shot and we can ask information from screen shot"""
    def __init__(self):
        self.image = None
        # cache - keep all cache values
        self.cache = {}
        # cache digit image
        self.digit_image = [cv2.imread(f'distance_num/{num}.png') for num in range(10)]+[cv2.imread(f'distance_num/no_tens_digit.png')]

    def remove_all_cache(self):
        self.cache = {}

    def capture(self):
        self.image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        self.remove_all_cache()
        return 'yes'

    def get_color(self, mon, color):
        cropped_image = self.image[mon[0]+5:mon[0]+6, mon[2]+5:mon[2]+6]
        # cv2.imwrite('output.png',cropped_image)
        if [a for a in cropped_image[0, 0]] == color:
                return True
        return False

    def compare_to_existing_image(self,old_image,mon, thresh):
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

    def is_required_AWS_acknowledge(self):
        if 'is_required_AWS_acknowledge' not in self.cache:
            self.cache['is_required_AWS_acknowledge'] = not self.get_color([970, 10, 1262, 10], [0,0,0])
        return self.cache['is_required_AWS_acknowledge']

    #one use
    def get_signal_aspect(self):
        """Return signal aspect as string"""
        if self.get_color([940, 10, 1302, 10], YELLOW):
            return 'double yellow'
        elif self.get_color([980, 10, 1302, 10], YELLOW):
            return 'yellow'
        elif self.get_color([1000, 10, 1302, 10], RED):
            return 'red'
        elif self.get_color([960, 10, 1300, 10], GREEN):
            return 'green'
        elif self.get_color([960, 10, 1300, 10], WHITE):
            return 'white'
        return 'out'

    def is_approaching_station(self):
        if 'is_approaching_station' not in self.cache:
            distance = self.get_distance_till_next_station1()
            print(distance)
            self.cache['is_approaching_station'] = (distance is not False) and (distance <= 0.2)
        return self.cache['is_approaching_station']

    #one use
    def is_at_station(self):
        return (self.get_distance_till_next_station1() is not False) and (self.get_distance_till_next_station1() == 0.0)

    def get_loading_advisory_message(self):
        if 'loading_advisory_message' not in self.cache:
            self.cache['loading_advisory_message'] = self.OCR([820,30,830,300],50,True)
        return self.cache['loading_advisory_message']
    def get_distance_till_next_station1(self):
        if 'distance_till_next_station' not in self.cache:
            #with no 10th digit [990,30,693,6] [990,30,680,6]
            #with 10th digit [990,30,711,6] [990,30,702,6] [990,30,689,6] [990,30,680,6] 
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
            #change to 10th digit
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
        return ((self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/ready_to_load1.png'), mon, 200) < 1000) or (self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/ready_to_load2.png'),mon, 200)) < 1000)

    #one use
    def need_close_door(self, under_signal_restriction):
        mon = [820,30,830,300]
        return ((self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/close_doors1.png'),mon, 200) < 1000) or (self.compare_to_existing_image(cv2.imread('need_to_load_passenger_or_close_doors/close_doors2.png'),mon, 200)) < 1000)
    
    #one use
    def get_speed_limit(self):
        if 'speed_limit' not in self.cache:
            min = [0,100000000]
            for speed_limit in [15,30,45,50,60,65,75,90,100,110,125]:
                result = self.compare_to_existing_image(cv2.imread(f'speed_limits/{speed_limit}.png'),[970, 20, 950, 30], 200)
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