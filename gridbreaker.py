#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GridBreaker — Modern Minesweeper (Fixed initialization)
Features:
- Fullscreen (F11), Exit confirmation (Esc), Restart (F2)
- Splash screen with optional image (assets/splash.png)
- Light/Dark themes, internationalization (EN, BN, HI, ES, JA)
- Safe first click, right-click (or Ctrl+Click) to flag, double-click chord
- Timer, mine counter, best times per difficulty
- Optional sounds via pygame if installed and assets/sound available
"""

import os
import time
import json
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# Optional audio (pygame)
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

APP_NAME = "GridBreaker"
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sound")

HIGHSCORE_FILE = os.path.join(os.path.expanduser("~"), ".gridbreaker_besttimes.json")

# -----------------------------
# Internationalization (i18n)
# -----------------------------
LANGUAGES = {
    "en": "English",
    "bn": "বাংলা",
    "hi": "हिन्दी",
    "es": "Español",
    "ja": "日本語",
}

I18N = {
    "en": {
        "game": "Game",
        "new_game": "New",
        "difficulty": "Difficulty",
        "beginner": "Beginner (9×9, 10)",
        "intermediate": "Intermediate (16×16, 40)",
        "expert": "Expert (16×30, 99)",
        "custom": "Custom…",
        "exit": "Exit",
        "view": "View",
        "fullscreen": "Fullscreen",
        "theme": "Theme",
        "light": "Light",
        "dark": "Dark",
        "language": "Language",
        "help": "Help",
        "about": "About",
        "about_text": "GridBreaker — a modern, polished Minesweeper.\nBuilt with Tkinter.",
        "you_win": "You win!",
        "you_lose": "Boom! You hit a mine.",
        "cleared_in": "Cleared in {seconds} seconds.",
        "new_record": "New best time for {difficulty}: {seconds}s 🎉",
        "invalid_custom": "Invalid custom settings.",
        "custom_prompt_title": "Custom Difficulty",
        "rows_prompt": "Rows (5–24):",
        "cols_prompt": "Columns (5–40):",
        "mines_prompt": "Mines (1–rows*cols-1):",
        "confirm_exit_title": "Exit",
        "confirm_exit_text": "Quit the game?",
        "loading": "Loading...",
        "play": "Play",
        "resume": "Resume",
    },
    "bn": {
        "game": "গেম",
        "new_game": "নতুন",
        "difficulty": "কঠিনতা",
        "beginner": "বেগিনার (9×9, 10)",
        "intermediate": "ইন্টারমিডিয়েট (16×16, 40)",
        "expert": "এক্সপার্ট (16×30, 99)",
        "custom": "কাস্টম…",
        "exit": "প্রস্থান",
        "view": "ভিউ",
        "fullscreen": "ফুলস্ক্রীন",
        "theme": "থিম",
        "light": "লাইট",
        "dark": "ডার্ক",
        "language": "ভাষা",
        "help": "সাহায্য",
        "about": "সম্পর্কে",
        "about_text": "গ্রিডব্রেকার — আধুনিক, সুন্দর মাইনসুইপার।\nTkinter দিয়ে নির্মিত।",
        "you_win": "আপনি জিতেছেন!",
        "you_lose": "বুম! আপনি একটি মাইনে ক্লিক করেছেন।",
        "cleared_in": "{seconds} সেকেন্ডে সম্পন্ন।",
        "new_record": "{difficulty} এর নতুন সেরা সময়: {seconds} সেকেন্ড 🎉",
        "invalid_custom": "কাস্টম সেটিংস সঠিক নয়।",
        "custom_prompt_title": "কাস্টম কঠিনতা",
        "rows_prompt": "সারি (5–24):",
        "cols_prompt": "কলাম (5–40):",
        "mines_prompt": "মাইন (1–সর্বোচ্চ-1):",
        "confirm_exit_title": "প্রস্থান",
        "confirm_exit_text": "গেমটি বন্ধ করবেন?",
        "loading": "লোড হচ্ছে...",
        "play": "খেলুন",
        "resume": "পুনরায় শুরু",
    },
    "hi": {
        "game": "गेम",
        "new_game": "नया",
        "difficulty": "कठिनाई",
        "beginner": "शुरुआती (9×9, 10)",
        "intermediate": "मध्य (16×16, 40)",
        "expert": "विशेषज्ञ (16×30, 99)",
        "custom": "कस्टम…",
        "exit": "बाहर निकलें",
        "view": "दृश्य",
        "fullscreen": "फुलस्क्रीन",
        "theme": "थीम",
        "light": "लाइट",
        "dark": "डार्क",
        "language": "भाषा",
        "help": "मदद",
        "about": "परिचय",
        "about_text": "GridBreaker — आधुनिक, सुसज्जित माइंसवीपर।\nTkinter से निर्मित।",
        "you_win": "आप जीत गए!",
        "you_lose": "धमाका! आप माइन पर क्लिक कर बैठे।",
        "cleared_in": "{seconds} सेकंड में साफ़ किया।",
        "new_record": "{difficulty} के लिए नया सर्वश्रेष्ठ समय: {seconds} सेकंड 🎉",
        "invalid_custom": "कस्टम सेटिंग्स अमान्य हैं।",
        "custom_prompt_title": "कस्टम कठिनाई",
        "rows_prompt": "पंक्तियाँ (5–24):",
        "cols_prompt": "स्तंभ (5–40):",
        "mines_prompt": "माइंस (1–अधिकतम-1):",
        "confirm_exit_title": "बाहर निकलें",
        "confirm_exit_text": "क्या आप गेम बंद करना चाहते हैं?",
        "loading": "लोड हो रहा है...",
        "play": "खेलें",
        "resume": "फिर से शुरू",
    },
    "es": {
        "game": "Juego",
        "new_game": "Nuevo",
        "difficulty": "Dificultad",
        "beginner": "Principiante (9×9, 10)",
        "intermediate": "Intermedio (16×16, 40)",
        "expert": "Experto (16×30, 99)",
        "custom": "Personalizado…",
        "exit": "Salir",
        "view": "Vista",
        "fullscreen": "Pantalla completa",
        "theme": "Tema",
        "light": "Claro",
        "dark": "Oscuro",
        "language": "Idioma",
        "help": "Ayuda",
        "about": "Acerca de",
        "about_text": "GridBreaker — Buscaminas moderno y pulido.\nHecho con Tkinter.",
        "you_win": "¡Has ganado!",
        "you_lose": "¡Boom! Diste en una mina.",
        "cleared_in": "Completado en {seconds} segundos.",
        "new_record": "Nuevo récord para {difficulty}: {seconds}s 🎉",
        "invalid_custom": "Configuración personalizada inválida.",
        "custom_prompt_title": "Dificultad personalizada",
        "rows_prompt": "Filas (5–24):",
        "cols_prompt": "Columnas (5–40):",
        "mines_prompt": "Minas (1–máx-1):",
        "confirm_exit_title": "Salir",
        "confirm_exit_text": "¿Salir del juego?",
        "loading": "Cargando...",
        "play": "Jugar",
        "resume": "Reanudar",
    },
    "ja": {
        "game": "ゲーム",
        "new_game": "新規",
        "difficulty": "難易度",
        "beginner": "ビギナー (9×9, 10)",
        "intermediate": "中級 (16×16, 40)",
        "expert": "上級 (16×30, 99)",
        "custom": "カスタム…",
        "exit": "終了",
        "view": "表示",
        "fullscreen": "フルスクリーン",
        "theme": "テーマ",
        "light": "ライト",
        "dark": "ダーク",
        "language": "言語",
        "help": "ヘルプ",
        "about": "情報",
        "about_text": "GridBreaker — 洗練された近代的マインスイーパ。\nTkinter 製。",
        "you_win": "勝利！",
        "you_lose": "ドカン！ 地雷に当たりました。",
        "cleared_in": "{seconds} 秒でクリア。",
        "new_record": "{difficulty} の最速記録: {seconds}秒 🎉",
        "invalid_custom": "カスタム設定が無効です。",
        "custom_prompt_title": "カスタム難易度",
        "rows_prompt": "行 (5–24):",
        "cols_prompt": "列 (5–40):",
        "mines_prompt": "地雷 (1–最大-1):",
        "confirm_exit_title": "終了",
        "confirm_exit_text": "ゲームを終了しますか？",
        "loading": "読み込み中…",
        "play": "プレイ",
        "resume": "再開",
    },
}

def T(lang, key, **kwargs):
    base = I18N.get(lang, I18N["en"])
    template = base.get(key, I18N["en"].get(key, key))
    return template.format(**kwargs) if kwargs else template

# -----------------------------
# Themes
# -----------------------------
NUMBER_COLORS_LIGHT = {1: "#1976D2", 2: "#388E3C", 3: "#D32F2F", 4: "#283593", 5: "#6D4C41", 6: "#00838F", 7: "#212121", 8: "#9E9E9E"}
NUMBER_COLORS_DARK  = {1: "#90CAF9", 2: "#A5D6A7", 3: "#EF9A9A", 4: "#9FA8DA", 5: "#BCAAA4", 6: "#80CBC4", 7: "#ECEFF1", 8: "#B0BEC5"}

THEMES = {
    "light": {
        "bg": "#ECEFF1", "panel": "#CFD8DC", "panel_dark": "#B0BEC5",
        "cell_up": "#ECEFF1", "cell_down": "#CFD8DC",
        "mine_bg": "#FFCDD2", "mine_bang_bg": "#F8BBD0", "wrong_flag_bg": "#FFE0B2",
        "text": "#212121", "time": "#1976D2", "counter": "#D32F2F",
        "num_colors": NUMBER_COLORS_LIGHT,
        "hover": "#E0E0E0"
    },
    "dark": {
        "bg": "#263238", "panel": "#37474F", "panel_dark": "#455A64",
        "cell_up": "#37474F", "cell_down": "#455A64",
        "mine_bg": "#8D6E63", "mine_bang_bg": "#6D4C41", "wrong_flag_bg": "#5D4037",
        "text": "#ECEFF1", "time": "#90CAF9", "counter": "#EF9A9A",
        "num_colors": NUMBER_COLORS_DARK,
        "hover": "#546E7A"
    },
}

# -----------------------------
# Difficulties
# -----------------------------
DIFFICULTIES = {
    "beginner": (9, 9, 10),
    "intermediate": (16, 16, 40),
    "expert": (16, 30, 99),
}

FACE_DEFAULT = "😃"
FACE_WON = "😎"
FACE_LOST = "😵"
FLAG = "🚩"
MINE = "💣"

# -----------------------------
# Audio Manager
# -----------------------------
class AudioManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.enabled = True
                self._load_sounds()
            except Exception:
                self.enabled = False

    def _load_sounds(self):
        # Optional: click.wav, flag.wav, boom.wav, win.wav
        for name in ("click", "flag", "boom", "win"):
            path = os.path.join(SOUNDS_DIR, f"{name}.wav")
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except Exception:
                    pass

    def play(self, name):
        if not self.enabled:
            return
        s = self.sounds.get(name)
        if s:
            try:
                s.play()
            except Exception:
                pass

# -----------------------------
# Game logic
# -----------------------------
class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines_total = mines

        self.is_mine = [[False]*cols for _ in range(rows)]
        self.number = [[0]*cols for _ in range(rows)]
        self.state  = [["hidden"]*cols for _ in range(rows)]  # hidden, revealed, flagged

        self.mines_placed = False
        self.revealed_count = 0
        self.flag_count = 0

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0: continue
                rr, cc = r+dr, c+dc
                if self.in_bounds(rr, cc):
                    yield rr, cc

    def place_mines(self, safe_r, safe_c):
        forbidden = {(safe_r, safe_c)}
        forbidden.update(self.neighbors(safe_r, safe_c))
        pool = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in forbidden]
        mines_to_place = min(self.mines_total, len(pool))
        for (r, c) in random.sample(pool, mines_to_place):
            self.is_mine[r][c] = True
        # compute numbers
        for r in range(self.rows):
            for c in range(self.cols):
                if self.is_mine[r][c]:
                    self.number[r][c] = -1
                else:
                    self.number[r][c] = sum(1 for (rr, cc) in self.neighbors(r, c) if self.is_mine[rr][cc])
        self.mines_placed = True

    def toggle_flag(self, r, c):
        if self.state[r][c] == "revealed":
            return 0
        if self.state[r][c] == "hidden":
            self.state[r][c] = "flagged"
            self.flag_count += 1
            return +1
        if self.state[r][c] == "flagged":
            self.state[r][c] = "hidden"
            self.flag_count -= 1
            return -1

    def reveal(self, r, c):
        if self.state[r][c] != "hidden":
            return False, []
        if self.is_mine[r][c]:
            self.state[r][c] = "revealed"
            return True, [(r, c)]

        stack = [(r, c)]
        newly = []
        while stack:
            cr, cc = stack.pop()
            if self.state[cr][cc] != "hidden":
                continue
            self.state[cr][cc] = "revealed"
            newly.append((cr, cc))
            if self.number[cr][cc] == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if self.state[nr][nc] == "hidden" and not self.is_mine[nr][nc]:
                        stack.append((nr, nc))
        self.revealed_count += len(newly)
        return False, newly

    def chord_reveal(self, r, c):
        if self.state[r][c] != "revealed" or self.number[r][c] <= 0:
            return False, []
        flags = sum(1 for (rr, cc) in self.neighbors(r, c) if self.state[rr][cc] == "flagged")
        if flags != self.number[r][c]:
            return False, []
        hit_mine = False
        newly_all = []
        for (rr, cc) in self.neighbors(r, c):
            if self.state[rr][cc] == "hidden":
                hm, newc = self.reveal(rr, cc)
                if hm:
                    hit_mine = True
                newly_all.extend(newc)
        return hit_mine, newly_all

    def is_win(self):
        total_cells = self.rows * self.cols
        return self.revealed_count == total_cells - self.mines_total

# -----------------------------
# Splash Screen
# -----------------------------
class Splash(tk.Toplevel):
    def __init__(self, root, lang):
        super().__init__(root)
        self.lang = lang
        self.overrideredirect(True)
        self.configure(bg="#111111")
        w, h = 520, 300
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Try to show splash image if exists; else text logo
        path = os.path.join(ASSETS_DIR, "splash.png")
        self.logo_img = None
        try:
            from PIL import Image, ImageTk
            if os.path.exists(path):
                img = Image.open(path).convert("RGBA")
                img = img.resize((460, 180))
                self.logo_img = ImageTk.PhotoImage(img)
        except Exception:
            self.logo_img = None

        if self.logo_img:
            lbl = tk.Label(self, image=self.logo_img, bg="#111111")
            lbl.pack(pady=30)
        else:
            title = tk.Label(self, text=f"🧠 {APP_NAME}", fg="#FAFAFA", bg="#111111",
                             font=("Segoe UI", 28, "bold"))
            subtitle = tk.Label(self, text="A modern Minesweeper", fg="#BDBDBD", bg="#111111",
                                font=("Segoe UI", 12))
            title.pack(pady=(48, 4))
            subtitle.pack()

        self.loading = tk.Label(self, text=T(self.lang, "loading"), fg="#BDBDBD", bg="#111111",
                                font=("Segoe UI", 12))
        self.loading.pack(pady=16)

        try:
            self.attributes("-alpha", 0.0)
            self.after(20, self._fade_in, 0.0)
        except Exception:
            pass
        self.after(1600, self._close)

    def _fade_in(self, a):
        try:
            if a < 1.0:
                self.attributes("-alpha", a)
                self.after(20, self._fade_in, a + 0.06)
        except Exception:
            pass

    def _close(self):
        try:
            self.destroy()
        except Exception:
            pass

# -----------------------------
# Main App UI
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # Hide until splash finishes

        self.title(APP_NAME)
        self.icon_path = os.path.join(ASSETS_DIR, "icon.ico")
        try:
            if os.path.exists(self.icon_path):
                self.iconbitmap(self.icon_path)
        except Exception:
            pass

        # Defaults
        self.lang = "en"
        self.theme = "light"
        self.theme_cfg = THEMES[self.theme]
        self.number_colors = self.theme_cfg["num_colors"]

        self.current_diff = "beginner"
        self.current_rows, self.current_cols, self.current_mines = DIFFICULTIES[self.current_diff]

        self.fullscreen = False

        self.board = None
        self.btns = []
        self.game_over = False
        self.first_click = True
        self.start_time = None
        self.timer_job = None

        self.audio = AudioManager()
        self.best_times = self._load_best()

        # Splash then init
        splash = Splash(self, self.lang)
        self.after(10, splash.update)
        self.wait_window(splash)
        self._init_ui()
        self.deiconify()

    # ---- UI Init ----
    def _init_ui(self):
        self._apply_theme_colors()
        self._create_menus()
        self._create_top_panel()
        self._create_board_area()
        self._bind_shortcuts()
        self._new_game(self.current_rows, self.current_cols, self.current_mines)

    def _apply_theme_colors(self):
        t = self.theme_cfg
        self.configure(bg=t["bg"])

    def _create_menus(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Game
        self.game_menu = tk.Menu(self.menubar, tearoff=0)
        self.game_menu.add_command(label=T(self.lang, "new_game"), command=self.reset_game, accelerator="F2")
        self.diff_menu = tk.Menu(self.game_menu, tearoff=0)
        self.diff_menu.add_command(label=T(self.lang, "beginner"), command=lambda: self._set_diff("beginner"))
        self.diff_menu.add_command(label=T(self.lang, "intermediate"), command=lambda: self._set_diff("intermediate"))
        self.diff_menu.add_command(label=T(self.lang, "expert"), command=lambda: self._set_diff("expert"))
        self.diff_menu.add_separator()
        self.diff_menu.add_command(label=T(self.lang, "custom"), command=self._custom_diff)
        self.game_menu.add_cascade(label=T(self.lang, "difficulty"), menu=self.diff_menu)
        self.game_menu.add_separator()
        self.game_menu.add_command(label=T(self.lang, "exit"), command=self._confirm_exit, accelerator="Esc")
        self.menubar.add_cascade(label=T(self.lang, "game"), menu=self.game_menu)

        # View (fullscreen, theme)
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_checkbutton(label=T(self.lang, "fullscreen"), command=self.toggle_fullscreen)
        self.theme_menu = tk.Menu(self.view_menu, tearoff=0)
        self.theme_menu.add_command(label=T(self.lang, "light"), command=lambda: self._set_theme("light"))
        self.theme_menu.add_command(label=T(self.lang, "dark"), command=lambda: self._set_theme("dark"))
        self.view_menu.add_cascade(label=T(self.lang, "theme"), menu=self.theme_menu)
        self.menubar.add_cascade(label=T(self.lang, "view"), menu=self.view_menu)

        # Language
        self.lang_menu = tk.Menu(self.menubar, tearoff=0)
        for code, name in LANGUAGES.items():
            self.lang_menu.add_command(label=name, command=lambda c=code: self._set_language(c))
        self.menubar.add_cascade(label=T(self.lang, "language"), menu=self.lang_menu)

        # Help
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label=T(self.lang, "about"), command=lambda: messagebox.showinfo(T(self.lang, "about"), T(self.lang, "about_text")))
        self.menubar.add_cascade(label=T(self.lang, "help"), menu=self.help_menu)

    def _refresh_menus(self):
        self._create_menus()

    def _create_top_panel(self):
        t = self.theme_cfg
        self.topbar = tk.Frame(self, bg=t["bg"], padx=8, pady=8)
        self.topbar.grid(row=0, column=0, sticky="ew")

        # FIX: Start with "000" at UI creation; will set correct mines after board is created
        self.mine_var = tk.StringVar(value="000")
        self.mine_label = tk.Label(self.topbar, textvariable=self.mine_var, font=("Consolas", 16, "bold"),
                                   fg=t["counter"], bg=t["bg"])
        self.mine_label.grid(row=0, column=0, padx=6)

        self.face_btn = tk.Button(self.topbar, text=FACE_DEFAULT, font=("Segoe UI Emoji", 16), width=3,
                                  command=self.reset_game, bg=self.theme_cfg["panel"], activebackground=self.theme_cfg["panel_dark"],
                                  fg=t["text"], relief="raised")
        self.face_btn.grid(row=0, column=1, padx=6)

        self.time_var = tk.StringVar(value="000")
        self.time_label = tk.Label(self.topbar, textvariable=self.time_var, font=("Consolas", 16, "bold"),
                                   fg=t["time"], bg=t["bg"])
        self.time_label.grid(row=0, column=2, padx=6)

    def _create_board_area(self):
        t = self.theme_cfg
        self.board_outer = tk.Frame(self, bg=t["panel_dark"], padx=6, pady=6)
        self.board_outer.grid(row=1, column=0)
        self.board_frame = tk.Frame(self.board_outer, bg=t["panel"])
        self.board_frame.grid(row=0, column=0)

    def _bind_shortcuts(self):
        self.bind("<F2>", lambda e: self.reset_game())
        self.bind("<Escape>", lambda e: self._confirm_exit())
        self.bind("<F11>", lambda e: self.toggle_fullscreen())

    # ---- Theme / Language / Fullscreen ----
    def _set_theme(self, theme):
        if theme not in THEMES: return
        self.theme = theme
        self.theme_cfg = THEMES[theme]
        self.number_colors = self.theme_cfg["num_colors"]
        self._apply_theme_colors()
        # repaint topbar
        self.topbar.configure(bg=self.theme_cfg["bg"])
        self.mine_label.configure(bg=self.theme_cfg["bg"], fg=self.theme_cfg["counter"])
        self.time_label.configure(bg=self.theme_cfg["bg"], fg=self.theme_cfg["time"])
        self.face_btn.configure(bg=self.theme_cfg["panel"], activebackground=self.theme_cfg["panel_dark"], fg=self.theme_cfg["text"])
        # repaint board
        self.board_outer.configure(bg=self.theme_cfg["panel_dark"])
        self.board_frame.configure(bg=self.theme_cfg["panel"])
        self._repaint_board()

    def _set_language(self, code):
        if code not in I18N: return
        self.lang = code
        self._refresh_menus()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        try:
            self.attributes("-fullscreen", self.fullscreen)
        except Exception:
            pass

    # ---- Difficulty / Game control ----
    def _set_diff(self, diff):
        if diff not in DIFFICULTIES: return
        self.current_diff = diff
        r, c, m = DIFFICULTIES[diff]
        self._new_game(r, c, m)

    def _custom_diff(self):
        lang = self.lang
        title = T(lang, "custom_prompt_title")
        try:
            rows = simpledialog.askinteger(title, T(lang, "rows_prompt"), minvalue=5, maxvalue=24, parent=self)
            if rows is None: return
            cols = simpledialog.askinteger(title, T(lang, "cols_prompt"), minvalue=5, maxvalue=40, parent=self)
            if cols is None: return
            max_m = rows*cols - 1
            mines = simpledialog.askinteger(title, T(lang, "mines_prompt"), minvalue=1, maxvalue=max_m, parent=self)
            if mines is None: return
        except Exception:
            messagebox.showerror(title, T(lang, "invalid_custom"))
            return
        if not (5 <= rows <= 24 and 5 <= cols <= 40 and 1 <= mines <= rows*cols - 1):
            messagebox.showerror(title, T(lang, "invalid_custom"))
            return
        self.current_diff = "custom"
        self._new_game(rows, cols, mines)

    def _new_game(self, rows, cols, mines):
        for ch in self.board_frame.winfo_children():
            ch.destroy()
        self.board = Board(rows, cols, mines)
        self.btns = [[None]*cols for _ in range(rows)]
        self.game_over = False
        self.first_click = True

        # FIX: Ensure proper timer reset and mine counter initialization
        self._stop_timer()
        self.start_time = None
        self.time_var.set("000")
        self.face_btn.config(text=FACE_DEFAULT)

        self._build_buttons(rows, cols)
        # FIX: Immediately show correct remaining mines (mines_total - flags)
        self._update_mine_counter()

        # Adaptive window size; keep fullscreen state
        width = cols * 32 + 24
        height = rows * 32 + 140
        if not self.fullscreen:
            try:
                self.geometry(f"{width}x{height}")
            except Exception:
                pass

    def reset_game(self):
        if self.board:
            self._new_game(self.board.rows, self.board.cols, self.board.mines_total)

    # ---- Buttons / events ----
    def _build_buttons(self, rows, cols):
        for r in range(rows):
            for c in range(cols):
                btn = tk.Button(
                    self.board_frame, text="", width=2, height=1,
                    font=("Segoe UI", 12, "bold"),
                    bg=self.theme_cfg["cell_up"], fg=self.theme_cfg["text"],
                    activebackground=self.theme_cfg["cell_down"],
                    relief="raised", bd=2
                )
                btn.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                btn.bind("<Button-1>", self._mk_left(r, c))
                btn.bind("<Double-Button-1>", self._mk_chord(r, c))
                btn.bind("<Button-3>", self._mk_right(r, c))
                btn.bind("<Control-Button-1>", self._mk_right(r, c))
                btn.bind("<Enter>", self._mk_hover_in(r, c))
                btn.bind("<Leave>", self._mk_hover_out(r, c))
                self.btns[r][c] = btn

        for r in range(rows):
            self.board_frame.grid_rowconfigure(r, weight=1)
        for c in range(cols):
            self.board_frame.grid_columnconfigure(c, weight=1)

    def _mk_left(self, r, c):
        def h(e):
            if self.game_over: return
            self._on_left(r, c)
        return h

    def _mk_right(self, r, c):
        def h(e):
            if self.game_over: return
            self._on_right(r, c)
        return h

    def _mk_chord(self, r, c):
        def h(e):
            if self.game_over: return
            self._on_chord(r, c)
        return h

    def _mk_hover_in(self, r, c):
        def h(e):
            if self.game_over: return
            if self.board.state[r][c] == "hidden" or self.board.state[r][c] == "flagged":
                self.btns[r][c].configure(bg=self.theme_cfg["hover"])
        return h

    def _mk_hover_out(self, r, c):
        def h(e):
            if self.game_over: return
            state = self.board.state[r][c]
            if state in ("hidden", "flagged"):
                self.btns[r][c].configure(bg=self.theme_cfg["cell_up"])
        return h

    def _on_left(self, r, c):
        if self.board.state[r][c] == "flagged":
            return
        if self.first_click:
            self.board.place_mines(r, c)
            self.first_click = False
            self._start_timer()
        hit, newly = self.board.reveal(r, c)
        if hit:
            self._reveal_all_mines(bang=(r, c))
            self._lose()
            self.audio.play("boom")
            return
        self._render_new(newly)
        self.audio.play("click")
        if self.board.is_win():
            self._win()

    def _on_right(self, r, c):
        delta = self.board.toggle_flag(r, c)
        if delta is None: return
        btn = self.btns[r][c]
        if self.board.state[r][c] == "flagged":
            btn.config(text=FLAG, fg=self.theme_cfg["counter"])
            self.audio.play("flag")
        else:
            btn.config(text="")
        self._update_mine_counter()

    def _on_chord(self, r, c):
        hit, newly = self.board.chord_reveal(r, c)
        if hit:
            self._reveal_all_mines()
            self._lose()
            self.audio.play("boom")
            return
        self._render_new(newly)
        if newly:
            self.audio.play("click")
        if newly and self.board.is_win():
            self._win()

    # ---- Rendering ----
    def _render_new(self, cells):
        for (r, c) in cells:
            btn = self.btns[r][c]
            btn.config(relief="sunken", bg=self.theme_cfg["cell_down"], activebackground=self.theme_cfg["cell_down"])
            val = self.board.number[r][c]
            if val == 0:
                btn.config(text="", fg=self.theme_cfg["text"])
            else:
                btn.config(text=str(val), fg=self.number_colors.get(val, self.theme_cfg["text"]))

    def _reveal_all_mines(self, bang=None):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                btn = self.btns[r][c]
                if self.board.is_mine[r][c]:
                    btn.config(text=MINE, fg=self.theme_cfg["text"], relief="sunken",
                               bg=(self.theme_cfg["mine_bang_bg"] if (bang == (r, c)) else self.theme_cfg["mine_bg"]))
                elif self.board.state[r][c] == "flagged" and not self.board.is_mine[r][c]:
                    btn.config(text="✖", fg=self.theme_cfg["counter"], relief="sunken", bg=self.theme_cfg["wrong_flag_bg"])

    def _repaint_board(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                btn = self.btns[r][c]
                st = self.board.state[r][c]
                if st == "hidden":
                    btn.config(text="", bg=self.theme_cfg["cell_up"], activebackground=self.theme_cfg["cell_down"],
                               fg=self.theme_cfg["text"], relief="raised")
                elif st == "flagged":
                    btn.config(text=FLAG, bg=self.theme_cfg["cell_up"], activebackground=self.theme_cfg["cell_down"],
                               fg=self.theme_cfg["counter"], relief="raised")
                elif st == "revealed":
                    btn.config(bg=self.theme_cfg["cell_down"], activebackground=self.theme_cfg["cell_down"], relief="sunken")
                    val = self.board.number[r][c]
                    if val > 0:
                        btn.config(text=str(val), fg=self.number_colors.get(val, self.theme_cfg["text"]))
                    else:
                        btn.config(text="", fg=self.theme_cfg["text"])

    # ---- End states ----
    def _lose(self):
        self.game_over = True
        self.face_btn.config(text=FACE_LOST)
        self._stop_timer()
        messagebox.showinfo(T(self.lang, "you_lose"), T(self.lang, "you_lose"))

    def _win(self):
        self.game_over = True
        self.face_btn.config(text=FACE_WON)
        self._stop_timer()
        elapsed = int(self.time_var.get())
        # Auto-flag remaining mines
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.is_mine[r][c] and self.board.state[r][c] != "flagged":
                    self.board.state[r][c] = "flagged"
                    self.btns[r][c].config(text=FLAG, fg="#2E7D32")
        self._update_mine_counter()
        self.audio.play("win")

        diff_label = {
            "beginner": T(self.lang, "beginner"),
            "intermediate": T(self.lang, "intermediate"),
            "expert": T(self.lang, "expert"),
            "custom": T(self.lang, "custom"),
        }.get(self.current_diff, "Custom")

        msg = T(self.lang, "cleared_in", seconds=elapsed)
        new_record = False
        if self.current_diff in ("beginner", "intermediate", "expert"):
            best = self.best_times.get(self.current_diff)
            if best is None or elapsed < best:
                self.best_times[self.current_diff] = elapsed
                self._save_best()
                new_record = True
        if new_record:
            msg += f"\n{T(self.lang, 'new_record', difficulty=diff_label.split('(')[0].strip(), seconds=elapsed)}"
        messagebox.showinfo(T(self.lang, "you_win"), msg)

    # ---- Timer / counters ----
    def _start_timer(self):
        if self.start_time is None:
            self.start_time = time.time()
            self._tick_timer()

    def _tick_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.time_var.set(f"{min(elapsed, 999):03d}")
        self.timer_job = self.after(1000, self._tick_timer)

    def _stop_timer(self):
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

    def _update_mine_counter(self):
        remaining = max(0, self.board.mines_total - self.board.flag_count) if self.board else 0
        self.mine_var.set(f"{min(remaining, 999):03d}")
        self.mine_label.configure(fg=self.theme_cfg["counter"])
        self.time_label.configure(fg=self.theme_cfg["time"])

    # ---- About / Exit ----
    def _confirm_exit(self):
        if messagebox.askokcancel(T(self.lang, "confirm_exit_title"), T(self.lang, "confirm_exit_text")):
            try:
                if PYGAME_AVAILABLE:
                    pygame.mixer.quit()
            except Exception:
                pass
            self.destroy()

    # ---- Best times ----
    def _load_best(self):
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {k: int(v) for k, v in data.items() if k in DIFFICULTIES}
        except Exception:
            pass
        return {}

    def _save_best(self):
        try:
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.best_times, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()