import sqlite3

def create_tables():
    connection = sqlite3.connect('db_ticketingSystem.db')
    cursor = connection.cursor()

    users_tbl = '''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY, 
        name TEXT, 
        email TEXT, 
        password TEXT, 
        role TEXT)
    '''

    tickets_tbl = '''CREATE TABLE IF NOT EXISTS tickets(
        ticket_id INTEGER PRIMARY KEY, 
        title TEXT, 
        category TEXT, 
        description TEXT,
        status TEXT,
        assignedTo TEXT,
        priority TEXT,
        created_by TEXT,
        created_at DATETIME)
    '''

    cursor.execute(users_tbl)
    cursor.execute(tickets_tbl)

    connection.commit()
    cursor.close()
    connection.close()

create_tables()
