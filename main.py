from follow_speed_limit import Follow_speed,Change_speed
from time import sleep
from get_OCR import OCR
from get_color import get_color
import keyboard
from datetime import datetime, timedelta
from sys import argv

class Main:
    def __init__(self,top_speed) -> None:
        self.signal_restricted_speed = False
        self.approaching_station = False
        self.speed_limit = 0
        self.last_current_speed = 0
        self.change_speed = Change_speed(top_speed)
        self.follow_speed = Follow_speed(self.change_speed)
        self.disable_control = False
        self.top_speed = top_speed
        self.aspect = None
        self.have_AWS = False
        self.under_signal_restriction = False

    def change_current_speed(self, new_current_speed):
        if self.follow_speed.current_speed != new_current_speed:
            self.follow_speed.change_current_speed(new_current_speed)

    def change_speed_limit(self, new_speed_limit):
        #change current speed
        
        #change speed limit
        if self.speed_limit != new_speed_limit:
            self.speed_limit = new_speed_limit

    def change_speed(self):
        if self.last_current_speed == self.follow_speed.current_speed[0] and self.follow_speed.current_speed[1] != 'e' and self.disable_control == False:
            self.follow_speed.change_speed()
            if self.last_current_speed == 0:
                self.last_current_speed = 1
            else:
                self.last_current_speed = self.follow_speed.current_speed[0]
        else:
            self.last_current_speed = self.follow_speed.current_speed[0]


    def get_signal_aspect(self):
        if get_color([940, 10, 1302, 10], [0, 190, 255]):
            return 'double yellow'
        elif get_color([980, 10, 1302, 10], [0, 190, 255]):
            return 'yellow'
        elif get_color([1000, 10, 1302, 10], [0, 0, 255]):
            return 'red'
        elif get_color([960, 10, 1300, 10], [0,255,0]):
            return 'green'
        elif get_color([960, 10, 1300, 10], [255,255,255]):
            return 'white'

    def get_signal_restricted_speed(self):
        signal_speed_dict = {'yellow':45, 'red':0, 'double_yellow':False, 'green':False, 'white':False, None:False}
        self.signal_restricted_speed = signal_speed_dict[self.aspect]
        if self.signal_restricted_speed != False and self.have_AWS == True:
            self.under_signal_restriction = True
        else:
            self.under_signal_restriction = False

    def acknowledge_AWS(self):
        print("acknowledged")
        keyboard.press_and_release('q')

    def is_approaching_station(self):
        ocr = OCR([990,100,680,60],100,filter_result = False)[:5]
        if ocr.replace('.','',1).replace('m','',1).strip().isnumeric():
            distance = float(ocr.replace('m','',1).strip())
            if distance <= 0.20:
                self.approaching_station = True
                print('now approaching station')
                if distance == 0.0:
                    print('disable control')
                    self.disable_control = True
            else:
                self.approaching_station = False
                self.disable_control = False

    def load(self):
        ocr = OCR([820,30,830,300],50,True)
        if 'Press T to open' in ocr or  'Press T to begin' in ocr or (('Press T to close doors' in ocr or 'Doors closing' in ocr) and self.under_signal_restriction != 'red'):
            keyboard.press_and_release('t')
            
    def determine_following_speed(self):
        if self.approaching_station == True:
            return 45
        elif self.signal_restricted_speed != False and self.under_signal_restriction == True:
            if self.speed_limit < self.signal_restricted_speed:
                return self.speed_limit
            else:
                return self.signal_restricted_speed
        else:
            return self.speed_limit


    def main(self):
        self.last_timestamp = datetime.now()
        while True:
            self.aspect = self.get_signal_aspect()
            self.change_current_speed(self.follow_speed.get_current_speed(self.top_speed))
            self.change_speed_limit(self.follow_speed.get_speed_limit())
            self.change_speed()
            print(f'The train\'s current speed is: {self.follow_speed.current_speed[0]}, speed this code is following is: {self.follow_speed.following_speed},the speed limit if the code is under signal restriction is: {self.speed_limit}, Is the code under signal restriction?: {self.under_signal_restriction}, The next signal aspect is: {self.aspect}, approaching station?: {self.approaching_station}, disabled control?: {self.disable_control}')
            if (not get_color([970, 10, 1262, 10], [0,0,0])):
                self.acknowledge_AWS()
                self.have_AWS = True
            else:
                self.have_AWS = False
            self.get_signal_restricted_speed()
            self.is_approaching_station()
            self.follow_speed.change_following_speed(self.determine_following_speed())
            self.load()
            
top_speed = int(argv[1])
Main(top_speed).main()