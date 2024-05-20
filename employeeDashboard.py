import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3

class EmployeeDashboard:
    def __init__(self, root, user_email):
        self.root = root
        self.root.title("Employee Dashboard")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.user_email = user_email
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        self.name = self.get_user_name()
        if not self.name:
            messagebox.showerror("Error", "User not found!")
            return
        
        self.show_dashboard()

    def show_dashboard(self):
        # Clear the current frame
        for widget in self.current_frame.winfo_children():
            widget.destroy()

        # Sidebar
        sidebar_frame = tk.Frame(self.current_frame, width=200, bg="#151515")
        sidebar_frame.pack(side="left", fill="y")

        tk.Label(sidebar_frame, text=f"Hello, {self.name}", font=("Helvetica", 15), bg="#151515", fg="white", padx=10, pady=10).pack(fill="x")

        # Sidebar items
        sidebar_items = ["Dashboard", "My Account"]
        for item in sidebar_items:
            tk.Button(sidebar_frame, text=item, font=("Helvetica", 12), bg="#151515", fg="white", padx=50, pady=10, command=lambda i=item: self.show_content(i)).pack(fill="x", padx=10, pady=10)

        # Logout button
        tk.Button(sidebar_frame, text="Logout", font=("Helvetica", 12), bg="#151515", fg="white", padx=50, pady=10, command=self.logout).pack(side="bottom", fill="x", padx=10, pady=10)

        # Main content area
        self.main_frame = tk.Frame(self.current_frame)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Initialize the dashboard content
        self.show_dashboard_content()

    def show_content(self, content):
        # Clear the main content area
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if content == "Dashboard":
            self.show_dashboard_content()
        elif content == "My Account":
            self.show_my_account_content()

    def show_dashboard_content(self):
        # Employee Dashboard title
        tk.Label(self.main_frame, text="Employee Dashboard", font=("Helvetica", 20)).pack(pady=(10, 110))

        tk.Label(self.main_frame, text="Ticket Form", font=("Helvetica", 18)).pack(pady=(10, 20))

        # Title entry
        title_frame = tk.Frame(self.main_frame)
        title_frame.pack(padx=20, pady=(0, 15))
        tk.Label(title_frame, text="Title:", font=("Helvetica", 12), width=10, anchor="e").pack(side="left")
        self.title_entry = tk.Entry(title_frame, font=("Helvetica", 12))
        self.title_entry.pack(side="left")

        # Category combobox
        category_frame = tk.Frame(self.main_frame)
        category_frame.pack(padx=20, pady=(0, 15))
        tk.Label(category_frame, text="Category:", font=("Helvetica", 12), width=10, anchor="e").pack(side="left")
        self.category_combo = ttk.Combobox(category_frame, values=["Hardware", "Software", "Network"], state="readonly", font=("Helvetica", 12))
        self.category_combo.pack(side="left")

        # Description entry (Text area with placeholder)
        description_frame = tk.Frame(self.main_frame)
        description_frame.pack(padx=20, pady=(0, 15))
        self.description_entry = tk.Text(description_frame, font=("Helvetica", 12), height=5, width=30)
        self.description_entry.pack(side="left")
        self.description_entry.insert("1.0", "Enter Issue Description Here")
        self.description_entry.bind("<FocusIn>", self.clear_placeholder)
        self.description_entry.bind("<FocusOut>", self.restore_placeholder)

        # Priority radio buttons
        priority_frame = tk.Frame(self.main_frame)
        priority_frame.pack(padx=20, pady=(0, 7))
        tk.Label(priority_frame, text="Priority:", font=("Helvetica", 12), width=10, anchor="e").pack(side="left")
        self.priority_var = tk.StringVar(value="Low")
        self.low_radio = tk.Radiobutton(priority_frame, text="Low", variable=self.priority_var, value="Low", font=("Helvetica", 12))
        self.low_radio.pack(side="left")
        self.medium_radio = tk.Radiobutton(priority_frame, text="Medium", variable=self.priority_var, value="Medium", font=("Helvetica", 12))
        self.medium_radio.pack(side="left")
        self.high_radio = tk.Radiobutton(priority_frame, text="High", variable=self.priority_var, value="High", font=("Helvetica", 12))
        self.high_radio.pack(side="left")

        # Create Ticket button
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        create_ticket_button = tk.Button(button_frame, text="Create Ticket", command=self.create_ticket, font=("Helvetica", 12))
        create_ticket_button.pack()


    def clear_placeholder(self, event):
        if self.description_entry.get("1.0", "end-1c") == "Enter Issue Description Here":
            self.description_entry.delete("1.0", "end-1c")
            self.description_entry.config(fg="white")

    def restore_placeholder(self, event):
        if not self.description_entry.get("1.0", "end-1c"):
            self.description_entry.insert("1.0", "Enter Issue Description Here")
            self.description_entry.config(fg="grey")


    def show_my_account_content(self):
        tk.Label(self.main_frame, text="My Account", font=("Helvetica", 16)).pack(pady=10)
        # Add content for the My Account section here

    def create_ticket(self):
        title = self.title_entry.get()
        category = self.category_combo.get()
        description = self.description_entry.get("1.0", "end-1c")
        priority = self.priority_var.get()
        status = "Pending"
        assignedTo = "None"
        created_by = self.name
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if any field is empty
        if not all([title, category, description, priority]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Store ticket data in the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tickets (title, category, description, priority, status, assignedTo, created_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (title, category, description, priority, status, assignedTo, created_by, created_at))
        connection.commit()
        connection.close()

        # Print ticket details
        print("Ticket created successfully!")
        messagebox.showinfo("Create Ticket", "Ticket created successfully!")

        # Clear entry fields
        self.title_entry.delete(0, tk.END)
        self.category_combo.set("")
        self.description_entry.delete("1.0", "end")
        self.low_radio.select()

    def get_user_name(self):
        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Execute the query to get the user's name based on email
        cursor.execute("SELECT name FROM users WHERE email=?", (self.user_email,))
        user = cursor.fetchone()

        # Close the connection
        connection.close()

        if user:
            return user[0]
        else:
            return None

    def logout(self):
        messagebox.showinfo("Logout", "Logged out successfully!")
        self.root.destroy()