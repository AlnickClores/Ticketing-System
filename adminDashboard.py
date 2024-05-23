import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class AdminDashboard:
    def __init__(self, root, admin_name):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("900x700")
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.root.resizable(False, False)
        self.admin_name = admin_name

        self.show_dashboard()

    def show_dashboard(self):
        for widget in self.current_frame.winfo_children():
            widget.destroy()

        sidebar_frame = tk.Frame(self.current_frame, width=200, bg="#151515")
        sidebar_frame.pack(side="left", fill="y")

        tk.Label(sidebar_frame, text=f"Hello, {self.admin_name}", font=("Helvetica", 15), bg="#151515", fg="white", padx=10, pady=10).pack(fill="x")

        sidebar_items = ["Main Dashboard", "Tickets", "Users"]
        for item in sidebar_items:
            tk.Button(sidebar_frame, text=item, font=("Helvetica", 12), bg="#151515", fg="white", padx=50, pady=10, command=lambda i=item: self.show_content(i)).pack(fill="x", padx=10, pady=10)

        tk.Button(sidebar_frame, text="Logout", font=("Helvetica", 12), bg="#151515", fg="white", padx=50, pady=10, command=self.logout).pack(side="bottom", fill="x", padx=10, pady=10)

        self.main_frame = tk.Frame(self.current_frame)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.show_content("Main Dashboard")

    def show_content(self, content):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if content == "Main Dashboard":
            self.show_main_dashboard()
        elif content == "Tickets":
            self.show_tickets_content()
        elif content == "Users":
            self.show_users()

    def show_main_dashboard(self):
        header_label = tk.Label(self.main_frame, text="Main Dashboard", font=("Helvetica", 20))
        header_label.pack(pady=(20, 10))

        stats_frame = tk.Frame(self.main_frame)
        stats_frame.pack(pady=10)

        total_tickets, pending_tickets, in_progress_tickets, closed_tickets = self.get_ticket_stats()
        total_users = self.get_user_stats()

        tk.Label(stats_frame, text=f"Total Users: {total_users-1}", font=("Helvetica", 14)).pack(anchor="w")
        tk.Label(stats_frame, text=f"Total Tickets: {total_tickets}", font=("Helvetica", 14)).pack(anchor="w")
        tk.Label(stats_frame, text=f"Tickets Pending: {pending_tickets}", font=("Helvetica", 14)).pack(anchor="w")
        tk.Label(stats_frame, text=f"Tickets In Progress: {in_progress_tickets}", font=("Helvetica", 14)).pack(anchor="w")
        tk.Label(stats_frame, text=f"Resolved Tickets: {closed_tickets}", font=("Helvetica", 14)).pack(anchor="w")

    def get_ticket_stats(self):
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*), "
                       "SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END), "
                       "SUM(CASE WHEN status='Working' THEN 1 ELSE 0 END), "
                       "SUM(CASE WHEN status='Resolved' THEN 1 ELSE 0 END) "
                       "FROM tickets")
        stats = cursor.fetchone()
        connection.close()
        return stats

    def get_user_stats(self):
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        connection.close()
        return total_users

    def get_recent_tickets(self):
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM tickets ORDER BY created_at DESC LIMIT 9")
        recent_tickets = cursor.fetchall()
        connection.close()
        return [ticket[0] for ticket in recent_tickets]

    def get_recent_users(self):
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM users ORDER BY created_at DESC LIMIT 5")
        recent_users = cursor.fetchall()
        connection.close()
        return [user[0] for user in recent_users]

    def show_tickets_content(self):
        tk.Label(self.main_frame, text="Tickets", font=("Helvetica", 16)).pack(pady=10)

        tickets = self.get_tickets()
        tickets_frame = tk.Frame(self.main_frame)
        tickets_frame.pack(fill="both", expand=True)

        rows, cols = 2, 2
        for index, ticket in enumerate(tickets):
            row, col = divmod(index, cols)
            self.create_ticket_card(tickets_frame, ticket).grid(row=row, column=col, padx=10, pady=10)

    def create_ticket_card(self, parent, ticket):
        frame = tk.Frame(parent, bd=2, relief="groove", padx=10, pady=10)
        tk.Label(frame, text=f"Title: {ticket[1]}", font=("Helvetica", 13)).grid(row=0, column=0, sticky="w")
        tk.Label(frame, text=f"Category: {ticket[2]}", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
        tk.Label(frame, text=f"Priority: {ticket[4]}", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
        tk.Label(frame, text=f"Status: {ticket[5]}", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")
        tk.Button(frame, text="Open Ticket", font=("Helvetica", 12), bg="#007fff", fg="white", cursor="hand2", command=lambda: self.open_ticket_frame(ticket)).grid(row=4, column=0, pady=10)
        return frame

    
    def open_ticket_frame(self, ticket):
        def delete_ticket():
            connection = sqlite3.connect('db_ticketingSystem.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tickets WHERE ticket_id=?", (ticket[0], ))
            connection.commit()
            connection.close()
            messagebox.showinfo("Ticket", "Ticket has been deleted")

        ticket_window = tk.Toplevel(self.root)
        ticket_window.title(f"Ticket {ticket[0]} - {ticket[1]}")
        ticket_window.geometry("500x400")
        ticket_window.resizable(False, False)

        # Create labels for column names and corresponding values
        tk.Label(ticket_window, text="Title:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[1], font=("Helvetica", 12)).grid(row=0, column=1, sticky="w")

        tk.Label(ticket_window, text="Category:", font=("Helvetica", 12, "bold")).grid(row=1, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[2], font=("Helvetica", 12)).grid(row=1, column=1, sticky="w")

        tk.Label(ticket_window, text="Description:", font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[3], font=("Helvetica", 12)).grid(row=2, column=1, sticky="w")

        tk.Label(ticket_window, text="Priority:", font=("Helvetica", 12, "bold")).grid(row=3, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[4], font=("Helvetica", 12)).grid(row=3, column=1, sticky="w")

        tk.Label(ticket_window, text="Status:", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[5], font=("Helvetica", 12)).grid(row=4, column=1, sticky="w")

        tk.Label(ticket_window, text="Created By:", font=("Helvetica", 12, "bold")).grid(row=5, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[7], font=("Helvetica", 12)).grid(row=5, column=1, sticky="w")

        tk.Label(ticket_window, text="Created At:", font=("Helvetica", 12, "bold")).grid(row=6, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[8], font=("Helvetica", 12)).grid(row=6, column=1, sticky="w")

        tk.Label(ticket_window, text="Assigned To:", font=("Helvetica", 12, "bold")).grid(row=7, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[6], font=("Helvetica", 12)).grid(row=7, column=1, sticky="w")

        tk.Label(ticket_window, text="Resolved At:", font=("Helvetica", 12, "bold")).grid(row=8, column=0, sticky="w")
        tk.Label(ticket_window, text=ticket[9], font=("Helvetica", 12)).grid(row=8, column=1, sticky="w")

        # Button to delete ticket
        delete_ticket_button = tk.Button(ticket_window, text="Delete Ticket", font=("Helvetica", 12), cursor="hand2", command=delete_ticket, bg="#d0312d", fg="white")
        delete_ticket_button.grid(row=9, columnspan=2, pady=10)


    def get_tickets(self):
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()
        cursor.execute("SELECT ticket_id, title, category, description, priority, status, assignedTo, created_by, created_at, resolved_at FROM tickets")
        tickets = cursor.fetchall()
        connection.close()
        return tickets
    
    def show_users(self):
        tk.Label(self.main_frame, text="Users", font=("Helvetica", 16)).pack(pady=10)

        # Connect to the database
        connection = sqlite3.connect('db_ticketingSystem.db')
        cursor = connection.cursor()

        # Execute the query to retrieve users excluding the Admin Account
        cursor.execute("SELECT * FROM users WHERE role != 'Admin'")
        users = cursor.fetchall()

        # Close the connection
        connection.close()

        # Frame for user cards
        users_frame = tk.Frame(self.main_frame)
        users_frame.pack(expand=True, fill="both")

        for i, user in enumerate(users):
            user_frame = tk.Frame(users_frame, bd=2, relief="groove", padx=20, pady=15)
            user_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")

            tk.Label(user_frame, text=f"Name: {user[1]}", font=("Helvetica", 13)).pack()
            tk.Label(user_frame, text=f"Email: {user[2]}", font=("Helvetica", 12)).pack()
            tk.Label(user_frame, text=f"Role: {user[4]}", font=("Helvetica", 12)).pack()

    def logout(self):
        messagebox.showinfo("Logout", "Logged out successfully!")
        self.root.destroy()