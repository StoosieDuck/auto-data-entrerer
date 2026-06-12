import subprocess
import json
import threading
import os
import sys
import time
from datetime import datetime

# imports
try:
    import keyboard
    from pynput import mouse
    import pyautogui
    from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFrame
    from PyQt6.QtCore import Qt, pyqtSignal
    import pyperclip
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Would you like to install the required modules? (y/n)")
    choice = input()
    if choice == "y":
        print("Installing required modules...")
        subprocess.run(["pip", "install", "keyboard", "pynput", "pyautogui", "PyQt6", "pyperclip"])
        import keyboard
        from pynput import mouse
        import pyautogui
        from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFrame
        from PyQt6.QtCore import Qt, pyqtSignal
        import pyperclip
    else:
        print("Exiting program.")
        exit()

justCalibrated = False
folder_path = None
lastSavedFile = None
delay_time = 0.2

file_explorer_corners = []
points = []

def force_exit():
    print("\nForce quitting automation...")
    log("force quit")
    os._exit(0) # Instantly kills the script and the Qt window

# Resolve config path once so it's available for all branches
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")
logfile_path = os.path.join(script_dir, "log.txt")

def log(text, newLine=True):
    with open(logfile_path, "a", encoding="utf-8") as logfile: 
        if newLine:
            logfile.write(f"{datetime.now().time()} : {text}\n")
        else:
            logfile.write(f"{datetime.now().time()} : {text}")

keyboard.add_hotkey('ctrl+shift+p', force_exit)

# Qt overlay
class TopOverlayBar(QWidget):
    # Signal to safely update the text from the background automation thread
    update_text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 30)

        # Window Flags (Frameless, Always on Top, Click-through)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.Tool
        )
    
        # Transparency attributes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.container = QFrame(self)
        self.container.setFixedSize(800, 30)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(50, 50, 50, 50);
                border: 1px solid lightgray;
                border-radius: 15px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
        """)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
    
        self.label = QLabel("FILMapper: Initializing...", self.container)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Connect the signal to the label's text updater
        self.update_text_signal.connect(self.label.setText)

        self.position_top_center()

    def position_top_center(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        self.move(x, 0)

#main script
def run_main(overlay):
    global justCalibrated
    
    click_event = threading.Event()

    def on_click(x, y, button, pressed):
        if pressed:
            points.append((x, y))
            click_event.set()

    listener = mouse.Listener(on_click=on_click)
    listener.start()

    # Initialize variables to None
    variables = {
        "measure_tab": None, "data_1": None, "data_2": None,
        "data_3": None, "data_4": None, "data_5": None, "data_6": None,
        "data_7": None, "data_8": None, "data_9": None, "data_10": None,
        "file_menu": None, "save_spectrum": None, "folder_path_box": None,
        "file_name_box": None, "file_type_box": None, "csv_file_select": None,
        "save_button": None, "save_nk_button": None, "material_info": None, "ok_button": None, "file_name_box_nk": None
    }

    print("\nWelcome to the Auto Data Enterer for FILMapper!")
    print("Ensure 'Auto Position legends' is UNCHECKED in setup -> display settings.")
    log("------------------------------------------------------------")
    log(datetime.now().date())

    overlay.update_text_signal.emit("Terminal: enter the path to the folder to save data")
    folder_path = input("Enter the path to the folder to save data: ")
    log(f"Folder path: {folder_path}")

    choice = input("\nCalibration: enter 1 to start, 2 to import JSON, 3 to exit: ")
    log(f"User chose {choice}")
    #calibration

    if choice == "1":
        if os.path.isfile(config_path):
            overlay.update_text_signal.emit("Terminal: config.json exists. Overwrite? (y/n)")
            log("config.json exists")
            if input("config.json exists. Overwrite? (y/n): ") != "y":
                log("user chose to overrite config.json")
                print("Exiting program.")
                force_exit()
    
        overlay.update_text_signal.emit("Please add first 10 data entries to measure and then click Ctrl+Shift+k to continue")
        print("\nPlease add first 10 data entries to measure and then click Ctrl+Shift+k to continue")

        keyboard.wait('ctrl+shift+k')

        # More efficient calibration process using a list of steps instead of repeating code
        # Each step is (var_name, prompt, extra) where extra can be a key to wait for or a sleep duration
        steps = [
            ("measure_tab", "Navigate to the 'measure' tab", None),
            ("data_1", "Select the first data entry", None),
            ("file_menu", "Select the file menu button", None),
            ("save_spectrum", "Select the 'save measured spectrum' button", None),
            ("folder_path_box", "Select the file path box at the top of explorer", None),
            ("file_name_box", "Click the name of the file, press Ctrl+A, Ctrl+C", 'ctrl+c'),
            ("file_type_box", "Click the file type dropdown menu", None),
            ("csv_file_select", "Select CSV in the dropdown", None),
            ("save_button", "Click save in the file explorer window", None),
            ("file_menu", "Click the file menu button again", None),
            ("save_nk_button", "Click the 'save measured n and k' button", None),
            ("material_info", "Click the big text box, type 'nk_', Ctrl+V, Ctrl+A, Ctrl+C", 'ctrl+c'),
            ("ok_button", "Click 'ok' in the popup", None),
            ("folder_path_box", "Click the folder path box again", None),
            (None, f"Input {folder_path} and press enter", 'enter'),
            ("file_name_box_nk", "Click the file name box, Ctrl+A, Ctrl+V", 'ctrl+v'),
            ("save_button", "Click the 'save' button", None),
            ("data_2", "Select the second data entry", None),
            ("data_3", "Select the third data entry", None),
            ("data_4", "Select the fourth data entry", None),
            ("data_5", "Select the fifth data entry", None),
            ("data_6", "Select the sixth data entry", None),
            ("data_7", "Select the seventh data entry", None),
            ("data_8", "Select the eigth data entry", None),
            ("data_9", "Select the ninth data entry", None),
            ("data_10", "Select the tenth data entry", None),
        ]

        for step in steps:
            # Skip empty steps if you have extra commas in your list
            if step is None:
                continue

            var_name, prompt, extra = step
            log(f"Prompt: {prompt}")
            overlay.update_text_signal.emit(f"Terminal: {prompt}")
            print(f"\nPrompt: {prompt}")

            start_time = time.time()

            # 1. If the step requires capturing a coordinate, wait for a mouse click
            if var_name is not None:
                click_event.clear()
                click_event.wait()
                variables[var_name] = points[-1]
                log(f"Recorded {var_name} at {points[-1]}")

            # 2. If the step requires waiting for a specific keybind, wait for it
            if extra is not None:
                keyboard.wait(extra)
                log(f"User pressed {extra}")

            end_time = time.time()
            log(f"Step took {end_time - start_time:.2f} sec")

        listener.stop()

        with open(config_path, "w") as f:
            json.dump(variables, f)
        print("Calibration complete. Saved to config.json")
        log("Calibration Complete")
        justCalibrated = True
    elif choice == "2":
        # Load calibration data if available; provide a helpful message if not
        if not os.path.isfile(config_path):
            overlay.update_text_signal.emit("Terminal: config.json not found. Please run calibration first (press 1).")
            print("Error: config.json not found. Please run calibration first (enter 1).\nExiting program.")
            log("config.json not found")
            os._exit(1)
        try:
            with open(config_path, "r") as f:
                variables = json.load(f)
        except Exception as e:
            overlay.update_text_signal.emit(f"Terminal: Failed to read config.json: {e}")
            print(f"Failed to read config.json: {e}\nExiting program.")
            log("failed to read config.json")
            os._exit(1)
        print(f"Calibration data imported from config.json created {os.path.getmtime(config_path)}")
        log(f"Calibration data imported from config.json created {os.path.getmtime(config_path)}")
    else:
        print("Exiting program.")
        force_exit() # Forces the Qt App to close as well

    def save_spectrum_and_nk():
        pyautogui.moveTo(variables["file_menu"])
        pyautogui.click()
        log("Moved to file menu")
        time.sleep(delay_time)

        pyautogui.moveTo(variables["save_spectrum"])
        pyautogui.click()
        log("Saved spectrum")
        time.sleep(delay_time)

        pyautogui.hotkey('ctrl', 'c')
        time.sleep(delay_time)

        log(f"copied {pyperclip.paste()}")
        original_name = pyperclip.paste()
        lastSavedFile = pyperclip.paste()
        time.sleep(delay_time)

        pyautogui.hotkey('alt','d')
        log("focused folder path box")
        time.sleep(delay_time)

        pyautogui.write(folder_path)
        pyautogui.press('enter')
        log(f"wrote folder path {folder_path}")
        time.sleep(delay_time)

        pyautogui.hotkey('alt', 't')
        log("selected file type dropdown")
        time.sleep(delay_time)

        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('enter')
        log(("selected to csv"))
        time.sleep(delay_time)

        pyautogui.hotkey('alt','s')
        log("saved spectrum")
        time.sleep(delay_time)
    
        pyautogui.moveTo(variables["file_menu"])
        pyautogui.click()
        log("clicked file menu")
        time.sleep(delay_time)

        pyautogui.moveTo(variables["save_nk_button"])
        pyautogui.click()
        log("clicked save n and k button")
        time.sleep(delay_time)

        pyautogui.moveTo(variables["material_info"])
        pyautogui.click()
        log("clicked material info box")
        time.sleep(delay_time)

        pyautogui.write("nk_")
        log("typed 'nk_'")
        pyautogui.hotkey('ctrl', 'v')
        log(f"pasted {pyperclip.paste()}")
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(delay_time)
        if (f"nk_{original_name}" != pyperclip.paste()):
            log(f"was supposed to write nk_{original_name} but wrote {pyperclip.paste()}")
            print(f"was supposed to write nk_{original_name} but wrote {pyperclip.paste()}")
            force_exit()
        log(f"copied {pyperclip.paste()}")
        time.sleep(delay_time)
        pyautogui.moveTo(variables["ok_button"])
        pyautogui.click()
        log("clicked ok button")
        time.sleep(delay_time)

        pyautogui.hotkey('ctrl', 'v')
        log(f"pasted {pyperclip.paste()}")
        time.sleep(delay_time)
             
        pyautogui.hotkey('alt','d')
        log("focused folder path box")
        time.sleep(delay_time)

        pyautogui.write(folder_path)
        pyautogui.press('enter')
        log("wrote folder path")
        time.sleep(delay_time)

        pyautogui.hotkey('alt','s')
        log("saved")
        time.sleep(delay_time)  

    print("\nStarting automation. Press Ctrl+Shift+p to stop.")
    points_to_save = 10 #default

    if (justCalibrated):
        for i in range(2, 11):
            overlay.update_text_signal.emit(f"Status: Saving Entry {i}/10 PRESS CTRL+SHIFT+P TO FORCE QUIT")
            pyautogui.moveTo(variables[f"data_{i}"])
            pyautogui.click()
            save_spectrum_and_nk()

    while True:
        # 1. Update the prompt to reflect the current amount and the new hotkey
        if lastSavedFile is not None:
            msg = f"Select {points_to_save} items. Ctrl+Shift+K (Run) or Ctrl+Shift+I (Amount). Last: {lastSavedFile}"
        else:
            msg = f"Select {points_to_save} items. Ctrl+Shift+K (Run) or Ctrl+Shift+I (Amount)."
            
        print(msg)
        overlay.update_text_signal.emit(f"Status: {msg}")
    
        # 2. Wait for either hotkey using a threading event
        user_choice = threading.Event()
        chosen_action = None

        def handle_k():
            nonlocal chosen_action
            chosen_action = 'k'
            user_choice.set()

        def handle_i():
            nonlocal chosen_action
            chosen_action = 'i'
            user_choice.set()

        hk_k = keyboard.add_hotkey('ctrl+shift+k', handle_k)
        hk_i = keyboard.add_hotkey('ctrl+shift+i', handle_i)
        
        # Pause the script here until one of the callbacks sets the event
        user_choice.wait() 
        
        # Remove the hotkeys so they don't duplicate/stack on the next loop iteration
        keyboard.remove_hotkey(hk_k)
        keyboard.remove_hotkey(hk_i)
        
        # 3. Handle the terminal focus and input
        if chosen_action == 'i':
            # Force the Windows console to the front
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 5) # 5 = SW_SHOW
                ctypes.windll.user32.SetForegroundWindow(hwnd)
            
            overlay.update_text_signal.emit("Terminal: Waiting for user input...")
            
            try:
                new_amount = input(f"\nEnter the new number of data points to save (currently {points_to_save}): ")
                points_to_save = int(new_amount)
                
                # Safety check: prevent asking for more points than you actually calibrated
                max_calibrated = sum(1 for k, v in variables.items() if k.startswith("data_") and v is not None)
                if points_to_save > max_calibrated:
                    print(f"Warning: You only calibrated {max_calibrated} points. Capping limit at {max_calibrated}.")
                    points_to_save = max_calibrated
                    
            except ValueError:
                print("Invalid number. Keeping previous amount.")
                
            continue # Jump back to the top of the while loop to update the UI and wait again

        # 4. Handle the actual automation run
        if chosen_action == 'k':
            pyautogui.moveTo(variables["measure_tab"])
            pyautogui.click()

            for i in range(1, points_to_save + 1):
                overlay.update_text_signal.emit(f"Status: Saving Entry {i}/{points_to_save} PRESS CTRL+SHIFT+P TO FORCE QUIT")
                pyautogui.moveTo(variables[f"data_{i}"])
                pyautogui.click()
                save_spectrum_and_nk()
        
    overlay.update_text_signal.emit("Status: Automation Stopped")
    print("Automation stopped.")
    force_exit() # Close

# Main
if __name__ == '__main__':
    # 1. Start the Qt Application
    app = QApplication(sys.argv)

    # 2. Create and show the overlay
    overlay = TopOverlayBar()
    overlay.show()

    # 3. Start your automation script in a background "Daemon" thread
    # Setting it as a daemon means it will automatically die if the UI is closed
    automation_thread = threading.Thread(target=run_main, args=(overlay,), daemon=True)
    automation_thread.start()

    # 4. Start the Qt Event Loop (This blocks the main thread, keeping the UI alive)
    sys.exit(app.exec())
