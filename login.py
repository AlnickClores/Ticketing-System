import tkinter as tk
from tkinter import messagebox
import sqlite3
from employeeDashboard import EmployeeDashboard
from ticketsDashboard import TicketsDashboard
from adminDashboard import AdminDashboard

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x250")
        self.current_frame = tk.Frame(self.root)
        self.root.resizable(False, False)

    def get_username(self):
        return self.get_username

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)

        tk.Label(self.current_frame, text="Login", font=("Helvetica", 20)).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Label(self.current_frame, text="Email:", font=("Helvetica", 12)).grid(row=3, column=0, pady=5, sticky="e")
        tk.Label(self.current_frame, text="Password:", font=("Helvetica", 12)).grid(row=4, column=0, pady=5, sticky="e")

        self.email_entry = tk.Entry(self.current_frame, font=("Helvetica", 12))
        self.password_entry = tk.Entry(self.current_frame, font=("Helvetica", 12), show="*")

        self.email_entry.grid(row=3, column=1)
        self.password_entry.grid(row=4, column=1)

        login_button = tk.Button(self.current_frame, text="Login", command=self.login, bg="#009CDF", fg="white", cursor="hand2")
        login_button.grid(row=5, column=0, columnspan=2, pady=10)
        login_button.config(font=("Helvetica", 12))
        login_button.config(borderwidth=0)
        login_button.config(activebackground="#007acc")
        login_button.config(padx="20")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Execute the query to check if the email and password match
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        # Close the connectionasddsolik
        connection.close()

        if user:
            name = user[1]
            user_email = user[2]
            role = user[4]
            if role == "Employee":
                messagebox.showinfo("Login", f"Welcome, {name}!")
                self.open_employee_dashboard(user_email)
            elif role == "IT Support":
                messagebox.showinfo("Login", f"Welcome, {name}!")
                self.open_tickets_dashboard(name)
            elif role == "Admin":
                messagebox.showinfo("Login", f"Welcome, {name}")
                self.open_admin_dashboard(name)
        else:
            messagebox.showerror("Login", "Invalid email or password")

    def open_employee_dashboard(self, user_email):
        self.root.withdraw()
        employee_dashboard_window = tk.Toplevel(self.root)
        employee_dashboard = EmployeeDashboard(employee_dashboard_window, user_email)
        employee_dashboard.show_dashboard()

    def open_tickets_dashboard(self, name):
        self.root.withdraw() 
        tickets_dashboard_window = tk.Toplevel(self.root) 
        tickets_dashboard = TicketsDashboard(tickets_dashboard_window, name)  
        tickets_dashboard.show_dashboard()
    
    def open_admin_dashboard(self, name):
        self.root.withdraw()
        admin_dashboard_window = tk.Toplevel(self.root)
        admin_dashboard_window = AdminDashboard(admin_dashboard_window, name)
        admin_dashboard_window.show_dashboard()
