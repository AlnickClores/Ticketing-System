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
        # Clear the main content area
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add your account-related content here
        account_label = tk.Label(self.main_frame, text="My Account", font=("Helvetica", 20))
        account_label.pack(pady=(20, 10))

        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Fetch user information
        cursor.execute("SELECT * FROM users WHERE name=?", (self.name,))
        user_info = cursor.fetchone()

        connection.close()

        if user_info:
            # Display user information
            user_frame = tk.Frame(self.main_frame, bd=1, relief="solid", padx=10, pady=10)
            user_frame.pack(fill="both", padx=20, pady=10)

            tk.Label(user_frame, text=f"Name: {user_info[1]}", font=("Helvetica", 12)).pack(anchor="w")
            tk.Label(user_frame, text=f"Email: {user_info[2]}", font=("Helvetica", 12)).pack(anchor="w")
            tk.Label(user_frame, text=f"Role: {user_info[4]}", font=("Helvetica", 12)).pack(anchor="w")

            # Button to change password
            change_password_button = tk.Button(self.main_frame, text="Change Password", font=("Helvetica", 12), cursor="hand2", command=self.open_change_password_frame)
            change_password_button.pack(pady=10)
        else:
            # Display message if user not found
            no_user_label = tk.Label(self.main_frame, text="User not found.", font=("Helvetica", 12))
            no_user_label.pack(pady=(10, 10))

    def open_change_password_frame(self):
        # Create a new window for changing password
        change_password_window = tk.Toplevel(self.root)
        change_password_window.title("Change Password")
        change_password_window.geometry("300x150")
        change_password_window.resizable(False, False)

        # Labels and entry widgets for current and new password
        tk.Label(change_password_window, text="Current Password:", font=("Helvetica", 12)).pack()
        current_password_entry = tk.Entry(change_password_window, show="*", font=("Helvetica", 12))
        current_password_entry.pack()

        tk.Label(change_password_window, text="New Password:", font=("Helvetica", 12)).pack()
        new_password_entry = tk.Entry(change_password_window, show="*", font=("Helvetica", 12))
        new_password_entry.pack()

        # Button to confirm password change
        confirm_button = tk.Button(change_password_window, text="Confirm", font=("Helvetica", 12), cursor="hand2", command=lambda: self.change_password(current_password_entry.get(), new_password_entry.get()))
        confirm_button.pack(pady=10)

    def change_password(self, current_password, new_password):
        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Fetch user's current password from the database
        # Check if the entered current password matches the saved password
        cursor.execute("SELECT COUNT(*) FROM users WHERE name=? AND password=?", (self.name, current_password))
        match_count = cursor.fetchone()[0]

        if match_count == 0:
            messagebox.showerror("Error", "Incorrect current password!")
        else:
            # Update the password in the database
            cursor.execute("UPDATE users SET password=? WHERE name=?", (new_password, self.name))
            connection.commit()
            messagebox.showinfo("Success", "Password updated successfully!")

        connection.close()

    def create_ticket(self):
        title = self.title_entry.get()
        category = self.category_combo.get()
        description = self.description_entry.get("1.0", "end-1c")
        priority = self.priority_var.get()
        status = "Pending"
        assignedTo = "None"
        created_by = self.name
        created_at = datetime.now().strftime("%d/%m/%Y %I:%M%p")
        resolved_at = None

        # Check if any field is empty
        if not all([title, category, description, priority]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Store ticket data in the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tickets (title, category, description, priority, status, assignedTo, created_by, created_at, resolved_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (title, category, description, priority, status, assignedTo, created_by, created_at, resolved_at))
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