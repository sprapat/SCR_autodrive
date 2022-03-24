from time import sleep
import keyboard

class Change_speed:
    def __init__(self, top_speed) -> None:
        self.top_speed = top_speed

    # def increase_speed(self,amount):
    #     keyboard.press('w')
    #     sleep(amount/(self.top_speed/4))
    #     keyboard.release('w')
        

    # def decrease_speed(self,amount):
    #     keyboard.press('s')
    #     sleep(amount/(self.top_speed/4))
    #     keyboard.release('s')
        
class Follow_speed:
    def __init__(self,change_speed_obj) -> None:
        self.change_speed_obj = change_speed_obj

    
 