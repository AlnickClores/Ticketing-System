import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from login import Login

class Register:
    def __init__(self, root):
        self.root = root
        self.current_frame = None

    def show_register(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)
        self.show_password_var = tk.BooleanVar()

        tk.Label(self.current_frame, text="Register", font=("Helvetica", 22)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Name:", "Email:", "Password:", "Confirm Password:"]
        for i, label_text in enumerate(labels, start=1):
            tk.Label(self.current_frame, text=label_text, font=("Helvetica", 14), anchor="e").grid(row=i, column=0, sticky="e", pady=5)

        tk.Label(self.current_frame, text="Role:", font=("Helvetica", 14)).grid(row=6, column=0, sticky="e", pady=5)
        
        self.new_name_entry = tk.Entry(self.current_frame, font=("Helvetica", 14))
        self.new_email_entry = tk.Entry(self.current_frame, font=("Helvetica", 14))
        self.new_password_entry = tk.Entry(self.current_frame, font=("Helvetica", 14), show="*")
        self.new_confirm_password_entry = tk.Entry(self.current_frame, font=("Helvetica", 14), show="*")
        self.show_password_checkbox = tk.Checkbutton(self.current_frame, text="Show Password", font=("Helvetica", 14), variable=self.show_password_var, command=self.toggle_password_visibility)
        self.new_role_combo = ttk.Combobox(self.current_frame, font=("Helvetica", 14), values=["Select a role", "IT Support", "Employee"], state="readonly")
        self.new_role_combo.current(0)

        entries = [self.new_name_entry, self.new_email_entry, self.new_password_entry, self.new_confirm_password_entry, self.show_password_checkbox, self.new_role_combo]
        for i, entry in enumerate(entries, start=1):
            entry.grid(row=i, column=1, sticky="w", padx=(10, 0), pady=5)

        register_button = tk.Button(self.current_frame, text="Register", command=self.register, bg="#009CDF", fg="white", cursor="hand2")
        register_button.config(font=("Helvetica", 14))
        register_button.config(borderwidth=0)
        register_button.config(activebackground="#007acc")
        register_button.config(padx="20")
        register_button.grid(row=7, column=0, columnspan=2, pady=30)

        self.login_label = tk.Label(self.current_frame, text="Already have an account? Login here.", fg="#2486e6", cursor="hand2", font=("Helvetica", 12))
        self.login_label.grid(row=8, column=0, columnspan=2, sticky="n")
        self.login_label.bind("<Button-1>", self.redirect_to_login)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.new_password_entry.config(show="")
            self.new_confirm_password_entry.config(show="")
        else:
            self.new_password_entry.config(show="*")
            self.new_confirm_password_entry.config(show="*")

    def redirect_to_login(self, event):
        self.current_frame.destroy()  # Destroy the current frame
        login_window = Login(self.root)  # Instantiate the Login class with root
        login_window.show_login()  # Show the login window

    def register(self):
        # Get input values from entries and combobox
        new_name = self.new_name_entry.get()
        new_email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.new_confirm_password_entry.get()
        new_role = self.new_role_combo.get()

        # Check if any field is empty
        if not all([new_name, new_email, new_password, new_role]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Check if passwords match
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Check if email already exists
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (new_email,))
        existing_user = cursor.fetchone()
        connection.close()

        if existing_user:
            messagebox.showerror("Error", "Account email already exists!")
            return

        # Store user data in the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", (new_name, new_email, new_password, new_role))
        connection.commit()
        connection.close()

        # Print registration details
        print(f"Registered New User: Name - {new_name}, Email = {new_email}, Password - {new_password}, Role - {new_role}")
        messagebox.showinfo("Register", "Registration successful!")

        # Clear entry fields
        self.new_name_entry.delete(0, tk.END)
        self.new_email_entry.delete(0, tk.END)
        self.new_password_entry.delete(0, tk.END)
        self.new_confirm_password_entry.delete(0, tk.END)
        self.new_role_combo.current(0)