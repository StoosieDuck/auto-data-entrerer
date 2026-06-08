import subprocess
import json
import threading
import os

try:
    import keyboard
    from pynput import mouse
    import pyautogui
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Would you like to install the required modules? (y/n)")
    choice = input()
    if choice == "y":
        print("Installing required modules...")
        subprocess.run(["pip", "install", "keyboard", "pynput", "pyautogui"])
        import keyboard
        from pynput import mouse
        import pyautogui
    else:
        print("Exiting program.")
        exit()

stopAutomation = False
keyboard.add_hotkey('ctrl+shift+c', lambda: setattr(globals(), 'stopAutomation', True))

folder_path = None
measure_tab = None
data_1 = None
data_2 = None
data_3 = None
data_4 = None
data_5 = None
data_6 = None
data_7 = None
data_8 = None
data_9 = None
data_10 = None
file_menu = None
save_spectrum = None
file_path_box = None
file_name_box = None
file_type_box = None
csv_file_select = None
save_nk_button = None
material_info = None

print("Welcome to the Auto Data Enterer for FILMapper! Please make sure that the 'Auto Position legends' box is unchecked in setup-> dislpay settings. If you had to uncheck it, please restart FILMapper")

#Step 1: Calibration
choice = input("Calibration: enter 1 to start calibration, enter 2 to import json file, enter 3 to exit: ")
if (choice == "1"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    if os.path.isfile(config_path):
        if input("A config.json file already exists. Do you want to overwrite it? (y/n): ") != "y":
            print("Exiting program.")
            exit()

    print("Enter the path to the folder where you would like the data to be saved (both saved spectrums and nk as csv files): ")
    folder_path = input()

    points = []
    click_event = threading.Event()

    def on_click(x, y, button, pressed):
        if pressed:
            points.append((x, y))
            click_event.set()

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    print("Please select first 10 data entries and then click Ctrl+Shift+k to continue")
    keyboard.wait('ctrl+shift+k')

    print("- Navigate to the 'measure' tab", end="", flush=True)
    click_event.clear()
    click_event.wait()
    measure_tab = points[-1]
    print(f" - {points[-1]}")

    print("- Select the first data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_1 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the file menu button", end="", flush=True)
    click_event.clear()
    click_event.wait()
    file_menu = points[-1]
    print(f" - {points[-1]}")

    print ("- Select the 'save measured spectrum' button", end="", flush=True)
    click_event.clear()
    click_event.wait()
    save_spectrum = points[-1]
    print(f" - {points[-1]}")

    print("- Select the file path box at the top of the file explorer window", end="", flush=True)
    click_event.clear()
    click_event.wait()
    folder_path_box = points[-1]
    print(f" - {points[-1]}")

    print("- Click the name of the file to be saved in the file explorer window, and then press Ctrl+A and then Ctrl+C", end="", flush=True)
    click_event.clear()
    click_event.wait()
    file_name_box = points[-1]
    print(f" - {points[-1]}")

    print("- Click the file type dropdown menu in the file explorer window", end="", flush=True)
    click_event.clear()
    click_event.wait()
    file_type_box = points[-1]
    print(f" - {points[-1]}")

    print("- Select CSV in the file type dropdown menu", end="", flush=True)
    click_event.clear()
    click_event.wait()
    csv_file_select = points[-1]
    print(f" - {points[-1]}")

    print("- Click save in the file explorer window", end="", flush=True)
    click_event.clear()
    click_event.wait()
    save_button = points[-1]
    print(f" - {points[-1]}")

    print("- Click the file menu button again")   
    click_event.clear()
    click_event.wait()

    print("- Click the 'save measured n and k' button", end="", flush=True)
    click_event.clear()
    click_event.wait()
    save_nk_button = points[-1]
    print(f" - {points[-1]}")

    print("- Click the big text box in the popup, type 'nk_' and then press Ctrl+V, then press Ctrl+A, then press Ctrl+C", end="", flush=True)
    click_event.clear()
    click_event.wait()
    material_info = points[-1]
    print(f" - {points[-1]}")

    print("- Click 'ok' in the popup to continue", end="", flush=True)
    click_event.clear()
    click_event.wait()
    ok_button = points[-1]
    print(f" - {points[-1]}")

    print("- Click the folder path box in the file explorer window again")
    click_event.clear()
    click_event.wait()

    print(f"- Input {folder_path} and then press enter in the file explorer window")
    click_event.clear()
    click_event.wait()

    print("- Click the file name box and then press Ctrl+A and then Ctrl+V")
    click_event.clear()
    click_event.wait()

    print("- Click the 'save' button in the file explorer window")
    click_event.clear()
    click_event.wait()

    print("- Select the second data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_2 = points[-1]
    print(f" - {points[-1]}")
    
    print("- Select the third data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_3 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the fourth data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_4 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the fifth data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_5 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the sixth data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_6 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the seventh data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_7 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the eigth data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_8 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the ninth data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_9 = points[-1]
    print(f" - {points[-1]}")

    print("- Select the tenth data entry", end="", flush=True)
    click_event.clear()
    click_event.wait()
    data_10 = points[-1]
    print(f" - {points[-1]}")
    
    data = {
        "folder_path": folder_path,
        "measure_tab": measure_tab,
        "data_1": data_1,
        "data_2": data_2,
        "data_3": data_3,
        "data_4": data_4,
        "data_5": data_5,
        "data_6": data_6,
        "data_7": data_7,
        "data_8": data_8,
        "data_9": data_9,
        "data_10": data_10,
        "file_menu": file_menu,
        "save_spectrum": save_spectrum,
        "folder_path_box": folder_path_box,
        "file_name_box": file_name_box,
        "file_type_box": file_type_box,
        "csv_file_select": csv_file_select,
        "save_nk_button": save_nk_button,
        "material_info": material_info
    }

    with open("config.json", "w") as f:
        json.dump(data, f)

    print("calibration complete. Points saved in json config file")
elif (choice == "2"):
    with open("config.json", "r") as f:
        data = json.load(f)
    folder_path = data["folder_path"]
    measure_tab = data["measure_tab"]
    data_1 = data["data_1"]
    data_2 = data["data_2"]
    data_3 = data["data_3"]
    data_4 = data["data_4"]
    data_5 = data["data_5"]
    data_6 = data["data_6"]
    data_7 = data["data_7"]
    data_8 = data["data_8"]
    data_9 = data["data_9"]
    data_10 = data["data_10"]
    file_menu = data["file_menu"]
    save_spectrum = data["save_spectrum"]
    folder_path_box = data["folder_path_box"]
    file_name_box = data["file_name_box"]
    file_type_box = data["file_type_box"]
    csv_file_select = data["csv_file_select"]
    save_nk_button = data["save_nk_button"]
    material_info = data["material_info"]
    print("Calibration data imported from config.json")
elif(choice == "3"):
    print("Exiting program.")
    exit()
else:
    print("Invalid input. Please enter 1, 2, or 3.")

# Step 2: Run automation script
def save_spectrum_and_nk():
    pyautogui.moveTo(file_menu)
    pyautogui.click()
    pyautogui.moveTo(save_spectrum)
    pyautogui.click()
    pyautogui.moveTo(folder_path_box)
    pyautogui.click()
    pyautogui.write(folder_path)
    pyautogui.press('enter')
    pyautogui.moveTo(file_name_box)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.moveTo(file_type_box)
    pyautogui.click()
    pyautogui.moveTo(csv_file_select)
    pyautogui.click()
    pyautogui.moveTo(save_button)
    pyautogui.click()
    pyautogui.moveTo(file_menu)
    pyautogui.click()
    pyautogui.moveTo(save_nk_button)
    pyautogui.click()
    pyautogui.moveTo(material_info)
    pyautogui.click()
    pyautogui.write("nk_")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.moveTo(ok_button)
    pyautogui.click()
    pyautogui.moveTo(folder_path_box)
    pyautogui.click()
    pyautogui.write(folder_path)
    pyautogui.press('enter')
    pyautogui.moveTo(file_name_box)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.moveTo(save_button)
    pyautogui.click()

print("Starting automation. To stop the automation at any time, please press Ctrl+Shift+c")
while not stopAutomation:
    print("Please select first 10 data entries and then click Ctrl+Shift+k to continue")
    keyboard.wait('ctrl+shift+k')
    pyautogui.moveTo(measure_tab)
    pyautogui.click()

    pyautogui.moveTo(data_1)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_2)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_3)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_4)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_5)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_6)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_7)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_8)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_9)
    pyautogui.click()
    save_spectrum_and_nk()

    pyautogui.moveTo(data_10)
    pyautogui.click()
    save_spectrum_and_nk()