# main.py
"""
Entry point for the Library Rental App GUI.
Contains buttons to access all modules.
"""
from tkinter import Tk, Button
import user_module as u_mod
import book_module as b_mod
import rent_module as r_mod

if __name__ == "__main__":
    root = Tk()
    root.title("도서 대여 시스템")
    root.geometry("600x500")

    Button(root, text="회원 정보", width=20, command=u_mod.display_user).pack(pady=10)
    Button(root, text="회원 등록", width=20, command=u_mod.add_user).pack(pady=10)
    Button(root, text="도서 목록", width=20, command=b_mod.display_book).pack(pady=10)
    Button(root, text="도서 등록", width=20, command=b_mod.add_book).pack(pady=10)
    Button(root, text="도서 대여", width=20, command=r_mod.rent_book).pack(pady=10)
    Button(root, text="도서 반납", width=20, command=r_mod.return_book).pack(pady=10)
    Button(root, text="대여 현황", width=20, command=r_mod.display_rent).pack(pady=10)

    root.mainloop()