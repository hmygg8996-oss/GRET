import customtkinter as ctk
import requests
import json
import threading

API_KEY = "VXdt4utF7kEFHsnTeNKe"
BASE_URL = "https://api.temp-mail.io/v1"
HEADERS = {"X-API-Key": API_KEY, "Accept": "application/json"}

current_email = ""

def api_create_email():
    try:
        r = requests.post(f"{BASE_URL}/emails", headers=HEADERS)
        return r.json().get("email") if r.status_code == 200 else None
    except:
        return None

def api_inbox(email):
    try:
        e = requests.utils.quote(email, safe="")
        r = requests.get(f"{BASE_URL}/emails/{e}/messages", headers=HEADERS)
        return r.json() if r.status_code == 200 else []
    except:
        return []

def create_email():
    global current_email
    btn_create.configure(state="disabled")
    msg_box.delete("0.0", "end")
    msg_box.insert("end", "[*] Creating email...\n")
    def task():
        global current_email
        email = api_create_email()
        if email:
            current_email = email
            email_label.configure(text=f"EMAIL: {email}")
            msg_box.insert("end", f"[+] Email created: {email}\n")
            msg_box.insert("end", "[*] Click the email to copy it\n")
        else:
            msg_box.insert("end", "[-] Failed to create email\n")
        btn_create.configure(state="normal")
    threading.Thread(target=task, daemon=True).start()

def refresh_inbox():
    if not current_email:
        msg_box.delete("0.0", "end")
        msg_box.insert("end", "[-] No active email. Click CREATE first.\n")
        return
    msg_box.delete("0.0", "end")
    msg_box.insert("end", "[*] Refreshing inbox...\n")
    def task():
        msgs = api_inbox(current_email)
        msg_box.delete("0.0", "end")
        if not msgs:
            msg_box.insert("end", "[-] Inbox is empty\n")
            return
        msg_box.insert("end", f"=== INBOX ({len(msgs)} messages) ===\n\n")
        for i, m in enumerate(msgs, 1):
            sub = m.get("subject") or "(no subject)"
            frm = m.get("from_email") or "unknown"
            body = m.get("body_text") or m.get("body_html") or "(empty)"
            msg_box.insert("end", f"[{i}] FROM: {frm}\n")
            msg_box.insert("end", f"    SUBJECT: {sub}\n")
            msg_box.insert("end", f"    {body[:200]}\n\n")
    threading.Thread(target=task, daemon=True).start()

def copy_email():
    if current_email:
        app.clipboard_clear()
        app.clipboard_append(current_email)
        msg_box.insert("end", f"[+] Copied: {current_email}\n")

# UI
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("TEMP MAIL ROXI")
app.geometry("800x550")
app.resizable(False, False)
app.configure(fg_color="#000000")

# Header
header = ctk.CTkFrame(app, fg_color="#1a0000", corner_radius=0, border_width=4, border_color="#ff0033")
header.pack(fill="x")
ctk.CTkLabel(header, text="TEMP MAIL ROXI", font=("Consolas", 24, "bold"), text_color="#ff0033").pack(side="left", pady=12, padx=20)

# Email display
email_frame = ctk.CTkFrame(app, fg_color="#110000", border_width=3, border_color="#ff0033")
email_frame.pack(pady=15, padx=40, fill="x")
email_label = ctk.CTkButton(email_frame, text="EMAIL: NOT GENERATED", font=("Consolas", 18, "bold"),
    fg_color="#220000", text_color="#ff3333", hover_color="#330000", command=copy_email)
email_label.pack(pady=10)

# Buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=8)
btn_create = ctk.CTkButton(btn_frame, text="CREATE EMAIL", font=("Consolas", 16, "bold"),
    fg_color="#cc0000", hover_color="#990000", width=250, height=50, command=create_email)
btn_create.grid(row=0, column=0, padx=20)
ctk.CTkButton(btn_frame, text="REFRESH INBOX", font=("Consolas", 16, "bold"),
    fg_color="#990000", hover_color="#660000", width=250, height=50, command=refresh_inbox).grid(row=0, column=1, padx=20)

# Message box
terminal = ctk.CTkFrame(app, fg_color="#0a0000", border_width=4, border_color="#ff0033")
terminal.pack(padx=40, pady=10, fill="both", expand=True)
msg_box = ctk.CTkTextbox(terminal, font=("Consolas", 13), fg_color="#110000", text_color="#ff6666")
msg_box.pack(padx=10, pady=10, fill="both", expand=True)
msg_box.insert("end", "[*] Click CREATE EMAIL to start\n")

app.mainloop()
