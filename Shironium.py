#updated ver 1.1
import os
import tkinter as tk
from customtkinter import *

# Function to open System Informer
def open_system_informer():
    try:
        os.system(r'"C:\Program Files\SystemInformer\SystemInformer.exe"')
    except Exception as e:
        print(f"Error opening SystemInformer: {e}")

# Function to open Everything search tool
def open_everything():
    try:
        os.system(r'"C:\Program Files\Everything\Everything.exe"')
    except Exception as e:
        print(f"Error opening Everything: {e}")

# Function to execute scans
def perform_system_scan():
    try:
        os.system(r'"C:\Users\User\Downloads\HorionInjector.exe"')
        os.system(r'"C:\Users\User\Downloads\Kionclicker.exe"')
        print('If the cheat was found, it will be opened.')
    except Exception as e:
        print(f"Error performing system scan: {e}")

# Main application setup
app = CTk(fg_color='purple')
app.geometry('500x500')
app.resizable(False, False)
app.title('Shironium')

# Scrollable frame to hold the buttons
frame = CTkScrollableFrame(master=app, fg_color='orange', border_color='orange', border_width=2, 
                           scrollbar_button_color='purple', width=200, height=500)
frame.pack(anchor='center', expand=True, padx=20, pady=200)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Buttons for each functionality
sysinformer_btn = CTkButton(master=frame, fg_color='purple', border_width=2, text='Process Hacker', 
                             command=open_system_informer)
sysinformer_btn.pack(anchor='n', expand=True, padx=20, pady=20)

everything_btn = CTkButton(master=frame, fg_color='purple', border_width=2, text='Everything', 
                            command=open_everything)
everything_btn.pack(anchor='center', expand=True, padx=20, pady=20)

scan_user_btn = CTkButton(master=frame, fg_color='purple', border_width=2, text='Scan User', 
                           command=perform_system_scan)
scan_user_btn.pack(anchor='center', expand=True, padx=20, pady=20)

# Start the app
app.mainloop()
