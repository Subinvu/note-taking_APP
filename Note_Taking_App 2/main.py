import tkinter as tk
from gui.login import LoginScreen

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
