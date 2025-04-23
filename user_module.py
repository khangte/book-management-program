# user_module.py
"""
User management module.
Functions:
- display_user(): show all users
- add_user(): open registration form
- user_register(): persist new user
"""
from tkinter import Tk, Frame, Canvas, Label, Entry, Button, messagebox
from datetime import datetime
from db import get_connection

def display_user():
    """Display all registered users in a Tkinter window."""
    con = get_connection()
    cur = con.cursor()
    root = Tk()
    root.title("회원 정보")
    root.geometry("600x500")

    Canvas(root, bg="lemon chiffon").pack(expand=True, fill='both')
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(root, text="회원 정보", bg='black', fg='white', font=('Courier', 15)).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.5)
    headers = "회원ID    이름    생년월일    주소    전화번호    등록일    대여권수"
    Label(frame, text=headers, bg='black', fg='white').place(relx=0, rely=0)

    y = 0.1
    cur.execute(
        "SELECT USER_ID, USER_NAME, USER_BIRTH, USER_ADDR, USER_PHONE, USER_REG_DATE, USER_RENT_COUNT"
        " FROM userTbl ORDER BY USER_NAME"
    )
    for uid, name, birth, addr, phone, reg_date, rent_count in cur.fetchall():
        text = f"{uid:<8} {name:<8} {birth:<10} {addr:<10} {phone:<12} {reg_date:<12} {rent_count}"
        Label(frame, text=text, bg='black', fg='white').place(relx=0, rely=y)
        y += 0.1

    Button(root, text="닫기", command=root.destroy).place(relx=0.4, rely=0.9)
    root.mainloop()

def add_user():
    """Open a form to register a new user."""
    global entries
    root = Tk()
    root.title("회원 등록")
    root.geometry("600x500")

    Canvas(root, bg="lemon chiffon").pack(expand=True, fill='both')
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(root, text="회원 등록", bg='black', fg='white', font=('Courier', 15)).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    fields = ["회원ID:", "이름:", "생년월일(YYYY-MM-DD):", "주소:", "전화번호:"]
    entries = []
    for i, label_text in enumerate(fields):
        Label(frame, text=label_text, bg='black', fg='white').place(relx=0.05, rely=0.15*i+0.1, relheight=0.08)
        e = Entry(frame)
        e.place(relx=0.3, rely=0.15*i+0.1, relwidth=0.6, relheight=0.08)
        entries.append(e)

    Button(root, text="등록", command=user_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)
    root.mainloop()

def user_register():
    """Insert a new user into the database if ID is unique."""
    con = get_connection()
    cur = con.cursor()
    now = datetime.now().date()

    uid, name, birth, addr, phone = [e.get() for e in entries]
    cur.execute('SELECT USER_ID FROM userTbl')
    existing_ids = {row[0] for row in cur.fetchall()}

    if uid in existing_ids:
        messagebox.showerror("등록 실패", "이미 존재하는 회원ID입니다.")
    else:
        cur.execute(
            "INSERT INTO userTbl"
            " (USER_ID, USER_NAME, USER_BIRTH, USER_ADDR, USER_PHONE, USER_REG_DATE, USER_RENT_COUNT)"
            " VALUES (%s,%s,%s,%s,%s,%s,0)",
            (uid, name, birth, addr, phone, now)
        )
        con.commit()
        messagebox.showinfo("등록 완료", "회원 등록이 완료되었습니다.")
        