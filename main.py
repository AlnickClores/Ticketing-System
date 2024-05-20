import tkinter as tk
from registration import Register
from login import Login

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ticketing System")
    root.tk.call("source", "AzureTheme/azure.tcl")
    root.tk.call("set_theme", "dark")

    register_window = Register(root)
    login_window = Login(root)

    register_window.show_register()

    window_width = 900
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.resizable(False, False)
    root.mainloop()
