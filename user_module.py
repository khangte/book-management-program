# user_module.py
"""
User management module.
Functions:
- display_user(): show all users in a scrollable, aligned table
- add_user(): open registration form
- user_register(): persist new user
"""

from tkinter import (
    Tk, Frame, Canvas, Label, Entry, Button,
    messagebox, Scrollbar, VERTICAL, RIGHT, Y, BOTH
)
from tkinter import ttk
from datetime import datetime
from db import get_connection

# 컬럼 헤더 및 고정 폭(픽셀) 설정
COLUMNS = [
    ("회원ID",     80),
    ("이름",      100),
    ("생년월일",   100),
    ("주소",      50),
    ("전화번호",   120),
    ("등록일",     120),
    ("대여권수",    80),
]

def display_user():
    """Display all registered users in a scrollable, aligned table."""
    con = get_connection()
    cur = con.cursor()

    root = Tk()
    root.title("회원 정보")
    root.geometry("800x600")

    # 배경 캔버스 (색상을 유지)
    Canvas(root, bg="lemon chiffon").pack(expand=True, fill=BOTH)

    # 헤딩
    heading_frame = Frame(root, bg="#FFBB00", bd=5)
    heading_frame.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
    Label(
        heading_frame,
        text="회원 정보",
        bg='black',
        fg='white',
        font=('Courier', 15)
    ).pack(expand=True, fill=BOTH)

    # 테이블 프레임
    table_frame = Frame(root, bg='black')
    table_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.65)

    # 수직 스크롤바
    vsb = Scrollbar(table_frame, orient=VERTICAL)
    vsb.pack(side=RIGHT, fill=Y)

    # 스타일 설정 (검정 배경, 흰색 글씨)
    style = ttk.Style()
    style.theme_use('default')
    style.configure(
        "Treeview",
        background="black",
        foreground="white",
        fieldbackground="black",
        rowheight=25
    )
    style.configure(
        "Treeview.Heading",
        background="black",
        foreground="white"
    )
    style.map(
        "Treeview",
        background=[('selected', 'gray')],
        foreground=[('selected', 'white')]
    )

    # Treeview 생성
    cols = [col for col, _ in COLUMNS]
    tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show='headings',
        yscrollcommand=vsb.set,
        selectmode='browse'
    )
    vsb.config(command=tree.yview)

    # 컬럼 헤더 및 너비 설정
    for col_name, col_width in COLUMNS:
        tree.heading(col_name, text=col_name)
        tree.column(col_name, width=col_width, anchor='w')

    tree.pack(expand=True, fill=BOTH)

    # 데이터 로드 및 삽입
    cur.execute("""
        SELECT USER_ID, USER_NAME, USER_BIRTH, USER_ADDR,
               USER_PHONE, USER_REG_DATE, USER_RENT_COUNT
          FROM userTbl
         ORDER BY USER_NAME
    """)
    for row in cur.fetchall():
        # 문자열로 변환된 값을 그대로 넣으면 컬럼 폭에 맞춰 잘 정렬됩니다
        tree.insert('', 'end', values=[str(x) for x in row])

    # 닫기 버튼
    Button(root, text="닫기", command=root.destroy).place(relx=0.45, rely=0.9)

    root.mainloop()


def add_user():
    """Open a form to register a new user."""
    global entries
    root = Tk()
    root.title("회원 등록")
    root.geometry("600x500")

    Canvas(root, bg="lemon chiffon").pack(expand=True, fill=BOTH)
    Frame(root, bg="#FFBB00", bd=5).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    Label(
        root,
        text="회원 등록",
        bg='black',
        fg='white',
        font=('Courier', 15)
    ).place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    frame = Frame(root, bg='black')
    frame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    fields = ["회원ID:", "이름:", "생년월일(YYYY-MM-DD):", "주소:", "전화번호:"]
    entries = []
    LABEL_X   = 0.05   # 레이블 시작 위치
    ENTRY_X   = 0.40   # Entry 시작 위치 (더 오른쪽으로)
    ENTRY_W   = 0.50   # Entry 너비 (줄여서 레이블이 가려지지 않도록)
    for i, label_text in enumerate(fields):
        y = 0.15*i + 0.1
        # 레이블
        Label(frame, text=label_text, bg='black', fg='white')\
            .place(relx=LABEL_X, rely=y, relheight=0.08)
        # 입력창
        e = Entry(frame)
        e.place(relx=ENTRY_X, rely=y, relwidth=ENTRY_W, relheight=0.08)
        entries.append(e)

    Button(root, text="등록", command=user_register).place(relx=0.28, rely=0.9)
    Button(root, text="닫기", command=root.destroy).place(relx=0.53, rely=0.9)
    root.mainloop()


def user_register():
    """Insert a new user into the database if ID is unique."""
    con = get_connection()
    cur = con.cursor()

    # 원래는 이 줄
    # uid, name, birth, addr, phone = [e.get() for e in entries]
    # 이렇게 바꿉니다:
    uid, name, birth_str, addr, phone = [e.get() for e in entries]

    # 문자열을 date 객체로 변환
    try:
        birth = datetime.strptime(birth_str, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("등록 실패", "생년월일 형식이 잘못되었습니다. YYYY-MM-DD 형태로 입력하세요.")
        return

    # 등록일도 datetime.date 로
    now = datetime.now().date()

    # 중복 검사
    cur.execute("SELECT USER_ID FROM userTbl")
    existing_ids = {row[0] for row in cur.fetchall()}

    if uid in existing_ids:
        messagebox.showerror("등록 실패", "이미 존재하는 회원ID입니다.")
        return

    # INSERT 시에 Python date 객체를 넘겨주면 pymssql이 올바르게 처리합니다.
    cur.execute(
        """
        INSERT INTO userTbl
          (USER_ID, USER_NAME, USER_BIRTH, USER_ADDR, USER_PHONE, USER_REG_DATE, USER_RENT_COUNT)
        VALUES (%s, %s, %s, %s, %s, %s, 0)
        """,
        (uid, name, birth, addr, phone, now)
    )
    con.commit()
    messagebox.showinfo("등록 완료", "회원 등록이 완료되었습니다.")
