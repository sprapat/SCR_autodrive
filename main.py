from follow_speed_limit import Follow_speed,Change_speed
import keyboard
from sys import argv
from Screenshot import ScreenShot
from time import sleep
from datetime import datetime

class Autodrive:
    SIGNAL_SPEED_DICT = {'yellow':45, 'red':0, 'double yellow':False, 'green':False, 'white':False, 'out':False}

    def __init__(self,top_speed) -> None:
        # Parameters
        self.speed_limit = 0
        self.last_current_speed = 0
        self.change_speed_obj = Change_speed(top_speed)
        self.follow_speed = Follow_speed(self.change_speed_obj)
        self.top_speed = top_speed
        self.screen_shot = ScreenShot()

        # Flags
        self.loading = False            

    def need_change_current_speed(self):
        if (self.last_current_speed == self.follow_speed.current_speed) and (self.screen_shot.is_at_station() == False) and (self.loading == False):
            return True
        self.last_current_speed = self.follow_speed.current_speed
        return False

    def acknowledge_AWS(self):
        """Perform action to acknowledge AWS"""
        print("acknowledged")
        keyboard.press_and_release('q')

    def determine_following_speed(self):
        # signal restricted speed is the max speed a train can travel if not approaching a station (can be lower if the speed limit is lower)
        signal_restricted_speed = self.SIGNAL_SPEED_DICT[self.screen_shot.get_signal_aspect()]
        # train is approaching a station, maximum speed limit will be 45 (can be less)
        if self.screen_shot.is_approaching_station() == True:
            return min(self.speed_limit, 45)
        # if train is not approaching a station but under signal_restricted_speed, maximum speed limit will be self.signal_restricted_speed (can be less)
        elif type(signal_restricted_speed) != bool:
            return min(self.speed_limit, signal_restricted_speed)

            
        return self.speed_limit

    def print_train_info(self):
        current_speed = f'The train\'s current speed is: {self.follow_speed.current_speed}'
        code_speed = f'speed this code is following is: {self.follow_speed.following_speed}'
        speed_limit = f'the speed limit if the code is under signal restriction is: {self.speed_limit}'
        signal_restricted_speed = f'the signal restricted speed is: {self.signal_restricted_speed}'
        next_signal_aspect = f'The next signal aspect is: {self.screen_shot.get_signal_aspect()}'
        approaching_station = f'approaching station?: {self.screen_shot.is_approaching_station()}'
        disabled_control = f'disabled control?: {self.screen_shot.is_at_station()}'
        loading = f'is the train loading?: {self.loading}'
        print(','.join([current_speed, code_speed, speed_limit, signal_restricted_speed, next_signal_aspect, approaching_station, disabled_control, loading]))

    # @profile
    def start(self):
        while True:
            before_start_timestamp = datetime.now()
            #capture screenshot that is use to determine: current_speed, speed_limit, distance, AWS, and signal aspect
            self.screen_shot.capture()
            
            #if require aws acknowledgement, then acknowledge AWS
            if self.screen_shot.is_required_AWS_acknowledge():
                self.acknowledge_AWS()

            #Press T at station section
            # if need to load passenger then load passenger by pressing T
            if self.screen_shot.need_load_passenger_action():
                keyboard.press_and_release('t')
                self.loading = True
            # if need to close doors (need to close doors and the signal is NOT Red) then close doors by pressing T
            if self.screen_shot.need_close_door(self.screen_shot.get_signal_aspect()):
                keyboard.press_and_release('t')
                self.loading = False

            # Update speed section
            # read current speed from screen and keep in Follow_speed
            current_speed = self.screen_shot.get_current_speed(self.top_speed)
            if current_speed is not None:
                self.follow_speed.change_current_speed_value(current_speed)
            # read speed limit from screen and keep in Autodrive
            speed_limit = self.screen_shot.get_speed_limit()
            if speed_limit is not None:
                self.speed_limit = speed_limit
               
            self.print_train_info()
            #Determine following_speed from approaching station, signal aspect and speed limit then change the following_speed accrodingly
            self.follow_speed.change_following_speed(self.determine_following_speed())
            # if need to change the current speed then change the current speed (meaning by actually pressing w or s)
            if self.need_change_current_speed():
                self.follow_speed.change_current_speed()
            # print(datetime.now()-before_start_timestamp)
            # break

if __name__=='__main__':            
    top_speed = int(argv[1])
    Autodrive(top_speed).start()