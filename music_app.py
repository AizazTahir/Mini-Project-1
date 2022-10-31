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

def page_redirect(old_page, new_page, id = None):
    old_page.destroy()
    if(id == None):
        new_page()
    else:
        new_page(id)

def choose_account_page(id):
    identify_page = Tk()
    identify_page.geometry('300x300')
    identify_page.title('Choose role to login')

    goto_users_home_page = partial(page_redirect, identify_page, users_home_page, id)
    goto_artists_home_page = partial(page_redirect, identify_page, artists_home_page, id)

    Label(identify_page, text = "Are you logging as a User or Artist?", font=("Arial", 10)).grid(row = 0, column = 1)
    Button(identify_page, text = "User", command = goto_users_home_page).grid(row = 1, column = 0)
    Button(identify_page, text = "Artist", command = goto_artists_home_page).grid(row = 2, column = 0)

def verify_new_user(cur_page, id, name, pwd):
    # Verify provided user id is valid and unique
    # FIX-ME: will need to catch invalid field values too. Also consider merging with login_check()
    # Currently only checks uniqueness
    
    cursor.execute("""SELECT uid FROM users WHERE uid = ?""", (id.get(),))
    user_result = cursor.fetchone()
    
    print("id: " + id.get())
    print("name: " + name.get())
    print("pwd: " + pwd.get())

    if(user_result):
        Label(cur_page, text = "User id already exists! Please try again.", font=("Arial", 10)).grid(row = 7, column = 1)
        ### Using pack
        """
        existing_user_lb = Label(cur_page, text = "User id already exists! Please try again.", font=("Arial", 10))
        existing_user_lb.pack(side=BOTTOM)
        """
    else:
        # Can add to database
        add_user_query = """INSERT INTO users
                        (uid, name, pwd)
                        VALUES (?, ?, ?);"""
        new_user_data = (id.get(), name.get(), pwd.get())
        cursor.execute(add_user_query, new_user_data)
        connection.commit()

        # Redirect to users homepage
        page_redirect(cur_page, users_home_page, id)

def signup_page():
    new_member_page = Tk()
    new_member_page.geometry('500x300')
    new_member_page.title('Sign Up')
    Label(new_member_page, text = "---New User---").grid(row = 0, column = 0)

    # Ask for uid, name, password
    Label(new_member_page, text = "Provide a user id:").grid(row = 1, column = 0)
    new_id = StringVar()
    Entry(new_member_page, bd = 5, textvariable = new_id).grid(row = 2, column = 1)

    Label(new_member_page, text = "Enter your name:").grid(row = 3, column = 0)
    new_name = StringVar()
    Entry(new_member_page, bd = 5, textvariable = new_name).grid(row = 4, column = 1)

    Label(new_member_page, text = "Provide a password:").grid(row = 5, column = 0)
    new_pwd = StringVar()
    Entry(new_member_page, bd = 5, textvariable = new_pwd).grid(row = 6, column = 1)

    verify = partial(verify_new_user, new_member_page, new_id, new_name, new_pwd)
    Button(new_member_page, text = "Confirm", command = verify).grid(row = 7, column = 0)
    
    

### Users Abilities
def start_session(uid):
    print("session started")
    print(uid.get())

def search_songs_pl_page(uid):
    #also applies for playlists
    print("search song and playlists")

def search_artists_page(uid):
    print("search artists")

def end_session(uid):
    print("end_session")

### Artists Abilities
def add_song_page(aid):
    print("add song page for artists")

def search_fans_pl_page(aid):
    print("Search for Top 3 Fans and Playlists")

### Home pages
def users_home_page(uid):
    user_menu = Tk()
    user_menu.geometry('300x300')
    user_menu.title('Welcome, user.')

    # Actions Available to Users
    start_user_session = partial(start_session, uid)
    end_user_session = partial(end_session, uid)
    goto_search_songs_pl = partial(page_redirect, user_menu, search_songs_pl_page, uid)
    goto_search_artists = partial(page_redirect, user_menu, search_artists_page, uid)
    logout = partial(page_redirect, user_menu, login_page)
    
    Button(user_menu, text = "Start a Session", command = start_user_session).grid(row = 1, column = 0) #No need to chage page
    Button(user_menu, text = "End the Current Session", command = end_user_session).grid(row = 2, column = 0) #No need to chage page
    Button(user_menu, text = "Search for Songs and Playlists", command = goto_search_songs_pl).grid(row = 3, column = 0)
    Button(user_menu, text = "Search for Artists", command = goto_search_artists).grid(row = 4, column = 0) 
    Button(user_menu, text = "Log Out", command = logout).grid(row = 5, column = 0)

    user_menu.mainloop()

def artists_home_page(aid):
    artist_menu = Tk()
    artist_menu.geometry('300x300')
    artist_menu.title('Welcome, artist.')

    # Actions Available to Users
    goto_add_songs = partial(page_redirect, artist_menu, add_song_page, aid)
    goto_search_fans_pl = partial(page_redirect, artist_menu, search_fans_pl_page, aid)
    logout = partial(page_redirect, artist_menu, login_page)
    
    Button(artist_menu, text = "Add a new song", command = goto_add_songs).grid(row = 1, column = 0)
    Button(artist_menu, text = "Fans and Top Playlists", command = goto_search_fans_pl).grid(row = 2, column = 0)
    Button(artist_menu, text = "Log Out", command = logout).grid(row = 3, column = 0)
    artist_menu.mainloop()

### Credentials Checker
#aeg$sdg
def login_check(login_screen, id, pwd):
    # id, pwd are StringVar()
    id_str = id.get()
    pwd_str = pwd.get()
    print("id is: " + id.get())
    print("pwd is: " + pwd.get())
    print(type(id))

    # Check which table(s) the id shows up in (users and artists)
    cursor.execute("""
        SELECT uid, pwd
        FROM users
        WHERE uid = ?
        AND pwd = ?""", (id.get(), pwd.get())
    )    
    users_result = cursor.fetchone()
    #print(users_result)
    
    cursor.execute("""
        SELECT aid, pwd
        FROM artists
        WHERE aid = ?
        AND pwd = ?""", (id.get(), pwd.get())
    )
    artists_result = cursor.fetchone()
    #print(artists_result)

    # incorrect password or user DNE              
    if(not users_result and not artists_result):
        Label(login_screen, text = "Invalid id or password!", font=("Arial", 10)).grid(row = 2, column = 1)
    # has to be user
    elif(users_result and not artists_result):
        print("has to be user")
        page_redirect(login_screen, users_home_page, id)
    # has to be artist
    elif(not users_result and artists_result):
        print("has to be artist")
        page_redirect(login_screen, artists_home_page, id)
    #If found in both users and artists tables, prompt user for specfic login
    else:
        #both artist and user (id: 30, pwd: uhasdf*3)
        # prompt user to choose user or artist
        print("prompt user to choose user or artist")
        page_redirect(login_screen, choose_account_page, id)

def login_page():
     #top is the login page
    top = Tk()
    top.geometry('400x200')
    top.title('Login to get started!')

    # id
    Label(top, text = "ID").grid(row = 0, column = 0)
    id = StringVar()
    Entry(top, bd = 5, textvariable = id).grid(row = 0, column = 1)
    
    # pwd
    Label(top, text = "pwd").grid(row = 1, column = 0)
    pwd = StringVar()
    Entry(top, bd = 5, textvariable = pwd).grid(row = 1, column = 1)
    
    # login button
    enter = partial(login_check, top, id, pwd)
    Button(top, text = "login", command = enter).grid(row = 2, column = 0)

    # sign-up
    goto_signup_page = partial(page_redirect, top, signup_page)
    Label(top, text = "New to the platform?").grid(row = 3, column = 0)
    Button(top, text = "Sign Up", command = goto_signup_page).grid(row = 4, column = 0)
    
    """
    ### using pack
    # id
    id_lb = Label(top, text = "ID")
    id_lb.pack(side=LEFT)
    id = StringVar()
    id_etr = Entry(top, bd = 5, textvariable = id)
    id_etr.pack(side=TOP)
    
    # pwd
    pwd_lb = Label(top, text = "pwd")
    pwd_lb.pack(side=LEFT)
    pwd = StringVar()
    pwd_etr = Entry(top, bd = 5, textvariable = pwd)
    pwd_etr.pack(side=TOP)
    
    # login button
    enter = partial(login_check, top, id, pwd)
    login_button = Button(top, text = "login", command = enter)
    login_button.pack(side=TOP)

    # sign-up
    goto_signup_page = partial(page_redirect, top, signup_page)
    signup_lb = Label(top, text = "New to the platform?")
    signup_lb.pack(side=LEFT)
    signup_button = Button(top, text = "Sign Up", command = goto_signup_page)
    signup_button.pack(side=TOP)
    """
    top.mainloop()

def main():
    global connection, cursor

    # 1. Connect to the DB
    path = sys.argv[1] #DB file is passed as a command line argument
    connect(path)
    # Now "connection" and "cursor" are ready

    # 2. Present login page
    login_page()

if __name__ == "__main__":
    main()