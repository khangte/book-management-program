# book_module.py
"""
Book management module.
Functions:
- display_book(): show all books in a scrollable, aligned table
- add_book(): open registration form
- book_register(): persist new book
"""

from tkinter import (
    Tk, Frame, Canvas, Label, Entry, Button,
    messagebox, Scrollbar, VERTICAL, RIGHT, Y, BOTH
)
from tkinter import ttk
from db import get_connection

# 컬럼 헤더 및 너비 설정
COLUMNS = [
    ("도서번호", 80),
    ("제목",   200),
    ("저자",   100),
    ("가격",    80),
    ("대여가능", 80),
]

def display_book():
    """Display all books in a scrollable, aligned table."""
    con = get_connection()
    cur = con.cursor()

    root = Tk()
    root.title("도서 목록")
    root.geometry("800x600")

    Canvas(root, bg="lavender").pack(expand=True, fill=BOTH)

    # 헤딩
    heading_frame = Frame(root, bg="#FFBB00", bd=5)
    heading_frame.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
    Label(
        heading_frame,
        text="도서 목록",
        bg='black',
        fg='white',
        font=('Courier', 15)
    ).pack(expand=True, fill=BOTH)

    # 테이블
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
        SELECT BOOK_ID, BOOK_TITLE, BOOK_AUTHOR, BOOK_PRICE, BOOK_RENT_YN
          FROM bookTbl
         ORDER BY BOOK_ID
    """)
    for row in cur.fetchall():
        tree.insert('', 'end', values=[str(x) for x in row])

    Button(root, text="닫기", command=root.destroy).place(relx=0.45, rely=0.9)
    root.mainloop()


def add_book():
    """Open a form to register a new book."""
    global entries
    root = Tk()
    root.title("도서 등록")
    root.geometry("600x500")

    Canvas(root, bg="lavender").pack(expand=True, fill=BOTH)
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(
        root,
        text="도서 등록",
        bg='black',
        fg='white',
        font=('Courier', 15)
    ).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    fields = ["도서번호:", "제목:", "저자:", "가격:"]
    entries = []
    for i, label_text in enumerate(fields):
        Label(frame, text=label_text, bg='black', fg='white').place(
            relx=0.05, rely=0.15*i+0.1, relheight=0.08
        )
        e = Entry(frame)
        e.place(relx=0.3, rely=0.15*i+0.1, relwidth=0.6, relheight=0.08)
        entries.append(e)

    Button(root, text="등록", command=book_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)
    root.mainloop()


def book_register():
    """Insert a new book into the database if ID is unique."""
    con = get_connection()
    cur = con.cursor()

    bid, title, author, price = [e.get() for e in entries]
    cur.execute('SELECT BOOK_ID FROM bookTbl')
    existing = {row[0] for row in cur.fetchall()}

    if bid in existing:
        messagebox.showerror("등록 실패", "이미 존재하는 도서번호입니다.")
    else:
        cur.execute(
            "INSERT INTO bookTbl "
            "(BOOK_ID, BOOK_TITLE, BOOK_AUTHOR, BOOK_PRICE, BOOK_RENT_YN) "
            "VALUES (%s,%s,%s,%s,'Y')",
            (bid, title, author, price)
        )
        con.commit()
        messagebox.showinfo("등록 완료", "도서 등록이 완료되었습니다.")
