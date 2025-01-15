#updated ver 1.7
import os
import glob
import psutil
from customtkinter import *

# Function to search for a file across the entire system
def find_file(file_name):
    search_paths = [
        r'C:\Users\User\Downloads',
        r'C:\Users\User\Documents',
        r'C:\Program Files',
        r'C:\Program Files (x86)',
        r'C:\Windows'
    ]
    
    for path in search_paths:
        result = glob.glob(os.path.join(path, '**', file_name), recursive=True)
        if result:
            return result[0]  # Return the first match if found
    return None

# Function to check if explorer.exe is running
def is_explorer_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'explorer.exe':
            return True
    return False

# Function to create a new trace file and log data
def create_trace_file():
    # Find the next available trace file number
    trace_number = 0
    while os.path.exists(f"Trace{trace_number}.txt"):
        trace_number += 1

    trace_filename = f"Trace{trace_number}.txt"
    
    # Open the file and write the header
    with open(trace_filename, 'w') as trace_file:
        trace_file.write(f"Trace Log - {trace_filename}\n")
        trace_file.write(f"Timestamp: {os.popen('date /T').read().strip()} {os.popen('time /T').read().strip()}\n\n")
    
    return trace_filename

# Function to log data to the trace file
def log_to_trace(trace_filename, message):
    with open(trace_filename, 'a') as trace_file:
        trace_file.write(f"{message}\n")

# Function to open System Informer
def open_system_informer():
    trace_filename = create_trace_file()  # Create new trace file
    try:
        if is_explorer_running():
            message = "explorer.exe is running."
            log_to_trace(trace_filename, message)
        os.system(r'"C:\Program Files\SystemInformer\SystemInformer.exe"')
        log_to_trace(trace_filename, 'SystemInformer.exe was opened.')
    except Exception as e:
        log_to_trace(trace_filename, f"Error opening SystemInformer: {e}")

# Function to open Everything search tool
def open_everything():
    trace_filename = create_trace_file()  # Create new trace file
    try:
        if is_explorer_running():
            message = "explorer.exe is running."
            log_to_trace(trace_filename, message)
        os.system(r'"C:\Program Files\Everything\Everything.exe"')
        log_to_trace(trace_filename, 'Everything.exe was opened.')
    except Exception as e:
        log_to_trace(trace_filename, f"Error opening Everything: {e}")

# Function to execute scans, searching for executables in any location
def perform_system_scan():
    trace_filename = create_trace_file()  # Create new trace file
    horion_path = find_file('HorionInjector.exe')
    kionclicker_path = find_file('Kionclicker.exe')
    borion_path = find_file('Borion.exe')
    
    # Log if explorer.exe is running
    if is_explorer_running():
        log_to_trace(trace_filename, "explorer.exe is running at the time of the scan.")

    # If found, open them
    if horion_path:
        os.system(f'"{horion_path}"')
        log_to_trace(trace_filename, 'HorionInjector.exe found and opened.')
    else:
        log_to_trace(trace_filename, 'HorionInjector.exe not found.')
    
    if kionclicker_path:
        os.system(f'"{kionclicker_path}"')
        log_to_trace(trace_filename, 'Kionclicker.exe found and opened.')
    else:
        log_to_trace(trace_filename, 'Kionclicker.exe not found.')

    if borion_path:
        os.system(f'"{borion_path}"')
        log_to_trace(trace_filename, 'Borion.exe found and opened.')
    else:
        log_to_trace(trace_filename, 'Borion.exe not found.')

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
