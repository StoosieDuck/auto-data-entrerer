import pyautogui
import time
from pynput import mouse

time.sleep(3)
# pyautogui.click(x=863, y=58)
# pyautogui.write('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
# pyautogui.press('enter')

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
