import subprocess
import json
import threading
import os
import sys

# imports
try:
    import keyboard
    from pynput import mouse
    import pyautogui
    from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Would you like to install the required modules? (y/n)")
    choice = input()
    if choice == "y":
        print("Installing required modules...")
        subprocess.run(["pip", "install", "keyboard", "pynput", "pyautogui", "PyQt6"])
        import keyboard
        from pynput import mouse
        import pyautogui
        from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFrame
    from PyQt6.QtCore import Qt, pyqtSignal
    else:
        print("Exiting program.")
        exit()

stopAutomation = False

def force_exit():
    print("\nForce quitting automation...")
    os._exit(0) # Instantly kills the script and the Qt window

keyboard.add_hotkey('ctrl+shift+p', force_exit)

# Qt overlay
class TopOverlayBar(QWidget):
    # Signal to safely update the text from the background automation thread
    update_text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 30)

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
        self.container.setFixedSize(500, 30)
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

# Automation
def run_automation(overlay):
    global stopAutomation
    
    # Initialize variables to None
    variables = {
        "folder_path": None, "measure_tab": None, "data_1": None, "data_2": None, 
        "data_3": None, "data_4": None, "data_5": None, "data_6": None, 
        "data_7": None, "data_8": None, "data_9": None, "data_10": None,
        "file_menu": None, "save_spectrum": None, "folder_path_box": None,
        "file_name_box": None, "file_type_box": None, "csv_file_select": None,
        "save_button": None, "save_nk_button": None, "material_info": None, "ok_button": None
    }

    print("\nWelcome to the Auto Data Enterer for FILMapper!")
    print("Ensure 'Auto Position legends' is UNCHECKED in setup -> display settings.")

    choice = input("\nCalibration: enter 1 to start, 2 to import JSON, 3 to exit: ")
    
    if choice == "1":
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "config.json")
        if os.path.isfile(config_path):
            overlay.update_text_signal.emit("Terminal: config.json exists. Overwrite? (y/n)")
            if input("config.json exists. Overwrite? (y/n): ") != "y":
                print("Exiting program.")
                os._exit(0)

        overlay.update_text_signal.emit("Terminal: enter the path to the folder to save data")
        variables["folder_path"] = input("Enter the path to the folder to save data: ")

        points = []
        click_event = threading.Event()

        def on_click(x, y, button, pressed):
            if pressed:
                points.append((x, y))
                click_event.set()

        listener = mouse.Listener(on_click=on_click)
        listener.start()
        
        overlay.update_text_signal.emit("Please add first 10 data entries to measure and then click Ctrl+Shift+k to continue")
        print("\nPlease add first 10 data entries to measure and then click Ctrl+Shift+k to continue")

        keyboard.wait('ctrl+shift+k')

        # More efficient calibration process using a list of steps instead of repeating code
        steps = [
            ("measure_tab", "- Navigate to the 'measure' tab"),
            ("data_1", "- Select the first data entry"),
            ("file_menu", "- Select the file menu button"),
            ("save_spectrum", "- Select the 'save measured spectrum' button"),
            ("folder_path_box", "- Select the file path box at the top of explorer"),
            ("file_name_box", "- Click the name of the file, press Ctrl+A, Ctrl+C"),
            ("file_type_box", "- Click the file type dropdown menu"),
            ("csv_file_select", "- Select CSV in the dropdown"),
            ("save_button", "- Click save in the file explorer window"),
            (None, "- Click the file menu button again"),
            ("save_nk_button", "- Click the 'save measured n and k' button"),
            ("material_info", "- Click the big text box, type 'nk_', Ctrl+V, Ctrl+A, Ctrl+C"),
            ("ok_button", "- Click 'ok' in the popup"),
            (None, "- Click the folder path box again"),
            (None, f"- Input {variables['folder_path']} and press enter"),
            (None, "- Click the file name box, Ctrl+A, Ctrl+V"),
            (None, "- Click the 'save' button"),
            ("data_2", "Select the second data entry"),
            ("data_3", "Select the third data entry"),
            ("data_4", "Select the fourth data entry"),
            ("data_5", "Select the fifth data entry"),
            ("data_6", "Select the sixth data entry"),
            ("data_7", "Select the seventh data entry"),
            ("data_8", "Select the eigth data entry"),
            ("data_9", "Select the ninth data entry"),
            ("data_10", "Select the tenth data entry")
        ]

        for var_name, prompt in steps:
            overlay.update_text_signal.emit(prompt)
            print(prompt, end="", flush=True)
            click_event.clear()
            click_event.wait()
            if var_name:
                variables[var_name] = points[-1]
            print(f" - {points[-1]}")

        listener.stop()

        with open("config.json", "w") as f:
            json.dump(variables, f)
        print("Calibration complete. Saved to config.json")

    elif choice == "2":
        with open("config.json", "r") as f:
            variables = json.load(f)
        print("Calibration data imported.")
    else:
        print("Exiting program.")
        os._exit(0) # Forces the Qt App to close as well

    def save_spectrum_and_nk():
        pyautogui.moveTo(variables["file_menu"])
        pyautogui.click()
        pyautogui.moveTo(variables["save_spectrum"])
        pyautogui.click()
        pyautogui.moveTo(variables["folder_path_box"])
        pyautogui.click()
        pyautogui.write(variables["folder_path"])
        pyautogui.press('enter')
        pyautogui.moveTo(variables["file_name_box"])
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.moveTo(variables["file_type_box"])
        pyautogui.click()
        pyautogui.moveTo(variables["csv_file_select"])
        pyautogui.click()
        pyautogui.moveTo(variables["save_button"])
        pyautogui.click()
        
        pyautogui.moveTo(variables["file_menu"])
        pyautogui.click()
        pyautogui.moveTo(variables["save_nk_button"])
        pyautogui.click()
        pyautogui.moveTo(variables["material_info"])
        pyautogui.click()
        pyautogui.write("nk_")
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.moveTo(variables["ok_button"])
        pyautogui.click()
        
        pyautogui.moveTo(variables["folder_path_box"])
        pyautogui.click()
        pyautogui.write(variables["folder_path"])
        pyautogui.press('enter')
        pyautogui.moveTo(variables["file_name_box"])
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.moveTo(variables["save_button"])
        pyautogui.click()

    print("\nStarting automation. Press Ctrl+Shift+p to stop.")
    overlay.update_text_signal.emit("Status: Ready. Waiting for input.")

    while not stopAutomation:
        print("Please select next 10 data entries and then click Ctrl+Shift+k")
        overlay.update_text_signal.emit("Status: Select 10 items, Press Ctrl+Shift+K")
        
        keyboard.wait('ctrl+shift+k')
        if stopAutomation:
            break
            
        overlay.update_text_signal.emit("Status: Processing...")
        
        pyautogui.moveTo(variables["measure_tab"]); pyautogui.click()

        # Loop through data points to clean up the code
        for i in range(1, 11):
            if stopAutomation: 
                break
            overlay.update_text_signal.emit(f"Status: Saving Entry {i}/10")
            pyautogui.moveTo(variables[f"data_{i}"])
            pyautogui.click()
            save_spectrum_and_nk()
            
    overlay.update_text_signal.emit("Status: Automation Stopped")
    print("Automation stopped.")
    os._exit(0) # Close 

# Main
if __name__ == '__main__':
    # 1. Start the Qt Application
    app = QApplication(sys.argv)
    
    # 2. Create and show the overlay
    overlay = TopOverlayBar()
    overlay.show()

    # 3. Start your automation script in a background "Daemon" thread
    # Setting it as a daemon means it will automatically die if the UI is closed
    automation_thread = threading.Thread(target=run_automation, args=(overlay,), daemon=True)
    automation_thread.start()

    # 4. Start the Qt Event Loop (This blocks the main thread, keeping the UI alive)
    sys.exit(app.exec())