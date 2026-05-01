import tkinter as tk
from pynput import mouse

class Calibrator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calibration")
        self.root.geometry("400x100")
        
        self.points = []
        self.label = tk.Label(self.root, text="Click anywhere on screen (0/3)", font=("Arial", 12))
        self.label.pack(pady=20)
        
        # Start the mouse listener in a non-blocking way
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()
        
        self.root.mainloop()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.points.append((int(x), int(y)))
            
            # Update the UI
            display_text = " ".join([f"click {i+1}: {p}" for i, p in enumerate(self.points)])
            self.label.config(text=display_text)
            
            if len(self.points) >= 3:
                self.listener.stop()
                print(f"Final Calibration: {self.points}")
                # Optional: self.root.after(2000, self.root.destroy) # Close after 2 seconds

if __name__ == "__main__":
    Calibrator()
