import tkinter as tk
from tkinter import ttk

# Lists that will be updated from your email_handler.py
routed_mails = []
blocked_spams = []

# Functions to show routed and spam mails
def show_routed_mails():
    content_text.config(state="normal")
    content_text.delete("1.0", tk.END)
    content_text.insert(tk.END, "📨 Routed Mails:\n\n")
    if routed_mails:
        for mail in routed_mails:
            content_text.insert(tk.END, f"- {mail}\n\n")
    else:
        content_text.insert(tk.END, "No routed mails yet.\n")
    content_text.config(state="disabled")

def show_blocked_spams():
    content_text.config(state="normal")
    content_text.delete("1.0", tk.END)
    content_text.insert(tk.END, "🚫 Blocked Spam Mails:\n\n")
    if blocked_spams:
        for mail in blocked_spams:
            content_text.insert(tk.END, f"- {mail}\n\n")
    else:
        content_text.insert(tk.END, "No blocked spams yet.\n")
    content_text.config(state="disabled")

def launch_gui():
    global content_text

    # Main window
    root = tk.Tk()
    root.title("📬 SpamGuard Dashboard")
    root.geometry("850x500")
    root.configure(bg="#f0f2f5")
    root.resizable(False, False)

    # Sidebar frame
    sidebar = tk.Frame(root, bg="#2c3e50", width=200)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="SpamGuard", bg="#2c3e50", fg="white", font=("Helvetica", 20, "bold")).pack(pady=30)

    ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=5)

    # Buttons
    tk.Button(sidebar, text="📨 Routed Mails", command=show_routed_mails, width=20, font=("Arial", 12), bg="#3498db", fg="white", relief="flat").pack(pady=20)
    tk.Button(sidebar, text="🚫 Blocked Spams", command=show_blocked_spams, width=20, font=("Arial", 12), bg="#e74c3c", fg="white", relief="flat").pack(pady=10)

    # Main content area
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    content_text = tk.Text(content_frame, wrap="word", font=("Arial", 13), state="disabled", bg="#ecf0f1", fg="#2c3e50")
    content_text.pack(expand=True, fill="both", padx=20, pady=20)

    # Set window size and position
    # Format: "widthxheight+x_offset+y_offset"

    root.geometry("500x430+230+350")  # Width x Height + X + Y


    root.mainloop()
