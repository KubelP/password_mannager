'''Part of the app which generates window visualisation'''
import tkinter as tk
from tkinter import ttk 
from alchemy2 import Password_Mannager_Db, DataBase

a = Password_Mannager_Db()
b = DataBase()
c = None
def take_all():
    '''Function for viewing list of all password manager's items'''
    table_win.clipboard_clear()
    c = b.get_items_list()
    for i in c:
        ii = tuple(i)
        table.insert('', 'end', values=[ii[0], ii[1], ii[2]])

def get_id(id, password):
    '''Function takes id and password from Entry fields and puts as queries to db'''
    cc = b.get_item_by_id(id, password)
    for i in cc:
        ii = tuple(i)
        table_id.insert('', 'end', values=[ii[0], ii[1], ii[2]])
        root.clipboard_append(ii[2])

def get_by_id():
    '''Function returns answer from db'''
    root.clipboard_clear()
    id = by_id.get()
    password = password_id.get()
    get_id(id, password)
    
def add_new_item(url, login, password, password_for_encr):
    '''Send credentials to db'''
    b = DataBase(url, login, password)
    b.add_item(password_for_encr)

def add_new():
    '''Function gets cerdentials from Entry fields and save in db'''
    n_url = new_url.get()
    n_login = new_login.get()
    n_password = new_password.get() 
    p_for_encr = password_for_encryption.get()
    add_new_item(n_url, n_login, n_password, p_for_encr)


root = tk.Tk()
root.title('Password manager')
root.geometry('800x600')

tabsystem = ttk.Notebook(root)

table_win = tk.Frame(tabsystem)
add_win = tk.Frame(tabsystem)

tabsystem.add(table_win, text = 'get password')
tabsystem.add(add_win, text = 'add password')

tabsystem.pack(expand = 1, fill = 'both')

#Table for list of all items in password manager
ttk.Label(table_win, text='*'*100).grid(column=1, row=5)
ttk.Label(table_win, text='take password by portal id').grid(column=1, row=6)
ttk.Label(table_win, text='id').grid(column=0, row=7)
ttk.Label(table_win, text='password').grid(column=0, row=8)

button_all = tk.Button(table_win, text = 'view whole list', state='normal', command=take_all)
button_all.grid(column=1, row=3)

#Labels, Entry fields and table for taking password by id
by_id = tk.Entry(table_win)
by_id.grid(column=1, row=7)
password_id = tk.Entry(table_win, show='*')
password_id.grid(column=1, row=8)

button_id = tk.Button(table_win, text = 'take password by id', state='normal', command=get_by_id)
button_id.grid(column=1, row=9)

table = ttk.Treeview(
    table_win, 
    columns=('id', 'url', 'login'),
    show='headings',
    height=5
)

table.heading('id', text='id')
table.heading('url', text='url')
table.heading('login', text='login')

table.grid(column=1, row=0)


table_id = ttk.Treeview(
    table_win, 
    columns=('url', 'login', 'password'),
    show='headings',
    height=5
)

table_id.heading('url', text='url')
table_id.heading('login', text='login')
table_id.heading('password', text='password')
table_id.grid(column=1, row=10)

#Second page of password manager 'add password'
ttk.Label(add_win, text='URL').grid(column=1, row=1)
ttk.Label(add_win, text='login').grid(column=1, row=2)
ttk.Label(add_win, text='password for portal').grid(column=1, row=3)
ttk.Label(add_win, text='password for manager').grid(column=1, row=4)

new_url = tk.Entry(add_win)
new_url.grid(column=2, row=1)
new_login = tk.Entry(add_win)
new_login.grid(column=2, row=2)
new_password = tk.Entry(add_win)
new_password.grid(column=2, row=3)
password_for_encryption = tk.Entry(add_win)
password_for_encryption.grid(column=2, row=4)

button_new = tk.Button(add_win, text = 'add new', state='normal', command=add_new)
button_new.grid(column=2, row=5)

root.mainloop()
