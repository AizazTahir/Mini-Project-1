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
def login(page, id, pwd):
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
    users_result = cursor.fetchone()
    #print(users_result)
    
    cursor.execute("""
        SELECT *
        FROM artists
        WHERE aid = '{}'
        AND pwd = '{}';
        """.format(id_str, pwd_str)
    )    
    artists_result = cursor.fetchone()
    #print(artists_result)
                        
    #If found in both users and artists tables, prompt user for specfic login
    if(not users_result and not artists_result):
        # prompt user to choose user or artist
        print("in progress")
    # has to be user
    elif(users_result and not artists_result):
        print("in progress")
    # has to be artist
    elif(len(users_result) == 0 and len(artists_result) == 1):
        print("in progress")
    # incorrect password or user DNE
    else:
        err_msg = Label(page, text = "Invalid id or password!", font=("Arial", 10)).grid(row = 2, column = 0)
        time.sleep(2)
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
    
    enter = partial(login, top, id, pwd)

    login_button = Button(top, text = "login", command = enter).grid(row = 4, column = 0)
    top.mainloop()


if __name__ == "__main__":
    main()