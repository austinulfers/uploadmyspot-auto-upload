from tkinter import *
from tkinter import ttk
import configparser

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini') 

def edit_config():
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini') 

    window = Toplevel(root)

    lbl_wix_user = Label(window, text="Wix Username")
    txt_wix_user = Entry(window, width=30)
    txt_wix_user.insert(END, config["CREDENTIALS"]["WIX_USERNAME"])
    lbl_wix_pass = Label(window, text="Wix Password")
    txt_wix_pass = Entry(window, width=30)
    txt_wix_pass.insert(END, config["CREDENTIALS"]["WIX_PASSWORD"])
    lbl_com_user = Label(window, text="Comcast Ad Delivery Username")
    txt_com_user = Entry(window, width=30)
    txt_com_user.insert(END, config["CREDENTIALS"]["COMCAST_USERNAME"])
    lbl_com_pass = Label(window, text="Comcast Ad Delivery Password")
    txt_com_pass = Entry(window, width=30)
    txt_com_pass.insert(END, config["CREDENTIALS"]["COMCAST_PASSWORD"])
   
    button = Button(
        window, 
        text="Save", 
        command=save_config(
            window, 
            txt_wix_user.get(), 
            txt_wix_pass.get(), 
            txt_com_user.get(), 
            txt_com_pass.get()
        )
    )

    lbl_wix_user.pack()
    txt_wix_user.pack()
    lbl_wix_pass.pack()
    txt_wix_pass.pack()
    lbl_com_user.pack()
    txt_com_user.pack()
    lbl_com_pass.pack()
    txt_com_pass.pack()
    button.pack()

def save_config(window, wix_u, wix_p, com_u, com_p):
    config.set("CREDENTIALS", "WIX_USERNAME", wix_u)
    config.set("CREDENTIALS", "WIX_PASSWORD", wix_p)
    config.set("CREDENTIALS", "COMCAST_USERNAME", com_u)
    config.set("CREDENTIALS", "COMCAST_PASSWORD", com_p)
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    Label(window, text="Save Successful").pack()


root = Tk()
menubar = Menu(root)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Credentials", command=edit_config)
editmenu.add_command(label="Preferences", command=None)
menubar.add_cascade(label="Edit", menu=editmenu)

root.config(menu=menubar)
root.mainloop()