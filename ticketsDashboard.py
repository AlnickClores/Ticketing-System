import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from datetime import datetime

class TicketsDashboard:
    def __init__(self, root, name):
        self.root = root
        self.root.title("Tickets Dashboard")
        self.root.geometry("900x700")
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.root.resizable(False, False)
        self.name = name

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
        sidebar_items = ["Dashboard", "Tickets Solved", "My Account"]
        for item in sidebar_items:
            tk.Button(sidebar_frame, text=item, font=("Helvetica", 12), bg="#151515", fg="white", padx=50, pady=10, command=lambda i=item: self.show_content(i)).pack(fill="x", padx=10, pady=10)

        # Logout button
        tk.Button(sidebar_frame, text="Logout", font=("Helvetica", 12), bg="#151515", fg="white", padx=50, pady=10, command=self.logout).pack(side="bottom", fill="x", padx=10, pady=10)

        # Main content area with scrollbar
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
        elif content == "Tickets Solved":
            self.show_tickets_solved_content()
        elif content == "My Account":
            self.show_my_account_content()

    def show_dashboard_content(self):
        # Header
        header_label = tk.Label(self.main_frame, text="Dashboard", font=("Helvetica", 20))
        header_label.pack(pady=(20, 10))

        # Filter dropdown
        filter_options = ['Date (Recent)', 'Priority (Highest)']
        self.filter_var = tk.StringVar()
        self.filter_var.set(filter_options[1])
        filter_dropdown = ttk.Combobox(self.main_frame, textvariable=self.filter_var, values=filter_options, state="readonly")
        filter_dropdown.pack(pady=10)

        # Frame for ticket cards
        cards_frame = tk.Frame(self.main_frame)
        cards_frame.pack(expand=True, fill="both")

        canvas = tk.Canvas(cards_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(cards_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(canvas)
        self.inner_frame.pack(fill="both", expand=True)
        
        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Retrieve and filter tickets
        tickets = self.get_tickets()
        self.filter_tickets(tickets)

        # Bind mouse wheel event for scrolling
        canvas.bind("<Configure>", lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Bind filter change event
        self.filter_var.trace_add('write', self.on_filter_change)

    def show_tickets_solved_content(self):
        # Clear the main content area
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Display text for solved tickets
        solved_label = tk.Label(self.main_frame, text="Solved Tickets", font=("Helvetica", 20))
        solved_label.pack(pady=(20, 10))

        # Frame for ticket cards
        cards_frame = tk.Frame(self.main_frame)
        cards_frame.pack(expand=True, fill="both")

        canvas = tk.Canvas(cards_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(cards_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        tickets_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=tickets_frame, anchor="nw")

        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Fetch solved tickets assigned to the user
        cursor.execute("SELECT * FROM tickets WHERE status='Resolved' AND assignedTo=?", (self.name,))
        solved_tickets = cursor.fetchall()

        connection.close()

        if solved_tickets:
            for ticket in solved_tickets:
                ticket_frame = tk.Frame(tickets_frame, bd=1, relief="solid", padx=10, pady=10)
                ticket_frame.pack(fill="x", pady=5)

                tk.Label(ticket_frame, text=f"Ticket ID: {ticket[0]}", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
                tk.Label(ticket_frame, text=f"Title: {ticket[1]}", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
                tk.Label(ticket_frame, text=f"Category: {ticket[2]}", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
                tk.Label(ticket_frame, text=f"Description: {ticket[3]}", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")
                tk.Label(ticket_frame, text=f"Priority: {ticket[6]}", font=("Helvetica", 12)).grid(row=4, column=0, sticky="w")
                tk.Label(ticket_frame, text=f"Created By: {ticket[7]}", font=("Helvetica", 12)).grid(row=5, column=0, sticky="w")
                tk.Label(ticket_frame, text=f"Created At: {ticket[8]}", font=("Helvetica", 12)).grid(row=6, column=0, sticky="w")
                tk.Label(ticket_frame, text=f"Resolved At: {ticket[9]}", font=("Helvetica", 12)).grid(row=7, column=0, sticky="w")
        else:
            no_tickets_label = tk.Label(tickets_frame, text="No solved tickets found.", font=("Helvetica", 12))
            no_tickets_label.pack(pady=(10, 10))

        # Update scroll region after widgets are added
        tickets_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


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



    def get_tickets(self):
        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Execute the query to retrieve tickets
        cursor.execute("SELECT * FROM tickets WHERE status !='Resolved'")
        tickets = cursor.fetchall()

        # Close the connection
        connection.close()

        return tickets

    def filter_tickets(self, tickets):
        filter_option = self.filter_var.get()
        if filter_option == 'Priority (Highest)':
            # Define a mapping for priority values
            priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
            # Sort tickets based on priority, using the priority_map
            tickets = sorted(tickets, key=lambda x: priority_map.get(x[6], 0), reverse=True)
        elif filter_option == 'Date (Recent)':
            tickets = sorted(tickets, key=lambda x: x[8], reverse=True)

        self.display_tickets(tickets)


    def display_tickets(self, tickets):
        # Clear existing ticket cards
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Display tickets in a card format
        for ticket in tickets:
            self.create_ticket_card(ticket)

    def create_ticket_card(self, ticket):
        ticket_frame = tk.Frame(self.inner_frame, bd=2, relief="groove", padx=20, pady=15)
        ticket_frame.pack(padx=230, pady=10, fill="both", expand=True, anchor="center")

        tk.Label(ticket_frame, text=f"Title: {ticket[1]}", font=("Helvetica", 13)).pack()
        tk.Label(ticket_frame, text=f"Category: {ticket[2]}", font=("Helvetica", 12)).pack()
        tk.Label(ticket_frame, text=f"Priority: {ticket[6]}", font=("Helvetica", 12)).pack()
        tk.Label(ticket_frame, text=f"Status: {ticket[4]}", font=("Helvetica", 12)).pack()  

        open_ticket_btn = tk.Button(ticket_frame, text="Open Ticket", font=("Helvetica", 12), bg="#007fff", fg="white", cursor="hand2", command=lambda: self.open_ticket_frame(ticket))
        open_ticket_btn.pack(pady=10)

    def on_filter_change(self, *args):
        tickets = self.get_tickets()
        self.filter_tickets(tickets)

    def open_ticket_frame(self, ticket):
        # Function to update ticket in the database
        def update_ticket():
            assigned_to = self.name
            status = "Working"

            # Update ticket data in the database
            connection = sqlite3.connect('db_ticketingSystem.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE tickets SET assignedTo=?, status=? WHERE ticket_id=?", (assigned_to, status, ticket[0]))
            connection.commit()
            connection.close()
            messagebox.showinfo("Ticket", "Ticket has been assigned to your account!")

        def resolve_ticket():
            status = "Resolved"
            resolved_at = datetime.now().strftime("%d/%m/%Y %I:%M%p")  # Get current date and time

            # Update ticket status and resolved_at in the database
            connection = sqlite3.connect('db_ticketingSystem.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE tickets SET status=?, resolved_at=? WHERE ticket_id=?", (status, resolved_at, ticket[0]))
            connection.commit()
            connection.close()
            messagebox.showinfo("Ticket", "Ticket status has been changed to 'Resolved'")
            # Optionally, close the window after resolving
            ticket_window.destroy()

        # Create a new window for displaying full ticket description
        ticket_window = tk.Toplevel(self.root)
        ticket_window.title(f"Ticket {ticket[0]} - {ticket[1]}")
        ticket_window.geometry("500x400")
        ticket_window.resizable(False, False)

        # Display full ticket description
        # Title
        tk.Label(ticket_window, text="Title:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[1], font=("Helvetica", 12)).grid(row=0, column=1, sticky="w")

        # Category
        tk.Label(ticket_window, text="Category:", font=("Helvetica", 12, "bold")).grid(row=1, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[2], font=("Helvetica", 12)).grid(row=1, column=1, sticky="w")

        # Description
        tk.Label(ticket_window, text="Description:", font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[3], font=("Helvetica", 12)).grid(row=2, column=1, sticky="w")

        # Priority
        tk.Label(ticket_window, text="Priority:", font=("Helvetica", 12, "bold")).grid(row=3, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[6], font=("Helvetica", 12)).grid(row=3, column=1, sticky="w")

        # Status
        tk.Label(ticket_window, text="Status:", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[4], font=("Helvetica", 12)).grid(row=4, column=1, sticky="w")

        # Created By
        tk.Label(ticket_window, text="Created By:", font=("Helvetica", 12, "bold")).grid(row=5, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[7], font=("Helvetica", 12)).grid(row=5, column=1, sticky="w")

        # Created At
        tk.Label(ticket_window, text="Created At:", font=("Helvetica", 12, "bold")).grid(row=6, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[8], font=("Helvetica", 12)).grid(row=6, column=1, sticky="w")

        # Assigned To
        tk.Label(ticket_window, text="Assigned To:", font=("Helvetica", 12, "bold")).grid(row=7, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[5], font=("Helvetica", 12)).grid(row=7, column=1, sticky="w")

        # Button to update ticket
        get_ticket_button = tk.Button(ticket_window, text="Get Ticket", font=("Helvetica", 12), command=update_ticket, bg="#a3c585", fg="white", relief=tk.FLAT, cursor="hand2")
        get_ticket_button.grid(row=8, column=0, sticky="w", pady=10, padx=10)

        # Button to resolve ticket
        resolve_ticket_button = tk.Button(ticket_window, text="Resolve Ticket", font=("Helvetica", 12), command=resolve_ticket, bg="#a3c585", fg="white", relief=tk.FLAT, cursor="hand2")
        resolve_ticket_button.grid(row=8, column=1, sticky="w", pady=10, padx=10)


        if ticket[4] == "Working":
            get_ticket_button.config(state="disabled")

        if ticket[5] == "None":
            resolve_ticket_button.config(state="disabled")
        else:
            resolve_ticket_button.config(state="normal")


    def logout(self):
        messagebox.showinfo("Logout", "Logged out successfully!")
        self.current_frame.destroy()
        self.current_frame.quit()