

from customtkinter import *
import os

def self_system_information():
    os.system(r'"C:\Program Files\SystemInformer\SystemInformer.exe"')
def self_system_everything():
    os.system(r'"C:\Program Files\Everything\Everything.exe"')

def self_system_scan():
    os.system(r'"C:\Users\User\Downloads\HorionInjector.exe"')
    os.system(r'"C:\Users\User\Downloads\Kionclicker.exe"')
    print('if the cheat was found it will be opened')
app=CTk(fg_color='purple')
app.geometry('500x500')
app.resizable(False,False)
app.title('Shironium')
frame = CTkScrollableFrame(master=app , fg_color = 'orange',border_color='orange',border_width=2,scrollbar_button_color='purple',width=200,height=500)
frame.pack(anchor='center',expand=True,padx=20,pady=200)
frame.place(relx=0.2,rely=0.5,anchor='center')

sysinformer = CTkButton(master=frame,fg_color='Purple',border_width=2,text='Process Hacker',command=self_system_information)
sysinformer.pack(anchor='n',expand=True,padx=20,pady=20)

everything_app = CTkButton(master=frame,fg_color='Purple',border_width=2,text='Everything',command=self_system_everything)
everything_app.pack(anchor='center',expand=True,padx=20,pady=20)

scan_user = CTkButton(master=frame,fg_color='purple',border_width=2,text='Scan User',command=self_system_scan)
scan_user.pack(anchor='center',expand=True,padx=20,pady=20)
app.mainloop()