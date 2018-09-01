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
uname=""
passwd=""

root = Tk()

frame1 = Frame(root)
frame2 = Frame(root, width=400, height=200, bg="grey40")
frame3 = Frame(root, width=400, height=200, bg="grey40")
frame5 = Frame(root, width=400, height=200, bg="grey40")
frame4 = Frame(root, width=400, height=200, bg="grey40")
frame6 = Frame(root, width=400, height=20, bg="grey60")
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

def login():
    global frame2, frame3, frame4, frame5, frame6, uname, passwd
    frame2.destroy()
    frame3.destroy()
    frame4.destroy()
    frame5.destroy()
    frame6.destroy()
    root.geometry("400x200+450+200")
    root.overrideredirect(True)
    frame2 = Frame(root, width=400, height=200, bg="grey40")

    heading = Label(frame2, text="Shrake Authentication", font=("consolas",18,"bold"), bg="grey40", fg="cyan").place(x=60, y=10)
    logo_img = Label(frame2, image=img, bg="grey40").place(x=290, y=50)
    setting_icon = Button(frame2, image=icon, border=0, command=setting, activebackground="grey40", bg="grey40").place(x=10, y=165)

    text1 = Label(frame2, text="Username : ", bg="grey40", fg="white").place(x=30, y=70)
    text2 = Label(frame2, text="Password  : ", bg="grey40", fg="white").place(x=30, y=100)
    uname = Entry(frame2, bg='grey90', width=25, font=("consolas",10,"bold"))
    uname.place(x=95, y=70)
    passwd = Entry(frame2, bg="grey90",show="\u2022", width=25, font=("consolas",10,"bold"))
    passwd.place(x=95, y=100)

    btn_design = Canvas(frame2, width=51, height=24).place(x=59, y=149)
    btn_design = Canvas(frame2, width=51, height=24).place(x=173, y=149)
    btn_design = Canvas(frame2, width=51, height=24).place(x=288, y=149)

    signup_btn = Button(frame2, text="Sign up", border=0, padx=4, pady=3, bg="grey40", fg="white", command=create_account).place(x=60, y=150)
    login_btn = Button(frame2, text="  Login ", border=0, padx=4, pady=3, command=redirect, bg="grey40", fg="white", font=("",9,"bold")).place(x=174, y=150)
    cancel_btn = Button(frame2, text=" Cancel ", border=0, padx=3, pady=3, command=quiting, bg="grey40", fg="white").place(x=289, y=150)

    frame2.pack()


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
        msg1 = tkinter.messagebox.showwarning("Info","Incorrect Credentials\n\nTry Again..")

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
    os.remove('shrake.png')
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
                change_folder()
            else:
                msg = tkinter.messagebox.showerror("Info", "Folder not selected")

        else:
            msg = tkinter.messagebox.showerror("Info", "Incorrect credential!")

    pass_btn = Button(frame6, text="Change Password",activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey60", command=change_password, border=0, padx=20).place(x=0, y=0)
    fold_btn = Button(frame6, text="Change Folder", activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey50", command=change_folder, border=0, padx=30).place(x=140, y=0)

    global frame3, frame4, frame5
    frame2.destroy()
    frame3.destroy()
    frame4.destroy()
    frame5.destroy()
    root.geometry("400x200+450+200")
    # root.overrideredirect(False)
    frame5 = Frame(root, width=400, height=200, bg="grey40")
    logo_img = Label(frame5, image=img, bg="grey40").place(x=290, y=10)

    text1 = Label(frame5, text="Username : ", bg="grey40", fg="white").place(x=30, y=30)
    text2 = Label(frame5, text="Password  : ", bg="grey40", fg="white").place(x=30, y=60)

    uname = Entry(frame5, width=25, bg="grey90", font=("consolas",10,"bold"))
    uname.place(x=95, y=30)
    passwd = Entry(frame5, width=25,show="\u2022", bg="grey90", font=("consolas",10,"bold"))
    passwd.place(x=95, y=60)

    btn_design = Canvas(frame5, width=75, height=24).place(x=139, y=89)
    btn_design = Canvas(frame5, width=55, height=24).place(x=99, y=129)
    btn_design = Canvas(frame5, width=52, height=24).place(x=199, y=129)

    add_btn = Button(frame5, text="select folder", border=0, command=select_folder, bg="grey40", fg="white",padx=4, pady=3).place(x=140, y=90)
    change_btn = Button(frame5, text=" Change  ", border=0, command=changefolder, bg="grey40", fg="white", padx=1, pady=3).place(x=100, y=130)
    cancel_btn = Button(frame5, text=" Cancel  ", border=0, command=quiting, bg="grey40", fg="white", padx=2, pady=3).place(x=200, y=130)
    frame5.pack()

def create_account():

    def quiting():
        os.remove('shrake.png')
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
                        text = Label(cr, text=' ', bg="grey40", padx=200).place(x=100, y=210)
                        review = tkinter.messagebox.showinfo('Information', "Account Successfully Created.")
                        if review=='ok':
                            login()
                    else:
                        text = Label(cr, text='* Folder not selected', fg='cyan', bg="grey40", padx=40).place(x=90, y=210)

                else:
                    text1 = Label(cr, text="* required fields are empty", fg='cyan', bg="grey40", padx=40).place(x=90, y=210)

            else:
                text = Label(cr, text='* password does not match', fg='cyan', bg="grey40", padx=40).place(x=90, y=210)

        else:
            text = Label(cr, text="* This username is not available...", fg='cyan', bg="grey40", padx=40).place(x=90, y=210)

    def address():
        global add
        add = tkinter.filedialog.askdirectory()

    global frame3, frame4
    frame2.destroy()
    cr = root
    cr.title("Create Account")
    cr.geometry("400x230+450+200")
    cr.overrideredirect(False)
    frame3 = Frame(cr)
    frame3.pack()
    frame4 = Frame(cr, width=400, height=250, bg="grey40")
    frame4.pack()

    label_1 = Label(frame3, text='Creating Account', font=("",10,"bold"), padx=200, bg='grey60').pack(fill=X)
    logo_img = Label(frame4, image=img, bg="grey40").place(x=290, y=30)

    label_4 = Label(frame4, text='Username', bg="grey40", fg="white").place(x=30, y=10)
    label_5 = Label(frame4, text='Password ', bg="grey40", fg="white").place(x=30, y=40)
    label_6 = Label(frame4, text='Confirm ', bg="grey40", fg="white").place(x=30, y=70)

    entry_3 = Entry(frame4, bg="grey90", width=25, font=("consolas",10,"bold","italic"))
    entry_3.place(x=100, y=10)

    entry_4 = Entry(frame4, bg="grey90",show="\u2022", width=25, font=("consolas",10,"bold","italic"))
    entry_4.place(x=100, y=40)

    entry_5 = Entry(frame4, bg="grey90",show="\u2022", width=25, font=("consolas",10,"bold","italic"))
    entry_5.place(x=100, y=70)

    btn_design = Canvas(frame4, width=75, height=24).place(x=154, y=99)
    btn_design = Canvas(frame4, width=51, height=24).place(x=166, y=159)
    btn_design = Canvas(frame4, width=51, height=24).place(x=269, y=159)


    fol = Button(frame4, text="select folder", border=0, padx=4, pady=3, bg="grey40", fg="white", command=address)
    fol.place(x=155, y=100)
    chk_btn = Checkbutton(frame4,bg="grey40", fg="cyan", text="I Agree to \' Term and Condition \'")
    chk_btn.place(x=85, y=130)
    sign_up_btn = Button(frame4, text="sign up ", font=("",9,"bold"), border=0, padx=2, pady=3, command=info_saving, bg='grey40', fg="white")
    sign_up_btn.place(x=167, y=160)
    close_btn = Button(frame4, text=' Close  ', border=0, padx=5, pady=3, command=quiting, bg='grey40', fg="white")
    close_btn.place(x=270, y=160)

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
                    change_password()
                else:
                    msg = tkinter.messagebox.showwarning("Info","Password Does not match")

            else:
                msg1 = tkinter.messagebox.showwarning("Info","Incorrect Credential")

    pass_btn = Button(frame6, text="Change Password",activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey50", command=change_password, border=0, padx=20).place(x=0, y=0)
    fold_btn = Button(frame6, text="Change Folder", activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey60", command=change_folder, border=0, padx=30).place(x=140, y=0)

    global frame5,frame3
    frame2.destroy()
    frame5.destroy()
    frame4.destroy()
    frame3.destroy()
    root.geometry("400x200+450+200")
    # root.overrideredirect(False)
    frame3 = Frame(root, width=400, height=180, bg="grey40")
    logo_img = Label(frame3, image=img, bg="grey40").place(x=290, y=10)

    btn_design = Canvas(frame3, width=51, height=24).place(x=119, y=129)
    btn_design = Canvas(frame3, width=51, height=24).place(x=219, y=129)

    save_btn = Button(frame3, text='   save  ', font=("",9,"bold"), bg="grey40", fg="white", border=0, padx=3, pady=3,command=save_change_password).place(x=120, y=130)
    close_btn = Button(frame3, text="    close   ", bg="grey40", fg="white", border=0, padx=0, pady=3, command=quiting ).place(x=220, y=130)

    text1 = Label(frame3, bg="grey40", fg="white", text="Username          : ").place(x=10, y=10)
    text2 = Label(frame3, bg="grey40", fg="white", text="Old Password      : ").place(x=10, y=40)
    text3 = Label(frame3, bg="grey40", fg="white", text="New Password      : ").place(x=10, y=70)
    text4 = Label(frame3, bg="grey40", fg="white", text="Re-type Password : ").place(x=10, y=100)

    u_name = Entry(frame3, width=23, bg="grey90", font=("consolas",10,"bold","italic"))
    u_name.place(x=115, y=10)
    old_1 = Entry(frame3, width=23,show="\u2022", bg="grey90", font=("consolas",10,"bold","italic"))
    old_1.place(x=115, y=40)
    new_1 = Entry(frame3, width=23,show="\u2022", bg="grey90", font=("consolas",10,"bold","italic"))
    new_1.place(x=115, y=70)
    new_2 = Entry(frame3, width=23,show="\u2022", bg="grey90", font=("consolas",10,"bold","italic"))
    new_2.place(x=115, y=100)
    frame3.pack()

def setting():
    global frame2, frame3, frame4, frame5, frame6
    frame2.destroy()
    frame3.destroy()
    frame4.destroy()
    frame5.destroy()
    root.title("Setting")
    root.geometry("400x200+450+200")
    root.overrideredirect(False)
    frame6 = Frame(root, width=400, height=20, bg="grey60")

    pass_btn = Button(frame6, text="Change Password",activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey60", command=change_password, border=0, padx=20).place(x=0, y=0)
    fold_btn = Button(frame6, text="Change Folder", activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey60", command=change_folder, border=0, padx=30).place(x=140, y=0)
    login_btn = Button(frame6, text="Login", activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey60", command=login, border=0,padx=30).place(x=310, y=0)
    frame6.pack()
    change_password()
    pass_btn = Button(frame6, text="Change Password",activebackground="grey70", font=("",8,"bold"), fg="white", bg="grey50", command=change_password, border=0, padx=20).place(x=0, y=0)

# explore("E:/shrake/shrake.exe")


ico = """iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAFZklEQVR4nI2WTWxc1RXHf+e++96MPzOJYxsp/oit1A6G4Lj52jUKdqR2X1yBQGqcFjZVDOqCVBWNmk0jpJZUors0qdSSKmGBuqyI40ZdQRPAER+KkYzjAbW2YzBTZzzz3rv3dDGesU0+ypHu5p17z1/n/M//nCf8HxucfCsXaPmQerdfjOlQ9XUiZhXIg7/hJH5n6six5YfFkAcH/+vOwPnjYs0PVemRwGTEGFRBBNR71PmyCJ/h9c20XD4/9YNjs98aZO/kGz8JJHhFQtulzqHOg+p9XgsSGCQIcEkyp96d/uDJZ//4UJCBDy9Hmfn0VWPNOGLQNN10OVVPqooVwYrZHMha8B7v3Nlye/jyx4+PxlXf+s1Tp0xmPn7VZMJxVe4BcOp5tGkbozu+w+6mrTj1m/yapigQZKIXswvJGVRrCdRA9h7efcxYe0KTFLxHUWLvSbwnVY9T5YWePZzafYjnd+4hVSVVT+wrR9FKJkmKmODFoasXf7wJZN8/L3cZ9NeICKqoKpEJGOse4EhrB9ujOp7p7Ofg1nYADm19hKc7+tke1THc1sFY9wCRCVDVCndGRERO73v7cheABdBy8lNTl9nhy5UyJup5bsejvLRriFQ9y0nM9ihbK02jDfll/wFe6HmcXJip8XP+9kdEEqCpw2SiDhenx4FTdnDyQg5lVFO3oRuEuWKB2HsiY9geZZktFphYzLNQWqUtW89wawc765sBiL1jtlio9HaVI+fAuR8NvnXhNRtodEhVevDrRIrAzcIS/03LtER1/H3hNmemr7NQWkVRBOGN/Cf8ou8AR9u6KKQxHxaW2Nhv6jwIvbbZHjTAPhPasKoDp0qqykhbJy1RHZ/dLXDm1nWW4hLZIKAusGSDgDvlVX5z6zqzxUKFm9ZOnCquqidVTBiGaoJ9BpUuTCXNVJW+xhy/f+J7nOjdC8DEYp75cpHwG7oITcB8+S4Ti3kAxnft5ewTh+lrzJFWgYyA1y6jaJa1b6l6BppbGGntosGGAMyXizzIFPhPqeJvCEJGWjsZaG4hrWpIQaHOCFKq6t6K4ZPCElcX8xRdRYxtmfoHggA8sua/6xImFvN8XFhanwYCAqsGkTm8roEIt1aWOXHzGq/PfADAcGsHbZk6km8oPFFPe6aeJ1s7AfjDzBTjN68xvbKMrXaZV0DmDPgbPkmTavsFIgQivL2QZyku0duwhZN9B9gWZll1ae1sC7O83L+fnoZmvoxLXFnI195WshB8kiSiXLdO4ncMmRkxpl+dq9V6oGkbTWu8fL+9m77GHFcW8szHRdoz9Yy0dtLbsAWARhvxWFNLhZ8qRmBQ9TN4+66dOnJseejqxctig1dqIKrsrG8mMkFN8b0NW3i+Z8umkt2JS+TCiMgYuhqa0cX1dSBBAIm7dOPo6NcWwIT2nC+Xx8TaHZo6QjFc+mIagNligY8KS4y0dfGz3kEabchKmvD6zBRXFuZ4rLmFnfXNXPpiutbmYgNcKf48sHJujf+KDU38ecwE4TlVrQxJlMQrUikvTpWzew4z0tbJxGKe8ZvXCCrzFAVCIwhSWWTGePX++HtHnv7TJhBU5buTF39rouglnzo2jhmogOxqzNHfmGN6ZZlPV5bXSa6aMRgb4Evxa+8NP/NzRBQ2Li0RLd0JT7rV+KzI2qbbYIEIn658xd/+PcP0ylf3AIi1CODLye9KX4YnqwCbM9lgQ/+4OCaYX5nQdn/bHe+T9LYmyen3jz53/p5r9wMBGJr4S7fBjmH8U4r03v9vxZVFmUF50+PPvz/87O37xXogSNUGJy/krM8eVPH7FelAtR6Ronj93CP/CtS+e+Po6NcPi/E/sTyKu04dnJAAAAAASUVORK5CYII="""


raw = """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"""

"""
raw1 and raw2 are encoded by base64
    raw = base64.b64encode(file)
decoded = base64.b64decode(raw)

"""


with open('shrake.png', 'wb') as txt:
    txt.write(base64.b64decode(raw))

with open('setting.png', "wb") as txt:
    txt.write(base64.b64decode(ico))

img = PhotoImage(file='shrake.png')
icon = PhotoImage(file='setting.png')

root.title("Shrake Authentication")
root.geometry("400x200+450+200")
root.overrideredirect(True)
root.tk.call('wm', 'iconphoto', root._w, img)


login()

root.mainloop()

conn.close()
