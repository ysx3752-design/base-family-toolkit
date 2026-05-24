import tkinter as tk
import pyperclip
from base import get_all_options

def show_menu(callback):
    clipboard_text = pyperclip.paste()
    if not clipboard_text.strip():
        print("[!] 剪贴板为空")
        return

    options = get_all_options()
    menu = tk.Tk()
    menu.overrideredirect(True)
    menu.attributes('-topmost', True)
    menu.configure(bg='#2d2d2d')

    # 两列网格布局
    for idx, (name, func) in enumerate(options):
        row = idx // 2
        col = idx % 2
        btn = tk.Button(
            menu, text=name,
            command=lambda n=name, f=func: [callback(n, f), menu.destroy()],
            bg='#3c3c3c', fg='white', relief='flat',
            padx=10, pady=5, width=22, anchor='w'
        )
        btn.grid(row=row, column=col, sticky='ew', padx=1, pady=1)
        btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#555'))
        btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#3c3c3c'))

    menu.grid_columnconfigure(0, weight=1)
    menu.grid_columnconfigure(1, weight=1)

    # 底部关闭按钮
    close_btn = tk.Button(
        menu, text="❌ 关闭 ", command=menu.destroy,
        bg='#555', fg='white', relief='flat', padx=10, pady=3, width=22
    )
    close_btn.grid(row=len(options)//2 + 1, column=0, columnspan=2, sticky='ew', padx=1, pady=(5,1))
    close_btn.bind("<Enter>", lambda e, b=close_btn: b.configure(bg='#777'))
    close_btn.bind("<Leave>", lambda e, b=close_btn: b.configure(bg='#555'))

    # 智能避让
    menu.update_idletasks()
    x, y = menu.winfo_pointerxy()
    menu_w = menu.winfo_reqwidth()
    menu_h = menu.winfo_reqheight()
    screen_w = menu.winfo_screenwidth()
    screen_h = menu.winfo_screenheight()

    new_x = x + 10
    new_y = y + 10
    if new_x + menu_w > screen_w:
        new_x = screen_w - menu_w - 5
    if new_y + menu_h > screen_h:
        new_y = screen_h - menu_h - 5
    menu.geometry(f"+{new_x}+{new_y}")

    # ---- 关闭方式（无需全局热键）----
    # 1. 按键盘左上角 Esc 键
    menu.bind("<Escape>", lambda e: menu.destroy())
    # 2. 点击菜单外部任意位置（失去焦点）
    menu.bind("<FocusOut>", lambda e: menu.destroy())

    menu.after(1, lambda: menu.focus_force())
    menu.mainloop()