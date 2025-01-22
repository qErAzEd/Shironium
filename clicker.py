import customtkinter as ctk
import threading
import time
import random
import json
import os
import sys
import logging
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode, Key
from tkinter import filedialog, messagebox, Label
from PIL import Image, ImageTk

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if getattr(sys, 'frozen', False):
    config_file_path = os.path.join(os.path.dirname(sys.executable), "config.json")
else:
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

key_binding_active = False  # Додано визначення змінної

def load_config():
    global min_cps, max_cps, toggle_key, appearance_mode, background_image_path, theme
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, "r") as file:
                settings = json.load(file)
                min_cps = settings.get("min_cps", 14)
                max_cps = settings.get("max_cps", 14)
                toggle_key_str = settings.get("toggle_key", "f6")
                if toggle_key_str:
                    toggle_key = KeyCode.from_char(toggle_key_str.lower()) if len(toggle_key_str) == 1 else getattr(Key, toggle_key_str.lower())
                else:
                    toggle_key = KeyCode.from_char("f6")
                appearance_mode = settings.get("appearance_mode", "dark")
                theme = settings.get("theme", "white")  # Loading theme from config
                background_image_path = settings.get("background_image", "")
        except json.JSONDecodeError:
            set_default_settings()
    else:
        set_default_settings()

def set_default_settings():
    global min_cps, max_cps, toggle_key, appearance_mode, background_image_path, theme
    min_cps = 14
    max_cps = 14
    toggle_key = KeyCode.from_char("f6")
    appearance_mode = "dark"
    theme = "white"  # Default theme is white
    background_image_path = ""

def save_config():
    settings = {
        "min_cps": min_cps,
        "max_cps": max_cps,
        "toggle_key": toggle_key.char if hasattr(toggle_key, 'char') else toggle_key.name,
        "appearance_mode": ctk.get_appearance_mode(),
        "theme": theme,  # Saving the theme in config
        "background_image": background_image_path
    }
    with open(config_file_path, "w") as file:
        json.dump(settings, file, indent=4)

def click_mouse():
    global clicking, min_cps, max_cps
    mouse = Controller()
    while True:
        if clicking:
            if min_cps > max_cps:
                min_cps, max_cps = max_cps, min_cps
            cps = random.uniform(min_cps, max_cps)
            mouse.click(Button.left)
            delay_variation = random.uniform(0.85, 1.15)
            time.sleep(1 / cps * delay_variation)
        else:
            time.sleep(0.1)

def toggle_clicking():
    global clicking
    clicking = not clicking
    logging.info(f"Clicking toggled to {'ON' if clicking else 'OFF'}")

def on_press(key):
    global toggle_key
    if key == toggle_key:
        toggle_clicking()

def show_error_popup():
    messagebox.showerror("Invalid CPS Values", "Min CPS cannot be greater than Max CPS!")


key_binding_active = False  # Глобальна змінна

def update_key_binding():
    global key_binding_active

    key_binding_active = True  # Встановлюємо значення на True перед запуском Listener

    def on_key_press(key):
        global toggle_key, keyboard_listener
        if hasattr(key, 'char') and key.char:
            toggle_key = KeyCode.from_char(key.char.lower())
        else:
            toggle_key = key
        key_label.config(text=f"Toggle Key: {toggle_key.char.upper() if hasattr(toggle_key, 'char') else toggle_key.name.capitalize()}")
        key_binding_button.configure(text="Change Key Bind")
        save_config()
        logging.info(f"Key bind updated to {toggle_key}")

        if key_binding_active:
            keyboard_listener.stop()
            key_binding_active = False
            key_binding_button.configure(text="Change Key Bind")

    key_binding_button.configure(text="Press any key to change the bind")

    def reset_button_text():
        global key_binding_active
        if key_binding_button.cget("text") == "Press any key to change the bind":
            key_binding_button.configure(text="Change Key Bind")
            if key_binding_active:
                keyboard_listener.stop()
                key_binding_active = False

    root.after(3000, reset_button_text)

    keyboard_listener = Listener(on_press=on_key_press)
    keyboard_listener.start()




def set_background_image():
    global background_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        background_image_path = file_path
        save_config()
        load_background_image()

def load_background_image():
    global bg_image_cached
    if background_image_path:
        img = Image.open(background_image_path)
        
        window_width, window_height = root.winfo_width(), root.winfo_height()

        # Зберігаємо співвідношення сторін
        img_ratio = img.width / img.height
        window_ratio = window_width / window_height

        if window_ratio > img_ratio:
            new_height = window_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = window_width
            new_height = int(new_width / img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        bg_image_cached = ImageTk.PhotoImage(img)
        
        background_label.config(image=bg_image_cached)
        background_label.image = bg_image_cached

# Function to apply the theme based on config
# Функція для застосування теми на основі конфігурації
def apply_theme():
    global theme
    ctk.set_appearance_mode(appearance_mode)  # Застосування режиму зовнішнього вигляду (світлий, темний, системний)

    theme_config = {
        "black": {
            "bg_color": "black", "fg_color": "white",
            "button_fg": "blue", "button_hover": "lightblue", "button_text": "white"
        },
        "white": {
            "bg_color": "white", "fg_color": "black",
            "button_fg": "green", "button_hover": "lightgreen", "button_text": "black"
        },
        "default": {
            "bg_color": "white", "fg_color": "system",
            "button_fg": "system", "button_hover": "system", "button_text": "system"
        }
    }

    config = theme_config.get(theme, theme_config["default"])
    root.configure(bg=config["bg_color"])
    key_label.configure(bg=config["bg_color"], fg=config["fg_color"])
    key_binding_button.configure(fg_color=config["button_fg"], hover_color=config["button_hover"], text_color=config["button_text"])
    min_cps_label.configure(bg=config["bg_color"], fg=config["fg_color"])
    max_cps_label.configure(bg=config["bg_color"], fg=config["fg_color"])
    background_label.configure(bg=config["bg_color"])

# Ініціалізація вікна
root = ctk.CTk()
root.title("Shironium")
root.resizable(False, False)

# Перемикач теми
def toggle_theme():
    global theme
    theme = "black" if theme == "white" else "white"  # Перемикання між чорної та білої темами
    apply_theme()
    save_config()
    logging.info(f"Тему змінено на {theme}")

theme_toggle_button = ctk.CTkButton(root, text="Toggle Theme", command=toggle_theme)
theme_toggle_button.grid(row=5, column=0, columnspan=3, padx=15, pady=10)

background_label = Label(root, bg='white')  # Початковий колір фону
background_label.place(x=0, y=0, relwidth=1, relheight=1)

load_config()

# Позначки та слайдери для налаштувань CPS
def create_labeled_slider(row, text, value, command):
    label = Label(root, text=text, bg='white', fg='black', font=("Arial", 12))
    label.grid(row=row, column=0, padx=15, pady=10)
    slider = ctk.CTkSlider(root, from_=1, to=30, command=command)
    slider.set(value)
    slider.grid(row=row, column=1, padx=15, pady=10)
    display_label = Label(root, text=str(value), bg='white', fg='black', font=("Arial", 12))
    display_label.grid(row=row, column=2, padx=15, pady=10)
    return slider, display_label

min_cps_slider, min_cps_display_label = create_labeled_slider(0, "Min CPS:", min_cps, lambda value: update_cps(value, True))
max_cps_slider, max_cps_display_label = create_labeled_slider(1, "Max CPS:", max_cps, lambda value: update_cps(value, False))

key_label = Label(root, text=f"Toggle Key: {toggle_key.char.upper() if hasattr(toggle_key, 'char') else toggle_key.name.capitalize()}", bg='white', fg='black', font=("Arial", 14))
key_label.grid(row=2, column=0, columnspan=3, padx=15, pady=10)

key_binding_button = ctk.CTkButton(root, text="Change Key Bind", font=("Arial", 12), command=update_key_binding, width=200, height=30)
key_binding_button.grid(row=3, column=0, columnspan=3, padx=15, pady=10)

clicking = False

click_thread = threading.Thread(target=click_mouse, daemon=True)
click_thread.start()

keyboard_listener = Listener(on_press=on_press)
keyboard_listener.start()

def update_cps(value, is_min):
    global min_cps, max_cps
    if is_min:
        min_cps = int(float(value))
        min_cps_display_label.config(text=str(min_cps))
    else:
        max_cps = int(float(value))
        max_cps_display_label.config(text=str(max_cps))
    
    if min_cps > max_cps:
        show_error_popup()
        if is_min:
            min_cps = max_cps
        else:
            max_cps = min_cps
        min_cps_slider.set(min_cps)
        min_cps_display_label.config(text=str(min_cps))
        max_cps_slider.set(max_cps)
        max_cps_display_label.config(text=str(max_cps))

    save_config()

def update_gui():
    if root.winfo_exists():
        load_background_image()
        root.after(100, update_gui)

def on_close():
    save_config()
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_close)

update_gui()

background_button = ctk.CTkButton(root, text="Choose Background Image", command=set_background_image, font=("Arial", 12), width=200, height=30)
background_button.grid(row=4, column=0, columnspan=3, padx=15, pady=10)

previous_width, previous_height = root.winfo_width(), root.winfo_height()
bg_image_cached = None

load_background_image()

root.mainloop()

