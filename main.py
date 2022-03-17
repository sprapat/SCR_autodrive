from follow_speed_limit import Follow_speed,Change_speed
from time import sleep
from get_OCR import OCR
from get_color import get_color
import keyboard
from datetime import datetime, timedelta
from sys import argv

class Autodrive:
    def __init__(self,top_speed) -> None:
        self.under_signal_restriction = False
        self.approaching_station = False
        self.speed_limit = 0
        self.last_timestamp = None
        self.last_current_speed = 0
        #self.change_speed = Change_speed(top_speed)
        #self.follow_speed = Follow_speed(self.change_speed)
        self.disable_control = False
        self.top_speed = top_speed
        self.aspect = None

    def change_speeds(self, new_current_speed, new_following_speed):
        speed_dict = {'red':0, 'yellow':45}
        if self.follow_speed.current_speed[0] != new_current_speed:
            self.follow_speed.change_current_speed(new_current_speed)
        
        if self.follow_speed.following_speed != new_following_speed:
            #If there's nothing influencing the speed limit,
            if self.under_signal_restriction == False and self.approaching_station == False:
                #Then change it immediately
                self.follow_speed.change_following_speed(new_following_speed)
            #maybe redundant
            #If the following_speed is by last signal
            elif self.under_signal_restriction != False:
                #change the speed limit to the new one in every situation
                self.speed_limit = new_following_speed
                self.follow_speed.change_following_speed(new_following_speed)
                if self.follow_signal_restriction() == new_following_speed:
                    self.follow_speed.change_following_speed(new_following_speed)
                # # If the old is higher than the new then change to the newn (for example if under_signal_restriction = 'yellow' and old following_speed is 45 and the new is 30 then we can change the following_speed and speed_limit)
                # if self.follow_speed.following_speed > new_following_speed:
                #     self.follow_speed.change_following_speed(new_following_speed)
                # # If the old is lower than the new,
                # elif self.follow_speed.following_speed < new_following_speed:
                #     #if (the new is higher than the speed restriction by the signal),
                #     if new_following_speed > speed_dict[self.under_signal_restriction]:
                #         #mean that the new speed limit is higher than the old one and higher than the speed restriction by the signal
                #         #then change the speed limit to the new one
                #         #if (the old is lower than the speed restriction by the signal):
                #         if self.follow_speed.following_speed < speed_dict[self.under_signal_restriction]:
                #             self.follow_speed.change_following_speed(speed_dict[self.under_signal_restriction])
                #     # if the new is lower than the speed restriction by the signal
                #     elif new_following_speed < speed_dict[self.under_signal_restriction]:
                #         #then change the speed limit and following_speed
                #         self.follow_speed.change_following_speed(new_following_speed)
        if self.last_current_speed == self.follow_speed.current_speed[0] and datetime.now()-self.last_timestamp >= timedelta(seconds=0.15) and self.follow_speed.current_speed[1] != 'e' and self.disable_control == False:
            self.follow_speed.change_speed()
            self.last_timestamp = datetime.now()
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

    def follow_signal_restriction(self):
        following_speed = self.follow_speed.following_speed
        if self.aspect == 'yellow':
            #making sure that the following_speed isn't 45 mph and make sure that the following_speed is the actual speed limit (because following_speed which is under signal restriction or approaching station can only be 45 or 0 both are nore more than 45)
            if self.follow_speed.following_speed > 45:
                self.under_signal_restriction = 'yellow'
                #since the following_speed is the real speed limit then we can subtitude it in to the speed_limit
                self.speed_limit = self.follow_speed.following_speed
                #change the following speed to be the speed restriction after passing single yellow signal (45 mph)
                following_speed = 45
            #if the signal before this one is red
            elif self.under_signal_restriction == 'red':
                self.under_signal_restriction = 'yellow'
                #since the following_speed would be zero due to the last signal being red, which mean following_speed wouldn't be the speed limit I would just change the following_speed to be 45
                following_speed = 45
            else:
                #if the following_speed isn't more than 45 (actual speed limit) or 0 (due to the last signal being red), then either:
                #    1.the speed limit is lower than 45 which I don't have to change the speed just change the under_signal_restriction
                # or 2.the speed limit is 45 which I don't have to change the speed just change the under_signal_restriction
                # or 3.the speed limit is higher than 45 but the signal before was yellow so the following_speed is 45 which I don't have to change the speed just change the under_signal_restriction
                self.under_signal_restriction = 'yellow'
        elif self.aspect == 'red':
            #If the following_speed isn't by last signal and the train isn't appraoching a station and a signal is red,
            following_speed = 0
            if self.approaching_station == False:
                if self.under_signal_restriction == False:
                    #then mean the following_speed is the speed_limit
                    self.speed_limit = self.follow_speed.following_speed
                self.under_signal_restriction = 'red'
            
        elif self.aspect in ['double_yellow', 'green', 'white', None]:
            self.under_signal_restriction = False
            if self.approaching_station == False:
                following_speed = self.speed_limit
        return following_speed

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
                if self.follow_speed.following_speed > 45:
                    self.speed_limit = self.follow_speed.following_speed
                    self.follow_speed.change_following_speed(45)
                if distance == 0.0:
                    print('disable control')
                    self.disable_control = True
            else:
                self.approaching_station = False
                self.disable_control = False
                if self.under_signal_restriction == False:
                    self.follow_speed.change_following_speed(self.speed_limit)

    def load(self):
        ocr = OCR([820,30,830,300],50,True)
        if ('Press T to open' in ocr) or \
           ('Press T to begin' in ocr) or \
           (('Press T to close doors' in ocr or 'Doors closing' in ocr) and (self.under_signal_restriction != 'red')):
            keyboard.press_and_release('t')
            
    def determine_following_speed(self):
        pass

    def print_train_info(self):
        current_speed = f'The train\'s current speed is: {self.follow_speed.current_speed[0]}'
        code_speed = f'speed this code is following is: {self.follow_speed.following_speed}'
        speed_limit = f'the speed limit if the code is under signal restriction is: {self.speed_limit}'
        is_under_signal_restriction = f'Is the code under signal restriction?: {self.under_signal_restriction}'
        next_signal_aspect = f'The next signal aspect is: {self.aspect}'
        approaching_station = f'approaching station?: {self.approaching_station}'
        disabled_control = f'disabled control?: {self.disable_control}'
        print(','.join[current_speed, code_speed, speed_limit, is_under_signal_restriction, next_signal_aspect, approaching_station, disabled_control])

    def start(self):
        """Main method to start the autodrive"""
        self.last_timestamp = datetime.now()
        while True:
            got_current_speed = self.follow_speed.get_current_speed(self.top_speed)
            new_current_speed = got_current_speed[0]
            self.follow_speed.current_speed[1] = got_current_speed[1]
            new_following_speed = self.follow_speed.get_following_speed()
            self.aspect = self.get_signal_aspect()
            self.change_speeds(new_current_speed, new_following_speed)
            self.print_train_info()
            if (not get_color([970, 10, 1262, 10], [0,0,0])) or self.under_signal_restriction != False:
                self.acknowledge_AWS()
                a = self.follow_signal_restriction()
                print('new change to following_speed is',a)
                self.follow_speed.change_following_speed(a)
            self.is_approaching_station()
            self.load()

# Todo - may add help for the argument later.            
if __name__=='__main__':            
    top_speed = int(argv[1])
    Autodrive(top_speed).start()