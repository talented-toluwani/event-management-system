import sqlite3

from event_config import DATABASE_PATH


def get_connection(): #provides a connection between the database and the sqlite 3 module
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_database():
    connection = get_connection() #creates a connection object with the previously connection established
    my_cursor = connection.cursor()#creates a cursor object

    my_cursor.execute("""CREATE TABLE IF NOT EXISTS users_table(
                      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      role TEXT NOT NULL
)""") #creates the users table
    
    my_cursor.execute("""CREATE TABLE if NOT EXISTS events_table(
                      event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      description TEXT NOT NULL,
                      date_time TEXT NOT NULL,
                      max_capacity INTEGER NOT NULL,
                      category TEXT NOT NULL,
                      current_participants INTEGER not NULL,
                      status TEXT NOT NULL                    
)""")#creates the event table 
    
    my_cursor.execute("""CREATE TABLE if NOT EXISTS registrations_table(
                      registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id  INTEGER NOT NULL,
                      event_id INTEGER  NOT NULL,
                      registered_at  TEXT NOT NULL,
                      UNIQUE(user_id, event_id)
                      )""") #creates the registration table 
    

    connection.commit() #saves all changes made
    connection.close()  #closes the connection
    