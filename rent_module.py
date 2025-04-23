# rent_module.py
"""
Rental management module.
Functions:
- display_rent(): show all rentals in a scrollable, aligned table
- rent_book(): open lending form
- rent_register(): persist new rental
- return_book(): open return form
- return_register(): process a return
"""

from tkinter import (
    Tk, Frame, Canvas, Label, Entry, Button,
    messagebox, Scrollbar, VERTICAL, RIGHT, Y, BOTH
)
from tkinter import ttk
from datetime import datetime, timedelta
from db import get_connection

# 컬럼 헤더 및 너비 설정
COLUMNS = [
    ("회원ID",      80),
    ("이름",      100),
    ("제목",      200),
    ("대여일",     100),
    ("반납예정일",   100),
    ("반납여부",     80),
]

def display_rent():
    """Display all rental records in a scrollable, aligned table."""
    con = get_connection()
    cur = con.cursor()

    root = Tk()
    root.title("대여 현황")
    root.geometry("900x600")

    Canvas(root, bg="lightblue").pack(expand=True, fill=BOTH)

    heading_frame = Frame(root, bg="#FFBB00", bd=5)
    heading_frame.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
    Label(
        heading_frame,
        text="대여 현황",
        bg='black',
        fg='white',
        font=('Courier', 15)
    ).pack(expand=True, fill=BOTH)

    table_frame = Frame(root, bg='black')
    table_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.65)

    vsb = Scrollbar(table_frame, orient=VERTICAL)
    vsb.pack(side=RIGHT, fill=Y)

    style = ttk.Style()
    style.theme_use('default')
    style.configure(
        "Treeview",
        background="black",
        foreground="white",
        fieldbackground="black",
        rowheight=25
    )
    style.configure("Treeview.Heading", background="black", foreground="white")
    style.map(
        "Treeview",
        background=[('selected', 'gray')],
        foreground=[('selected', 'white')]
    )

    cols = [c for c,_ in COLUMNS]
    tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show='headings',
        yscrollcommand=vsb.set,
        selectmode='browse'
    )
    vsb.config(command=tree.yview)

    for name, width in COLUMNS:
        tree.heading(name, text=name)
        tree.column(name, width=width, anchor='w')

    tree.pack(expand=True, fill=BOTH)

    cur.execute("""
        SELECT r.USER_ID, u.USER_NAME, b.BOOK_TITLE,
               r.RENT_DATE, r.RENT_RETURN_DATE, r.RENT_RETURN_CHECK
          FROM rentTbl r
          JOIN userTbl u ON r.USER_ID = u.USER_ID
          JOIN bookTbl b ON r.BOOK_ID = b.BOOK_ID
         ORDER BY r.RENT_RETURN_CHECK, r.RENT_RETURN_DATE
    """)
    for row in cur.fetchall():
        tree.insert('', 'end', values=[str(x) for x in row])

    Button(root, text="닫기", command=root.destroy).place(relx=0.45, rely=0.9)
    root.mainloop()


def rent_book():
    """Open a form to lend a book."""
    global rent_entries
    root = Tk()
    root.title("도서 대여")
    root.geometry("600x450")

    Canvas(root, bg="lavender").pack(expand=True, fill=BOTH)

    heading_frame = Frame(root, bg="#FFBB00", bd=5)
    heading_frame.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
    Label(heading_frame, text="도서 대여", bg='black', fg='white',
          font=('Courier', 16, 'bold')).pack(expand=True, fill=BOTH)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.5)

    LABEL_X, ENTRY_X, ENTRY_W = 0.05, 0.35, 0.60
    labels = ["회원 ID:", "도서 번호:"]
    rent_entries = []
    for i, txt in enumerate(labels):
        y = 0.2 * i + 0.1
        Label(frame, text=txt, bg='black', fg='white', font=('Courier', 12))\
            .place(relx=LABEL_X, rely=y, relheight=0.1)
        e = Entry(frame)
        e.place(relx=ENTRY_X, rely=y, relwidth=ENTRY_W, relheight=0.1)
        rent_entries.append(e)

    # 버튼 크기/위치 통일
    Button(root, text="대여", command=rent_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)

    root.mainloop()


def rent_register():
    """Persist a new rental if the book is available."""
    con = get_connection()
    cur = con.cursor()
    uid, bid = [e.get() for e in rent_entries]
    today = datetime.now().date()
    due = today + timedelta(weeks=2)

    cur.execute("SELECT BOOK_RENT_YN FROM bookTbl WHERE BOOK_ID=%s", (bid,))
    yn = cur.fetchone()
    if not yn:
        messagebox.showerror("대여 실패", "존재하지 않는 도서번호입니다.")
        return

    if yn[0] == 'Y':
        cur.execute(
            "INSERT INTO rentTbl (USER_ID, BOOK_ID, RENT_DATE, RENT_RETURN_DATE, RENT_RETURN_CHECK) "
            "VALUES (%s,%s,%s,%s,'X')",
            (uid, bid, today, due)
        )
        cur.execute("UPDATE bookTbl SET BOOK_RENT_YN='N' WHERE BOOK_ID=%s", (bid,))
        cur.execute("UPDATE userTbl SET USER_RENT_COUNT = USER_RENT_COUNT + 1 WHERE USER_ID=%s", (uid,))
        con.commit()
        messagebox.showinfo("대여 완료", "대여가 완료되었습니다.")
    else:
        messagebox.showwarning("대여 실패", "이미 대여 중인 도서입니다.")


def return_book():
    """Open a form to process a return."""
    global return_entry
    root = Tk()
    root.title("도서 반납")
    root.geometry("600x400")

    Canvas(root, bg="lavender").pack(expand=True, fill=BOTH)

    heading_frame = Frame(root, bg="#FFBB00", bd=5)
    heading_frame.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
    Label(heading_frame, text="도서 반납", bg='black', fg='white',
          font=('Courier', 16, 'bold')).pack(expand=True, fill=BOTH)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.5)

    LABEL_X, ENTRY_X, ENTRY_W = 0.05, 0.35, 0.55
    y = 0.2
    Label(frame, text="반납할 도서 번호:", bg='black', fg='white',
          font=('Courier', 12)).place(relx=LABEL_X, rely=y, relheight=0.1)
    return_entry = Entry(frame)
    return_entry.place(relx=ENTRY_X, rely=y, relwidth=ENTRY_W, relheight=0.1)

    # 버튼 크기/위치 통일
    Button(root, text="반납", command=return_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)

    root.mainloop()


def return_register():
    """Process a book return."""
    con = get_connection()
    cur = con.cursor()
    bid = return_entry.get()

    # 대여 중인 레코드를 찾고 반납 처리
    cur.execute(
        "SELECT USER_ID FROM rentTbl WHERE BOOK_ID=%s AND RENT_RETURN_CHECK='X'",
        (bid,)
    )
    rec = cur.fetchone()
    if not rec:
        messagebox.showerror("반납 실패", "대여 중인 도서가 아닙니다.")
        return

    uid = rec[0]
    cur.execute(
        "UPDATE rentTbl SET RENT_RETURN_CHECK='O' "
        "WHERE BOOK_ID=%s AND RENT_RETURN_CHECK='X'",
        (bid,)
    )
    cur.execute("UPDATE bookTbl SET BOOK_RENT_YN='Y' WHERE BOOK_ID=%s", (bid,))
    cur.execute("UPDATE userTbl SET USER_RENT_COUNT = USER_RENT_COUNT - 1 WHERE USER_ID=%s", (uid,))
    con.commit()
    messagebox.showinfo("반납 완료", "반납이 완료되었습니다.")
