from time import sleep
import keyboard

class Change_speed:
    def __init__(self, top_speed) -> None:
        self.top_speed = top_speed

    def increase_speed(self,amount):
        keyboard.press('w')
        sleep(amount/(self.top_speed/4))
        keyboard.release('w')
        

    def decrease_speed(self,amount):
        keyboard.press('s')
        sleep(amount/(self.top_speed/4))
        keyboard.release('s')
        
class Follow_speed:
    def __init__(self,change_speed_obj) -> None:
        self.following_speed = 0
        self.current_speed = 0
        self.change_speed_obj = change_speed_obj

    def change_current_speed_value(self, current_speed):
        self.current_speed = current_speed
    
    def change_following_speed(self, following_speed):
        self.following_speed = following_speed

    def change_current_speed(self, current_speed, following_speed):
        speed_difference = following_speed - current_speed
        if speed_difference > 0:
            self.change_speed_obj.increase_speed(speed_difference)
        elif speed_difference < 0:
            self.change_speed_obj.decrease_speed(abs(speed_difference))
 