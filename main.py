import os
import json
import time
import keyboard
import pyautogui
import win32api
import win32con
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading

# Function to handle clicking
def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)

# Function to look for images
def look_for_image(image_path):
    try:
        start = pyautogui.locateCenterOnScreen(image_path, grayscale=True, confidence=0.60)
        if start is not None:
            message_label.config(text=f'{image_path} image found, clicking')
            pyautogui.moveTo(start)  # Moves the mouse to the coordinates of the image
            click()
    except Exception:
        message_label.config(text=f'no {image_path} image found, sleeping')

# Function to add more images via file explorer
def add_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        images_listbox.insert(tk.END, file_path)
        save_images()

# Function to save added images to a file
def save_images():
    with open("saved_images.json", "w") as f:
        json.dump(images_listbox.get(0, tk.END), f)

# Function to load saved images from file
def load_images():
    if os.path.exists("saved_images.json"):
        with open("saved_images.json", "r") as f:
            data = json.load(f)
            for item in data:
                images_listbox.insert(tk.END, item)

# Function to clear saved images
def clear_images():
    images_listbox.delete(0, tk.END)
    save_images()

# Function to start looking for images
def start_looking():
    global looking_thread
    if looking_thread:
        return  # Cancel the previous thread if it exists
    looking_thread = threading.Thread(target=continuous_image_search)
    looking_thread.start()

# Function to continuously look for images
def continuous_image_search():
    while not keyboard.is_pressed('q'):
        for item in images_listbox.get(0, tk.END):
            look_for_image(item)
            time.sleep(click_time_slider.get())  # Adjust this delay according to your needs

# Create Tkinter window
root = tk.Tk()
root.title("Ryan's Auto Clicker")

# Label to display messages
message_label = tk.Label(root, text="", wraplength=500)
message_label.pack()

# Button to add images
add_button = tk.Button(root, text="Add Image", command=add_image)
add_button.pack()

# Listbox to display added images
images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100, height=15)
images_listbox.pack()

# Load saved images
load_images()

# Start button to initiate searching for images
start_button = tk.Button(root, text="Start Looking", command=start_looking)
start_button.pack()

# Button to clear saved images
clear_button = tk.Button(root, text="Clear Images", command=clear_images)
clear_button.pack()

# Button to exit window
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

# Slider to adjust click time
click_time_label = tk.Label(root, text="Click time: 0 seconds")
click_time_label.pack()

def update_click_time_label(event):
    click_time_label.config(text=f"Click time: Every {click_time_slider.get()} seconds")

click_time_slider = tk.Scale(root, from_=0.1, to=5, resolution=0.1, orient=tk.HORIZONTAL, command=update_click_time_label)
click_time_slider.set(2.5)  # Initial value
click_time_slider.pack()

# Main loop
looking_thread = None
root.mainloop()
