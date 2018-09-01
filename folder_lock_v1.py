import base64
import os
import sqlite3
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import subprocess


from PIL import ImageTk, Image

conn = sqlite3.connect("fl.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS data(username text, password text, folder text)")
conn.commit()

# c.execute("INSERT INTO data VALUES())

add=""
passwd=""

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


def redirect():
    user_name = uname.get()
    pass_word = passwd.get()
    c.execute("SELECT username, password, folder FROM data WHERE username=? AND password=?",(user_name,pass_word))
    conn.commit()
    get = c.fetchone()
    if get!=None:
        fol_der = get[2]
        explore(fol_der)
        root.quit()
    else:
        msg1 = tkinter.messagebox.showwarning("Info","Incorrect Credential")

def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])


def donothing():
    pass

def quiting():
    os.remove('shrake1.png')
    os.remove('shrake2.png')
    root.quit()

def about():
    msg = tkinter.messagebox.showinfo('About', '\tShrake\n\nhttps://www.shrake.com\n\nVersion : 1.5.0\n\nBuild : 3176')

def change_folder():

    def select_folder():
        global add
        add = tkinter.filedialog.askdirectory()

    def changefolder():
        global add
        un_name = uname.get()
        pass_wd = passwd.get()
        c.execute("SELECT username, password FROM data WHERE username=? AND password=?", (un_name, pass_wd))
        conn.commit()
        getinfo = c.fetchone()
        if getinfo != None:
            if add!="":
                c.execute("UPDATE data SET folder=? WHERE username=?",(add,un_name))
                conn.commit()
                msg = tkinter.messagebox.showinfo("Info", "Folder Changed")
            else:
                msg = tkinter.messagebox.showerror("Info", "Folder not selected")

        else:
            msg = tkinter.messagebox.showerror("Info", "Incorrect credential!")
    global frame3, frame5
    frame2.destroy()
    frame3.destroy()
    frame5.destroy()
    root.geometry("350x150+450+200")
    frame5 = Frame(root, width=350, height=150)
    logo_img = Label(frame5, image=img2).place(x=270, y=6)
    shrake_img = Label(frame5, image=img1).place(x=265, y=65)

    text1 = Label(frame5, text="Username : ").place(x=30, y=10)
    text2 = Label(frame5, text="Password  : ").place(x=30, y=40)
    uname = Entry(frame5)
    uname.place(x=95, y=10)
    passwd = Entry(frame5)
    passwd.place(x=95, y=40)
    add_btn = Button(frame5, text="select folder", command=select_folder, bg="light blue").place(x=120, y=70)
    change_btn = Button(frame5, text=" Change ", command=changefolder, bg="light green").place(x=80, y=100)
    cancel_btn = Button(frame5, text=" Cancel ", command=quiting, bg="red").place(x=180, y=100)
    frame5.pack()

def create_account():

    def quiting():
        os.remove('shrake1.png')
        os.remove('shrake2.png')
        root.quit()

    def info_saving():

        p1 = entry_4.get()
        p2 = entry_5.get()
        u1 = entry_3.get()
        c.execute("SELECT username FROM data WHERE username=?",(u1,))
        conn.commit()
        l = c.fetchall()
        if l==[]:

            if p1 == p2:

                if entry_3.get() is not "" and entry_4.get() is not '':
                    global add
                    if add!="":
                        uname_ = entry_3.get()
                        passwd_ = entry_4.get()

                        c.execute("INSERT INTO data VALUES(?,?,?)", (uname_, passwd_, add))
                        conn.commit()
                        text = Label(cr, text='                                                      ').place(x=90, y=210)
                        review = tkinter.messagebox.showinfo('Information', "Account Successfully Created.")
                        if review=='ok':
                            root.quit()
                    else:
                        text = Label(cr, text='        Folder not selected             ', fg='red').place(x=90, y=210)

                else:
                    text1 = Label(cr, text="      required fields are empty       ", fg='red').place(x=90, y=210)

            else:
                text = Label(cr, text='        password does not match         ', fg='red').place(x=90, y=210)

        else:
            text = Label(cr, text="       This username is not available...      ", fg='red').place(x=70, y=210)

    def address():
        global add
        add = tkinter.filedialog.askdirectory()

    frame2.destroy()
    cr = root
    cr.title("Create Account")
    cr.geometry("350x230+450+200")
    frame3 = Frame(cr)
    frame3.pack()
    frame4 = Frame(cr, width=350, height=250)
    frame4.pack()
    label_1 = Label(frame3, text='Creating Account', bg='light blue').pack(fill=X)
    logo_img = Label(frame4, image=img2).place(x=270, y=6)
    shrake_img = Label(frame4, image=img1).place(x=265, y=65)

    label_4 = Label(frame4, text='Username').place(x=30, y=10)
    label_5 = Label(frame4, text='Password ').place(x=30, y=40)
    label_6 = Label(frame4, text='Confirm ').place(x=30, y=70)

    entry_3 = Entry(frame4)
    entry_3.place(x=100, y=10)

    entry_4 = Entry(frame4)
    entry_4.place(x=100, y=40)

    entry_5 = Entry(frame4)
    entry_5.place(x=100, y=70)

    fol = Button(frame4, text="select folder", bg="light green", command=address)
    fol.place(x=125, y=100)
    chk_btn = Checkbutton(frame4, text="I Agree to \' Term and Condition \'")
    chk_btn.place(x=65, y=130)
    sign_up_btn = Button(frame4, text="sign up", command=info_saving, bg='light green')
    sign_up_btn.place(x=135, y=160)
    close_btn = Button(frame4, text=' Close ', command=quiting, bg='red')
    close_btn.place(x=250, y=160)

def change_password():

    def save_change_password():
        user_name = u_name.get()
        old_pass = old_1.get()
        new_pass = new_1.get()
        new_pass_c = new_2.get()


        c.execute("SELECT username,password FROM data WHERE username=?",(user_name,))
        conn.commit()
        rec = c.fetchone()
        if rec==None:
            msg = tkinter.messagebox.showwarning("Info","  Username not found.  ")
        else:

            if rec[1]==old_pass:
                if new_pass==new_pass_c:

                    c.execute("UPDATE data SET password=? WHERE username=?",(new_pass,user_name))
                    conn.commit()
                    msg1 = tkinter.messagebox.showwarning("Info","Password Changed Successfully")
                else:
                    msg = tkinter.messagebox.showwarning("Info","Password Does not match")

            else:
                msg1 = tkinter.messagebox.showwarning("Info","Incorrect Credential")

    global frame5,frame3
    frame2.destroy()
    frame5.destroy()
    frame3.destroy()
    root.geometry("350x170+450+200")
    frame3 = Frame(root, width=350, height=170)
    logo_img = Label(frame3, image=img2).place(x=270, y=6)
    shrake_img = Label(frame3, image=img1).place(x=265, y=65)

    save_btn = Button(frame3, text='    save    ', bg='light green',command=save_change_password).place(x=100, y=130)
    close_btn = Button(frame3, text="    close   ", bg="red", command=quiting ).place(x=200, y=130)
    text1 = Label(frame3, text="Username          : ").place(x=10, y=10)
    text2 = Label(frame3, text="Old Password      : ").place(x=10, y=40)
    text3 = Label(frame3, text="New Password      : ").place(x=10, y=70)
    text4 = Label(frame3, text="Re-type Password : ").place(x=10, y=100)

    u_name = Entry(frame3)
    u_name.place(x=115, y=10)
    old_1 = Entry(frame3)
    old_1.place(x=115, y=40)
    new_1 = Entry(frame3)
    new_1.place(x=115, y=70)
    new_2 = Entry(frame3)
    new_2.place(x=115, y=100)
    frame3.pack()

# explore("E:/shrake/shrake.exe")
root = Tk()

raw1 = """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"""

raw2 = """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"""

"""
raw1 and raw2 are encoded by base64
    raw = base64.b64encode(file)
decoded = base64.b64decode(raw)

"""


with open('shrake1.png', 'wb') as txt:
    txt.write(base64.b64decode(raw1))

with open('shrake2.png', 'wb') as txt:
    txt.write(base64.b64decode(raw2))

img1 = PhotoImage(file='shrake1.png')
img2 = PhotoImage(file='shrake2.png')
root.title("Shrake Authentication")
root.geometry("350x150+450+200")
root.tk.call('wm', 'iconphoto', root._w, img2)

frame1 = Frame(root)
frame2 = Frame(root, width=350, height=150)
frame3 = Frame(root, width=350, height=150)
frame5 = Frame(root, width=350, height=150)
mainMenu = Menu(frame1)
root.config(menu=mainMenu)

fileSubMenu = Menu(mainMenu)
mainMenu.add_cascade(label="File", menu=fileSubMenu)
fileSubMenu.add_command(label="New      Ctrl+N", command=donothing)
fileSubMenu.add_command(label="open     Ctrl+O", command=donothing)
fileSubMenu.add_command(label="Save      Ctrl+S", command=donothing)
fileSubMenu.add_command(label="save as", command=donothing)
fileSubMenu.add_separator()
fileSubMenu.add_command(label="Exit", command=root.quit)

editSubMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Edit", menu=editSubMenu)
editSubMenu.add_command(label="change password", command=change_password)
editSubMenu.add_command(label="change folder  ", command=change_folder)

helpMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="twitter", command=donothing)
helpMenu.add_command(label="Update License", command=donothing)
helpMenu.add_command(label="Check for Update..", command=donothing)
helpMenu.add_command(label="About", command=about)
frame1.pack()

logo_img = Label(frame2, image=img2).place(x=270, y=6)
shrake_img = Label(frame2, image=img1).place(x=265, y=65)

text1 = Label(frame2, text="Username : ").place(x=30, y=10)
text2 = Label(frame2, text="Password  : ").place(x=30, y=40)
uname = Entry(frame2)
uname.place(x=95, y=10)
passwd = Entry(frame2)
passwd.place(x=95, y=40)


check_btn = Checkbutton(frame2, text="Keep me logged in.").place(x=60, y=70)
login_btn = Button(frame2, text=" Login ", command=redirect, bg="light green").place(x=80, y=100)
cancel_btn = Button(frame2, text=" Cancel", command=quiting, bg="red").place(x=180, y=100)
signup_btn = Button(frame2, text="Sign up", command=create_account, bg='light blue')
signup_btn.place(x=280, y=100)

frame2.pack()

root.mainloop()

conn.close()
