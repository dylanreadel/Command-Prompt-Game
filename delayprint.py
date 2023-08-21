"""import time module"""
import time

GAMESPEED = 0.05

# delay print letter by letter
def delay_print(string, speed):
    """delay print function"""
    for char in string:
        print(char, end="", flush=True)
        time.sleep(speed)
    print("\n")