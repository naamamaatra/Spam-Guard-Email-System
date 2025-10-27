🛡️ SpamGuard Email System

SpamGuard Email System is a Python-based desktop application that automates email classification and spam filtering in real time. It connects to a master Gmail account, scans incoming emails, routes them to respective departments, and blocks spam — all without using AI or databases.

🚀 Features

Automated Email Routing: Forwards emails to Support, Sales, or Technical departments using keyword-based logic.

Spam Detection: Blocks promotional or suspicious emails automatically.

Real-Time Monitoring: Fetches and processes emails every 60 seconds.

Lightweight Implementation: No AI or large datasets required.

Secure Access: Uses Gmail API with OAuth 2.0 authentication.

Interactive GUI: Built with Tkinter for live tracking of routed and spam emails.

🧠 System Overview

SpamGuard analyzes each unread email from a master Gmail account, checks for department-specific keywords, and forwards it to the appropriate department Gmail ID. Suspicious or spammy emails are flagged and blocked before reaching end users.

The system runs locally as a desktop app and ensures both efficiency and security through a lightweight, rule-based design.

🛠️ Tech Stack

Language: Python

GUI: Tkinter

Email Access: Gmail API (OAuth 2.0)

Libraries Used:

imaplib, smtplib, email, base64, tkinter, time, os

⚙️ Installation

Clone the repository:

git clone https://github.com/yourusername/SpamGuard-Email-System.git
cd SpamGuard-Email-System


Install dependencies:

pip install -r requirements.txt


Set up Gmail API credentials:

Create OAuth 2.0 credentials from Google Cloud Console.

Download credentials.json and place it in the project folder.

Enable the Gmail API for your account.

Run the application:

python spamguard.py

🖥️ GUI Interface

The Tkinter-based GUI displays:

Routed emails with timestamps

Blocked spam emails

Real-time updates every 60 seconds

🧩 Folder Structure
SpamGuard-Email-System/
│
├── spamguard.py
├── credentials.json
├── requirements.txt
└── README.md

🔒 Security Note

SpamGuard uses OAuth 2.0 for secure Gmail access. No emails or credentials are stored locally or on any server.

🎯 Project Aim

To automate real-time email management and spam filtering without using AI or databases, ensuring an efficient, secure, and user-friendly communication system for organizations.

👨‍💻 Author

G N Nagaraj
📧 [07nagarajhegde@gmail.com
]
💼 Designed for academic and organizational use
