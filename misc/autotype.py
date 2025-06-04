from pynput import keyboard
import pyautogui
import time

column1 = [
0.000,
3.000,
3.400,
4.300,
5.200,
5.800,
6.400,
6.900,
7.400,
7.900,
7.900,
7.900,
8.000,
8.100
]

running = False

def start_typing():
    global running
    if not running:
        running = True
        row = -1
        while running and row < len(column1):
            # pyautogui.typewrite("0")
            
            # num = 10+row*7
            # pyautogui.typewrite(str(num))
            
            pyautogui.typewrite(str(column1[row]))
            pyautogui.press("down")
            row += 1
            time.sleep(0.5)
    exit()
            

def stop_typing():
    global running
    running = False

def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l and keyboard.Key.alt_l and keyboard.KeyCode(char='t'):
            start_typing()
        if key == keyboard.Key.ctrl_l and keyboard.Key.alt_l and keyboard.KeyCode(char='s'):
            stop_typing()
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Press Ctrl+Opt+T to start.")

while True:
    time.sleep(1)
    