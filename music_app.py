import sqlite3
from tkinter import *
# maybe see later if we have to use partial
from functools import partial
import time
import sys
from tkinter import messagebox

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
    
def playlists_info(pid, uid):
    # Create a window to display the playlist information
    playlist_info_page = Tk()
    playlist_info_page.geometry('500x300')
    playlist_info_page.title('Playlist Information')
    
    # Display the pid and the title of the playlist
    cursor.execute("""SELECT pid, title FROM playlists WHERE pid = ?""", (pid.get(),))
    playlist_info = cursor.fetchone()
    
    Label(playlist_info_page, text = "Playlist ID: " + str(playlist_info[0])).grid(row = 0, column = 0)
    Label(playlist_info_page, text = "Playlist Title: " + playlist_info[1]).grid(row = 1, column = 0)
    
    # Display the total duration of the playlist
    cursor.execute("""SELECT SUM(duration) FROM songs WHERE sid IN (SELECT sid FROM plinclude WHERE plinclude.pid = ?)""", (pid.get(),))
    total_duration = cursor.fetchone()[0]
    
    Label(playlist_info_page, text = "Total Duration: " + str(total_duration)).grid(row = 2, column = 0)
    

    # Create a back button that allows the user to go back to the song select menu
    back_pl_song_results = partial(page_redirect, playlist_info_page, song_select_menu, uid)
    Button(playlist_info_page, text = "Back to Song Select Menu", command = back_pl_song_results).grid(row = 4, column = 0)
    
    
    playlist_info_page.mainloop()

def search_results_page(search_results, uid):
    # Create a window to display the search results
    search_page = Tk()
    search_page.geometry('500x300')
    search_page.title('Search Results')
    
    # Display the search results
    # FIX-ME: need to get the search results from the search function
    # FIX-ME: need to display the search results in the window
    # FIX-ME: need to add a button to each search result that allows the user to add the song to the playlist
    
    #  [(id, title, duration, # of matches, song/playlist), (id, title, duration, # of matches, song/playlist), ...]
    
   
    # print the rows in search_results
    for i in range(0, 5):
        print(search_results[i])
        print(type(search_results[i]))
        

        
    
    # Create a back button that allows the user to go back to the song select menu
    back_song_results = partial(page_redirect, search_page, search_songs_pl_page, uid)
    Button(search_page, text = "Back to Song Select Menu", command = back_song_results).grid(row = 4, column = 0)
    
    search_page.mainloop()

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
    
    # Create a button that allows user to search for the song or playlist
    search_songs_pl = partial(page_redirect, search_page, search_songs_pl_query, search_page, search_name, uid)
    Button(search_page, text = "Search", command = search_songs_pl).grid(row = 3, column = 0)

   
def search_songs_pl_query(cur_page, search_name, uid):

    # Search for songs and playlists that match the search name and order by the most number of keyword matches
    # """SELECT MAX(sno) FROM sessions WHERE uid = ?""", (uid.get(),)
    
    # strings to be constructed as part of query
    incre_songs = ""
    like_songs = ""
    incre_pl = ""
    like_pl = ""

    #input
    key_words = search_name.get().split(' ') #separate by space
    num_of_words = len(key_words)

    #constructing strings can continue only if we have input
    if(num_of_words != 0):
        for i in range(0, num_of_words):
            if(i != num_of_words-1):
                incre_songs += ("CASE WHEN s.title LIKE \'%" + key_words[i] + "%\' THEN 1 ELSE 0 END +\n")
            else:
                incre_songs += ("CASE WHEN s.title LIKE \'%" + key_words[i] + "%\' THEN 1 ELSE 0 END AS key_word_matches")
            like_songs += (" OR s.title LIKE \'%" + key_words[i] + "%\'")

        incre_pl = incre_songs.replace("s.title", "pl.title" )
        like_songs = like_songs[4:]
        like_pl = like_songs.replace("s.title", "pl.title" )

        query = """
        SELECT *
        FROM
            (
            --returns sid, title, duration, key_word_matches
            SELECT *, "song" AS "type", {}
            FROM songs s WHERE {}

            UNION

            --returns pid, title, tot_duration, key_word_matches
            SELECT pl.pid, pl.title, SUM(s.duration) AS tot_duration, "playlist" AS "type", {}
            FROM playlists pl, plinclude plcdl, songs s
            WHERE pl.pid = plcdl.pid AND plcdl.sid = s.sid
            AND({})
            GROUP BY pl.pid
            )
        ORDER BY key_word_matches DESC;""".format(incre_songs, like_songs, incre_pl, like_pl)

        #print(query)
        cursor.execute(query)
        search_results = cursor.fetchall()
        
        #for row in search_results:
            #print(row)
        
        # display search results
        search_results_page(search_results, uid)

    
def song_select_menu(sid, uid):
    # Create a menu where the user can perform any of these actions: (1) listen to it, 
    # (2) see more information about it, or (3) add it to a playlist.
    song_select_page = Tk()
    song_select_page.geometry('400x300')
    song_select_page.title('Song Select Menu')
    Label(song_select_page, text = "---Song Select Menu---").grid(row = 0, column = 0)
    
    # Add a button that allows the user to listen to the song
    listen_song = partial(page_redirect, song_select_page, listento_song, sid, uid)
    Button(song_select_page, text = "Listen to Song", command = listen_song).grid(row = 1, column = 0)
    
    # Add a button that allows the user to see more information about the song
    more_info_song = partial(page_redirect, song_select_page, more_info_song_func, sid)
    Button(song_select_page, text = "More Info", command = more_info_song).grid(row = 2, column = 0)
    
    # Add a button that allows the user to add the song to a playlist
    add_song_pl = partial(page_redirect, song_select_page, add_song_pl_func, sid, uid)
    Button(song_select_page, text = "Add to Playlist", command = add_song_pl).grid(row = 3, column = 0)
    
    # Add a button that allows the user to go back to the search results page
    back_search_results = partial(page_redirect, song_select_page, search_songs_pl_page, song_select_page, uid)
    Button(song_select_page, text = "Back to Search Results", command = back_search_results).grid(row = 4, column = 0)
    
    song_select_page.mainloop()

def add_song_pl_func(sid, uid):
    # Create a page where the user can add the song to a playlist
    add_song_pl_page = Tk()
    add_song_pl_page.geometry('400x300')
    add_song_pl_page.title('Add Song to Playlist')
    Label(add_song_pl_page, text = "---Add Song to Playlist---").grid(row = 0, column = 0)
    
    # Create a search bar that allows user to input the name of the playlist they want to add the song to
    Label(add_song_pl_page, text = "Enter the name of the playlist you want to add the song to:").grid(row = 1, column = 0)
    pl_name = StringVar()
    Entry(add_song_pl_page, bd = 5, textvariable = pl_name).grid(row = 2, column = 0)
    
    # create a button that adds the song to the playlist
    add_song_pl = partial(page_redirect, add_song_pl_page, add_song_pl_query, add_song_pl_page, pl_name, sid, uid)
    Button(add_song_pl_page, text = "Add Song to Playlist", command = add_song_pl).grid(row = 3, column = 0)
    
    # Create a back button that allows the user to go back to the song select menu
    back_song_select = partial(page_redirect, add_song_pl_page, song_select_menu, sid, uid)
    Button(add_song_pl_page, text = "Back to Song Select Menu", command = back_song_select).grid(row = 4, column = 0)
    
    
    add_song_pl_page.mainloop()

def add_song_pl_query(add_song_pl_page, pl_name, sid, uid):

    
    # Find the playlist that matches the given playlist name
    cursor.execute("SELECT pid FROM playlists WHERE title = %s", (pl_name.get(),))
    pid = cursor.fetchone()
    
    # If the playlist exists, add the song to the playlist
    if pid:
    
        # insert into plinclude with the order as max order + 1
        cursor.execute("SELECT MAX(sorder) FROM plinclude WHERE pid = %s", (pid[0],))
        max_order = cursor.fetchone()
        if max_order[0] == None:
            cursor.execute("INSERT INTO plinclude VALUES (%s, %s, %s)", (pid[0], sid, 1))
        else:
            cursor.execute("INSERT INTO plinclude VALUES (%s, %s, %s)", (pid[0], sid, max_order[0] + 1))
        
        connection.commit()
        # Display a successfully added message
        messagebox.showinfo("Success", "The song was successfully added to the playlist!")
    else:
        # Create a new playlist with the playlist name as pl 
        # Find the max pid and add 1 to it to get the new pid
        cursor.execute("SELECT MAX(pid) FROM playlists")
        max_pid = cursor.fetchone()
        new_pid = max_pid[0] + 1
        # Insert the song into the playlist with the uid and pid and pl from what we have
        cursor.execute("INSERT INTO playlists VALUES (%s, %s, %s)", (new_pid, pl_name.get(), uid))
        
        cursor.execute("INSERT INTO plinclude VALUES (%s, %s, %s)", (new_pid, sid, 1))
        connection.commit()
        
        # Display a successfully created playlist message and add the song to the playlist
        messagebox.showinfo("Success", "The playlist was successfully created and the song was added to it!")

def more_info_song_func(sid):
    # Create a page that shows more information about the song
    more_info_page = Tk()
    more_info_page.geometry('400x300') 
    more_info_page.title('More Info')
    Label(more_info_page, text = "---More Info---").grid(row = 0, column = 0)
    
    # Create a page for the user to veiw more information about the song
    more_info_page = Tk()
    more_info_page.geometry('400x300')
    more_info_page.title('More Info')
    Label(more_info_page, text = "---More Info---").grid(row = 0, column = 0)
    
    # display more informatoin about the song. 
    
    # find the song title the sid the duration and the artists who made the song
    cursor.execute("SELECT title, duration FROM songs WHERE sid = %s", (sid.get(),))
    song_title_duration = cursor.fetchall()
    
    # Find the name of the artist who made the song
    cursor.execute("SELECT name FROM artists WHERE aid IN (SELECT aid FROM perform WHERE sid = %s)", (sid.get(),))
    artist_names = cursor.fetchall()
    
    # Find the names of all of the playlists that the song is in
    cursor.execute("SELECT title FROM playlists WHERE pid IN (SELECT pid FROM plinclude WHERE sid = %s)", (sid.get(),))
    playlist_names = cursor.fetchall()
    
    # Display all of the information about the song on the page
    Label(more_info_page, text = "Song ID: " + sid.get()).grid(row = 1, column = 0)
    Label(more_info_page, text = "Song Title: " + song_title_duration[0][0]).grid(row = 2, column = 0)
    Label(more_info_page, text = "Duration: " + str(song_title_duration[0][1])).grid(row = 3, column = 0)
    Label(more_info_page, text = "Artists: " + str(artist_names)).grid(row = 4, column = 0)
    Label(more_info_page, text = "Playlists: " + str(playlist_names)).grid(row = 5, column = 0)
    
    # Add a button that allows the user to go back to the song select menu
    back_song_select = partial(page_redirect, more_info_page, song_select_menu, sid)
    Button(more_info_page, text = "Back to Song Select Menu", command = back_song_select).grid(row = 6, column = 0)
    
    more_info_page.mainloop()

def listento_song(sid, uid):
    # Create a page that allows the user to listen to the song
    listen_song_page = Tk()
    listen_song_page.geometry('400x300')
    listen_song_page.title('Listen to Song')
    Label(listen_song_page, text = "---Listen to Song---").grid(row = 0, column = 0)
    
    # find the current sno by finding the max sno with the given uid and write the song to the user's listening history in python
    # only if the max sno does not have an end time (i.e. the user is still listening to the song) otherwise sno is the max sno + 1
    cursor.execute("SELECT MAX(sno) FROM sessions WHERE uid = %s AND end IS NULL", (uid,))
    sno = cursor.fetchone()[0]
    
    if sno is None:
        # find the max sno from Sessions and add 1 to it
        cursor.execute("SELECT MAX(sno) FROM sessions")
        sno = cursor.fetchone()[0] + 1
        # insert the new sno into Sessions with current date and time as the start time
        cursor.execute("""INSERT INTO sessions (uid, sno, start, end) VALUES (?, ?, ?, ?)""", (uid.get(), sno, time.strftime("%Y-%m-%d"), None))
        # commit the changes to the database
        connection.commit()
        
    # Add the song to the user's listening history if not there or update the cnt if it is there already
    # check the uid sid and sno in the listening history    
    cursor.execute("SELECT * FROM listening_history WHERE uid = %s AND sid = %s AND sno = %s", (uid, sid, sno))
    
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO listens VALUES (%s, %s, %s, %s)", (uid.get(), sno, sid.get(), 1))
    else:
        cursor.execute("UPDATE listen SET cnt = cnt + 1 WHERE uid = %s AND sno = %s AND sid = %s", (uid.get(), sno, sid.get()))
            
    # Add a button that allows the user to go back to the song select menu
    back_song_select = partial(page_redirect, listen_song_page, song_select_menu, listen_song_page, sid)
    Button(listen_song_page, text = "Done listening to song", command = back_song_select).grid(row = 1, column = 0)
    
    connection.commit()
    listen_song_page.mainloop()

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
      
    # Create a button that allows user to search for the artist
    search_artists = partial(page_redirect, search_page, search_artists_query, search_page, search_name, uid)
    Button(search_page, text = "Search", command = search_artists).grid(row = 3, column = 0)
    

    search_page.mainloop()

def search_artists_query(cur_page, search_name, uid):
    # Create a window that shows the results of the search
    search_artists_result_page = Tk()
    search_artists_result_page.geometry('400x300')
    search_artists_result_page.title('Search Results')
    Label(search_artists_result_page, text = "---Search Results---").grid(row = 0, column = 0)

    # Search for artists that match the search name and order by the most number of keyword matches

    # Add button for user to see the next 5 matches (if there are more than 5 matches)
    # Add button for user to see the previous 5 matches (if there are more than 5 matches)
    # Add button for user to see the details of the artist
    # Add button for user to add the artist to their playlist

    search_artists_result_page.mainloop()

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
        # split the aid2 string into a list of aid
        aid2_list = aid2.split()
        # Add each aid to the perform table
        for aid2 in aid2_list: 
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