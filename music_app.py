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

def page_redirect(old_page, new_page, *argument):
    old_page.destroy()
    new_page(*argument)

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
def start_session(cur_page, uid):
    print("session started")
    print(uid.get())
    
    # Create a unique session id and add to database
    cursor.execute("""SELECT MAX(sno) FROM sessions""")
    # add 1 to the max session id
    
    max_sno = cursor.fetchone()[0]
    
    if(max_sno == None):
        max_sno = 0
        
    new_sno = max_sno + 1
    # Debug: print(new_sno)
    # add the new sid to the database with the start date as today and the end date as null
    cursor.execute("""INSERT INTO sessions (uid, sno, start, end) VALUES (?, ?, ?, ?)""", (uid.get(), new_sno, time.strftime("%Y-%m-%d"), None))
    
    # add label to the page to show that the session has started
    Label(cur_page, text = "Session started").grid(row = 1, column = 1)
    #Label(cur_page, text = "User id already exists! Please try again.", font=("Arial", 10)).grid(row = 7, column = 1)
    connection.commit()
    

def search_songs_pl_page(uid):
    #also applies for playlists
    print("search song and playlists")
    # create a page for serching songs and playlists on
    search_page = Tk()
    search_page.geometry('400x300')
    search_page.title('Search Songs and Playlists')
    Label(search_page, text = "---Search Songs and Playlists---").grid(row = 0, column = 0)
    
    # Create a search bar that allows user to input the name of the song or playlist they want to search for
    Label(search_page, text = "Enter the name of the song or playlist you want to search for:").grid(row = 1, column = 0)
    search_name = StringVar()
    Entry(search_page, bd = 5, textvariable = search_name).grid(row = 2, column = 0)
   



def search_artists_page(uid):
    print("search artists")
    # Create a page for searching artists on
    search_page = Tk()
    search_page.geometry('400x300')
    search_page.title('Search Artists')
    Label(search_page, text = "---Search Artists---").grid(row = 0, column = 0)

    # Create a search bar for the user to input the name of the artist they want to search for
    Label(search_page, text = "Enter the name of the artist you want to search for:").grid(row = 1, column = 0)
    search_name = StringVar()
    Entry(search_page, bd = 5, textvariable = search_name).grid(row = 2, column = 0)
      
    print(search_name.get())
    

    search_page.mainloop()


def end_session(cur_page, uid):
    print("end_session")
    # set the current session end to the current date in the database
    cursor.execute("""SELECT MAX(sno) FROM sessions WHERE uid = ?""", (uid.get(),))
    max_sno = cursor.fetchone()[0]
    # debug: print(max_sno)
    cursor.execute("""UPDATE sessions SET end = ? WHERE sno = ?""", (time.strftime("%Y-%m-%d"), max_sno))
    
    # Add label to the page to show that the session has ended
    Label(cur_page, text = "Session ended").grid(row = 2, column = 1)
    connection.commit()
    

### Artists Abilities
def add_song_page(aid):
    print("add song page for artists")
    # create a add song page for artists to add songs to the database
    add_song_page = Tk()
    add_song_page.geometry('350x300')
    add_song_page.title('Add Song')
    Label(add_song_page, text = "---Add Song---").grid(row = 0, column = 0)

    # Create a search bar for the user to input the name of the artist they want to search for
    Label(add_song_page, text = "Enter the title of the song you want to add:").grid(row = 1, column = 0)
    song_title = StringVar()
    Entry(add_song_page, bd = 5, textvariable = song_title).grid(row = 2, column = 0)

    # Create a search bar for the duration of the songs in seconds
    Label(add_song_page, text = "Enter the duration of the song in seconds:").grid(row = 3, column = 0)
    song_duration = StringVar()
    Entry(add_song_page, bd = 5, textvariable = song_duration).grid(row = 4, column = 0)
    
    # Create a search bar for if there are any other artists on the song
    Label(add_song_page, text = "Enter the Id of the other artists on the song:").grid(row = 5, column = 0)
    song_artists_id = StringVar()
    Entry(add_song_page, bd = 5, textvariable = song_artists_id).grid(row = 6, column = 0)
    
    # create a add song button for the user to add the song to the database
    add_song = partial(add_song_to_db, song_title, song_duration, aid, song_artists_id, add_song_page)
    Button(add_song_page, text = "Add Song", command = add_song).grid(row = 7, column = 0)
    
    # add button for the user to leave the menu and go back to the main page
    goto_artists_home_page = partial(page_redirect, add_song_page, artists_home_page, aid)
    Button(add_song_page, text = "Back", command = goto_artists_home_page).grid(row = 8, column = 0)


    add_song_page.mainloop()


def add_song_to_db(title, duration, aid, aid2, add_song_page):
    print("add song to db")
    title = title.get()
    duration = duration.get()
    aid = aid.get()
    aid2 = aid2.get()
    print(title, duration, aid, aid2)
    
    # make sure that the title and duration of the new song is not already in the database
    cursor.execute("""SELECT title, duration FROM songs WHERE title = ? AND duration = ?""", (title, duration))
    song = cursor.fetchone()
    if(song != None):
        Label(add_song_page, text = "Song already exists! Please try again.", font=("Arial", 10)).grid(row = 10, column = 0)
        return
    
     # Create a new sid for the new song that we are going to add to the database
    cursor.execute("""SELECT MAX(sid) FROM songs""")
    max_sid = cursor.fetchone()[0]
    if(max_sid == None):
        max_sid = 0
    new_sid = max_sid + 1
    # Debug: print(new_sid)
    
    # add the new song to the database with sid title and duration
    cursor.execute("""INSERT INTO songs (sid, title, duration) VALUES (?, ?, ?)""", (new_sid, title, duration))
    
    # Add the aid of the arist and the sid of the song to the perform table
    cursor.execute("""INSERT INTO perform (aid, sid) VALUES (?, ?)""", (aid, new_sid))
    
    # If there are other artists on the song, add them to the perform table
    
    if(aid2 != ""):
        cursor.execute("""INSERT INTO perform (aid, sid) VALUES (?, ?)""", (aid2, new_sid))

    # Add label to the page to show that the song has been added
    Label(add_song_page, text = "Song added").grid(row = 8, column = 1)
    connection.commit()



def search_fans_pl_page(aid):
    print("Search for Top 3 Fans and Playlists")
    # create a search fans/playlists page for artists to search for their top 3 fans and playlists
    search_fans_pl_page = Tk()
    search_fans_pl_page.geometry('350x300')
    search_fans_pl_page.title('Search Fans and Playlists')
    Label(search_fans_pl_page, text = "---Search Fans and Playlists---").grid(row = 0, column = 0)

   # create a button that displays the top 3 fans of the artist by amount of time listened to
    top_3fans = partial(page_redirect, search_fans_pl_page, top_3_fans, aid)
    Button(search_fans_pl_page, text = "Top 3 Fans", command = top_3fans).grid(row = 1, column = 0)
    
    # create a button that displays the top 3 playlists of the artist by the amount of their songs in the playlist
    top_3pl = partial(page_redirect, search_fans_pl_page, top_3_pl, aid)
    Button(search_fans_pl_page, text = "Top 3 Playlists", command = top_3pl).grid(row = 2, column = 0)
    
    # add button for the user to leave the menu and go back to the main page
    goto_artists_home_page = partial(page_redirect, search_fans_pl_page, artists_home_page, aid)
    Button(search_fans_pl_page, text = "Back", command = goto_artists_home_page).grid(row = 3, column = 0)

    search_fans_pl_page.mainloop()
    
def top_3_fans(aid):
    print("top 3 fans")
    
    # Create a new window object to display the top 3 fans of the artist
    top_3_fans_page = Tk()
    top_3_fans_page.geometry('350x300')
    top_3_fans_page.title('Top 3 Fans')
    Label(top_3_fans_page, text = "---Top 3 Fans---").grid(row = 0, column = 0)
    
    # get the top 3 fans of the artist by amount of time listened to which is determined by cnt in the listen table multipied by the duration of the song in the songs table
    # SELECT l.uid, u.name
    # FROM songs s, listen l, perform p, users u
    # WHERE p.aid = <artist>
    # AND l.sid = s.sid AND l.sid = p.sid AND l.uid = u.uid
    # GROUP BY u.uid
    # ORDER BY COUNT(l.cnt * s.duration)
    # LIMIT 3;
    # convert the above to python
    cursor.execute("""SELECT l.uid, u.name FROM songs s, listen l, perform p, users u WHERE p.aid = ? AND l.sid = s.sid AND l.sid = p.sid AND l.uid = u.uid GROUP BY u.uid ORDER BY COUNT(l.cnt * s.duration) DESC LIMIT 3""", (aid.get(),))
    top_3_fans = cursor.fetchall()


    # Display the top 3 fans in the new window
    for i in range(len(top_3_fans)):
        Label(top_3_fans_page, text = top_3_fans[i][1]).grid(row = i + 1, column = 0)
        
     # add button for the user to leave the menu and go back to the main page
    goto_search_fans_pl = partial(page_redirect, top_3_fans_page, search_fans_pl_page, aid)
    Button(top_3_fans_page, text = "Back", command = goto_search_fans_pl).grid(row = 4, column = 0)
    top_3_fans_page.mainloop()


    
def top_3_pl(aid):
    print("top 3 playlists")
    # Create a new window object to display the top 3 playlists of the artist
    top_3_pl_page = Tk()
    top_3_pl_page.geometry('350x300')
    top_3_pl_page.title('Top 3 Playlists')
    Label(top_3_pl_page, text = "---Top 3 Playlists---").grid(row = 0, column = 0)

    # get the top 3 playlists of the artist by the amount of their songs in the playlist
    #SELECT plcdl.pid, pl.title
    # FROM playlists pl, plinclude plcdl, perform per
    # WHERE per.aid = <artist>
    # AND pl.pid = plcdl.pid AND plcdl.sid = per.sid
    # GROUP BY plcdl.pid
    # ORDER BY COUNT(plcdl.sid)
    # LIMIT 3;
    # Convert the above to python
    cursor.execute("""SELECT plcdl.pid, pl.title FROM playlists pl, plinclude plcdl, perform per WHERE per.aid = ? AND pl.pid = plcdl.pid AND plcdl.sid = per.sid GROUP BY plcdl.pid ORDER BY COUNT(plcdl.sid) DESC LIMIT 3""", (aid.get(),))
    top_3_pl = cursor.fetchall()
    
    # display the top 3 playlists in the new window
    for i in range(len(top_3_pl)):
        Label(top_3_pl_page, text = top_3_pl[i][1]).grid(row = i + 1, column = 0)
        
     # add button for the user to leave the menu and go back to the main page
    goto_search_fans_pl = partial(page_redirect, top_3_pl_page, search_fans_pl_page, aid)
    Button(top_3_pl_page, text = "Back", command = goto_search_fans_pl).grid(row = 4, column = 0)
    top_3_pl_page.mainloop()



### Home pages
def users_home_page(uid):
    user_menu = Tk()
    user_menu.geometry('350x300')
    user_menu.title('Welcome, user.')

    # Actions Available to Users
    start_user_session = partial(start_session, user_menu ,uid)
    end_user_session = partial(end_session, user_menu, uid)
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
    # center the following button  

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
    login_portal = Tk()
    login_portal.geometry('400x200')
    login_portal.title('Login to get started!')

    # id
    Label(login_portal, text = "ID").grid(row = 0, column = 0)
    id = StringVar()
    Entry(login_portal, bd = 5, textvariable = id).grid(row = 0, column = 1)

    
    # pwd
    Label(login_portal, text = "pwd").grid(row = 1, column = 0)
    pwd = StringVar()
    Entry(login_portal, bd = 5, textvariable = pwd).grid(row = 1, column = 1)
    
    # login button
    enter = partial(login_check, login_portal, id, pwd)
    Button(login_portal, text = "login", command = enter).grid(row = 2, column = 0)

    # sign-up
    goto_signup_page = partial(page_redirect, login_portal, signup_page)
    Label(login_portal, text = "New to the platform?").grid(row = 3, column = 0)
    Button(login_portal, text = "Sign Up", command = goto_signup_page).grid(row = 4, column = 0)

    login_portal.mainloop()

def main():
    global connection, cursor

    # 1. Connect to the DB
    # path = sys.argv[1] #DB file is passed as a command line argument
    
    path = "mini_proj_test.db" #DB file is passed as a command line argument
    connect(path)
    # Now "connection" and "cursor" are ready

    # 2. Present login page
    login_page()

if __name__ == "__main__":
    main()