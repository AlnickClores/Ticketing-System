import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

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
        # Display text for solved tickets
        solved_label = tk.Label(self.main_frame, text="Solved Tickets", font=("Helvetica", 20))
        solved_label.pack(pady=(20, 10))

    def show_my_account_content(self):
        # Add your account-related content here
        account_label = tk.Label(self.main_frame, text="My Account", font=("Helvetica", 20))
        account_label.pack(pady=(20, 10))

    def get_tickets(self):
        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Execute the query to retrieve tickets
        cursor.execute("SELECT * FROM tickets")
        tickets = cursor.fetchall()

        # Close the connection
        connection.close()

        return tickets

    def filter_tickets(self, tickets):
        filter_option = self.filter_var.get()
        if filter_option == 'Priority (Highest)':
            tickets = sorted(tickets, key=lambda x: x[4])
        elif filter_option == 'Date (Recent)':
            tickets = sorted(tickets, key=lambda x: x[6], reverse=True)

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
        ticket_frame.pack(padx=195, pady=10, fill="both", expand=True, anchor="center")

        tk.Label(ticket_frame, text=f"Title: {ticket[1]}", font=("Helvetica", 13)).pack()
        tk.Label(ticket_frame, text=f"Category: {ticket[2]}", font=("Helvetica", 12)).pack()
        tk.Label(ticket_frame, text=f"Priority: {ticket[6]}", font=("Helvetica", 12)).pack()
        tk.Label(ticket_frame, text=f"Status: {ticket[4]}", font=("Helvetica", 12)).pack()  

        open_ticket_btn = tk.Button(ticket_frame, text="Open Ticket", font=("Helvetica", 12), bg="#007fff", fg="white", command=lambda: self.open_ticket_frame(ticket))
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

        def delete_ticket():
            connection = sqlite3.connect('db_ticketingSystem.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tickets WHERE ticket_id=?", (ticket[0], ))
            connection.commit()
            connection.close()
            messagebox.showinfo("Ticker", "Ticket has been deleted")

        # Create a new window for displaying full ticket description
        ticket_window = tk.Toplevel(self.root)
        ticket_window.title(f"Ticket {ticket[0]} - {ticket[1]}")
        ticket_window.geometry("500x400")
        ticket_window.resizable(False, False)

        # Display full ticket description
        tk.Label(ticket_window, text=f"Title: {ticket[1]}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(ticket_window, text=f"Category: {ticket[2]}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(ticket_window, text=f"Description: {ticket[3]}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(ticket_window, text=f"Priority: {ticket[4]}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(ticket_window, text=f"Created By: {ticket[7]}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(ticket_window, text=f"Created At: {ticket[8]}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(ticket_window, text=f"Assigned To: {ticket[5]}", font=("Helvetica", 12)).pack(anchor="w")

        # Button to update ticket
        get_ticket_button = tk.Button(ticket_window, text="Get Ticket", font=("Helvetica", 12), command=update_ticket)
        get_ticket_button.pack(anchor="w", pady=10)
        get_ticket_button = tk.Button(ticket_window, text="Delete Ticket", font=("Helvetica", 12), command=delete_ticket)
        get_ticket_button.pack(anchor="w", pady=10)

    def logout(self):
        messagebox.showinfo("Logout", "Logged out successfully!")
        self.current_frame.destroy()
        self.current_frame.quit()