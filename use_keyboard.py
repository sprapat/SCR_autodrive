import keyboard

class Keyboard:
    def __init__(self) -> None:
        pass

    def press(self, key):
        keyboard.press(key)
        
    def release(self, key):
        keyboard.release(key)
    
    def press_and_release(self, key):
        keyboard.press_and_release(key)