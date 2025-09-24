from maple import *
import tkinter as tk
import ctypes

# -------- Windows DPI 适配 --------
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Windows 8.1+
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()  # Windows 7
    except Exception:
        pass

# -------- Tkinter GUI --------

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        
        self.root.title("Competition Result Analysis")
        label = tk.Label(self.root, text="Input a valid WCA ID", font=('Segoe UI', 18))
        label.pack(padx=20, pady=20)

        # wcaID = input("Please input the WCA ID: ")
        self.wcaID = tk.StringVar()
        self.frame = tk.Frame(self.root)

        identry = tk.Entry(self.frame, textvariable=self.wcaID, font=("Arial", 18), width=15)
        identry.grid(row=0, column=0)

        button = tk.Button(self.frame, text="Submit", command=self.get_input, font=("Arial", 12))
        button.grid(row=0, column=1)

        self.frame.pack()

        self.output = tk.Text(self.root, height=10, width=50, font=('Arial', 16))
        self.output.pack(pady=10)

        self.root.mainloop()

    def get_input(self):
        wca_id = self.wcaID.get() 
        filename = getRecent(wca_id) 
        result = gendata(filename)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, filename+'\n')
        self.output.insert(tk.END, result)

MyGUI()