import schedule
import time
import threading
from plyer import notification
import tkinter as tk
from tkinter import simpledialog, messagebox
import pystray
from PIL import Image, ImageDraw
import os

def send_reminder(message):
    notification.notify(
        title="Reminder!",
        message=message,
        app_name="Python Reminder",
        timeout=10
    )
    print(f"Reminder sent: '{message}'")

def open_tk_dialog():
    root = tk.Tk()
    root.withdraw()

    message = simpledialog.askstring("New Reminder", "What would you like to be reminded of?", parent=root)
    if not message:
        root.destroy()
        return

    interval = simpledialog.askfloat("New Reminder", "In how many minutes?", parent=root)
    if not interval:
        root.destroy()
        return

    schedule.every(interval).minutes.do(send_reminder, message=message)
    messagebox.showinfo("Reminder Set", f"Reminding you to '{message}' every {interval} minutes.")
    root.destroy()

def schedule_reminder(icon=None, item=None):
    # run Tkinter dialogs on the main thread
    threading.Thread(target=open_tk_dialog).start()

def create_image():
    img = Image.new('RGB', (64, 64), color=(0, 128, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return img

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray():
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem("New Reminder", schedule_reminder),
        pystray.MenuItem("Quit", on_quit)
    )
    icon = pystray.Icon("Reminder", image, "Python Reminder", menu)
    # Run the icon in a background thread
    icon.run_detached()
    # Run the scheduler on the main thread
    run_scheduler()

if __name__ == "__main__":
    setup_tray()
