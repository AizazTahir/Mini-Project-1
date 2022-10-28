import sqlite3
from tkinter import *
# maybe see later if we have to use partial
from functools import partial
import time
import sys

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

#aeg$sdg
def login(id, pwd):
    # id, pwd are StringVar()
    id_str = id.get()
    pwd_str = pwd.get()
    print("id is: " + id_str)
    print("pwd is: " + pwd_str)
    print(type(id))
    # Check which table(s) the id shows up in (users and artists)
    cursor.execute("""
        SELECT *
        FROM users
        WHERE uid = '{}'
        AND pwd = '{}';
        """.format(id_str, pwd_str)
    )    
    
    rows = cursor.fetchone()
    print(rows)
    
                        
    #If found in both users and artists tables, prompt user for specfic login
    
    #Redirect to correct page
    return

def main():
    global connection, cursor

    # 1. Connect to the DB
    path = sys.argv[1] #DB file is passed as a command line argument
    connect(path)
    # Now "connection" and "cursor" are ready

    #top is the login page
    top = Tk()
    top.geometry('400x200')
    top.title('Login to get started!')

    # id
    id_label = Label(top, text = "ID").grid(row = 0, column = 0)
    id = StringVar()
    id_entry = Entry(top, bd = 5, textvariable = id).grid(row = 0, column = 1)
    
    # pwd
    pwd_label = Label(top, text = "pwd").grid(row = 1, column = 0)
    pwd = StringVar()
    pwd_entry = Entry(top, bd = 5, textvariable = pwd).grid(row = 1, column = 1)
    
    enter = partial(login, id, pwd)

    login_button = Button(top, text = "login", command = enter).grid(row = 4, column = 0)
    top.mainloop()


if __name__ == "__main__":
    main()