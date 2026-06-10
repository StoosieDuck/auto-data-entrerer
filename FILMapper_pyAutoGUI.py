    import subprocess
    import json
    import threading
    import os
    import sys
    import time
    import datetime

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

    file_explorer_corners[] #top right, top left...
    points = []

    def force_exit():
        print("\nForce quitting automation...")
        log("force quit", True)
        os._exit(0) # Instantly kills the script and the Qt window

    # Resolve config path once so it's available for all branches
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    logfile_path = os.path.join(script_dir, "log.txt")

    def log(text, newLine):
        with open (logfile_path, "w", encoding="utfi-8") as logfile:
            if newLine:
                file.write(f"{datetime.now()} : {text}\n")
            else:
                file.write(f"{datetime.now()} : {text}")

    keyboard.add_hotkey('ctrl+shift+p', force_exit)

    # Qt overlay
    class TopOverlayBar(QWidget):
        # Signal to safely update the text from the background automation thread
        update_text_signal = pyqtSignal(str)

        def __init__(self):
            super().__init__()
            self.setFixedSize(600, 30)

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
            self.container.setFixedSize(600, 30)
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

        # Initialize variables to None
        variables = {
            "measure_tab": None, "data_1": None, "data_2": None,
            "data_3": None, "data_4": None, "data_5": None, "data_6": None,
            "data_7": None, "data_8": None, "data_9": None, "data_10": None,
            "file_menu": None, "save_spectrum": None, "folder_path_box": None,
            "file_name_box": None, "file_type_box": None, "csv_file_select": None,
            "save_button": None, "save_nk_button": None, "material_info": None, "ok_button": None
        }

        print("\nWelcome to the Auto Data Enterer for FILMapper!")
        print("Ensure 'Auto Position legends' is UNCHECKED in setup -> display settings.")
        log(fdatetime.now()), True

        overlay.update_text_signal.emit("Terminal: enter the path to the folder to save data")
        folder_path = input("Enter the path to the folder to save data: ")
        log(f"Folder path: {folder_path}", True)

        choice = input("\nCalibration: enter 1 to start, 2 to import JSON, 3 to exit: ")
        log(f"User chose {choice}", True)
    
        if choice == "1":
            if os.path.isfile(config_path):
                overlay.update_text_signal.emit("Terminal: config.json exists. Overwrite? (y/n)")
                log("config.json exists", True)
                if input("config.json exists. Overwrite? (y/n): ") != "y":
                    log("user chose to overrite config.json", True)
                    print("Exiting program.")
                    force_exit()

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
            # Uses architecture: variable to be changed, prompt for terminal and overlay, and then keyboard input for if it requires that 
            steps = [
                ("measure_tab", "Navigate to the 'measure' tab"), None,
                ("data_1", "Select the first data entry", None),
                ("file_menu", "Select the file menu button", None),
                ("save_spectrum", "Select the 'save measured spectrum' button"), None,
                ("folder_path_box", "Select the file path box at the top of explorer", None),
                ("file_name_box", "Click the name of the file, press Ctrl+A, Ctrl+C", 'ctrl+c'),
                ("file_type_box", "Click the file type dropdown menu", None),
                ("csv_file_select", "Select CSV in the dropdown", None),
                ("save_button", "Click save in the file explorer window", None),
                (None, "Click the file menu button again", None),
                ("save_nk_button", "Click the 'save measured n and k' button", None),
                ("material_info", "Click the big text box, type 'nk_', Ctrl+V, Ctrl+A, Ctrl+C", 'ctrl+c'),
                ("ok_button", "Click 'ok' in the popup", None),
                (None, "Click the folder path box again"), None,
                (None, f"Input {variables['folder_path']} and press enter", 'enter'),
                (None, "Click the file name box, Ctrl+A, Ctrl+V"), 'ctrl+v',
                (None, "Click the 'save' button", None),
                ("data_2", "Select the second data entry", None),
                ("data_3", "Select the third data entry", None),
                ("data_4", "Select the fourth data entry", None),
                ("data_5", "Select the fifth data entry"), None,
                ("data_6", "Select the sixth data entry", None),
                ("data_7", "Select the seventh data entry"), None,
                ("data_8", "Select the eigth data entry", None),
                ("data_9", "Select the ninth data entry", None),
                ("data_10", "Select the tenth data entry", None)
            ]

            for var_name, prompt, keypress in steps:
                overlay.update_text_signal.emit(prompt)
                print(prompt, end="", flush=True)
                start_time = time.perf_counter()
                click_event.clear()
                click_event.wait()
                end_time - time.perf_counter()
                if keypress:
                    keyboard.wait(keypress)
                if var_name:
                    variables[var_name] = points[-1]
                print(f" - {points[-1]} - {end_time - start_time} sec")
                log(f"{var_name} - {points[-1]} - {end_time - start_time} sec", True)
    
            listener.stop()

            with open(config_path, "w") as f:
                json.dump(variables, f)
            print("Calibration complete. Saved to config.json")
            log("Calibration Complete", True)
            justCalibrated = True

        elif choice == "2":
            # Load calibration data if available; provide a helpful message if not
            if not os.path.isfile(config_path):
                overlay.update_text_signal.emit("Terminal: config.json not found. Please run calibration first (press 1).")
                print("Error: config.json not found. Please run calibration first (enter 1).\nExiting program.")
                log("config.json not found", True)
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
            log("Moved to file menu", True)
            time.sleep(1)
            pyautogui.moveTo(variables["save_spectrum"])
            pyautogui.click()
            log("Saved spectrum", True)
            time.sleep(1)
            pyautogui.moveTo(variables["folder_path_box"])
            pyautogui.click()
            log("clicked folder path box", True)
            time.sleep(1)
            pyautogui.write(folder_path)
            pyautogui.press('enter')
            log(f"wrote folder path {folder_path}", True)
            time.sleep(1)
            pyautogui.moveTo(variables["file_name_box"])
            pyautogui.click()
            log("clicked file name box", True)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            log("selected file name (ctrl+a)")
            pyautogui.hotkey('ctrl', 'c')
            log(f"copied {pyperclip.paste()}")
            original_name = pyperclip.paste()
            time.sleep(1)
            pyautogui.moveTo(variables["file_type_box"])
            pyautogui.click()
            log("clicked file type dropdown", True)
            time.sleep(1)
            pyautogui.moveTo(variables["csv_file_select"])
            pyautogui.click()
            log("selected csv", True)
            time.sleep(1)
            pyautogui.moveTo(variables["save_button"])
            pyautogui.click()
            log("saved spectrum")
            time.sleep(1)
        
            pyautogui.moveTo(variables["file_menu"])
            pyautogui.click()
            log("clicked file menu")
            time.sleep(1)
            pyautogui.moveTo(variables["save_nk_button"])
            pyautogui.click()
            log("clicked save n and k button")
            time.sleep(1)
            pyautogui.moveTo(variables["material_info"])
            pyautogui.click()
            log("clicked material info box")
            time.sleep(1)
            pyautogui.write("nk_")
            log("typed 'nk_'")
            pyautogui.hotkey('ctrl', 'v')
            log(f"pasted {pyperclip.paste()}")
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            if (f"nk_{original_name}" != pyperclip.paste):
                log(f"was supposed to write nk_{original_name} but wrote {pyperclip.paste}")
                print(f"was supposed to write nk_{original_name} but wrote {pyperclip.paste}")
                force_exit()
            log(f"copied {pyperclip.paste()}")
            time.sleep(1)
            pyautogui.moveTo(variables["ok_button"])
            pyautogui.click()
            log("clicked ok button")
            time.sleep(1)

            overlay.update_text_signal.emit("Please select the top right corner of the file explorer window")
            click_event.clear()
            click_event.wait()
            top_right_corner = points[-1]
            overlay.update_text_signal.emit("Please select the bottom left corner of the file explorer window")
            click_event.clear()
            click_event.wait()
            bottom_left_corner = points[-1]     
            file_explorer_corners.append((top_right_corner, bottom_left_corner))
            log(f"bottom left: {bottom_left_corner}, top right: {top_right_corner}")
            print(f"bottom left: {bottom_left_corner}, top right: {top_right_corner}")       

            pyautogui.moveTo(variables["folder_path_box"])
            pyautogui.click()
            log("clicked folder path box")
            time.sleep(1)
            pyautogui.write(folder_path)
            pyautogui.press('enter')
            log("wrote folder path")
            time.sleep(1)
            pyautogui.moveTo(variables["file_name_box"])
            pyautogui.click()
            log("clicked file name box")
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'v')
            log(f"pasted {pyperclip.paste}")
            time.sleep(1)
            pyautogui.moveTo(variables["save_button"])
            pyautogui.click()
            time.sleep(1)

        print("\nStarting automation. Press Ctrl+Shift+p to stop.")

        if (justCalibrated):
            for i in range(2, 11):
                overlay.update_text_signal.emit(f"Status: Saving Entry {i}/10 PRESS CTRL+SHIFT+P TO FORCE QUIT")
                pyautogui.moveTo(variables[f"data_{i}"])
                pyautogui.click()
                save_spectrum_and_nk()

        while True:
            print("Please select next 10 data entries and then click Ctrl+Shift+k. Press Ctrl+Shift+P to exit")
            overlay.update_text_signal.emit("Status: Select 10 items, Press Ctrl+Shift+K. Press Ctrl+Shift+P to exit")
        
            keyboard.wait('ctrl+shift+k')
            
            overlay.update_text_signal.emit("Status: Processing...")
        
            pyautogui.moveTo(variables["measure_tab"]); pyautogui.click()

            # Loop through data points to clean up the code
            for i in range(1, 11):
                overlay.update_text_signal.emit(f"Status: Saving Entry {i}/10 PRESS CTRL+SHIFT+P TO FORCE QUIT")
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
        automation_thread = threading.Thread(target=run_automation, args=(overlay,), daemon=True)
        automation_thread.start()

        # 4. Start the Qt Event Loop (This blocks the main thread, keeping the UI alive)
        sys.exit(app.exec())
