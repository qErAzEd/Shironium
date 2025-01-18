import customtkinter as ctk
import threading
import time
import random
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode, Key

clicking = False
min_cps = 14
max_cps = 16
toggle_key = KeyCode.from_char('k')

mouse = Controller()

def click_mouse():
    global clicking, min_cps, max_cps
    while True:
        if clicking:
            cps = random.randint(min_cps, max_cps)
            mouse.click(Button.left)
            time.sleep(1 / cps)
        else:
            time.sleep(0.1)

def toggle_clicking():
    global clicking
    clicking = not clicking

def on_press(key):
    global toggle_key
    if key == toggle_key:
        toggle_clicking()

def update_key_binding():
    global toggle_key
    key_string = key_entry.get().lower()

    if key_string.startswith('f') and key_string[1:].isdigit():
        try:
            f_key_number = int(key_string[1:])
            if 1 <= f_key_number <= 12:
                toggle_key = getattr(Key, f"f{f_key_number}")
        except ValueError:
            pass
    elif len(key_string) == 1:
        toggle_key = KeyCode.from_char(key_string)
    else:
        try:
            toggle_key = getattr(Key, key_string.upper())
        except AttributeError:
            pass

    key_label.configure(text=f"Toggle Key: {toggle_key.char.upper() if hasattr(toggle_key, 'char') else toggle_key.name.capitalize()}")

def switch_to_dark_mode():
    ctk.set_appearance_mode("dark")

def switch_to_light_mode():
    ctk.set_appearance_mode("light")

ctk.set_appearance_mode("system")  # Default mode is system mode (can be dark or light based on system settings)
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Shironium")

min_cps_label = ctk.CTkLabel(root, text="Min CPS:")
min_cps_label.grid(row=0, column=0, padx=10, pady=5)
min_cps_slider = ctk.CTkSlider(root, from_=1, to=30, command=lambda value: update_min_cps(value))
min_cps_slider.set(min_cps)
min_cps_slider.grid(row=0, column=1, padx=10, pady=5)

min_cps_display_label = ctk.CTkLabel(root, text=str(min_cps))
min_cps_display_label.grid(row=0, column=2, padx=10, pady=5)

max_cps_label = ctk.CTkLabel(root, text="Max CPS:")
max_cps_label.grid(row=1, column=0, padx=10, pady=5)
max_cps_slider = ctk.CTkSlider(root, from_=1, to=30, command=lambda value: update_max_cps(value))
max_cps_slider.set(max_cps)
max_cps_slider.grid(row=1, column=1, padx=10, pady=5)

max_cps_display_label = ctk.CTkLabel(root, text=str(max_cps))
max_cps_display_label.grid(row=1, column=2, padx=10, pady=5)

key_label = ctk.CTkLabel(root, text=f"Toggle Key: {toggle_key.char.upper() if hasattr(toggle_key, 'char') else toggle_key.name.capitalize()}")
key_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

key_entry_label = ctk.CTkLabel(root, text="Bind Toggle Key:")
key_entry_label.grid(row=3, column=0, padx=10, pady=5)
key_entry = ctk.CTkEntry(root)
key_entry.insert(0, toggle_key.char if hasattr(toggle_key, 'char') else toggle_key.name)
key_entry.grid(row=3, column=1, padx=10, pady=5)
key_binding_button = ctk.CTkButton(root, text="Update Key Binding", command=update_key_binding)
key_binding_button.grid(row=3, column=2, padx=10, pady=5)

click_thread = threading.Thread(target=click_mouse, daemon=True)
click_thread.start()

keyboard_listener = Listener(on_press=on_press)
keyboard_listener.start()

def update_min_cps(value):
    global min_cps
    min_cps = int(float(value))
    min_cps_display_label.configure(text=str(min_cps))

def update_max_cps(value):
    global max_cps
    max_cps = int(float(value))
    max_cps_display_label.configure(text=str(max_cps))

def update_gui():
    root.after(100, update_gui)

update_gui()

dark_mode_button = ctk.CTkButton(root, text="Dark Mode", command=switch_to_dark_mode)
dark_mode_button.grid(row=4, column=0, padx=10, pady=5)

light_mode_button = ctk.CTkButton(root, text="Light Mode", command=switch_to_light_mode)
light_mode_button.grid(row=4, column=1, padx=10, pady=5)

root.mainloop()
