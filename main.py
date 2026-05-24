import tkinter as tk
from tkinter import scrolledtext
import keyboard
from ui import show_menu
import pyperclip
import sys
import os
import ctypes

# ---------- 高 DPI 支持 ----------
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass
# ---------------------------------

class BaseToolApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Base 家族")
        self.root.geometry("480x480")
        self.root.minsize(380, 380)
        self.root.configure(bg='#2d2d2d')

        self.topmost = False

        try:
            if getattr(sys, 'frozen', False):
                ico_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                ico_path = 'icon.ico'
            self.root.iconbitmap(ico_path)
        except:
            pass

        # ---- 标题 ----
        title = tk.Label(self.root, text="🔐 Base 家族", font=("微软雅黑", 14, "bold"),
                         fg="#00ff88", bg="#2d2d2d")
        title.pack(pady=(15, 5))

        hint = tk.Label(self.root, text="全局快捷键：Alt + X", font=("微软雅黑", 10),
                        fg="#cccccc", bg="#2d2d2d")
        hint.pack(pady=(0, 5))

        # ---- 日志框 ----
        log_frame = tk.Frame(self.root, bg='#2d2d2d')
        log_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.font_family = "Consolas"
        self.font_size = 9

        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=(self.font_family, self.font_size),
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="white",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.log_area.bind("<Control-MouseWheel>", self.on_font_size_change)

        # ---- 底部按钮栏 ----
        btn_frame = tk.Frame(self.root, bg='#2d2d2d')
        btn_frame.pack(pady=(5, 10), fill=tk.X, padx=10)

        self.pin_btn = tk.Button(
            btn_frame, text="📌 置顶", command=self.toggle_topmost,
            bg="#555555", fg="white", activebackground="#777777",
            activeforeground="white", relief="flat", padx=12, pady=4
        )
        self.pin_btn.pack(side=tk.LEFT, padx=(0, 5))

        exit_btn = tk.Button(
            btn_frame, text="退  出", command=self.quit_app,
            bg="#444444", fg="white", activebackground="#666666",
            activeforeground="white", relief="flat", padx=20, pady=4
        )
        exit_btn.pack(side=tk.RIGHT)

        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.log("✨ Base 工具箱已启动")
        self.log("支持：Base16/32/58/62/64/85/91/92/100")
        self.log("按 Alt+X 呼出菜单")
        self.log("💡 Ctrl+滚轮 缩放字体 | 📌 置顶实时查看")

        # 修改快捷键为 Alt+X
        keyboard.add_hotkey('alt+x', lambda: show_menu(self.conversion_callback))

    def toggle_topmost(self):
        self.topmost = not self.topmost
        self.root.attributes('-topmost', self.topmost)
        if self.topmost:
            self.pin_btn.config(text="📌 取消置顶", bg="#57e3e6")
        else:
            self.pin_btn.config(text="📌 置顶", bg="#229582")

    def on_font_size_change(self, event):
        if event.delta > 0:
            self.font_size += 1
        else:
            self.font_size -= 1
        self.font_size = max(6, min(self.font_size, 24))
        self.log_area.configure(font=(self.font_family, self.font_size))
        return "break"

    def conversion_callback(self, name, func):
        original = pyperclip.paste()
        result = func(original)
        pyperclip.copy(result)
        display = result if len(result) <= 60 else result[:60] + "..."
        self.log(f"✅ [{name}] {display}")

    def log(self, message):
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state=tk.DISABLED)

    def quit_app(self):
        keyboard.unhook_all()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

def main():
    app = BaseToolApp()
    app.run()

if __name__ == '__main__':
    main()