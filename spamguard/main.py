import time
from threading import Thread
from email_handler import process_emails
from gui import launch_gui

def start_email_loop():
    while True:
        process_emails()
        time.sleep(60)

def main():
    # Start GUI once
    Thread(target=launch_gui, daemon=True).start()

    # Start email checking loop (separate thread optional)
    start_email_loop()

if __name__ == "__main__":
    main()
