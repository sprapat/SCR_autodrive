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
        self.signal_restricted_speed = False  
        self.disable_control = False             
        self.loading = False            

    def change_speed(self):
        if self.last_current_speed == self.follow_speed.current_speed and self.disable_control == False and self.loading == False:
            self.follow_speed.change_speed()
            if self.last_current_speed == 0:
                self.last_current_speed = 1
            else:
                self.last_current_speed = self.follow_speed.current_speed
        else:
            self.last_current_speed = self.follow_speed.current_speed

    def is_under_signal_restriction(self):
        # TODO: under_signal_restriction is either False or String
        # This is a mixed value of different type.
        # We may change this later.
        if type(self.signal_restricted_speed) != bool and self.signal_restricted_speed != False and (self.screen_shot.is_required_AWS_acknowledge() == True or self.loading == True):
            return self.screen_shot.get_signal_aspect()
        elif type(self.signal_restricted_speed) == bool and self.signal_restricted_speed == False:
            return False

    def acknowledge_AWS(self):
        """Perform action to acknowledge AWS"""
        # print("acknowledged")
        keyboard.press_and_release('q')

    def determine_following_speed(self):
        # train is approaching station, maximum speed limit will be 45
        if self.screen_shot.is_approaching_station() == True:
            return min(self.speed_limit, 45)

        elif type(self.signal_restricted_speed) != bool and self.signal_restricted_speed != False and self.is_under_signal_restriction() != False:
            if self.speed_limit < self.signal_restricted_speed:
                return self.speed_limit
            return self.signal_restricted_speed
            
        return self.speed_limit

    def print_train_info(self):
        current_speed = f'The train\'s current speed is: {self.follow_speed.current_speed}'
        code_speed = f'speed this code is following is: {self.follow_speed.following_speed}'
        speed_limit = f'the speed limit if the code is under signal restriction is: {self.speed_limit}'
        signal_restricted_speed = f'the signal restricted speed is: {self.signal_restricted_speed}'
        is_under_signal_restriction = f'Is the code under signal restriction?: {self.is_under_signal_restriction()}'
        next_signal_aspect = f'The next signal aspect is: {self.screen_shot.get_signal_aspect()}'
        approaching_station = f'approaching station?: {self.screen_shot.is_approaching_station()}'
        disabled_control = f'disabled control?: {self.disable_control}'
        loading = f'is the train loading?: {self.loading}'
        print(','.join([current_speed, code_speed, speed_limit, signal_restricted_speed, is_under_signal_restriction, next_signal_aspect, approaching_station, disabled_control, loading]))

    # @profile
    def start(self):
        while True:
            before_start_timestamp = datetime.now()
            self.screen_shot.capture()
            self.print_train_info()
            if self.screen_shot.is_required_AWS_acknowledge():
                self.acknowledge_AWS()
            self.signal_restricted_speed = self.SIGNAL_SPEED_DICT[self.screen_shot.get_signal_aspect()]

            if self.screen_shot.is_at_station():
                print('is at station')
                self.disable_control = True
            else:
                self.disable_control = False
            if self.screen_shot.need_load_passenger_action():
                keyboard.press_and_release('t')
                self.loading = True
            if self.screen_shot.need_close_door(self.is_under_signal_restriction()):
                keyboard.press_and_release('t')
                self.loading = False

            # read current speed from screen and keep in Follow_speed
            current_speed = self.screen_shot.get_current_speed( self.top_speed)
            if current_speed is not None:
                self.follow_speed.change_current_speed(current_speed)
            # read speed limit from screen and keep in Autodrive
            speed_limit = self.screen_shot.get_speed_limit()
            if speed_limit is not None:
                self.speed_limit = speed_limit
                
            self.follow_speed.change_following_speed(self.determine_following_speed())
            self.change_speed()
            # print(datetime.now()-before_start_timestamp)
            # break

if __name__=='__main__':            
    top_speed = int(argv[1])
    Autodrive(top_speed).start()
# lp = LineProfiler()
# lp_wrapper = lp(Autodrive(125).start)
# lp.print_stats()
