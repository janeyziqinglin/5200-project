import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
import mysql.connector


# Connect  to books database
def get_connection(username, password):
    global connection
    connection = pymysql.connect(
        host ='localhost',
        user = username,
        password = password,
        database = 'books',
        cursorclass=pymysql.cursors.DictCursor)
    print('Succefully connected to the database books')
    return connection
    
             
# Display connecton error 
def show_connection_error(err_msg):
    error_msg = 'Cannot connect to books database: ' +'\n' + err_msg +'. Please try again.' 
    err_msg = Message(frame_connect, text = error_msg, font=("TkDefaultFont",14), fg='red3',justify=CENTER, width=300)
    err_msg.place(x=350, y=260)
    
    
# Connect to database and jump to user login page
# If error occures, will display the error
def connect_to_db():
    try:
        get_connection(username_var.get(), password_var.get())
        frame_login.tkraise()

    except pymysql.Error as error:
        code, msg = error.args
        show_connection_error(msg)

# Check user's inputted user id
# if the user id is already in the database, and user clicked on Login in button, then successfully log in
# if the user id is not in the database, ask user to click on Sign up button to sign up with the inputted user id
# Else, successfully log in to the App
def check_user_login():
    try:
        global user_id
        cursor = connection.cursor()
        args = [userid_var.get()]
        cursor.callproc('check_user_login', args)
        result = cursor.fetchall()
        cursor.close()
        if len(result) == 0:
            show_no_user()
        else:
            user_id = userid_var.get()
            login_to_db()
            print(user_id)
        
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
    

# Display provided user id is not yet registered warning
def show_no_user():
    msg = 'This User ID is not registered. Please click Sign Up' 
    login_msg = Message(frame_login, text = msg, font=("TkDefaultFont",14), fg='red3', justify=CENTER, width=600)
    login_msg.place(x=350, y=250) 
    

# Login successfully and jump to the main menu page
def login_to_db():
    frame_menu.tkraise()


# Display provided user id is already registered warning
def show_duplicated_user():
    msg = "This User ID is already registered. Please click Log In"
    signup_msg = Message(frame_login, text = msg, font=("TkDefaultFont",14), fg='red3', justify=CENTER, width=600)
    signup_msg.place(x=350, y=250) 


# User sign up with unregistered user id, this record will be inserted into user table
def user_sign_up():
    try:
        global user_id
        cursor = connection.cursor()
        args = [userid_var.get()]
        cursor.callproc('add_user', args)
        connection.commit()
        cursor.close()
        user_id = userid_var.get()
        print(user_id)
        login_to_db()
        
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        show_duplicated_user()
        cursor.close()


# Check in main menu page: table that the user selected to explore more and jump to the corresponding page
def select_table():
    table = menu_var.get()
    if table == 'Book':
        frame_book.tkraise()
    elif table == 'Author':
        frame_author.tkraise()
    elif table == 'Format':
        frame_format.tkraise()
    elif table == 'Genre':
        frame_genre.tkraise()
    elif table == 'Language':
        frame_language.tkraise()
    elif table == 'Author Nationality':
        frame_nat.tkraise()
   

# Jump back to the main menu page
def back_to_menu():
    frame_menu.tkraise()


# Jump to the books rating page
def go_to_rating():
    frame_rate.tkraise()


# Show up error message box and the application window should be closed
def show_error_and_close(msg):
    messagebox.showerror(msg)
    root.withdraw()


# Show up mysql workben error message and display it to a specific frame
def show_input_error(msg, frame):
    err_msg = Message(frame, text = msg, font=("TkDefaultFont",14), fg='red3', justify=CENTER, width=600)
    err_msg.place(x=660, y=40) 
    err_msg.after(4000, err_msg.destroy)
    

##-----------------------------------Show All Book related Tables----------------------------

# display all book data
def show_all_book():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_book_all')
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])


    all_book_tree = ttk.Treeview(frame_book)
    all_book_tree.place(x = 3, y = 200)
    

    all_book_tree['show'] = 'headings'
    all_book_tree['columns'] = ['book_id', 'ISBN_10', 'book_title','author','edition',
                                'page_count','publisher','language','format','genre','published_date','avg_rating']
    
    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(all_book_tree['columns'])
    for col in all_book_tree['columns']:
        all_book_tree.column(col, width = col_width, anchor=W)
        all_book_tree.heading(col, text=col, anchor=W)
    

    # create striped row tags
    all_book_tree.tag_configure('oddrow', background = 'white')
    all_book_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            all_book_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('evenrow'))
        else:
            all_book_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('oddrow'))

        i = i+1
      
# check which checking condition that user selected in the dropdown menu
# and use the input to do search
def select_book_con():
    con = book_menu_var.get()
    con_input = book_con_var.get()
    if con == 'Author Name':
        show_book_by_authorname(con_input)
    
    elif con == 'Genre':
        show_book_by_genre(con_input)
    
    if con == 'Format':
        show_book_by_format(con_input)
    
    if con == 'Language':
        show_book_by_lan(con_input)

# display data for one book based on book id from user input
def show_book_by_id():
    try:
        cursor = connection.cursor()
        args = [ bookid_var.get()]
        cursor.callproc('read_book_one', args)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_input_error(msg, frame_book)
            
            
        else:
            cursor.close()
            show_error_and_close(msg) 
    # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    one_book_tree = ttk.Treeview(frame_book)
    one_book_tree.place(x = 3, y = 200)
    

    one_book_tree['show'] = 'headings'
    one_book_tree['columns'] = ['book_id', 'ISBN_10', 'book_title','author','edition',
                                'page_count','publisher','language','format','genre','published_date','avg_rating']
    
        # set up treeview table headings and columns
    col_width = root.winfo_width() // len(one_book_tree['columns'])
    for col in one_book_tree['columns']:
        one_book_tree.column(col, width = col_width, anchor=W)
        one_book_tree.heading(col, text=col, anchor=W)
    
    # create striped row tags
    one_book_tree.tag_configure('oddrow', background = 'white')
    one_book_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            one_book_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('evenrow'))
        else:
            one_book_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('oddrow'))

        i = i+1


# display data for one book based on author name from user input
def show_book_by_authorname(input_str):
    try:
        cursor = connection.cursor()
        args = [input_str]
        cursor.callproc('read_author_book', args)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_input_error(msg, frame_book)
            
        else:
            cursor.close()
            show_error_and_close(msg) 
    # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    book_author_tree = ttk.Treeview(frame_book)
    book_author_tree.place(x = 3, y = 200)
    

    book_author_tree['show'] = 'headings'
    book_author_tree['columns'] = ['book_id', 'ISBN_10', 'book_title','author','edition',
                                'page_count','publisher','language','format','genre','published_date','avg_rating']
    
        # set up treeview table headings and columns
    col_width = root.winfo_width() // len(book_author_tree['columns'])
    for col in book_author_tree['columns']:
        book_author_tree.column(col, width = col_width, anchor=W)
        book_author_tree.heading(col, text=col, anchor=W)
    
    # create striped row tags
    book_author_tree.tag_configure('oddrow', background = 'white')
    book_author_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            book_author_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('evenrow'))
        else:
            book_author_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('oddrow'))

        i = i+1


# display book data based on genre type from user input
def show_book_by_genre(input_str):
    try:
        cursor = connection.cursor()
        args = [input_str]
        cursor.callproc('read_genre_book', args)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_input_error(msg, frame_book)
            
        else:
            cursor.close()
            show_error_and_close(msg) 
    # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    book_genre_tree = ttk.Treeview(frame_book)
    book_genre_tree.place(x = 3, y = 200)
    

    book_genre_tree['show'] = 'headings'
    book_genre_tree['columns'] = ['book_id', 'ISBN_10', 'book_title','author','edition',
                                'page_count','publisher','language','format','genre','published_date','avg_rating']
    
        # set up treeview table headings and columns
    col_width = root.winfo_width() // len(book_genre_tree['columns'])
    for col in book_genre_tree['columns']:
        book_genre_tree.column(col, width = col_width, anchor=W)
        book_genre_tree.heading(col, text=col, anchor=W)
    
    # create striped row tags
    book_genre_tree.tag_configure('oddrow', background = 'white')
    book_genre_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            book_genre_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('evenrow'))
        else:
            book_genre_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('oddrow'))

        i = i+1


# display book data based on format type from user input
def show_book_by_format(input_str):
    try:
        cursor = connection.cursor()
        args = [input_str]
        cursor.callproc('read_format_book', args)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_input_error(msg, frame_book)
            
        else:
            cursor.close()
            show_error_and_close(msg) 
    # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    book_format_tree = ttk.Treeview(frame_book)
    book_format_tree.place(x = 3, y = 200)
    

    book_format_tree['show'] = 'headings'
    book_format_tree['columns'] = ['book_id', 'ISBN_10', 'book_title','author','edition',
                                'page_count','publisher','language','format','genre','published_date','avg_rating']
    
    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(book_format_tree['columns'])
    for col in book_format_tree['columns']:
        book_format_tree.column(col, width = col_width, anchor=W)
        book_format_tree.heading(col, text=col, anchor=W)
    
    # create striped row tags
    book_format_tree.tag_configure('oddrow', background = 'white')
    book_format_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            book_format_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('evenrow'))
        else:
            book_format_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('oddrow'))

        i = i+1


# display book data based on language type from user input
def show_book_by_lan(input_str):
    try:
        cursor = connection.cursor()
        args = [input_str]
        cursor.callproc('read_language_book', args)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_input_error(msg, frame_book)
            
        else:
            cursor.close()
            show_error_and_close(msg) 
    # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    book_lan_tree = ttk.Treeview(frame_book)
    book_lan_tree.place(x = 3, y = 200)
    

    book_lan_tree['show'] = 'headings'
    book_lan_tree['columns'] = ['book_id', 'ISBN_10', 'book_title','author','edition',
                                'page_count','publisher','language','format','genre','published_date','avg_rating']
    
        # set up treeview table headings and columns
    col_width = root.winfo_width() // len(book_lan_tree['columns'])
    for col in book_lan_tree['columns']:
        book_lan_tree.column(col, width = col_width, anchor=W)
        book_lan_tree.heading(col, text=col, anchor=W)
    
    # create striped row tags
    book_lan_tree.tag_configure('oddrow', background = 'white')
    book_lan_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            book_lan_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('evenrow'))
        else:
            book_lan_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['author'],r['edition'],r['page_count'],r['publisher'],
                                                        r['language'],r['format'],r['genre'],r['published_date'],r['avg_rating']), tags=('oddrow'))

        i = i+1



## -------------Show all Author related Tale in Author Page----------------------

# display all author data
def show_all_author():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_author_all')
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    all_author_tree = ttk.Treeview(frame_author)
    all_author_tree.place(x = 3, y = 200)
    

    all_author_tree['show'] = 'headings'
    all_author_tree['columns'] = ['author_id', 'author_name', 'nationality','born', 'died', 'author_description']

    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(all_author_tree['columns'])
    for col in all_author_tree['columns']:
        all_author_tree.column(col, width = col_width, anchor=W)
        all_author_tree.heading(col, text=col, anchor=W)
    

    # create striped row tags
    all_author_tree.tag_configure('oddrow', background = 'white')
    all_author_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            all_author_tree.insert('', i, text='', values = (r['author_id'], r['author_name'], r['nationality'],r['born'],r['died'],r['author_description']), tags=('evenrow'))
        else:
            all_author_tree.insert('', i, text='', values = (r['author_id'], r['author_name'],  r['nationality'],r['born'],r['died'],r['author_description']), tags=('oddrow'))

        i = i+1


# display one author data based on author id from user input
def show_author_by_id():
    try:
        cursor = connection.cursor()
        args = [ authorid_var.get()]
        cursor.callproc('read_author_one', args)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_input_error(msg, frame_author)
            
        else:
            cursor.close()
            show_error_and_close(msg) 
    # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    one_author_tree = ttk.Treeview(frame_author)
    one_author_tree.place(x = 3, y = 200)
    

    one_author_tree['show'] = 'headings'
    one_author_tree['columns'] = ['author_id','author_name','nationality','born', 'died', 'author_description' ]
    
    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(one_author_tree['columns'])
    for col in one_author_tree['columns']:
        one_author_tree.column(col, width = col_width, anchor=W)
        one_author_tree.heading(col, text=col, anchor=W)

    # create striped row tags
    one_author_tree.tag_configure('oddrow', background = 'white')
    one_author_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            one_author_tree.insert('', i, text='', values = (r['author_id'], r['author_name'], r['nationality'],r['born'],r['died'],r['author_description']), tags=('evenrow'))
        else:
            one_author_tree.insert('', i, text='', values = (r['author_id'], r['author_name'], r['nationality'],r['born'],r['died'],r['author_description']), tags=('oddrow'))

        i = i+1


# display one author data based on nationality name from user input
def show_author_by_nat():
    try:
        cursor = connection.cursor()
        args = [ authornat_var.get()]
        cursor.callproc('read_nat_author', args)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_input_error(msg, frame_author)
            
        else:
            cursor.close()
            show_error_and_close(msg) 
    # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    nat_author_tree = ttk.Treeview(frame_author)
    nat_author_tree.place(x = 3, y = 200)
    

    nat_author_tree['show'] = 'headings'
    nat_author_tree['columns'] = ['author_id','author_name','nationality','born', 'died', 'author_description' ]
    
    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(nat_author_tree['columns'])
    for col in nat_author_tree['columns']:
        nat_author_tree.column(col, width = col_width, anchor=W)
        nat_author_tree.heading(col, text=col, anchor=W)

    # create striped row tags
    nat_author_tree.tag_configure('oddrow', background = 'white')
    nat_author_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            nat_author_tree.insert('', i, text='', values = (r['author_id'], r['author_name'], r['nationality'],r['born'],r['died'],r['author_description']), tags=('evenrow'))
        else:
            nat_author_tree.insert('', i, text='', values = (r['author_id'], r['author_name'], r['nationality'],r['born'],r['died'],r['author_description']), tags=('oddrow'))

        i = i+1
    

#---------------------------------Show all Format related table in Format Page-------------
    
# display all data in format table
def show_all_format():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_format_all')
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    all_format_tree = ttk.Treeview(frame_format)
    all_format_tree.place(x = 3, y = 140)
    

    all_format_tree['show'] = 'headings'
    all_format_tree['columns'] = ['format_name', 'format_description']

    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(all_format_tree['columns'])
    for col in all_format_tree['columns']:
        all_format_tree.column(col, width = col_width, anchor=W)
        all_format_tree.heading(col, text=col, anchor=W)
    

    # create striped row tags
    all_format_tree.tag_configure('oddrow', background = 'white')
    all_format_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            all_format_tree.insert('', i, text='', values = (r['format_name'],r['format_description']), tags=('evenrow'))
        else:
            all_format_tree.insert('', i, text='', values = (r['format_name'],r['format_description']), tags=('oddrow'))

        i = i+1
    
#----------------------------Show all Genre related table in Genre Page----------------------
# display all data in genre table
def show_all_genre():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_genre_all')
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    all_genre_tree = ttk.Treeview(frame_genre)
    all_genre_tree.place(x = 3, y = 140)
    

    all_genre_tree['show'] = 'headings'
    all_genre_tree['columns'] = ['genre_type', 'genre_description']

    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(all_genre_tree['columns'])
    for col in all_genre_tree['columns']:
        all_genre_tree.column(col, width = col_width, anchor=W)
        all_genre_tree.heading(col, text=col, anchor=W)
    
    # create striped row tags
    all_genre_tree.tag_configure('oddrow', background = 'white')
    all_genre_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            all_genre_tree.insert('', i, text='', values = (r['genre_type'],r['genre_description']), tags=('evenrow'))
        else:
            all_genre_tree.insert('', i, text='', values = (r['genre_type'],r['genre_description']), tags=('oddrow'))

        i = i+1

#-------------------------------Show all language related table in Language page----------------
# display all data in language table
def show_all_language():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_language_all')
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    all_lan_tree = ttk.Treeview(frame_language)
    all_lan_tree.place(x = 3, y = 140)
    

    all_lan_tree['show'] = 'headings'
    all_lan_tree['columns'] = ['language_name', 'language_description']

    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(all_lan_tree['columns'])
    for col in all_lan_tree['columns']:
        all_lan_tree.column(col, width = col_width, anchor=W)
        all_lan_tree.heading(col, text=col, anchor=W)
    

    # create striped row tags
    all_lan_tree.tag_configure('oddrow', background = 'white')
    all_lan_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            all_lan_tree.insert('', i, text='', values = (r['language_name'],r['language_description']), tags=('evenrow'))
        else:
            all_lan_tree.insert('', i, text='', values = (r['language_name'],r['language_description']), tags=('oddrow'))

        i = i+1

#-------------------------------------Show all nationality related table in Nationality page----------
# display all data in Nationality table
def show_all_nat():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_nationality_all')
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    all_nat_tree = ttk.Treeview(frame_nat)
    all_nat_tree.place(x = 370, y = 140)
    

    all_nat_tree['show'] = 'headings'
    all_nat_tree['columns'] = ['nationality_name']
    
    all_nat_tree.column('nationality_name', width = 300,minwidth= 100, anchor=W)
 
    all_nat_tree.heading('nationality_name', text='Nationality', anchor=W)
    
    # create striped row tags
    all_nat_tree.tag_configure('oddrow', background = 'white')
    all_nat_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            all_nat_tree.insert('', i, text='', values = (r['nationality_name']), tags=('evenrow'))
        else:
            all_nat_tree.insert('', i, text='', values = (r['nationality_name']), tags=('oddrow'))

        i = i+1

#---------------------------All user rating related table in Rating Page--------------------

# display current user's user id
def show_user_id():
    id_label = tk.Label(frame_rate, text =user_id, font=("TkDefaultFont", 17, 'bold'), fg='dark orange')
    id_label.place(x = 900, y = 20)


# display all ratings from the current user
def show_user_rate():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_user_rating', (user_id,))
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    rate_tree = ttk.Treeview(frame_rate)
    rate_tree.place(x = 3, y = 140)
    

    rate_tree['show'] = 'headings'
    rate_tree['columns'] = ['book_id', 'ISBN_10','book_title','publisher','language','genre','avg_rating','your_rating']

    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(rate_tree['columns'])
    for col in rate_tree['columns']:
        rate_tree.column(col, width = col_width, anchor=W)
        rate_tree.heading(col, text=col, anchor=W)
    
    
    # create striped row tags
    rate_tree.tag_configure('oddrow', background = 'white')
    rate_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            rate_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['publisher'],r['language'],r['genre'],r['avg_rating'], r['your_rating']), tags=('evenrow'))
        else:
            rate_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['publisher'],r['language'],r['genre'],r['avg_rating'], r['your_rating']), tags=('oddrow'))

        i = i+1



# display all books rating (for validating the user rating update)
def show_books_rate():
    try:
        cursor = connection.cursor()
        cursor.callproc('read_books_rating')
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        cursor.close()
        show_error_and_close(msg) 
    
        # set configuration for treeview
    style = ttk.Style()
    
    style.configure("Treeview", background = "white", foreground = 'black', rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=("TkDefaultFont", 13, 'bold'), foreground = 'black')
    style.map('Treeview', background=[('selected', 'LightBlue3')])

    book_rate_tree = ttk.Treeview(frame_rate)
    book_rate_tree.place(x = 3, y = 140)
    

    book_rate_tree['show'] = 'headings'
    book_rate_tree['columns'] = ['book_id', 'ISBN_10','book_title','publisher','language','genre','format','avg_rating']

    # set up treeview table headings and columns
    col_width = root.winfo_width() // len(book_rate_tree['columns'])
    for col in book_rate_tree['columns']:
        book_rate_tree.column(col, width = col_width, anchor=W)
        book_rate_tree.heading(col, text=col, anchor=W)
    
    
    # create striped row tags
    book_rate_tree.tag_configure('oddrow', background = 'white')
    book_rate_tree.tag_configure('evenrow', background = 'LightBlue1')

    # insert data
    i = 0
    for r in result:
        if i % 2 == 0:
            book_rate_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['publisher'],r['language'],r['genre'],r['format'],r['avg_rating']), tags=('evenrow'))
        else:
            book_rate_tree.insert('', i, text='', values = (r['book_id'], r['ISBN_10'], r['book_title'],
                                                        r['publisher'],r['language'],r['genre'],r['format'],r['avg_rating']), tags=('oddrow'))

        i = i+1

    

# check which action user selected in rate page, and use
# the inputting book id and rating value to update the rating records
def select_rate_action():
    action = rate_menu_var.get()
    book_id = rate_bookid_var.get()
    rating_value = rate_value_var.get()
    if action == 'Add':
        add_book_rate(book_id, rating_value)
    elif action == 'Delete':
        delete_book_rate(book_id)
    elif action == 'Update':
        update_book_rate(book_id, rating_value)


# display an successful action message to the user if the action
# is successful
def show_success_msg():
    msg = 'You have successfully update your record! Please click on Check All My Ratings to see your updated records!'
    succ_msg = Message(frame_rate, text = msg, font=("TkDefaultFont",14), fg='dark orange', justify=CENTER, width=300)
    succ_msg.place(x=250, y=500) 
    succ_msg.after(4000, succ_msg.destroy)


# display the input checking warnings from the database procedures
def show_rate_error(msg):
    err_msg = Message(frame_rate, text=msg,font=("TkDefaultFont",14), fg='red3', justify=CENTER, width=300)
    err_msg.place(x =250, y=500)
    err_msg.after(4000, err_msg.destroy)


# Use user provided book id and rating value to insert a new rating record
def add_book_rate(input_book_id, input_rate):
    try:
        cursor = connection.cursor()
        args = [user_id, input_book_id, input_rate]
        cursor.callproc('add_new_rating', args)
        connection.commit()
        show_success_msg()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_rate_error(msg)
        else:
            cursor.close()
            show_error_and_close(msg)


# Use user provided book id to delete an existing rating record
def delete_book_rate(input_book_id):
    try:
        cursor = connection.cursor()
        args = [user_id, input_book_id]
        cursor.callproc('delete_exist_rating', args)
        connection.commit()
        show_success_msg()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_rate_error(msg)
        else:
            cursor.close()
            show_error_and_close(msg)


# Use user provided book id and new rating value to update an existing rating record
def update_book_rate(input_book_id, input_rate):
    try:
        cursor = connection.cursor()
        args = [user_id, input_book_id, input_rate]
        cursor.callproc('update_exist_rating', args)
        connection.commit()
        show_success_msg()
        cursor.close()
    except pymysql.Error as error:
        code, msg = error.args
        print(code, msg)
        if code == 1644:
            show_rate_error(msg)
        else:
            cursor.close()
            show_error_and_close(msg)
 






##########------------- GUI Canvas---------------------

root = tk.Tk()
root.geometry("1000x600")
root.title("Books Database")


# -----------SQL Connection page
frame_connect = tk.Frame(root, width=1000, height=600)
frame_connect.grid(row=0, column=0)

# SQL connection page: ask for SQL Server username and password
username_label = tk.Label(frame_connect, text ="SQL Server Username:", font=("TkDefaultFont", 17, 'bold'))
username_label.place(x = 300, y = 120)

username_var = StringVar(frame_connect, name = 'username') 
Username = ttk.Entry(frame_connect,textvariable=username_var, font=("TkDefaultFont", 17))
Username.place(x = 560, y = 120, width = 150, height=35)

password_label = tk.Label(frame_connect, text ="SQL Server Password:",font=("TkDefaultFont", 17, 'bold'))
password_label.place(x = 300, y = 200)
 
password_var = StringVar(frame_connect,name='password')
Password = ttk.Entry(frame_connect, textvariable=password_var, font=("TkDefaultFont", 17))
Password.place(x = 560, y = 200, width = 150, height=35)

connectbtn = tk.Button(frame_connect, text ="Connect",font=("TkDefaultFont", 16, 'bold'),fg='steel blue', 
                      bg ='light gray', command = connect_to_db)
connectbtn.place(x =450, y = 400, width = 100, height=50)


# --------------Login page
frame_login = tk.Frame(root, width=1000, height=600)
frame_login.grid(row = 0, column=0)

welcome_label = tk.Label(frame_login, text ="Welcome to Books Database!", font=("TkDefaultFont", 21, 'bold'))
welcome_label.place(x = 370, y = 20)

welc_txt = 'Please enter your User ID to log in, ' +'\n' +'or register with a new one.'
welcome_msg = Message(frame_login, text=welc_txt, justify=CENTER, width=300, font=("TkDefaultFont", 15), fg='dark orange')
welcome_msg.place(x=390, y=60)

userid_label = tk.Label(frame_login,text='Books User ID:',font=("TkDefaultFont", 17, 'bold') )
userid_label.place(x = 370, y = 170)

userid_var = IntVar(frame_login, name = 'userid')
UserId = ttk.Entry(frame_login, textvariable=userid_var, font=("TkDefaultFont", 17))
UserId.place(x = 500, y = 165, width = 150, height=35)


login_btn = tk.Button(frame_login, text ="Log In",font=("TkDefaultFont", 16, 'bold'), bg ='light gray',fg='steel blue',
                       command=check_user_login)
login_btn.place(x=370, y = 380,width = 100, height=50)

signup_btn = tk.Button(frame_login, text ="Sign Up",font=("TkDefaultFont", 16, 'bold'),bg ='light gray',fg='steel blue', 
                       command=user_sign_up)
signup_btn.place(x=610, y = 380,width = 100, height=50)


# --------------------Main Menu------
frame_menu = tk.Frame(root, width=1000, height=600)
frame_menu.grid(row = 0, column=0)

welcome_label = tk.Label(frame_menu, text ="Welcome to Books Database!", font=("TkDefaultFont", 21, 'bold'))
welcome_label.place(x = 370, y = 20)

welc_txt = 'Check tables or leave your rating to the books!'
welcome_msg = Message(frame_menu, text=welc_txt, justify=CENTER, width=300, font=("TkDefaultFont", 15), fg='dark orange')
welcome_msg.place(x=390, y=80)

menu_label = tk.Label(frame_menu, text ="Check One Table:", font=("TkDefaultFont", 17, 'bold'))
menu_label.place(x = 330, y = 170)

all_tables = ['Book', 'Author', 'Format', 'Genre', 'Language', 'Author Nationality']
# Create Dropdown menu 
menu_var = StringVar()
# style of dropdown button
style = ttk.Style()
style.configure('my.TMenubutton', font=('TkDefaultFont', 17, 'bold'))
# initial value of the dropdown menu
menu_width = len(max(all_tables, key=len))
dropdown_menu = ttk.OptionMenu(frame_menu, menu_var, all_tables[0], *all_tables,style = 'my.TMenubutton')
dropdown_menu.config(width = menu_width) 
dropdown_menu['menu'].config(font=("TkDefaultFont", 17))
dropdown_menu.place(x=500, y =170) 

menu_submit_btn = tk.Button(frame_menu, text ="Go",font=("TkDefaultFont", 16, 'bold'), bg ='light gray',command=select_table,fg='steel blue')
menu_submit_btn.place(x=800,  y =165,  height=35)

## go to rating page
rating_label = tk.Label(frame_menu, text ="Post or Update Your Book Ratings:", font=("TkDefaultFont", 17, 'bold'))
rating_label.place(x =330, y = 300)

rating_btn = tk.Button(frame_menu, text ="Go",font=("TkDefaultFont", 16, 'bold'), bg ='light gray', command=go_to_rating,fg='steel blue')
rating_btn.place(x=650,  y =295,  height=35)


# ------------------------------Book Page---------------------
frame_book = tk.Frame(root, width=1000, height=600)
frame_book.grid(row = 0, column=0)

btitle_label = tk.Label(frame_book, text ="Welcom to Book Table!", font=("TkDefaultFont", 21, 'bold'))
btitle_label.place(x = 370, y = 20)

back_btn = tk.Button(frame_book,text='\u2190', command=back_to_menu, font=("TkDefaultFont", 16,'bold' ),bg ='light gray',fg='steel blue')
back_btn.place(x = 20, y=20)

all_book_btn = tk.Button(frame_book,text='Check All Books', command=show_all_book, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
all_book_btn.place(x = 150, y=15, height=40)

bookid_label = tk.Label(frame_book, text ="Check By Book ID:", font=("TkDefaultFont", 17, 'bold'))
bookid_label.place(x = 300, y = 80)

bookid_var = IntVar(frame_book, name = 'bookid')
bookId = ttk.Entry(frame_book, textvariable=bookid_var, font=("TkDefaultFont", 17))
bookId.place(x = 480, y = 75, width = 150, height=35)

search_id_btn = tk.Button(frame_book,text="Go", command=show_book_by_id, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
search_id_btn.place(x = 650,y =75, height=35 )

book_check_label = tk.Label(frame_book, text ="Check By Others:", font=("TkDefaultFont", 17, 'bold'))
book_check_label.place(x = 300, y = 130)

# Create Dropdown menu for user to select the conditions for checking books
all_conditions = ['Author Name', 'Format', 'Genre', 'Language']
book_menu_var = StringVar()
# style of dropdown button
style = ttk.Style()
style.configure('my.TMenubutton', font=('TkDefaultFont', 17, 'bold'))
# initial value of the dropdown menu
book_menu_width = len(max(all_conditions, key=len))
book_dropdown = ttk.OptionMenu(frame_book, book_menu_var, all_conditions[0], *all_conditions,style = 'my.TMenubutton')
book_dropdown.config(width = book_menu_width) 
book_dropdown['menu'].config(font=("TkDefaultFont", 17))
book_dropdown.place(x=470, y =130) 

book_con_var = StringVar(frame_book, name = 'book_condition')
book_con = ttk.Entry(frame_book, textvariable=book_con_var, font=("TkDefaultFont", 17))
book_con.place(x = 650, y = 125, width = 150, height=35)

search_con_btn = tk.Button(frame_book,text="Go", font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue', command=select_book_con)
search_con_btn.place(x = 780,y =125, height=35 )



# -----------------------------Author Page------------------
frame_author = tk.Frame(root, width=1000, height=600)
frame_author.grid(row = 0, column=0)

atitle_label = tk.Label(frame_author, text ="Welcom to Author Table!", font=("TkDefaultFont", 21, 'bold'))
atitle_label.place(x = 370, y = 20)

back_btn = tk.Button(frame_author,text='\u2190', command=back_to_menu, font=("TkDefaultFont", 16,'bold' ),bg ='light gray',fg='steel blue')
back_btn.place(x = 20, y=20)

all_author_btn = tk.Button(frame_author,text='Check All Authors', command=show_all_author, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
all_author_btn.place(x = 150, y=15, height=40)

author_id_label = tk.Label(frame_author, text ="Check By Author ID:", font=("TkDefaultFont", 17, 'bold'))
author_id_label.place(x = 300, y = 80)

authorid_var = IntVar(frame_author, name = 'author_id')
authorID = ttk.Entry(frame_author, textvariable=authorid_var, font=("TkDefaultFont", 17))
authorID.place(x = 480, y = 75, width = 150, height=35)

search_id_btn = tk.Button(frame_author,text="Go", command=show_author_by_id, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
search_id_btn.place(x = 650,y =75, height=35 )

author_nat_label  = tk.Label(frame_author, text ="Check By Nationality:", font=("TkDefaultFont", 17, 'bold'))
author_nat_label.place(x = 300, y = 130)

authornat_var = StringVar(frame_author, name = 'author_nat')
authorNat = ttk.Entry(frame_author, textvariable=authornat_var, font=("TkDefaultFont", 17))
authorNat.place(x = 490, y = 125, width = 150, height=35)

search_nat_btn = tk.Button(frame_author,text="Go", font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue', command=show_author_by_nat)
search_nat_btn.place(x = 650,y =125, height=35 )

#-----------------------------Format Page-------------------
frame_format = tk.Frame(root, width=1000, height=600)
frame_format.grid(row = 0, column=0)

ftitle_label = tk.Label(frame_format, text ="Welcom to Format Table!", font=("TkDefaultFont", 21, 'bold'))
ftitle_label.place(x = 370, y = 20)

back_btn = tk.Button(frame_format,text='\u2190', command=back_to_menu, font=("TkDefaultFont", 16,'bold' ),bg ='light gray',fg='steel blue')
back_btn.place(x = 20, y=20)

all_format_btn = tk.Button(frame_format,text='Check All Formats', command=show_all_format, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
all_format_btn.place(x = 400, y=70, height=40)

#-----------------------------Genre Page--------------------
frame_genre = tk.Frame(root, width=1000, height=600)
frame_genre.grid(row = 0, column=0)

gtitle_label = tk.Label(frame_genre, text ="Welcom to Genre Table!", font=("TkDefaultFont", 21, 'bold'))
gtitle_label.place(x = 370, y = 20)

back_btn = tk.Button(frame_genre,text='\u2190', command=back_to_menu,  font=("TkDefaultFont", 16,'bold' ),bg ='light gray',fg='steel blue')
back_btn.place(x = 20, y=20)

all_genre_btn = tk.Button(frame_genre,text='Check All Genres', command=show_all_genre, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
all_genre_btn.place(x = 400, y=70, height=40)

#-----------------------------Language Page--------------------
frame_language = tk.Frame(root, width=1000, height=600)
frame_language.grid(row = 0, column=0)

ltitle_label = tk.Label(frame_language, text ="Welcom to Language Table!", font=("TkDefaultFont", 21, 'bold'))
ltitle_label.place(x = 370, y = 20)

back_btn = tk.Button(frame_language,text='\u2190', command=back_to_menu, font=("TkDefaultFont", 16,'bold' ),bg ='light gray',fg='steel blue')
back_btn.place(x = 20, y=20)

all_language_btn = tk.Button(frame_language,text='Check All Languages', command=show_all_language, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
all_language_btn.place(x = 400, y=70, height=40)

#-----------------------------Nationality Page--------------------
frame_nat = tk.Frame(root, width=1000, height=600)
frame_nat.grid(row = 0, column=0)

ntitle_label = tk.Label(frame_nat, text ="Welcom to Nationality Table!", font=("TkDefaultFont", 21, 'bold'))
ntitle_label.place(x = 370, y = 20)

back_btn = tk.Button(frame_nat,text='\u2190', command=back_to_menu, font=("TkDefaultFont", 16,'bold' ),bg ='light gray',fg='steel blue')
back_btn.place(x =20 , y=20)

all_nat_btn = tk.Button(frame_nat,text='Check All Nationalities', command=show_all_nat, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
all_nat_btn.place(x = 400, y=70, height=40)


#------------------------------Rating Page-----------------------------
frame_rate= tk.Frame(root, width=1000, height=600)
frame_rate.grid(row = 0, column=0)

rtitle_label = tk.Label(frame_rate, text ="Welcom to Books Rating!", font=("TkDefaultFont", 21, 'bold'))
rtitle_label.place(x = 370, y = 20)

back_btn = tk.Button(frame_rate,text='\u2190', command=back_to_menu, font=("TkDefaultFont", 16,'bold' ),bg ='light gray', fg='steel blue')
back_btn.place(x =20 , y=20)

all_rate_btn = tk.Button(frame_rate,text='Check All My Ratings', font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue', command=show_user_rate)
all_rate_btn.place(x = 130, y=15, height=40)

book_rate_btn = tk.Button(frame_rate,text='Check All Books Ratings', font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue', command=show_books_rate)
book_rate_btn.place(x = 110, y=80, height=40)

check_user_id_btn = tk.Button(frame_rate,text='My User Id ', command=show_user_id, font=("TkDefaultFont",16, 'bold'),bg ='light gray',fg='steel blue')
check_user_id_btn.place(x = 760, y=20)

welc_txt = 'Post a new rating or update your old ratings here! (Please click on Check All My Ratings to refresh the records after editing)'
welcome_msg = Message(frame_rate, text=welc_txt, justify=CENTER, width=300, font=("TkDefaultFont", 15), fg='dark orange')
welcome_msg.place(x=350, y=55)

ask_bookid_label = tk.Label(frame_rate, text ="Book Id", font=("TkDefaultFont", 16, 'bold'))
ask_bookid_label.place(x = 250, y = 430)

ask_rate_label = tk.Label(frame_rate, text ="Rating Value(integer 0-5)", font=("TkDefaultFont", 16, 'bold'))
ask_rate_label.place(x = 370, y = 430)

rate_bookid_var = IntVar(frame_rate, name='rating_book_id')
rate_book_id= ttk.Entry(frame_rate, textvariable=rate_bookid_var, font=("TkDefaultFont", 16))
rate_book_id.place(x = 250, y = 460, width = 100, height=35)

rate_value_var = IntVar(frame_rate, name='rating_value')
rate_value= ttk.Entry(frame_rate, textvariable=rate_value_var, font=("TkDefaultFont", 16))
rate_value.place(x = 370, y = 460, width = 100, height=35)

rate_action_label = tk.Label(frame_rate, text ="Action", font=("TkDefaultFont", 16, 'bold'))
rate_action_label.place(x = 600, y = 430)

# Create Dropdown menu for user to select the actions
all_actions = ['Add', 'Delete', 'Update']
rate_menu_var = StringVar()
# style of dropdown button
style = ttk.Style()
style.configure('my.TMenubutton', font=('TkDefaultFont', 16, 'bold'))
# initial value of the dropdown menu
rate_menu_width = len(max(all_actions, key=len))
rate_dropdown = ttk.OptionMenu(frame_rate, rate_menu_var, all_actions[0], *all_actions,style = 'my.TMenubutton')
rate_dropdown.config(width = rate_menu_width) 
rate_dropdown['menu'].config(font=("TkDefaultFont", 16))
rate_dropdown.place(x=600, y =460) 

submit_btn = tk.Button(frame_rate,text='Submit', command=select_rate_action, font=("TkDefaultFont",17, 'bold'),bg ='light gray',fg='steel blue')
submit_btn.place(x = 750, y=460, height=40)


#---------------------------------
frame_connect.tkraise()
root.mainloop()




