# rent_module.py
"""
Rental management module.
Functions:
- rent_book(): open rental form
- rent_register(): save rental
- return_book(): open return form
- return_register(): process return
- display_rent(): show rental status
"""
from tkinter import Tk, Frame, Canvas, Label, Entry, Button, messagebox
from datetime import datetime, timedelta
from db import get_connection

def rent_book():
    """Open a form to rent a book."""
    global rent_entries
    root = Tk()
    root.title("도서 대여")
    root.geometry("500x400")

    Canvas(root, bg="lavender").pack(expand=True, fill='both')
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(root, text="도서 대여", bg='black', fg='white', font=('Courier', 15)).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.4)
    fields = ["회원ID:", "도서ID:"]
    rent_entries = []
    for i, label_text in enumerate(fields):
        Label(frame, text=label_text, bg='black', fg='white').place(relx=0.05, rely=0.2*i+0.1, relheight=0.1)
        e = Entry(frame)
        e.place(relx=0.3, rely=0.2*i+0.1, relwidth=0.6, relheight=0.1)
        rent_entries.append(e)

    Button(root, text="대여", command=rent_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)
    root.mainloop()

def rent_register():
    """Record a new rental and update book/user counts."""
    con = get_connection()
    cur = con.cursor()
    uid, bid = [e.get() for e in rent_entries]
    today = datetime.now().date()
    due = today + timedelta(weeks=2)

    cur.execute('SELECT BOOK_RENT_YN FROM bookTbl WHERE BOOK_ID=%s', (bid,))
    status = cur.fetchone()
    if status and status[0] == 'Y':
        cur.execute(
            "INSERT INTO rentTbl"
            " (USER_ID, BOOK_ID, RENT_DATE, RENT_RETURN_DATE, RENT_RETURN_CHECK)"
            " VALUES (%s,%s,%s,%s,'X')",
            (uid, bid, today, due)
        )
        cur.execute("UPDATE bookTbl SET BOOK_RENT_YN='N' WHERE BOOK_ID=%s", (bid,))
        cur.execute("UPDATE userTbl SET USER_RENT_COUNT = USER_RENT_COUNT + 1 WHERE USER_ID=%s", (uid,))
        con.commit()
        messagebox.showinfo("대여 완료", "도서 대여가 완료되었습니다.")
    else:
        messagebox.showerror("대여 실패", "대여할 수 없습니다.")

def return_book():
    """Open a form to process book return."""
    global return_entry
    root = Tk()
    root.title("도서 반납")
    root.geometry("400x250")

    Canvas(root, bg="lavender").pack(expand=True, fill='both')
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(root, text="도서 반납", bg='black', fg='white', font=('Courier', 15)).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.3)
    Label(frame, text="도서ID:", bg='black', fg='white').place(relx=0.05, rely=0.2)
    return_entry = Entry(frame)
    return_entry.place(relx=0.3, rely=0.2, relwidth=0.6)

    Button(root, text="반납", command=return_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)
    root.mainloop()

def return_register():
    """Update rental record, book availability, and user count."""
    con = get_connection()
    cur = con.cursor()
    bid = return_entry.get()

    cur.execute("UPDATE rentTbl SET RENT_RETURN_CHECK='O' WHERE BOOK_ID=%s AND RENT_RETURN_CHECK='X'", (bid,))
    cur.execute("UPDATE bookTbl SET BOOK_RENT_YN='Y' WHERE BOOK_ID=%s", (bid,))
    cur.execute(
        "UPDATE userTbl SET USER_RENT_COUNT = USER_RENT_COUNT - 1"
        " WHERE USER_ID = (SELECT USER_ID FROM rentTbl WHERE BOOK_ID=%s LIMIT 1)",
        (bid,)
    )
    con.commit()
    messagebox.showinfo("반납 완료", "도서 반납이 완료되었습니다.")

def display_rent():
    """Show current rental status."""
    con = get_connection()
    cur = con.cursor()
    root = Tk()
    root.title("대여 현황")
    root.geometry("700x500")

    Canvas(root, bg="lightblue").pack(expand=True, fill='both')
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(root, text="대여 현황", bg='black', fg='white', font=('Courier', 15)).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    headers = "회원ID    이름     제목            대출일         반납예정일       상태"
    Label(frame, text=headers, bg='black', fg='white').place(relx=0, rely=0)

    y = 0.1
    cur.execute(
        "SELECT r.USER_ID, u.USER_NAME, b.BOOK_TITLE, r.RENT_DATE, r.RENT_RETURN_DATE, r.RENT_RETURN_CHECK"
        " FROM rentTbl r"
        " JOIN userTbl u ON r.USER_ID=u.USER_ID"
        " JOIN bookTbl b ON r.BOOK_ID=b.BOOK_ID"
        " ORDER BY r.RENT_RETURN_CHECK, r.RENT_RETURN_DATE"
    )
    for uid, name, title, rent_date, return_date, status in cur.fetchall():
        text = f"{uid:<8} {name:<8} {title:<15} {rent_date} {return_date} {status}"
        Label(frame, text=text, bg='black', fg='white').place(relx=0, rely=y)
        y += 0.1

    Button(root, text="닫기", command=root.destroy).place(relx=0.4, rely=0.9)
    root.mainloop()
    