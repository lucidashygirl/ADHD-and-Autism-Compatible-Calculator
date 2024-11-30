import platform
import pygame as py
import time
import os
import sys

if platform.system() == 'Linux':
    import tk
else:
    import tkinter as tk

# I hate you PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# For the sound effects ;)
py.init()
buttonPress = py.mixer.Sound(resource_path("sfx/buttonPress.mp3"))
explode = py.mixer.Sound(resource_path("sfx/explosion.mp3"))
correct = py.mixer.Sound(resource_path("sfx/correctSfx.mp3"))
incorrect = py.mixer.Sound(resource_path("sfx/incorrectSfx.mp3"))
delete = py.mixer.Sound(resource_path("sfx/delete.mp3"))
close = py.mixer.Sound(resource_path("sfx/closing.mp3"))

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("ADHD & Autism Compatible Calculator")
        self.master.resizable(False, False)
        self.master.geometry("400x610")
        self.master.configure(bg="mediumpurple2")
        self.master.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.master.iconbitmap(resource_path("sfx/epicLogo.ico"))

        # For shake
        self.doDisable = True

        # epic bg music
        py.mixer.music.load(resource_path("sfx/bg music.mp3"))
        py.mixer.music.play(-1)

        # Show answer
        self.text_result = "0"
        self.result = tk.Label(master, text=self.text_result, font=("bahnschrift", 24), anchor="e", bg="white", relief="sunken")
        self.result.pack(padx=10, pady=10, fill="x")

        # Grid system
        button_frame = tk.Frame(master, bg="mediumpurple2")  # Add a frame to hold buttons
        button_frame.pack(pady=20)

        # Button size
        button_width = 8
        button_height = 3

        # Number Buttons
        btn7 = tk.Button(button_frame, text="7", width=button_width, height=button_height, bg='chocolate1', command=lambda: self.number("7"))
        btn7.grid(row=0, column=0, padx=5, pady=5)
        btn8 = tk.Button(button_frame, text="8", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("8"))
        btn8.grid(row=0, column=1, padx=5, pady=5)
        btn9 = tk.Button(button_frame, text="9", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("9"))
        btn9.grid(row=0, column=2, padx=5, pady=5)
        btn4 = tk.Button(button_frame, text="4", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("4"))
        btn4.grid(row=1, column=0, padx=5, pady=5)
        btn5 = tk.Button(button_frame, text="5", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("5"))
        btn5.grid(row=1, column=1, padx=5, pady=5)
        btn6 = tk.Button(button_frame, text="6", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("6"))
        btn6.grid(row=1, column=2, padx=5, pady=5)
        btn1 = tk.Button(button_frame, text="1", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("1"))
        btn1.grid(row=2, column=0, padx=5, pady=5)
        btn2 = tk.Button(button_frame, text="2", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("2"))
        btn2.grid(row=2, column=1, padx=5, pady=5)
        btn3 = tk.Button(button_frame, text="3", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("3"))
        btn3.grid(row=2, column=2, padx=5, pady=5)
        btn0 = tk.Button(button_frame, text="0", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("0"))
        btn0.grid(row=3, column=1, padx=5, pady=5)

        # Operation Buttons
        btn_add = tk.Button(button_frame, text="+", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("+"))
        btn_add.grid(row=4, column=0, padx=5, pady=5)
        btn_subtract = tk.Button(button_frame, text="-", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("-"))
        btn_subtract.grid(row=4, column=1, padx=5, pady=5)
        btn_multiply = tk.Button(button_frame, text="*", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("*"))
        btn_multiply.grid(row=4, column=2, padx=5, pady=5)
        btn_divide = tk.Button(button_frame, text="/", width=button_width, height=button_height, bg='chocolate1',command=lambda: self.number("/"))
        btn_divide.grid(row=5, column=0, padx=5, pady=5)
        self.btn_equals = tk.Button(button_frame, text="=", width=button_width * 2 + 1, height=button_height, bg='OliveDrab1',command=self.calculate)
        self.btn_equals.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        self.btn_clear = tk.Button(button_frame, text="Clear", width=button_width * 2, height=button_height, bg='red',command=self.clear)
        self.btn_clear.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        self.btn_backspace = tk.Button(button_frame, text="Backspace", width=button_width + 3, height=button_height, bg='firebrick3',command=self.removeNumber)
        self.btn_backspace.grid(row=6, column=0, columnspan=5, padx=5, pady=5, sticky="se")
        self.btn_music = tk.Button(button_frame, text="Toggle Music", font=("TkDefaultFont", 7),  width=9, height=2, bg='orange',command=self.toggleMusic)
        self.btn_music.grid(row=7, column=2, columnspan=1, padx=5, pady=5, sticky="se")
        self.watermark = tk.Label(button_frame, text="Made by RileyIsPurple!", font=("TkDefaultFont", 8),bg="mediumpurple2")
        self.watermark.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

    def number(self, value):  # Add number/operator to expression
        py.mixer.Sound.play(buttonPress)
        if self.text_result == "0":
            self.text_result = value
        else:
            self.text_result += value
        self.result.config(text=self.text_result)

    def removeNumber(self):
        py.mixer.Sound.play(delete)
        self.text_result = self.text_result[:-1] # This slices/backspaces a character from string
        if not self.text_result:
            self.text_result = "0"
        self.result.config(text=self.text_result)
        self.doDisable = False
        self.shake_window(shakes=10, distance=4, interval=3)

    def onClosing(self):
        py.mixer.music.stop()
        py.mixer.Sound.play(close)
        self.master.withdraw() # Hide window
        time.sleep(2)
        self.master.destroy()

    def calculate(self):  # Perform calculation
        try:
            self.text_result = str(eval(self.text_result))  # Evaluate the expression
            py.mixer.Sound.play(correct)
        except Exception: # Exception
            py.mixer.Sound.play(incorrect)
            self.text_result = "Error"
            self.result.config(text=self.text_result)
            self.shake_window(shakes=45, distance=10, interval=15)
            self.text_result = "0"  # Clear
        self.result.config(text=self.text_result)

    def clear(self):
        py.mixer.Sound.play(explode)
        self.text_result = "0"  # Clear
        self.result.config(text=self.text_result)
        self.shake_window(shakes=45, distance=25, interval=2)

    def shake_window(self, shakes=0, distance=0, interval=0):
        """Makes the window shake by moving it back and forth."""
        # Disable the shake button while the window shakes
        if self.doDisable == True:
            self.btn_equals.config(state=tk.DISABLED, bg='gray')
            self.btn_clear.config(state=tk.DISABLED, bg='gray')
        self.doDisable = True
        
        original_x = self.master.winfo_x()  # Get the current x-coordinate of the window
        original_y = self.master.winfo_y()  # Get the current y-coordinate of the window
        
        for i in range(shakes):
            if i % 2 == 0:
                self.master.geometry(f'+{original_x + distance}+{original_y}')
            else:
                self.master.geometry(f'+{original_x - distance}+{original_y}')
            self.master.update()  # Update the window to reflect the new position
            self.master.after(interval)  # Wait before moving again

        # Return the window to its original position after shaking
        self.master.geometry(f'+{original_x}+{original_y}')

        # Re-enable the button after a short delay (interval * shakes + some buffer)
        self.btn_equals.config(state=tk.NORMAL, bg='OliveDrab1')
        self.btn_clear.config(state=tk.NORMAL, bg='red')

    def toggleMusic(self):
        if py.mixer_music.get_busy() == True:
            py.mixer.music.stop()
        else:
            py.mixer.music.play(-1)
        


if __name__ == "__main__":
    window = tk.Tk()
    app = Calculator(window)
    window.mainloop()
