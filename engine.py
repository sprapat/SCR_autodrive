# Set value to True to work on a machine without SCR program
import os
if os.getenv('PAPA_MACHINE')=='1':
    print('papa machine')
    PAPA_MACHINE = True
else:
    print('not papa machine')
    PAPA_MACHINE = False

if PAPA_MACHINE:
    from MockKeyboard import keyboard
else:
    import keyboard

from time import sleep

class Engine:
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

    def acknowledge_AWS(self):
        """Perform action to acknowledge AWS"""
        print("acknowledged")
        keyboard.press_and_release('q')

    def load_passenger(self):
        keyboard.press_and_release('t')

    def close_door(self):
        keyboard.press_and_release('t')

    def change_current_speed(self, current_speed, following_speed):
        speed_difference = following_speed - current_speed
        if speed_difference > 0:
            self.increase_speed(speed_difference)
        elif speed_difference < 0:
            self.decrease_speed(abs(speed_difference))