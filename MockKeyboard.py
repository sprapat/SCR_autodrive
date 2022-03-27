"""
Mock keyboard to use in PAPA MACHINE
"""
class keyboard:
    @staticmethod
    def press(key):
        print(f'press: {key}', key)

    @staticmethod
    def release(key):
        print(f'release: {key}', key)

    @staticmethod
    def press_and_release(key):
        print(f'press and release: {key}', key)