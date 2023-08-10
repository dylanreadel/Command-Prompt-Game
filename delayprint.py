"""import time module"""
import time

# delay print letter by letter
def delay_print(string):
    """delay print function"""
    for char in string:
        print(char, end="", flush=True)
        time.sleep(0.05)
    print("\n")