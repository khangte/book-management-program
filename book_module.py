# book_module.py
"""
Book management module.
Functions:
- display_book(): show all books
- add_book(): open new-book form
- book_register(): persist new book
"""
from tkinter import Tk, Frame, Canvas, Label, Entry, Button, messagebox
from db import get_connection

def display_book():
    """Display all books."""
    con = get_connection()
    cur = con.cursor()
    root = Tk()
    root.title("도서 목록")
    root.geometry("600x500")

    Canvas(root, bg="lavender").pack(expand=True, fill='both')
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(root, text="도서 목록", bg='black', fg='white', font=('Courier', 15)).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    headers = "ID    제목            저자          가격    대여여부"
    Label(frame, text=headers, bg='black', fg='white').place(relx=0, rely=0)

    y = 0.1
    cur.execute('SELECT BOOK_ID, BOOK_TITLE, BOOK_AUTHOR, BOOK_PRICE, BOOK_RENT_YN FROM bookTbl')
    for bid, title, author, price, yn in cur.fetchall():
        text = f"{bid:<4} {title:<15} {author:<12} {price:<6} {yn}"
        Label(frame, text=text, bg='black', fg='white').place(relx=0, rely=y)
        y += 0.1

    Button(root, text="닫기", command=root.destroy).place(relx=0.4, rely=0.9)
    root.mainloop()

def add_book():
    """Open a form to add a new book."""
    global book_entries
    root = Tk()
    root.title("도서 등록")
    root.geometry("600x500")

    Canvas(root, bg="lavender").pack(expand=True, fill='both')
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(root, text="도서 등록", bg='black', fg='white', font=('Courier', 15)).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    fields = ["도서ID:", "제목:", "저자:", "가격:"]
    book_entries = []
    for i, label_text in enumerate(fields):
        Label(frame, text=label_text, bg='black', fg='white').place(relx=0.05, rely=0.15*i+0.1, relheight=0.08)
        e = Entry(frame)
        e.place(relx=0.3, rely=0.15*i+0.1, relwidth=0.6, relheight=0.08)
        book_entries.append(e)

    Button(root, text="등록", command=book_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)
    root.mainloop()

def book_register():
    """Insert a new book if ID is unique."""
    con = get_connection()
    cur = con.cursor()
    bid, title, author, price = [e.get() for e in book_entries]
    cur.execute('SELECT BOOK_ID FROM bookTbl')
    existing_ids = {row[0] for row in cur.fetchall()}

    if bid in existing_ids:
        messagebox.showerror("등록 실패", "이미 존재하는 도서ID입니다.")
    else:
        cur.execute(
            "INSERT INTO bookTbl"
            " (BOOK_ID, BOOK_TITLE, BOOK_AUTHOR, BOOK_PRICE, BOOK_RENT_YN)"
            " VALUES (%s,%s,%s,%s,'Y')",
            (bid, title, author, price)
        )
        con.commit()
        messagebox.showinfo("등록 완료", "도서 등록이 완료되었습니다.")
