import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import hashlib
import os
import re
import sys
from datetime import datetime
import csv
import json
import webbrowser

# ============================================================
# OPTIONAL LIBRARIES
# ============================================================

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        PageBreak,
        KeepTogether
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ============================================================
# RESOURCE PATH (PyInstaller --onefile support)
# ============================================================

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# ============================================================
# HASHFORGE
# Complete File Integrity / Hashing Application
# ============================================================


class HashForgeApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.title("HashForge - File Integrity System")
        self.geometry("1450x850")
        self.minsize(1100, 700)

        # ----------------------------------------------------
        # LOGO / APP ICON
        # ----------------------------------------------------

        self.logo_path = resource_path("logo.jpeg")

        self.logo_image = None

        self.icon_path_ico = resource_path("logo.ico")
        self.icon_path_jpeg = resource_path("logo.jpeg")

        self.window_icon_image = None

        self.set_window_icon()

        # ----------------------------------------------------
        # THEMES
        # ----------------------------------------------------

        self.themes = {

            "Emerald": {
                "bg": "#F5F7F9",
                "sidebar": "#F8FAFB",
                "white": "#FFFFFF",
                "primary": "#087F6B",
                "primary_dark": "#056653",
                "primary_light": "#DDF4EE",
                "text": "#172033",
                "secondary": "#667085",
                "muted": "#98A2B3",
                "border": "#E4E7EC",
                "success": "#12B76A",
                "danger": "#F04438",
                "warning": "#F79009",
                "card_icon": "#123D35",
                "hover": "#E8F5F1",
                "active_text": "#087F6B",
                "content": "#F7F8FA",
                "table_heading": "#087F6B"
            },

            "Midnight": {
                "bg": "#101418",
                "sidebar": "#151B21",
                "white": "#1B232B",
                "primary": "#20C997",
                "primary_dark": "#159B76",
                "primary_light": "#183D36",
                "text": "#F2F4F7",
                "secondary": "#AAB4C0",
                "muted": "#66717D",
                "border": "#2D3742",
                "success": "#32D583",
                "danger": "#F97066",
                "warning": "#FDB022",
                "card_icon": "#0C3D32",
                "hover": "#20352F",
                "active_text": "#20C997",
                "content": "#151B21",
                "table_heading": "#20C997"
            },

            "Ocean": {
                "bg": "#F2F8FC",
                "sidebar": "#F6FAFD",
                "white": "#FFFFFF",
                "primary": "#087EA4",
                "primary_dark": "#05617F",
                "primary_light": "#D9F0F8",
                "text": "#102A43",
                "secondary": "#627D98",
                "muted": "#829AB1",
                "border": "#D9E2EC",
                "success": "#18A558",
                "danger": "#D64545",
                "warning": "#D9822B",
                "card_icon": "#103B52",
                "hover": "#E5F4FA",
                "active_text": "#087EA4",
                "content": "#F5F9FC",
                "table_heading": "#087EA4"
            },

            "Royal": {
                "bg": "#F7F5FC",
                "sidebar": "#FAF9FD",
                "white": "#FFFFFF",
                "primary": "#6D28D9",
                "primary_dark": "#5521AD",
                "primary_light": "#EDE5FF",
                "text": "#211A35",
                "secondary": "#6F6682",
                "muted": "#9B93AA",
                "border": "#E5E0EF",
                "success": "#12B76A",
                "danger": "#E04444",
                "warning": "#D99000",
                "card_icon": "#392060",
                "hover": "#F0EAFF",
                "active_text": "#6D28D9",
                "content": "#F8F6FC",
                "table_heading": "#6D28D9"
            }
        }

        # ----------------------------------------------------
        # CURRENT THEME
        # ----------------------------------------------------

        self.current_theme = "Emerald"
        self.colors = self.themes[self.current_theme]

        self.configure(
            bg=self.colors["bg"]
        )

        # ----------------------------------------------------
        # FONTS
        # ----------------------------------------------------

        self.fonts = {
            "title": ("Segoe UI", 25, "bold"),
            "subtitle": ("Segoe UI", 10),
            "section": ("Segoe UI", 11, "bold"),
            "normal": ("Segoe UI", 10),
            "small": ("Segoe UI", 9),
            "card_number": ("Segoe UI", 22, "bold"),
            "card_label": ("Segoe UI", 9),
            "button": ("Segoe UI", 10, "bold"),
            "sidebar": ("Segoe UI", 10),
        }

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.current_page = "Dashboard"

        self.stats = {
            "files": 0,
            "errors": 0,
            "last_scan": "--",
            "algorithms": 6
        }

        self.recent_scans = []
        self.recent_exports = []

        self.selected_files = []
        self.hash_results = []
        self.history = []

        self.verify_file = None

        # ----------------------------------------------------
        # DUPLICATE FINDER STATE
        # ----------------------------------------------------

        self.duplicate_files = []
        self.duplicate_groups = []
        self.duplicate_algorithm_var = None
        self.duplicate_subfolders_var = None

        self.algorithms = {
            "MD5": "md5",
            "SHA-1": "sha1",
            "SHA-224": "sha224",
            "SHA-256": "sha256",
            "SHA-384": "sha384",
            "SHA-512": "sha512"
        }

        self.algorithm_vars = {}

        # ----------------------------------------------------
        # CASE INFORMATION
        # ----------------------------------------------------

        self.case_information = {
            "case_name": "",
            "base_directory": "",
            "case_type": "Single-user",
            "case_number": "",
            "examiner_name": "",
            "phone": "",
            "email": "",
            "organization": "",
            "notes": ""
        }

        # ----------------------------------------------------
        # MAIN LAYOUT
        # ----------------------------------------------------

        self.apply_ttk_style()
        self.create_layout()
        self.create_menu()
        self.show_dashboard()

    # ========================================================
    # LOGO
    # ========================================================

    def load_logo(self, width=48, height=48):

        if not PIL_AVAILABLE:
            return None

        if not os.path.exists(self.logo_path):
            return None

        try:

            image = Image.open(
                self.logo_path
            ).convert("RGB")

            image.thumbnail(
                (width, height),
                Image.Resampling.LANCZOS
            )

            canvas = Image.new(
                "RGB",
                (width, height),
                self.colors["sidebar"]
            )

            x = (width - image.width) // 2
            y = (height - image.height) // 2

            canvas.paste(
                image,
                (x, y)
            )

            self.logo_image = ImageTk.PhotoImage(
                canvas
            )

            return self.logo_image

        except Exception:
            return None

    # ========================================================
    # APP ICON (TITLEBAR / TASKBAR)
    # ========================================================

    def set_window_icon(self):

        if os.path.exists(self.icon_path_ico):

            try:

                self.iconbitmap(
                    self.icon_path_ico
                )

                return

            except Exception:
                pass

        if not PIL_AVAILABLE:
            return

        if not os.path.exists(self.icon_path_jpeg):
            return

        try:

            icon_source = Image.open(
                self.icon_path_jpeg
            ).convert("RGBA")

            self.window_icon_image = ImageTk.PhotoImage(
                icon_source
            )

            self.iconphoto(
                True,
                self.window_icon_image
            )

        except Exception:
            pass

    # ========================================================
    # MENU
    # ========================================================

    def create_menu(self):

        menubar = tk.Menu(
            self,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["primary_light"],
            activeforeground=self.colors["primary"],
            tearoff=False
        )

        # ----------------------------------------------------
        # FILE
        # ----------------------------------------------------

        file_menu = tk.Menu(
            menubar,
            tearoff=False,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["primary_light"],
            activeforeground=self.colors["primary"]
        )

        file_menu.add_command(
            label="New Scan",
            accelerator="Ctrl+N",
            command=self.show_scan
        )

        file_menu.add_command(
            label="Select Files",
            accelerator="Ctrl+O",
            command=self.select_files
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Export PDF Report",
            command=self.export_pdf_report
        )

        file_menu.add_command(
            label="Export CSV",
            command=self.export_csv
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            accelerator="Alt+F4",
            command=self.destroy
        )

        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        # ----------------------------------------------------
        # VIEW
        # ----------------------------------------------------

        view_menu = tk.Menu(
            menubar,
            tearoff=False,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["primary_light"],
            activeforeground=self.colors["primary"]
        )

        view_menu.add_command(
            label="Dashboard",
            command=self.show_dashboard
        )

        view_menu.add_command(
            label="Scan",
            command=self.show_scan
        )

        view_menu.add_separator()

        view_menu.add_command(
            label="Verify",
            command=self.show_verify
        )

        view_menu.add_command(
            label="History",
            command=self.show_history
        )

        view_menu.add_command(
            label="Duplicates",
            command=self.show_duplicates
        )

        view_menu.add_separator()

        view_menu.add_command(
            label="Settings",
            command=self.show_settings
        )

        menubar.add_cascade(
            label="View",
            menu=view_menu
        )

        # ----------------------------------------------------
        # TOOLS
        # ----------------------------------------------------

        tools_menu = tk.Menu(
            menubar,
            tearoff=False,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["primary_light"],
            activeforeground=self.colors["primary"]
        )

        tools_menu.add_command(
            label="Generate Hashes",
            command=self.generate_hashes
        )

        tools_menu.add_command(
            label="Export PDF Report",
            command=self.export_pdf_report
        )

        tools_menu.add_command(
            label="Export CSV",
            command=self.export_csv
        )

        tools_menu.add_separator()

        tools_menu.add_command(
            label="Clear Selected Files",
            command=self.clear_selected_files
        )

        tools_menu.add_command(
            label="Clear Results",
            command=self.clear_hash_results
        )

        menubar.add_cascade(
            label="Tools",
            menu=tools_menu
        )

        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        help_menu = tk.Menu(
            menubar,
            tearoff=False,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["primary_light"],
            activeforeground=self.colors["primary"]
        )

        help_menu.add_command(
            label="About HashForge",
            command=self.show_about
        )

        help_menu.add_command(
            label="Supported Algorithms",
            command=self.show_algorithms_help
        )

        help_menu.add_separator()

        help_menu.add_command(
            label="Keyboard Shortcuts",
            command=self.show_shortcuts
        )

        menubar.add_cascade(
            label="Help",
            menu=help_menu
        )

        self.config(
            menu=menubar
        )

        # ----------------------------------------------------
        # SHORTCUTS
        # ----------------------------------------------------

        self.bind(
            "<Control-n>",
            lambda event: self.show_scan()
        )

        self.bind(
            "<Control-o>",
            lambda event: self.select_files()
        )

        self.bind(
            "<Control-l>",
            lambda event: self.clear_selected_files()
        )

        self.bind(
            "<Escape>",
            lambda event: self.clear_selected_files()
        )

    # ========================================================
    # THEME
    # ========================================================

    def change_theme(self, theme_name):

        if theme_name not in self.themes:
            return

        self.current_theme = theme_name
        self.colors = self.themes[theme_name]

        self.configure(
            bg=self.colors["bg"]
        )

        self.apply_ttk_style()

        self.main_container.configure(
            bg=self.colors["bg"]
        )

        self.main_canvas.configure(
            bg=self.colors["bg"]
        )

        self.main_area.configure(
            bg=self.colors["bg"]
        )

        for widget in self.sidebar.winfo_children():
            widget.destroy()

        self.sidebar.configure(
            bg=self.colors["sidebar"]
        )

        self.create_sidebar()

        if self.current_page == "Dashboard":
            self.show_dashboard()

        elif self.current_page == "Scan":
            self.show_scan()

        elif self.current_page == "Verify":
            self.show_verify()

        elif self.current_page == "Export":
            self.show_export()

        elif self.current_page == "History":
            self.show_history()

        elif self.current_page == "Duplicates":
            self.show_duplicates()

        elif self.current_page == "Settings":
            self.show_settings()

    # ========================================================
    # TTK STYLE (Treeview / Combobox / Scrollbar theming)
    # ========================================================

    def apply_ttk_style(self):

        style = ttk.Style(self)

        style.theme_use("clam")

        # Treeview

        style.configure(
            "Treeview",
            background=self.colors["white"],
            fieldbackground=self.colors["white"],
            foreground=self.colors["text"],
            bordercolor=self.colors["border"],
            borderwidth=0,
            rowheight=30,
            font=self.fonts["normal"]
        )

        style.map(
            "Treeview",
            background=[
                ("selected", self.colors["primary"])
            ],
            foreground=[
                ("selected", "#FFFFFF")
            ]
        )

        style.configure(
            "Treeview.Heading",
            background=self.colors["sidebar"],
            foreground=self.colors["text"],
            relief="flat",
            borderwidth=1,
            font=self.fonts["section"]
        )

        style.map(
            "Treeview.Heading",
            background=[
                ("active", self.colors["hover"])
            ]
        )

        # Combobox

        style.configure(
            "TCombobox",
            fieldbackground=self.colors["white"],
            background=self.colors["white"],
            foreground=self.colors["text"],
            arrowcolor=self.colors["text"],
            bordercolor=self.colors["border"],
            selectbackground=self.colors["white"],
            selectforeground=self.colors["text"]
        )

        style.map(
            "TCombobox",
            fieldbackground=[
                ("readonly", self.colors["white"]),
                ("disabled", self.colors["white"])
            ],
            foreground=[
                ("readonly", self.colors["text"]),
                ("disabled", self.colors["muted"])
            ]
        )

        self.option_add(
            "*TCombobox*Listbox*Background",
            self.colors["white"]
        )

        self.option_add(
            "*TCombobox*Listbox*Foreground",
            self.colors["text"]
        )

        self.option_add(
            "*TCombobox*Listbox*selectBackground",
            self.colors["primary"]
        )

        self.option_add(
            "*TCombobox*Listbox*selectForeground",
            "#FFFFFF"
        )

        # Scrollbars

        style.configure(
            "Vertical.TScrollbar",
            background=self.colors["border"],
            troughcolor=self.colors["bg"],
            arrowcolor=self.colors["text"],
            bordercolor=self.colors["bg"],
            relief="flat"
        )

        style.map(
            "Vertical.TScrollbar",
            background=[
                ("active", self.colors["secondary"])
            ]
        )

        style.configure(
            "Horizontal.TScrollbar",
            background=self.colors["border"],
            troughcolor=self.colors["bg"],
            arrowcolor=self.colors["text"],
            bordercolor=self.colors["bg"],
            relief="flat"
        )

        style.map(
            "Horizontal.TScrollbar",
            background=[
                ("active", self.colors["secondary"])
            ]
        )

    # ========================================================
    # ABOUT
    # ========================================================

    def show_about(self):

        messagebox.showinfo(
            "About HashForge",
            "HashForge Desktop\n\n"
            "Version 1.0.0\n"
            "File Integrity System\n\n"
            "Local file hashing and integrity "
            "verification application.\n\n"
            "All hashing operations are performed "
            "locally on your computer."
        )

    # ========================================================
    # ALGORITHM HELP
    # ========================================================

    def show_algorithms_help(self):

        messagebox.showinfo(
            "Supported Algorithms",
            "HashForge supports:\n\n"
            "• MD5\n"
            "• SHA-1\n"
            "• SHA-224\n"
            "• SHA-256\n"
            "• SHA-384\n"
            "• SHA-512\n\n"
            "SHA-256 and SHA-512 are preferred "
            "for modern integrity checking."
        )

    # ========================================================
    # SHORTCUTS
    # ========================================================

    def show_shortcuts(self):

        messagebox.showinfo(
            "Keyboard Shortcuts",
            "HashForge Shortcuts\n\n"
            "Ctrl + N    New Scan\n"
            "Ctrl + O    Select Files\n"
            "Ctrl + L    Clear Selected Files\n"
            "Esc         Clear Selected Files\n"
            "Alt + F4    Exit Application\n\n"
            "Double-click a hash to copy it."
        )

    # ========================================================
    # LAYOUT
    # ========================================================

    def create_layout(self):

        self.sidebar = tk.Frame(
            self,
            bg=self.colors["sidebar"],
            width=275
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        self.main_container = tk.Frame(
            self,
            bg=self.colors["bg"]
        )

        self.main_container.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SCROLLABLE MAIN AREA
        # (so pages that overflow the window height, like
        # Dashboard's "Recent Exports" section, stay reachable
        # instead of being cut off)
        # ----------------------------------------------------

        self.main_canvas = tk.Canvas(
            self.main_container,
            bg=self.colors["bg"],
            highlightthickness=0
        )

        self.main_scrollbar = ttk.Scrollbar(
            self.main_container,
            orient="vertical",
            command=self.main_canvas.yview
        )

        self.main_canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        self.main_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.main_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.main_area = tk.Frame(
            self.main_canvas,
            bg=self.colors["bg"]
        )

        self.main_area_window = self.main_canvas.create_window(
            (0, 0),
            window=self.main_area,
            anchor="nw"
        )

        def _on_main_area_configure(event):

            self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )

        self.main_area.bind(
            "<Configure>",
            _on_main_area_configure
        )

        def _on_canvas_configure(event):

            self.main_canvas.itemconfigure(
                self.main_area_window,
                width=event.width
            )

        self.main_canvas.bind(
            "<Configure>",
            _on_canvas_configure
        )

        def _on_mousewheel(event):

            self.main_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        def _bind_mousewheel(event):

            self.main_canvas.bind_all(
                "<MouseWheel>",
                _on_mousewheel
            )

        def _unbind_mousewheel(event):

            self.main_canvas.unbind_all(
                "<MouseWheel>"
            )

        self.main_canvas.bind(
            "<Enter>",
            _bind_mousewheel
        )

        self.main_canvas.bind(
            "<Leave>",
            _unbind_mousewheel
        )

        self.create_sidebar()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        brand_frame = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )

        brand_frame.pack(
            fill="x",
            padx=25,
            pady=(28, 25)
        )

        logo_image = self.load_logo(
            width=52,
            height=52
        )

        if logo_image:

            logo_label = tk.Label(
                brand_frame,
                image=logo_image,
                bg=self.colors["sidebar"],
                borderwidth=0
            )

            logo_label.image = logo_image

            logo_label.pack(
                side="left"
            )

        else:

            logo = tk.Canvas(
                brand_frame,
                width=48,
                height=48,
                bg=self.colors["sidebar"],
                highlightthickness=0
            )

            logo.pack(
                side="left"
            )

            logo.create_oval(
                3,
                3,
                45,
                45,
                fill=self.colors["primary_light"],
                outline=""
            )

            logo.create_text(
                24,
                24,
                text="#",
                fill=self.colors["primary"],
                font=("Segoe UI", 19, "bold")
            )

        brand_text = tk.Frame(
            brand_frame,
            bg=self.colors["sidebar"]
        )

        brand_text.pack(
            side="left",
            padx=10
        )

        tk.Label(
            brand_text,
            text="HashForge",
            bg=self.colors["sidebar"],
            fg=self.colors["text"],
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            brand_text,
            text="File Integrity System",
            bg=self.colors["sidebar"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 8)
        ).pack(
            anchor="w"
        )

        self.nav_buttons = {}

        self.create_nav_button(
            "⌂",
            "Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "⌕",
            "Scan",
            self.show_scan
        )

        tk.Frame(
            self.sidebar,
            height=1,
            bg=self.colors["border"]
        ).pack(
            fill="x",
            padx=22,
            pady=(12, 18)
        )

        tk.Label(
            self.sidebar,
            text="TOOLS",
            bg=self.colors["sidebar"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 8)
        )

        self.create_nav_button(
            "✓",
            "Verify",
            self.show_verify
        )

        self.create_nav_button(
            "⇩",
            "Export",
            self.show_export
        )

        self.create_nav_button(
            "▤",
            "History",
            self.show_history
        )

        self.create_nav_button(
            "▣",
            "Duplicates",
            self.show_duplicates
        )

        tk.Frame(
            self.sidebar,
            height=1,
            bg=self.colors["border"]
        ).pack(
            fill="x",
            padx=22,
            pady=(18, 18)
        )

        self.create_nav_button(
            "⚙",
            "Settings",
            self.show_settings
        )

        bottom_frame = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )

        bottom_frame.pack(
            side="bottom",
            fill="x",
            padx=35,
            pady=25
        )

        tk.Label(
            bottom_frame,
            text="HashForge v1.0.0",
            bg=self.colors["sidebar"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )

        tk.Label(
            bottom_frame,
            text="●  Local Processing • Secure",
            bg=self.colors["sidebar"],
            fg=self.colors["primary"],
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

    # ========================================================
    # NAV BUTTON
    # ========================================================

    def create_nav_button(
        self,
        icon,
        text,
        command
    ):

        frame = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"],
            cursor="hand2"
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=2
        )

        icon_label = tk.Label(
            frame,
            text=icon,
            width=4,
            bg=self.colors["sidebar"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 13)
        )

        icon_label.pack(
            side="left",
            padx=(5, 0)
        )

        text_label = tk.Label(
            frame,
            text=text,
            bg=self.colors["sidebar"],
            fg=self.colors["secondary"],
            font=self.fonts["sidebar"],
            anchor="w"
        )

        text_label.pack(
            side="left",
            fill="x",
            expand=True,
            pady=11
        )

        self.nav_buttons[text] = (
            frame,
            icon_label,
            text_label
        )

        for widget in (
            frame,
            icon_label,
            text_label
        ):

            widget.bind(
                "<Button-1>",
                lambda event, cmd=command: cmd()
            )

            widget.bind(
                "<Enter>",
                lambda event, f=frame:
                self.nav_hover(f, True)
            )

            widget.bind(
                "<Leave>",
                lambda event, f=frame:
                self.nav_hover(f, False)
            )

    # ========================================================
    # NAV HOVER
    # ========================================================

    def nav_hover(
        self,
        frame,
        entering
    ):

        active_frame = self.nav_buttons.get(
            self.current_page,
            (None, None, None)
        )[0]

        if frame != active_frame:

            color = (
                self.colors["hover"]
                if entering
                else self.colors["sidebar"]
            )

            frame.configure(
                bg=color
            )

            for child in frame.winfo_children():
                child.configure(
                    bg=color
                )

    # ========================================================
    # ACTIVE NAV
    # ========================================================

    def set_active_nav(self, name):

        for key, widgets in self.nav_buttons.items():

            frame, icon, label = widgets

            if key == name:

                frame.configure(
                    bg=self.colors["primary_light"]
                )

                icon.configure(
                    bg=self.colors["primary_light"],
                    fg=self.colors["primary"]
                )

                label.configure(
                    bg=self.colors["primary_light"],
                    fg=self.colors["primary"],
                    font=("Segoe UI", 10, "bold")
                )

            else:

                frame.configure(
                    bg=self.colors["sidebar"]
                )

                icon.configure(
                    bg=self.colors["sidebar"],
                    fg=self.colors["secondary"]
                )

                label.configure(
                    bg=self.colors["sidebar"],
                    fg=self.colors["secondary"],
                    font=self.fonts["sidebar"]
                )

        self.current_page = name

    # ========================================================
    # CLEAR MAIN
    # ========================================================

    def clear_main(self):

        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_main()
        self.set_active_nav("Dashboard")

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=35
        )

        header = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        header.pack(
            fill="x"
        )

        title_area = tk.Frame(
            header,
            bg=self.colors["bg"]
        )

        title_area.pack(
            side="left"
        )

        tk.Label(
            title_area,
            text="Dashboard",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_area,
            text="Professional file integrity and hashing",
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        tk.Button(
            header,
            text="+  New Scan",
            command=self.show_scan,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=25,
            pady=12,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="right",
            pady=3
        )

        cards = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        cards.pack(
            fill="x",
            pady=(35, 25)
        )

        self.create_stat_card(
            cards,
            "#",
            "Files Hashed",
            str(self.stats["files"]),
            0
        )

        self.create_stat_card(
            cards,
            "△",
            "Errors",
            str(self.stats["errors"]),
            1
        )

        self.create_stat_card(
            cards,
            "◷",
            "Last Scan Time",
            self.stats["last_scan"],
            2
        )

        self.create_stat_card(
            cards,
            "#",
            "Hash Algorithms",
            str(self.stats["algorithms"]),
            3
        )

        actions = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        actions.pack(
            fill="x",
            pady=(0, 30)
        )

        self.create_action_card(
            actions,
            "⌕",
            "Start New Scan",
            "Scan files and generate cryptographic hashes",
            self.show_scan,
            0
        )

        self.create_action_card(
            actions,
            "✓",
            "Verify Integrity",
            "Compare a file against an expected hash",
            self.show_verify,
            1
        )

        self.create_action_card(
            actions,
            "⇩",
            "Export Report",
            "Export scan results to PDF or CSV",
            self.show_export,
            2
        )

        self.create_recent_section(
            container,
            "Recent Scans",
            "⌕",
            self.recent_scans,
            "No scans yet — start a new scan above"
        )

        self.create_recent_section(
            container,
            "Recent Exports",
            "⇩",
            self.recent_exports,
            "No exports yet"
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        icon,
        label,
        value,
        column
    ):

        card = tk.Frame(
            parent,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        icon_canvas = tk.Canvas(
            card,
            width=48,
            height=48,
            bg=self.colors["white"],
            highlightthickness=0
        )

        icon_canvas.pack(
            side="left",
            padx=(20, 15),
            pady=20
        )

        icon_canvas.create_oval(
            3,
            3,
            45,
            45,
            fill=self.colors["card_icon"],
            outline=""
        )

        icon_canvas.create_text(
            24,
            24,
            text=icon,
            fill=self.colors["primary"],
            font=("Segoe UI", 15, "bold")
        )

        info = tk.Frame(
            card,
            bg=self.colors["white"]
        )

        info.pack(
            side="left",
            pady=18
        )

        tk.Label(
            info,
            text=value,
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["card_number"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            info,
            text=label,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=self.fonts["card_label"]
        ).pack(
            anchor="w"
        )

    # ========================================================
    # ACTION CARD
    # ========================================================

    def create_action_card(
        self,
        parent,
        icon,
        title,
        description,
        command,
        column
    ):

        card = tk.Frame(
            parent,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            cursor="hand2"
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
            ipadx=10,
            ipady=15
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        icon_label = tk.Label(
            card,
            text=icon,
            bg=self.colors["white"],
            fg=self.colors["primary"],
            font=("Segoe UI", 24, "bold")
        )

        icon_label.pack(
            side="left",
            padx=(22, 15)
        )

        text_frame = tk.Frame(
            card,
            bg=self.colors["white"]
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        tk.Label(
            text_frame,
            text=title,
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_frame,
            text=description,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        arrow = tk.Label(
            card,
            text="›",
            bg=self.colors["white"],
            fg=self.colors["muted"],
            font=("Segoe UI", 24)
        )

        arrow.pack(
            side="right",
            padx=20
        )

        for widget in (
            card,
            icon_label,
            text_frame,
            arrow
        ):

            widget.bind(
                "<Button-1>",
                lambda event, cmd=command: cmd()
            )

            widget.bind(
                "<Enter>",
                lambda event, c=card:
                self.action_hover(c, True)
            )

            widget.bind(
                "<Leave>",
                lambda event, c=card:
                self.action_hover(c, False)
            )

    # ========================================================
    # ACTION HOVER
    # ========================================================

    def action_hover(
        self,
        card,
        entering
    ):

        color = (
            self.colors["hover"]
            if entering
            else self.colors["white"]
        )

        card.configure(
            bg=color
        )

        for child in card.winfo_children():

            try:
                child.configure(
                    bg=color
                )
            except tk.TclError:
                pass

            for subchild in child.winfo_children():

                try:
                    subchild.configure(
                        bg=color
                    )
                except tk.TclError:
                    pass

    # ========================================================
    # RECENT SECTION
    # ========================================================

    def create_recent_section(
        self,
        parent,
        title,
        icon,
        data,
        empty_text
    ):

        outer = tk.Frame(
            parent,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        outer.pack(
            fill="x",
            pady=(0, 22)
        )

        header = tk.Frame(
            outer,
            bg=self.colors["white"]
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        tk.Label(
            header,
            text=icon,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 14)
        ).pack(
            side="left"
        )

        tk.Label(
            header,
            text=title,
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            side="left",
            padx=10
        )

        content = tk.Frame(
            outer,
            bg=self.colors["content"],
            height=130
        )

        content.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        content.pack_propagate(False)

        if not data:

            tk.Label(
                content,
                text="□",
                bg=self.colors["content"],
                fg=self.colors["muted"],
                font=("Segoe UI", 30)
            ).pack(
                pady=(18, 0)
            )

            tk.Label(
                content,
                text=empty_text,
                bg=self.colors["content"],
                fg=self.colors["secondary"],
                font=("Segoe UI", 9)
            ).pack(
                pady=(3, 0)
            )

        else:

            for item in data:

                tk.Label(
                    content,
                    text=item,
                    bg=self.colors["content"],
                    fg=self.colors["text"],
                    font=("Segoe UI", 9)
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=5
                )

    # ========================================================
    # SCAN PAGE
    # ========================================================

    def show_scan(self):

        self.clear_main()
        self.set_active_nav("Scan")

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=30
        )

        header = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        header.pack(
            fill="x"
        )

        title_area = tk.Frame(
            header,
            bg=self.colors["bg"]
        )

        title_area.pack(
            side="left"
        )

        tk.Label(
            title_area,
            text="New Scan",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_area,
            text="Select files and generate cryptographic hashes",
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ----------------------------------------------------
        # FILE CARD
        # ----------------------------------------------------

        file_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        file_card.pack(
            fill="x",
            pady=(25, 15)
        )

        file_header = tk.Frame(
            file_card,
            bg=self.colors["white"]
        )

        file_header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        tk.Label(
            file_header,
            text="Selected Files",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            side="left"
        )

        tk.Button(
            file_header,
            text="Clear",
            command=self.clear_selected_files,
            bg=self.colors["white"],
            fg=self.colors["danger"],
            activebackground=self.colors["white"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="right"
        )

        tk.Button(
            file_header,
            text="+  Select Files",
            command=self.select_files,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=8,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="right",
            padx=(0, 10)
        )

        list_frame = tk.Frame(
            file_card,
            bg=self.colors["content"]
        )

        list_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 25)
        )

        self.file_listbox = tk.Listbox(
            list_frame,
            height=5,
            bg=self.colors["content"],
            fg=self.colors["text"],
            selectbackground=self.colors["primary_light"],
            selectforeground=self.colors["text"],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 9)
        )

        self.file_listbox.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.file_scrollbar = tk.Scrollbar(
            list_frame,
            command=self.file_listbox.yview
        )

        self.file_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.file_listbox.configure(
            yscrollcommand=self.file_scrollbar.set
        )

        for file_path in self.selected_files:

            self.file_listbox.insert(
                tk.END,
                os.path.basename(file_path)
            )

        # ----------------------------------------------------
        # ALGORITHM CARD
        # ----------------------------------------------------

        algorithm_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        algorithm_card.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            algorithm_card,
            text="Hash Algorithms",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        tk.Label(
            algorithm_card,
            text="Select one or more algorithms to calculate.",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=25
        )

        algorithms_frame = tk.Frame(
            algorithm_card,
            bg=self.colors["white"]
        )

        algorithms_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 22)
        )

        self.algorithm_vars = {}

        for index, algorithm in enumerate(self.algorithms):

            var = tk.BooleanVar(
                value=algorithm in (
                    "SHA-256",
                    "SHA-512"
                )
            )

            self.algorithm_vars[algorithm] = var

            cb = tk.Checkbutton(
                algorithms_frame,
                text=algorithm,
                variable=var,
                bg=self.colors["white"],
                activebackground=self.colors["white"],
                fg=self.colors["text"],
                activeforeground=self.colors["text"],
                selectcolor=self.colors["primary_light"],
                font=(
                    "Segoe UI",
                    9,
                    "bold"
                    if algorithm in (
                        "SHA-256",
                        "SHA-512"
                    )
                    else "normal"
                ),
                cursor="hand2"
            )

            cb.grid(
                row=0,
                column=index,
                padx=(0, 20),
                sticky="w"
            )

        tk.Label(
            algorithm_card,
            text="⚠ MD5 and SHA-1 are included for compatibility. "
                 "SHA-256 and SHA-512 are preferred for modern integrity checking.",
            bg=self.colors["white"],
            fg=self.colors["warning"],
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 18)
        )

        # ----------------------------------------------------
        # ACTION CARD
        # ----------------------------------------------------

        action_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        action_card.pack(
            fill="x",
            pady=(0, 15)
        )

        action_top = tk.Frame(
            action_card,
            bg=self.colors["white"]
        )

        action_top.pack(
            fill="x",
            padx=25,
            pady=18
        )

        self.generate_button = tk.Button(
            action_top,
            text="⚡  Generate Hashes",
            command=self.generate_hashes,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=25,
            pady=11,
            font=self.fonts["button"],
            cursor="hand2"
        )

        self.generate_button.pack(
            side="left"
        )

        self.status_label = tk.Label(
            action_top,
            text="Ready",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        )

        self.status_label.pack(
            side="left",
            padx=20
        )

        self.progress = ttk.Progressbar(
            action_card,
            orient="horizontal",
            mode="determinate"
        )

        self.progress.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        result_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        result_card.pack(
            fill="both",
            expand=True
        )

        result_header = tk.Frame(
            result_card,
            bg=self.colors["white"]
        )

        result_header.pack(
            fill="x",
            padx=25,
            pady=(18, 10)
        )

        tk.Label(
            result_header,
            text="Hash Results",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            side="left"
        )

        tk.Label(
            result_header,
            text="Double-click a hash to copy it",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 8)
        ).pack(
            side="right"
        )

        table_frame = tk.Frame(
            result_card,
            bg=self.colors["white"]
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        columns = (
            "file",
            "algorithm",
            "hash"
        )

        self.result_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.result_tree.heading(
            "file",
            text="File"
        )

        self.result_tree.heading(
            "algorithm",
            text="Algorithm"
        )

        self.result_tree.heading(
            "hash",
            text="Hash Value"
        )

        self.result_tree.column(
            "file",
            width=300,
            anchor="w"
        )

        self.result_tree.column(
            "algorithm",
            width=130,
            anchor="center"
        )

        self.result_tree.column(
            "hash",
            width=650,
            anchor="w"
        )

        tree_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.result_tree.yview
        )

        self.result_tree.configure(
            yscrollcommand=tree_scroll.set
        )

        self.result_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        tree_scroll.pack(
            side="right",
            fill="y"
        )

        self.result_tree.bind(
            "<Double-1>",
            self.copy_selected_hash
        )

        for result in self.hash_results:

            self.result_tree.insert(
                "",
                tk.END,
                values=(
                    result["file_name"],
                    result["algorithm"],
                    result["hash"]
                )
            )

    # ========================================================
    # SELECT FILES
    # ========================================================

    def select_files(self):

        files = filedialog.askopenfilenames(
            title="Select files to hash"
        )

        if not files:
            return

        added = 0

        for file_path in files:

            if file_path not in self.selected_files:

                self.selected_files.append(
                    file_path
                )

                if hasattr(
                    self,
                    "file_listbox"
                ):

                    self.file_listbox.insert(
                        tk.END,
                        os.path.basename(file_path)
                    )

                added += 1

        if added and hasattr(
            self,
            "status_label"
        ):

            self.status_label.configure(
                text=f"{len(self.selected_files)} file(s) selected",
                fg=self.colors["primary"]
            )

    # ========================================================
    # CLEAR FILES
    # ========================================================

    def clear_selected_files(self):

        self.selected_files.clear()

        if hasattr(
            self,
            "file_listbox"
        ):

            self.file_listbox.delete(
                0,
                tk.END
            )

        if hasattr(
            self,
            "result_tree"
        ):

            for item in self.result_tree.get_children():
                self.result_tree.delete(item)

        self.hash_results.clear()

        if hasattr(
            self,
            "status_label"
        ):

            self.status_label.configure(
                text="Ready",
                fg=self.colors["secondary"]
            )

        if hasattr(
            self,
            "progress"
        ):

            self.progress["value"] = 0

    # ========================================================
    # CLEAR RESULTS
    # ========================================================

    def clear_hash_results(self):

        if hasattr(
            self,
            "result_tree"
        ):

            for item in self.result_tree.get_children():
                self.result_tree.delete(item)

        self.hash_results.clear()

        if hasattr(
            self,
            "progress"
        ):

            self.progress["value"] = 0

        if hasattr(
            self,
            "status_label"
        ):

            self.status_label.configure(
                text="Results cleared",
                fg=self.colors["secondary"]
            )

    # ========================================================
    # SELECTED ALGORITHMS
    # ========================================================

    def get_selected_algorithms(self):

        return [
            algorithm
            for algorithm, variable
            in self.algorithm_vars.items()
            if variable.get()
        ]

    # ========================================================
    # CALCULATE HASH
    # ========================================================

    def calculate_file_hash(
        self,
        file_path,
        algorithm
    ):

        hash_object = hashlib.new(
            self.algorithms[algorithm]
        )

        chunk_size = 1024 * 1024

        with open(
            file_path,
            "rb"
        ) as file:

            while True:

                chunk = file.read(
                    chunk_size
                )

                if not chunk:
                    break

                hash_object.update(
                    chunk
                )

        return hash_object.hexdigest()

    # ========================================================
    # GENERATE HASHES
    # ========================================================

    def generate_hashes(self):

        if not self.selected_files:

            messagebox.showwarning(
                "No Files Selected",
                "Please select at least one file before generating hashes."
            )

            return

        selected_algorithms = (
            self.get_selected_algorithms()
        )

        if not selected_algorithms:

            messagebox.showwarning(
                "No Algorithm Selected",
                "Please select at least one hashing algorithm."
            )

            return

        if not hasattr(
            self,
            "result_tree"
        ):

            self.show_scan()

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.hash_results.clear()

        total_operations = (
            len(self.selected_files)
            * len(selected_algorithms)
        )

        completed = 0
        errors = 0

        self.generate_button.configure(
            state="disabled",
            text="⏳  Generating..."
        )

        self.progress["value"] = 0
        self.progress["maximum"] = total_operations

        self.update_idletasks()

        for file_path in self.selected_files:

            file_name = os.path.basename(
                file_path
            )

            for algorithm in selected_algorithms:

                try:

                    self.status_label.configure(
                        text=(
                            f"Hashing {file_name} • "
                            f"{algorithm}"
                        ),
                        fg=self.colors["primary"]
                    )

                    self.update_idletasks()

                    digest = self.calculate_file_hash(
                        file_path,
                        algorithm
                    )

                    result = {
                        "file": file_path,
                        "file_name": file_name,
                        "algorithm": algorithm,
                        "hash": digest,
                        "timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    }

                    self.hash_results.append(
                        result
                    )

                    history_entry = dict(result)
                    history_entry["type"] = "scan"

                    self.history.insert(
                        0,
                        history_entry
                    )

                    self.result_tree.insert(
                        "",
                        tk.END,
                        values=(
                            file_name,
                            algorithm,
                            digest
                        )
                    )

                except (
                    OSError,
                    PermissionError
                ) as error:

                    errors += 1
                    self.stats["errors"] += 1

                    messagebox.showerror(
                        "File Error",
                        f"Could not read:\n\n"
                        f"{file_path}\n\n"
                        f"Reason:\n{error}"
                    )

                except Exception as error:

                    errors += 1
                    self.stats["errors"] += 1

                    messagebox.showerror(
                        "Hashing Error",
                        f"An unexpected error occurred:\n\n"
                        f"{error}"
                    )

                completed += 1

                self.progress["value"] = completed

                self.update_idletasks()

        self.stats["files"] = len(
            self.selected_files
        )

        self.stats["last_scan"] = (
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )

        scan_text = (
            f"{len(self.selected_files)} file(s) • "
            f"{len(selected_algorithms)} algorithm(s) • "
            f"{datetime.now().strftime('%H:%M:%S')}"
        )

        self.recent_scans.insert(
            0,
            scan_text
        )

        self.recent_scans = (
            self.recent_scans[:5]
        )

        self.generate_button.configure(
            state="normal",
            text="⚡  Generate Hashes"
        )

        if errors == 0:

            self.status_label.configure(
                text=(
                    f"Completed • "
                    f"{len(self.hash_results)} "
                    f"hash(es) generated"
                ),
                fg=self.colors["success"]
            )

            messagebox.showinfo(
                "Hash Generation Complete",
                f"Successfully generated "
                f"{len(self.hash_results)} hash(es)."
            )

        else:

            self.status_label.configure(
                text=(
                    f"Completed with "
                    f"{errors} error(s)"
                ),
                fg=self.colors["warning"]
            )

    # ========================================================
    # COPY HASH
    # ========================================================

    def copy_selected_hash(
        self,
        event=None
    ):

        if not hasattr(
            self,
            "result_tree"
        ):
            return

        selected = self.result_tree.selection()

        if not selected:
            return

        item = self.result_tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if len(values) < 3:
            return

        hash_value = values[2]

        self.clipboard_clear()
        self.clipboard_append(hash_value)
        self.update()

        if hasattr(
            self,
            "status_label"
        ):

            self.status_label.configure(
                text="Hash copied to clipboard",
                fg=self.colors["success"]
            )

    # ========================================================
    # CASE INFORMATION DIALOG
    # ========================================================

    def show_case_information(
        self,
        on_finish=None
    ):

        dialog = tk.Toplevel(self)

        dialog.title(
            "New Case Information"
        )

        dialog.geometry(
            "900x700"
        )

        dialog.minsize(
            850,
            620
        )

        dialog.configure(
            bg=self.colors["white"]
        )

        dialog.transient(self)
        dialog.grab_set()

        # ====================================================
        # MAIN
        # ====================================================

        main = tk.Frame(
            dialog,
            bg=self.colors["white"]
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            main,
            bg=self.colors["white"]
        )

        header.pack(
            fill="x",
            padx=28,
            pady=(20, 12)
        )

        tk.Label(
            header,
            text="New Case Information",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w"
        )

        # ====================================================
        # CONTENT
        # ====================================================

        content = tk.Frame(
            main,
            bg=self.colors["white"]
        )

        content.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 10)
        )

        # ====================================================
        # LEFT STEPS
        # ====================================================

        steps_panel = tk.Frame(
            content,
            bg=self.colors["sidebar"],
            width=220
        )

        steps_panel.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        steps_panel.pack_propagate(False)

        tk.Label(
            steps_panel,
            text="Steps",
            bg=self.colors["sidebar"],
            fg=self.colors["text"],
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(25, 10)
        )

        tk.Frame(
            steps_panel,
            height=1,
            bg=self.colors["border"]
        ).pack(
            fill="x",
            padx=20
        )

        # Step 1

        step1 = tk.Frame(
            steps_panel,
            bg=self.colors["sidebar"]
        )

        step1.pack(
            fill="x",
            padx=18,
            pady=(25, 8)
        )

        tk.Label(
            step1,
            text="1.",
            bg=self.colors["sidebar"],
            fg=self.colors["primary"],
            font=("Segoe UI", 10, "bold"),
            width=3,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            step1,
            text="Case Information",
            bg=self.colors["sidebar"],
            fg=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(
            side="left"
        )

        # Step 2

        step2 = tk.Frame(
            steps_panel,
            bg=self.colors["sidebar"]
        )

        step2.pack(
            fill="x",
            padx=18,
            pady=8
        )

        tk.Label(
            step2,
            text="2.",
            bg=self.colors["sidebar"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 10, "bold"),
            width=3,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            step2,
            text="Optional Information",
            bg=self.colors["sidebar"],
            fg=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(
            side="left"
        )

        # ====================================================
        # RIGHT CONTAINER
        # ====================================================

        right_container = tk.Frame(
            content,
            bg=self.colors["white"]
        )

        right_container.pack(
            side="left",
            fill="both",
            expand=True
        )

        canvas = tk.Canvas(
            right_container,
            bg=self.colors["white"],
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            right_container,
            orient="vertical",
            command=canvas.yview
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        form = tk.Frame(
            canvas,
            bg=self.colors["white"]
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=form,
            anchor="nw"
        )

        def update_scroll_region(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        form.bind(
            "<Configure>",
            update_scroll_region
        )

        def resize_form(event):

            canvas.itemconfigure(
                canvas_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            resize_form
        )

        # ====================================================
        # VARIABLES
        # ====================================================

        case_name_var = tk.StringVar(
            value=self.case_information.get(
                "case_name",
                ""
            )
        )

        base_directory_var = tk.StringVar(
            value=self.case_information.get(
                "base_directory",
                os.path.expanduser("~/Desktop")
            )
        )

        case_type_var = tk.StringVar(
            value=self.case_information.get(
                "case_type",
                "Single-user"
            )
        )

        case_number_var = tk.StringVar(
            value=self.case_information.get(
                "case_number",
                ""
            )
        )

        examiner_name_var = tk.StringVar(
            value=self.case_information.get(
                "examiner_name",
                ""
            )
        )

        phone_var = tk.StringVar(
            value=self.case_information.get(
                "phone",
                ""
            )
        )

        email_var = tk.StringVar(
            value=self.case_information.get(
                "email",
                ""
            )
        )

        organization_var = tk.StringVar(
            value=self.case_information.get(
                "organization",
                ""
            )
        )

        # ====================================================
        # FIELD HELPER
        # ====================================================

        def create_field(
            label,
            variable
        ):

            row = tk.Frame(
                form,
                bg=self.colors["white"]
            )

            row.pack(
                fill="x",
                pady=7
            )

            row.grid_columnconfigure(
                1,
                weight=1
            )

            tk.Label(
                row,
                text=label,
                bg=self.colors["white"],
                fg=self.colors["text"],
                font=("Segoe UI", 9),
                width=18,
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=(0, 10)
            )

            entry = tk.Entry(
                row,
                textvariable=variable,
                bg=self.colors["white"],
                fg=self.colors["text"],
                insertbackground=self.colors["text"],
                relief="solid",
                bd=1,
                font=("Segoe UI", 9)
            )

            entry.grid(
                row=0,
                column=1,
                sticky="ew",
                ipady=6
            )

            return entry

        # ====================================================
        # CASE INFORMATION
        # ====================================================

        tk.Label(
            form,
            text="Case Information",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        tk.Frame(
            form,
            height=1,
            bg=self.colors["border"]
        ).pack(
            fill="x",
            pady=(0, 18)
        )

        create_field(
            "Case Name:",
            case_name_var
        )

        # Base directory

        base_row = tk.Frame(
            form,
            bg=self.colors["white"]
        )

        base_row.pack(
            fill="x",
            pady=7
        )

        base_row.grid_columnconfigure(
            1,
            weight=1
        )

        tk.Label(
            base_row,
            text="Base Directory:",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 9),
            width=18,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10)
        )

        base_entry = tk.Entry(
            base_row,
            textvariable=base_directory_var,
            bg=self.colors["white"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="solid",
            bd=1,
            font=("Segoe UI", 9)
        )

        base_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            ipady=6
        )

        def browse_directory():

            directory = filedialog.askdirectory(
                parent=dialog,
                title="Select Base Directory"
            )

            if directory:
                base_directory_var.set(
                    directory
                )

        tk.Button(
            base_row,
            text="Browse",
            command=browse_directory,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["primary_light"],
            relief="solid",
            bd=1,
            padx=15,
            pady=5,
            cursor="hand2"
        ).grid(
            row=0,
            column=2,
            padx=(8, 0)
        )

        # Case type

        type_row = tk.Frame(
            form,
            bg=self.colors["white"]
        )

        type_row.pack(
            fill="x",
            pady=9
        )

        type_row.grid_columnconfigure(
            1,
            weight=1
        )

        tk.Label(
            type_row,
            text="Case Type:",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 9),
            width=18,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10)
        )

        tk.Radiobutton(
            type_row,
            text="Single-user",
            variable=case_type_var,
            value="Single-user",
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["white"],
            selectcolor=self.colors["primary_light"],
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        tk.Radiobutton(
            type_row,
            text="Multi-user",
            variable=case_type_var,
            value="Multi-user",
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["white"],
            selectcolor=self.colors["primary_light"],
            font=("Segoe UI", 9)
        ).grid(
            row=0,
            column=1,
            padx=(120, 0),
            sticky="w"
        )

        create_field(
            "Case Number:",
            case_number_var
        )

        # ====================================================
        # OPTIONAL INFORMATION
        # ====================================================

        tk.Label(
            form,
            text="Optional Information",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            pady=(28, 5)
        )

        tk.Frame(
            form,
            height=1,
            bg=self.colors["border"]
        ).pack(
            fill="x",
            pady=(0, 18)
        )

        create_field(
            "Examiner Name:",
            examiner_name_var
        )

        create_field(
            "Phone:",
            phone_var
        )

        create_field(
            "Email:",
            email_var
        )

        create_field(
            "Organization:",
            organization_var
        )

        # ====================================================
        # NOTES
        # ====================================================

        notes_row = tk.Frame(
            form,
            bg=self.colors["white"]
        )

        notes_row.pack(
            fill="x",
            pady=8
        )

        notes_row.grid_columnconfigure(
            1,
            weight=1
        )

        tk.Label(
            notes_row,
            text="Notes:",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 9),
            width=18,
            anchor="nw"
        ).grid(
            row=0,
            column=0,
            sticky="nw",
            padx=(0, 10)
        )

        notes_text = tk.Text(
            notes_row,
            height=6,
            wrap="word",
            bg=self.colors["white"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="solid",
            bd=1,
            font=("Segoe UI", 9)
        )

        notes_text.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        existing_notes = self.case_information.get(
            "notes",
            ""
        )

        if existing_notes:

            notes_text.insert(
                "1.0",
                existing_notes
            )

        notes_scroll = ttk.Scrollbar(
            notes_row,
            orient="vertical",
            command=notes_text.yview
        )

        notes_scroll.grid(
            row=0,
            column=2,
            sticky="ns",
            padx=(5, 0)
        )

        notes_text.configure(
            yscrollcommand=notes_scroll.set
        )

        tk.Frame(
            form,
            height=25,
            bg=self.colors["white"]
        ).pack()

        # ====================================================
        # FINISH
        # ====================================================

        def finish_case():

            case_name = case_name_var.get().strip()

            if not case_name:

                messagebox.showwarning(
                    "Case Information",
                    "Please enter a Case Name.",
                    parent=dialog
                )

                return False

            self.case_information = {
                "case_name": case_name,
                "base_directory":
                    base_directory_var.get().strip(),
                "case_type":
                    case_type_var.get(),
                "case_number":
                    case_number_var.get().strip(),
                "examiner_name":
                    examiner_name_var.get().strip(),
                "phone":
                    phone_var.get().strip(),
                "email":
                    email_var.get().strip(),
                "organization":
                    organization_var.get().strip(),
                "notes":
                    notes_text.get(
                        "1.0",
                        tk.END
                    ).strip()
            }

            dialog.destroy()

            if on_finish:
                on_finish()

            return True

        def cancel_case():

            dialog.destroy()

        # ====================================================
        # BOTTOM BUTTONS
        # ====================================================

        button_bar = tk.Frame(
            main,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        button_bar.pack(
            fill="x",
            side="bottom"
        )

        tk.Button(
            button_bar,
            text="Cancel",
            command=cancel_case,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            relief="solid",
            bd=1,
            padx=25,
            pady=9,
            font=("Segoe UI", 9),
            cursor="hand2"
        ).pack(
            side="right",
            padx=(8, 22),
            pady=15
        )

        tk.Button(
            button_bar,
            text="Finish",
            command=finish_case,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=10,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="right",
            pady=15
        )

        # ====================================================
        # MOUSE WHEEL
        # ====================================================

        def mousewheel(event):

            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            mousewheel
        )

        def close_dialog():

            try:
                canvas.unbind_all(
                    "<MouseWheel>"
                )
            except Exception:
                pass

            dialog.destroy()

        dialog.protocol(
            "WM_DELETE_WINDOW",
            close_dialog
        )

        # Center

        dialog.update_idletasks()

        width = dialog.winfo_width()
        height = dialog.winfo_height()

        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()

        x = max(
            0,
            (screen_width - width) // 2
        )

        y = max(
            0,
            (screen_height - height) // 2
        )

        dialog.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ========================================================
    # EXPORT PAGE
    # ========================================================

    def show_export(self):

        self.clear_main()
        self.set_active_nav("Export")

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=35
        )

        tk.Label(
            container,
            text="Export Reports",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            container,
            text="Save generated hash results as PDF or CSV",
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(4, 30)
        )

        card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.pack(
            fill="x"
        )

        tk.Label(
            card,
            text="Export Hash Results",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(30, 8)
        )

        tk.Label(
            card,
            text=(
                f"{len(self.hash_results)} hash result(s) "
                f"currently available."
            ),
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=30
        )

        button_frame = tk.Frame(
            card,
            bg=self.colors["white"]
        )

        button_frame.pack(
            fill="x",
            padx=30,
            pady=30
        )

        tk.Button(
            button_frame,
            text="📄  Export PDF Report",
            command=self.export_pdf_report,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=13,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="left",
            padx=(0, 15)
        )

        tk.Button(
            button_frame,
            text="⇩  Export CSV",
            command=self.export_csv,
            bg=self.colors["white"],
            fg=self.colors["primary"],
            activebackground=self.colors["primary_light"],
            relief="solid",
            bd=1,
            padx=25,
            pady=12,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="left"
        )

        info = tk.Frame(
            container,
            bg=self.colors["primary_light"]
        )

        info.pack(
            fill="x",
            pady=20
        )

        tk.Label(
            info,
            text="PDF Report Includes",
            bg=self.colors["primary_light"],
            fg=self.colors["text"],
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 8)
        )

        tk.Label(
            info,
            text=(
                "• Case information\n"
                "• Examiner information\n"
                "• Notes\n"
                "• File names\n"
                "• Full file paths\n"
                "• Hash algorithms\n"
                "• Actual hash values\n"
                "• Hash generation timestamps"
            ),
            justify="left",
            bg=self.colors["primary_light"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    # ========================================================
    # PDF EXPORT
    # ========================================================

    def export_pdf_report(self):

        if not REPORTLAB_AVAILABLE:

            messagebox.showerror(
                "ReportLab Required",
                "PDF export requires ReportLab.\n\n"
                "Install it using:\n\n"
                "pip install reportlab"
            )

            return

        if not self.hash_results:

            messagebox.showwarning(
                "No Hash Results",
                "Please scan files and generate hash values "
                "before exporting the PDF."
            )

            return

        # ----------------------------------------------------
        # CASE INFORMATION FIRST
        # ----------------------------------------------------

        self.show_case_information(
            on_finish=self._save_pdf_after_case
        )

    # ========================================================
    # SAVE PDF AFTER CASE
    # ========================================================

    def _save_pdf_after_case(self):

        case_name = (
            self.case_information.get(
                "case_name",
                "HashForge_Report"
            )
            or "HashForge_Report"
        )

        safe_case_name = "".join(
            c if c.isalnum() or c in (
                " ",
                "_",
                "-"
            ) else "_"
            for c in case_name
        ).strip()

        if not safe_case_name:
            safe_case_name = "HashForge_Report"

        default_filename = (
            f"{safe_case_name}_Hash_Report.pdf"
        )

        file_path = filedialog.asksaveasfilename(
            title="Save HashForge PDF Report",
            defaultextension=".pdf",
            initialfile=default_filename,
            filetypes=[
                (
                    "PDF Files",
                    "*.pdf"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        try:

            self.create_pdf_report(
                file_path
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            export_text = (
                f"PDF • {os.path.basename(file_path)} • "
                f"{timestamp}"
            )

            self.recent_exports.insert(
                0,
                export_text
            )

            self.recent_exports = (
                self.recent_exports[:5]
            )

            messagebox.showinfo(
                "PDF Export Complete",
                "PDF report saved successfully.\n\n"
                f"File:\n{file_path}"
            )

        except Exception as error:

            messagebox.showerror(
                "PDF Export Error",
                "Could not create the PDF report.\n\n"
                f"Reason:\n{error}"
            )

    # ========================================================
    # CREATE PDF
    # ========================================================

    def create_pdf_report(
        self,
        file_path
    ):

        # ----------------------------------------------------
        # DOCUMENT
        # ----------------------------------------------------

        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
            title="HashForge Hash Report",
            author=(
                self.case_information.get(
                    "examiner_name",
                    ""
                )
                or "HashForge"
            )
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "HFTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor(
                self.colors["primary"]
            ),
            alignment=TA_CENTER,
            spaceAfter=8
        )

        subtitle_style = ParagraphStyle(
            "HFSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor(
                "#667085"
            ),
            alignment=TA_CENTER,
            spaceAfter=18
        )

        heading_style = ParagraphStyle(
            "HFHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor(
                self.colors["primary"]
            ),
            spaceBefore=10,
            spaceAfter=8
        )

        normal_style = ParagraphStyle(
            "HFNormal",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor(
                "#172033"
            )
        )

        small_style = ParagraphStyle(
            "HFSmall",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor(
                "#667085"
            )
        )

        hash_style = ParagraphStyle(
            "HFHash",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=7,
            leading=9,
            textColor=colors.HexColor(
                "#172033"
            )
        )

        story = []

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "HASHFORGE",
                title_style
            )
        )

        story.append(
            Paragraph(
                "File Integrity & Hash Verification Report",
                subtitle_style
            )
        )

        # ----------------------------------------------------
        # REPORT DATE
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Report Generated: "
                + datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                normal_style
            )
        )

        story.append(
            Spacer(
                1,
                10
            )
        )

        # ----------------------------------------------------
        # CASE INFORMATION
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Case Information",
                heading_style
            )
        )

        case = self.case_information

        case_data = [
            [
                Paragraph(
                    "<b>Case Name</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "case_name",
                            ""
                        )
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Case Number</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "case_number",
                            ""
                        )
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Case Type</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "case_type",
                            ""
                        )
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Base Directory</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "base_directory",
                            ""
                        )
                    ),
                    small_style
                )
            ]
        ]

        case_table = Table(
            case_data,
            colWidths=[
                42 * mm,
                135 * mm
            ],
            repeatRows=0
        )

        case_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#F2F4F7")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#D9DDE3")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(
            case_table
        )

        # ----------------------------------------------------
        # OPTIONAL INFORMATION
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Optional Information",
                heading_style
            )
        )

        optional_data = [
            [
                Paragraph(
                    "<b>Examiner Name</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "examiner_name",
                            ""
                        )
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Phone</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "phone",
                            ""
                        )
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Email</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "email",
                            ""
                        )
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Organization</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "organization",
                            ""
                        )
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Notes</b>",
                    normal_style
                ),
                Paragraph(
                    self.pdf_escape(
                        case.get(
                            "notes",
                            ""
                        )
                    ).replace(
                        "\n",
                        "<br/>"
                    ),
                    normal_style
                )
            ]
        ]

        optional_table = Table(
            optional_data,
            colWidths=[
                42 * mm,
                135 * mm
            ]
        )

        optional_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#F2F4F7")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#D9DDE3")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(
            optional_table
        )

        story.append(
            Spacer(
                1,
                15
            )
        )

        # ----------------------------------------------------
        # HASH SUMMARY
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Hash Summary",
                heading_style
            )
        )

        algorithms_used = sorted(
            set(
                result["algorithm"]
                for result in self.hash_results
            )
        )

        summary_text = (
            f"Files processed: "
            f"{len(set(r['file'] for r in self.hash_results))}"
            f"<br/>"
            f"Hash records: "
            f"{len(self.hash_results)}"
            f"<br/>"
            f"Algorithms: "
            f"{self.pdf_escape(', '.join(algorithms_used))}"
        )

        story.append(
            Paragraph(
                summary_text,
                normal_style
            )
        )

        story.append(
            Spacer(
                1,
                15
            )
        )

        # ----------------------------------------------------
        # HASH RESULTS
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Hash Results",
                heading_style
            )
        )

        hash_data = [
            [
                Paragraph(
                    "<b>File</b>",
                    normal_style
                ),
                Paragraph(
                    "<b>Algorithm</b>",
                    normal_style
                ),
                Paragraph(
                    "<b>Hash Value</b>",
                    normal_style
                ),
                Paragraph(
                    "<b>Timestamp</b>",
                    normal_style
                )
            ]
        ]

        for result in self.hash_results:

            file_name = self.pdf_escape(
                result.get(
                    "file_name",
                    ""
                )
            )

            algorithm = self.pdf_escape(
                result.get(
                    "algorithm",
                    ""
                )
            )

            hash_value = self.pdf_escape(
                result.get(
                    "hash",
                    ""
                )
            )

            timestamp = self.pdf_escape(
                result.get(
                    "timestamp",
                    ""
                )
            )

            hash_data.append(
                [
                    Paragraph(
                        file_name,
                        small_style
                    ),
                    Paragraph(
                        algorithm,
                        small_style
                    ),
                    Paragraph(
                        hash_value,
                        hash_style
                    ),
                    Paragraph(
                        timestamp,
                        small_style
                    )
                ]
            )

        hash_table = Table(
            hash_data,
            colWidths=[
                38 * mm,
                25 * mm,
                88 * mm,
                27 * mm
            ],
            repeatRows=1
        )

        hash_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        self.colors["primary"]
                    )
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor("#D9DDE3")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FAFC")
                    ]
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        story.append(
            hash_table
        )

        # ----------------------------------------------------
        # FILE PATH DETAILS
        # ----------------------------------------------------

        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "File Details",
                heading_style
            )
        )

        file_data = [
            [
                Paragraph(
                    "<b>File Name</b>",
                    normal_style
                ),
                Paragraph(
                    "<b>Full File Path</b>",
                    normal_style
                )
            ]
        ]

        unique_files = []

        for result in self.hash_results:

            if result["file"] not in unique_files:

                unique_files.append(
                    result["file"]
                )

        for file_path in unique_files:

            file_data.append(
                [
                    Paragraph(
                        self.pdf_escape(
                            os.path.basename(
                                file_path
                            )
                        ),
                        small_style
                    ),
                    Paragraph(
                        self.pdf_escape(
                            file_path
                        ),
                        small_style
                    )
                ]
            )

        file_table = Table(
            file_data,
            colWidths=[
                55 * mm,
                123 * mm
            ],
            repeatRows=1
        )

        file_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        self.colors["primary"]
                    )
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor("#D9DDE3")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FAFC")
                    ]
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(
            file_table
        )

        story.append(
            Spacer(
                1,
                20
            )
        )

        # ----------------------------------------------------
        # INTEGRITY STATEMENT
        # ----------------------------------------------------

        integrity_box = Table(
            [[
                Paragraph(
                    "<b>Integrity Record</b><br/>"
                    "The hash values in this report were "
                    "calculated locally by HashForge from "
                    "the selected files. The values shown "
                    "above are the generated cryptographic "
                    "digest values at the time of scanning.",
                    normal_style
                )
            ]],
            colWidths=[
                178 * mm
            ]
        )

        integrity_box.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#EEF9F5")
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.HexColor(
                        self.colors["primary"]
                    )
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                )
            ])
        )

        story.append(
            integrity_box
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        def add_page_number(
            canvas,
            doc
        ):

            canvas.saveState()

            canvas.setFont(
                "Helvetica",
                7
            )

            canvas.setFillColor(
                colors.HexColor("#667085")
            )

            canvas.drawString(
                15 * mm,
                8 * mm,
                "HashForge • File Integrity System"
            )

            canvas.drawRightString(
                A4[0] - 15 * mm,
                8 * mm,
                f"Page {doc.page}"
            )

            canvas.restoreState()

        doc.build(
            story,
            onFirstPage=add_page_number,
            onLaterPages=add_page_number
        )

    # ========================================================
    # PDF ESCAPE
    # ========================================================

    def pdf_escape(
        self,
        value
    ):

        if value is None:
            return ""

        value = str(value)

        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;"
        }

        for old, new in replacements.items():
            value = value.replace(
                old,
                new
            )

        return value

    # ========================================================
    # CSV EXPORT
    # ========================================================

    def export_csv(self):

        if not self.hash_results:

            messagebox.showwarning(
                "No Hash Results",
                "Please generate hash values before exporting."
            )

            return

        file_path = filedialog.asksaveasfilename(
            title="Export Hash Results",
            defaultextension=".csv",
            initialfile="HashForge_Hash_Report.csv",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as csv_file:

                writer = csv.writer(
                    csv_file
                )

                writer.writerow([
                    "Case Name",
                    "Case Number",
                    "Examiner Name",
                    "Organization",
                    "File Name",
                    "File Path",
                    "Algorithm",
                    "Hash Value",
                    "Timestamp"
                ])

                for result in self.hash_results:

                    writer.writerow([
                        self.case_information.get(
                            "case_name",
                            ""
                        ),
                        self.case_information.get(
                            "case_number",
                            ""
                        ),
                        self.case_information.get(
                            "examiner_name",
                            ""
                        ),
                        self.case_information.get(
                            "organization",
                            ""
                        ),
                        result.get(
                            "file_name",
                            ""
                        ),
                        result.get(
                            "file",
                            ""
                        ),
                        result.get(
                            "algorithm",
                            ""
                        ),
                        result.get(
                            "hash",
                            ""
                        ),
                        result.get(
                            "timestamp",
                            ""
                        )
                    ])

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.recent_exports.insert(
                0,
                f"CSV • {os.path.basename(file_path)} • {timestamp}"
            )

            self.recent_exports = (
                self.recent_exports[:5]
            )

            messagebox.showinfo(
                "CSV Export Complete",
                "CSV report saved successfully.\n\n"
                f"{file_path}"
            )

        except Exception as error:

            messagebox.showerror(
                "CSV Export Error",
                f"Could not export CSV.\n\n{error}"
            )

    # ========================================================
    # GENERIC PAGE
    # ========================================================

    def show_generic_page(
        self,
        page_name,
        title,
        subtitle,
        icon,
        description
    ):

        self.clear_main()
        self.set_active_nav(page_name)

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=35
        )

        tk.Label(
            container,
            text=title,
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            container,
            text=subtitle,
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(4, 30)
        )

        card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text=icon,
            bg=self.colors["white"],
            fg=self.colors["primary"],
            font=("Segoe UI", 48)
        ).pack(
            pady=(100, 15)
        )

        tk.Label(
            card,
            text=title,
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 18, "bold")
        ).pack()

        tk.Label(
            card,
            text=description,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 10)
        ).pack(
            pady=10
        )

        badge = tk.Label(
            card,
            text="READY",
            bg=self.colors["primary_light"],
            fg=self.colors["primary"],
            font=("Segoe UI", 9, "bold"),
            padx=15,
            pady=7
        )

        badge.pack(
            pady=20
        )

    # ========================================================
    # VERIFY
    # ========================================================

    def show_verify(self):

        self.clear_main()
        self.set_active_nav("Verify")

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=30
        )

        header = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        header.pack(
            fill="x"
        )

        title_area = tk.Frame(
            header,
            bg=self.colors["bg"]
        )

        title_area.pack(
            side="left"
        )

        tk.Label(
            title_area,
            text="Verify Integrity",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_area,
            text="Check whether a file matches its expected hash",
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ----------------------------------------------------
        # FILE CARD
        # ----------------------------------------------------

        file_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        file_card.pack(
            fill="x",
            pady=(25, 15)
        )

        file_header = tk.Frame(
            file_card,
            bg=self.colors["white"]
        )

        file_header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        tk.Label(
            file_header,
            text="File to Verify",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            side="left"
        )

        tk.Button(
            file_header,
            text="Clear",
            command=self.clear_verify_file,
            bg=self.colors["white"],
            fg=self.colors["danger"],
            activebackground=self.colors["white"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="right"
        )

        tk.Button(
            file_header,
            text="+  Select File",
            command=self.select_verify_file,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=8,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="right",
            padx=(0, 10)
        )

        file_display = tk.Frame(
            file_card,
            bg=self.colors["content"]
        )

        file_display.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        self.verify_file_label = tk.Label(
            file_display,
            text=(
                os.path.basename(self.verify_file)
                if self.verify_file
                else "No file selected"
            ),
            bg=self.colors["content"],
            fg=(
                self.colors["text"]
                if self.verify_file
                else self.colors["muted"]
            ),
            font=("Segoe UI", 9),
            anchor="w"
        )

        self.verify_file_label.pack(
            fill="x",
            padx=15,
            pady=12
        )

        # ----------------------------------------------------
        # VERIFICATION DETAILS CARD
        # ----------------------------------------------------

        details_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        details_card.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            details_card,
            text="Verification Details",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        tk.Label(
            details_card,
            text="Choose the algorithm and enter the hash you expect the file to match.",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=25
        )

        algo_row = tk.Frame(
            details_card,
            bg=self.colors["white"]
        )

        algo_row.pack(
            fill="x",
            padx=25,
            pady=(15, 10)
        )

        tk.Label(
            algo_row,
            text="Algorithm:",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 9),
            width=14,
            anchor="w"
        ).pack(
            side="left"
        )

        self.verify_algo_var = tk.StringVar(
            value="SHA-256"
        )

        verify_algo_menu = ttk.Combobox(
            algo_row,
            textvariable=self.verify_algo_var,
            values=list(self.algorithms.keys()),
            state="readonly",
            width=14
        )

        verify_algo_menu.pack(
            side="left"
        )

        hash_row = tk.Frame(
            details_card,
            bg=self.colors["white"]
        )

        hash_row.pack(
            fill="x",
            padx=25,
            pady=(0, 10)
        )

        hash_row.grid_columnconfigure(
            1,
            weight=1
        )

        tk.Label(
            hash_row,
            text="Expected Hash:",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 9),
            width=14,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.verify_hash_var = tk.StringVar()

        verify_hash_entry = tk.Entry(
            hash_row,
            textvariable=self.verify_hash_var,
            bg=self.colors["white"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="solid",
            bd=1,
            font=("Consolas", 9)
        )

        verify_hash_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            ipady=6
        )

        hash_actions = tk.Frame(
            details_card,
            bg=self.colors["white"]
        )

        hash_actions.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        tk.Button(
            hash_actions,
            text="Paste from Clipboard",
            command=self.paste_verify_hash,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=6,
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            side="left"
        )

        tk.Button(
            hash_actions,
            text="Load from Checksum File",
            command=self.load_verify_hash_from_file,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=6,
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            side="left",
            padx=(10, 0)
        )

        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        action_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        action_card.pack(
            fill="x",
            pady=(0, 15)
        )

        action_top = tk.Frame(
            action_card,
            bg=self.colors["white"]
        )

        action_top.pack(
            fill="x",
            padx=25,
            pady=18
        )

        self.verify_button = tk.Button(
            action_top,
            text="✓  Verify Integrity",
            command=self.run_verification,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=25,
            pady=11,
            font=self.fonts["button"],
            cursor="hand2"
        )

        self.verify_button.pack(
            side="left"
        )

        self.verify_status_label = tk.Label(
            action_top,
            text="Ready",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        )

        self.verify_status_label.pack(
            side="left",
            padx=20
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        self.verify_result_container = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        self.verify_result_container.pack(
            fill="both",
            expand=True
        )

        self.render_verify_result()

    # ========================================================
    # VERIFY — SELECT / CLEAR FILE
    # ========================================================

    def select_verify_file(self):

        file_path = filedialog.askopenfilename(
            title="Select file to verify"
        )

        if not file_path:
            return

        self.verify_file = file_path

        if hasattr(
            self,
            "verify_file_label"
        ):

            self.verify_file_label.configure(
                text=os.path.basename(file_path),
                fg=self.colors["text"]
            )

        if hasattr(
            self,
            "verify_status_label"
        ):

            self.verify_status_label.configure(
                text=f"{os.path.basename(file_path)} selected",
                fg=self.colors["primary"]
            )

        self.render_verify_result()

    def clear_verify_file(self):

        self.verify_file = None

        if hasattr(
            self,
            "verify_file_label"
        ):

            self.verify_file_label.configure(
                text="No file selected",
                fg=self.colors["muted"]
            )

        if hasattr(
            self,
            "verify_hash_var"
        ):

            self.verify_hash_var.set("")

        if hasattr(
            self,
            "verify_status_label"
        ):

            self.verify_status_label.configure(
                text="Ready",
                fg=self.colors["secondary"]
            )

        self.render_verify_result()

    # ========================================================
    # VERIFY — HASH INPUT HELPERS
    # ========================================================

    def paste_verify_hash(self):

        try:

            clipboard_text = self.clipboard_get().strip()

        except tk.TclError:

            messagebox.showwarning(
                "Clipboard Empty",
                "There is nothing on the clipboard to paste."
            )

            return

        if hasattr(
            self,
            "verify_hash_var"
        ):

            self.verify_hash_var.set(clipboard_text)

    def load_verify_hash_from_file(self):

        file_path = filedialog.askopenfilename(
            title="Select checksum file",
            filetypes=[
                (
                    "Checksum / Text Files",
                    "*.txt *.sha1 *.sha256 *.sha512 *.md5 *.cksum *.*"
                )
            ]
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as checksum_file:

                content = checksum_file.read()

        except Exception as error:

            messagebox.showerror(
                "Read Error",
                f"Could not read checksum file.\n\n{error}"
            )

            return

        candidates = re.findall(
            r"\b[0-9A-Fa-f]{32,128}\b",
            content
        )

        valid_lengths = {
            32,
            40,
            56,
            64,
            96,
            128
        }

        candidates = [
            token
            for token in candidates
            if len(token) in valid_lengths
        ]

        if not candidates:

            messagebox.showwarning(
                "No Hash Found",
                "Could not find a valid hash value in that file."
            )

            return

        if hasattr(
            self,
            "verify_hash_var"
        ):

            self.verify_hash_var.set(candidates[0])

        if hasattr(
            self,
            "verify_status_label"
        ):

            self.verify_status_label.configure(
                text=f"Hash loaded from {os.path.basename(file_path)}",
                fg=self.colors["primary"]
            )

    # ========================================================
    # VERIFY — RUN
    # ========================================================

    def run_verification(self):

        if not self.verify_file:

            messagebox.showwarning(
                "No File Selected",
                "Please select a file to verify."
            )

            return

        if not os.path.exists(self.verify_file):

            messagebox.showerror(
                "File Not Found",
                "The selected file no longer exists at that location."
            )

            return

        expected_hash = self.verify_hash_var.get().strip()

        if not expected_hash:

            messagebox.showwarning(
                "No Expected Hash",
                "Please enter, paste, or load the hash you want to "
                "verify the file against."
            )

            return

        algorithm = self.verify_algo_var.get()

        self.verify_button.configure(
            state="disabled",
            text="⏳  Verifying..."
        )

        self.verify_status_label.configure(
            text=f"Hashing {os.path.basename(self.verify_file)} • {algorithm}",
            fg=self.colors["primary"]
        )

        self.update_idletasks()

        try:

            computed_hash = self.calculate_file_hash(
                self.verify_file,
                algorithm
            )

        except Exception as error:

            self.verify_button.configure(
                state="normal",
                text="✓  Verify Integrity"
            )

            self.verify_status_label.configure(
                text="Verification failed",
                fg=self.colors["danger"]
            )

            messagebox.showerror(
                "Verification Error",
                f"Could not compute the hash for this file.\n\n{error}"
            )

            self.render_verify_result(
                error=str(error)
            )

            return

        match = (
            computed_hash.strip().lower()
            == expected_hash.strip().lower()
        )

        self.verify_button.configure(
            state="normal",
            text="✓  Verify Integrity"
        )

        if match:

            self.verify_status_label.configure(
                text="Verification complete • MATCH",
                fg=self.colors["success"]
            )

        else:

            self.verify_status_label.configure(
                text="Verification complete • MISMATCH",
                fg=self.colors["danger"]
            )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.history.insert(
            0,
            {
                "type": "verify",
                "file": self.verify_file,
                "file_name": os.path.basename(self.verify_file),
                "algorithm": algorithm,
                "hash": computed_hash,
                "expected_hash": expected_hash,
                "match": match,
                "timestamp": timestamp
            }
        )

        self.render_verify_result(
            computed_hash=computed_hash,
            expected_hash=expected_hash,
            match=match,
            algorithm=algorithm
        )

    # ========================================================
    # VERIFY — RESULT DISPLAY
    # ========================================================

    def render_verify_result(
        self,
        computed_hash=None,
        expected_hash=None,
        match=None,
        algorithm=None,
        error=None
    ):

        if not hasattr(
            self,
            "verify_result_container"
        ):
            return

        for widget in self.verify_result_container.winfo_children():
            widget.destroy()

        card = tk.Frame(
            self.verify_result_container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True
        )

        if error:

            tk.Label(
                card,
                text="△",
                bg=self.colors["white"],
                fg=self.colors["danger"],
                font=("Segoe UI", 40)
            ).pack(
                pady=(40, 10)
            )

            tk.Label(
                card,
                text="Verification could not be completed",
                bg=self.colors["white"],
                fg=self.colors["text"],
                font=("Segoe UI", 14, "bold")
            ).pack()

            tk.Label(
                card,
                text=error,
                bg=self.colors["white"],
                fg=self.colors["secondary"],
                font=("Segoe UI", 9)
            ).pack(
                pady=(6, 40)
            )

            return

        if computed_hash is None:

            tk.Label(
                card,
                text="✓",
                bg=self.colors["white"],
                fg=self.colors["muted"],
                font=("Segoe UI", 40)
            ).pack(
                pady=(40, 10)
            )

            tk.Label(
                card,
                text="No verification performed yet",
                bg=self.colors["white"],
                fg=self.colors["text"],
                font=("Segoe UI", 14, "bold")
            ).pack()

            tk.Label(
                card,
                text="Select a file, enter the expected hash, "
                     "and click Verify Integrity.",
                bg=self.colors["white"],
                fg=self.colors["secondary"],
                font=("Segoe UI", 9)
            ).pack(
                pady=(6, 40)
            )

            return

        badge_color = (
            self.colors["success"]
            if match
            else self.colors["danger"]
        )

        badge_bg = (
            self.colors["primary_light"]
            if match
            else self.colors["white"]
        )

        header_row = tk.Frame(
            card,
            bg=self.colors["white"]
        )

        header_row.pack(
            fill="x",
            padx=25,
            pady=(25, 15)
        )

        tk.Label(
            header_row,
            text=(
                "✓  HASHES MATCH"
                if match
                else "✕  HASHES DO NOT MATCH"
            ),
            bg=badge_bg,
            fg=badge_color,
            font=("Segoe UI", 13, "bold"),
            padx=18,
            pady=10,
            highlightbackground=badge_color,
            highlightthickness=1 if not match else 0
        ).pack(
            side="left"
        )

        tk.Label(
            header_row,
            text=(
                "File integrity verified — no tampering detected."
                if match
                else "The file's hash does not match the expected value."
            ),
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            side="left",
            padx=15
        )

        detail_frame = tk.Frame(
            card,
            bg=self.colors["content"]
        )

        detail_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        rows = [
            (
                "File",
                os.path.basename(self.verify_file)
                if self.verify_file
                else ""
            ),
            (
                "Algorithm",
                algorithm or ""
            ),
            (
                "Computed Hash",
                computed_hash
            ),
            (
                "Expected Hash",
                expected_hash
            )
        ]

        for label, value in rows:

            row = tk.Frame(
                detail_frame,
                bg=self.colors["content"]
            )

            row.pack(
                fill="x",
                padx=15,
                pady=6
            )

            tk.Label(
                row,
                text=label,
                bg=self.colors["content"],
                fg=self.colors["secondary"],
                font=("Segoe UI", 9, "bold"),
                width=16,
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text=value,
                bg=self.colors["content"],
                fg=self.colors["text"],
                font=("Consolas", 9),
                anchor="w",
                wraplength=850,
                justify="left"
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

        tk.Button(
            card,
            text="Copy Computed Hash",
            command=lambda: self.copy_text_to_clipboard(computed_hash),
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=6,
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    def copy_text_to_clipboard(
        self,
        text
    ):

        if not text:
            return

        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

        if hasattr(
            self,
            "verify_status_label"
        ):

            self.verify_status_label.configure(
                text="Hash copied to clipboard",
                fg=self.colors["success"]
            )

    # ========================================================
    # HISTORY
    # ========================================================

    def show_history(self):

        self.clear_main()
        self.set_active_nav("History")

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=35
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        header.pack(
            fill="x"
        )

        title_area = tk.Frame(
            header,
            bg=self.colors["bg"]
        )

        title_area.pack(
            side="left"
        )

        tk.Label(
            title_area,
            text="Scan History",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_area,
            text="Every hash generated in this session, searchable and exportable",
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        button_area = tk.Frame(
            header,
            bg=self.colors["bg"]
        )

        button_area.pack(
            side="right"
        )

        tk.Button(
            button_area,
            text="⇩  Export CSV",
            command=self.export_history_csv,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=10,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="right"
        )

        tk.Button(
            button_area,
            text="🗑  Clear History",
            command=self.clear_history,
            bg=self.colors["white"],
            fg=self.colors["danger"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=18,
            pady=10,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="right",
            padx=(0, 10)
        )

        # ----------------------------------------------------
        # STAT CARDS
        # ----------------------------------------------------

        stats_row = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        stats_row.pack(
            fill="x",
            pady=(30, 20)
        )

        unique_files = len({
            entry.get("file")
            for entry in self.history
        })

        unique_algorithms = len({
            entry.get("algorithm")
            for entry in self.history
        })

        last_activity = (
            self.history[0]["timestamp"]
            if self.history
            else "--"
        )

        self.create_stat_card(
            stats_row,
            "▤",
            "Total Records",
            str(len(self.history)),
            0
        )

        self.create_stat_card(
            stats_row,
            "#",
            "Unique Files",
            str(unique_files),
            1
        )

        self.create_stat_card(
            stats_row,
            "⚙",
            "Algorithms Used",
            str(unique_algorithms),
            2
        )

        self.create_stat_card(
            stats_row,
            "◷",
            "Last Activity",
            last_activity,
            3
        )

        # ----------------------------------------------------
        # TOOLBAR (SEARCH + FILTER)
        # ----------------------------------------------------

        toolbar = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        toolbar.pack(
            fill="x",
            pady=(0, 20)
        )

        toolbar_inner = tk.Frame(
            toolbar,
            bg=self.colors["white"]
        )

        toolbar_inner.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Label(
            toolbar_inner,
            text="⌕",
            bg=self.colors["white"],
            fg=self.colors["muted"],
            font=("Segoe UI", 12)
        ).pack(
            side="left"
        )

        self.history_search_var = tk.StringVar()

        search_entry = tk.Entry(
            toolbar_inner,
            textvariable=self.history_search_var,
            font=self.fonts["normal"],
            relief="flat",
            bg=self.colors["content"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"]
        )

        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            ipady=6
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_history_tree()
        )

        tk.Label(
            toolbar_inner,
            text="Algorithm",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=self.fonts["small"]
        ).pack(
            side="left",
            padx=(15, 6)
        )

        self.history_algo_var = tk.StringVar(
            value="All"
        )

        algo_menu = ttk.Combobox(
            toolbar_inner,
            textvariable=self.history_algo_var,
            values=(
                ["All"]
                + list(self.algorithms.keys())
            ),
            state="readonly",
            width=12
        )

        algo_menu.pack(
            side="left"
        )

        algo_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_history_tree()
        )

        tk.Button(
            toolbar_inner,
            text="Reset",
            command=self.reset_history_filters,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=5,
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            side="left",
            padx=(10, 0)
        )

        # ----------------------------------------------------
        # RECORDS TABLE
        # ----------------------------------------------------

        result_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        result_card.pack(
            fill="both",
            expand=True
        )

        result_header = tk.Frame(
            result_card,
            bg=self.colors["white"]
        )

        result_header.pack(
            fill="x",
            padx=25,
            pady=(18, 10)
        )

        tk.Label(
            result_header,
            text="All Records",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            side="left"
        )

        self.history_count_label = tk.Label(
            result_header,
            text="",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 8)
        )

        self.history_count_label.pack(
            side="right"
        )

        table_frame = tk.Frame(
            result_card,
            bg=self.colors["white"]
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        columns = (
            "timestamp",
            "type",
            "file",
            "algorithm",
            "hash"
        )

        self.history_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.history_tree.heading(
            "timestamp",
            text="Timestamp"
        )

        self.history_tree.heading(
            "type",
            text="Type"
        )

        self.history_tree.heading(
            "file",
            text="File"
        )

        self.history_tree.heading(
            "algorithm",
            text="Algorithm"
        )

        self.history_tree.heading(
            "hash",
            text="Hash Value"
        )

        self.history_tree.column(
            "timestamp",
            width=140,
            anchor="w"
        )

        self.history_tree.column(
            "type",
            width=120,
            anchor="center"
        )

        self.history_tree.column(
            "file",
            width=230,
            anchor="w"
        )

        self.history_tree.column(
            "algorithm",
            width=100,
            anchor="center"
        )

        self.history_tree.column(
            "hash",
            width=490,
            anchor="w"
        )

        tree_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.history_tree.yview
        )

        self.history_tree.configure(
            yscrollcommand=tree_scroll.set
        )

        self.history_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        tree_scroll.pack(
            side="right",
            fill="y"
        )

        self.history_tree.bind(
            "<Double-1>",
            self.copy_history_hash
        )

        self.refresh_history_tree()

    # ========================================================
    # HISTORY — REFRESH / FILTER
    # ========================================================

    def refresh_history_tree(self):

        if not hasattr(
            self,
            "history_tree"
        ):
            return

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        search_term = (
            self.history_search_var.get().strip().lower()
            if hasattr(self, "history_search_var")
            else ""
        )

        algo_filter = (
            self.history_algo_var.get()
            if hasattr(self, "history_algo_var")
            else "All"
        )

        filtered = []

        for entry in self.history:

            if (
                algo_filter != "All"
                and entry.get("algorithm") != algo_filter
            ):
                continue

            if search_term:

                haystack = " ".join([
                    entry.get("file_name", ""),
                    entry.get("file", ""),
                    entry.get("hash", "")
                ]).lower()

                if search_term not in haystack:
                    continue

            filtered.append(entry)

        for entry in filtered:

            if entry.get("type") == "verify":

                type_label = (
                    "Verify ✓"
                    if entry.get("match")
                    else "Verify ✕"
                )

            else:

                type_label = "Scan"

            self.history_tree.insert(
                "",
                tk.END,
                values=(
                    entry.get("timestamp", ""),
                    type_label,
                    entry.get("file_name", ""),
                    entry.get("algorithm", ""),
                    entry.get("hash", "")
                )
            )

        if hasattr(
            self,
            "history_count_label"
        ):

            self.history_count_label.configure(
                text=(
                    f"{len(filtered)} of {len(self.history)} "
                    f"record(s) • Double-click a row to copy its hash"
                )
            )

    # ========================================================
    # HISTORY — RESET FILTERS
    # ========================================================

    def reset_history_filters(self):

        if hasattr(
            self,
            "history_search_var"
        ):
            self.history_search_var.set("")

        if hasattr(
            self,
            "history_algo_var"
        ):
            self.history_algo_var.set("All")

        self.refresh_history_tree()

    # ========================================================
    # HISTORY — COPY HASH
    # ========================================================

    def copy_history_hash(
        self,
        event=None
    ):

        if not hasattr(
            self,
            "history_tree"
        ):
            return

        selected = self.history_tree.selection()

        if not selected:
            return

        item = self.history_tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if len(values) < 5:
            return

        hash_value = values[4]

        self.clipboard_clear()
        self.clipboard_append(hash_value)
        self.update()

        if hasattr(
            self,
            "history_count_label"
        ):

            self.history_count_label.configure(
                text="Hash copied to clipboard",
                fg=self.colors["success"]
            )

            self.after(
                1500,
                self.refresh_history_tree
            )

    # ========================================================
    # HISTORY — CLEAR
    # ========================================================

    def clear_history(self):

        if not self.history:

            messagebox.showinfo(
                "History Empty",
                "There is no history to clear."
            )

            return

        confirm = messagebox.askyesno(
            "Clear History",
            "This will permanently remove all hashing history "
            "records for this session. Continue?"
        )

        if not confirm:
            return

        self.history.clear()
        self.show_history()

    # ========================================================
    # HISTORY — EXPORT CSV
    # ========================================================

    def export_history_csv(self):

        if not self.history:

            messagebox.showwarning(
                "No History",
                "There is no history to export yet."
            )

            return

        file_path = filedialog.asksaveasfilename(
            title="Export History",
            defaultextension=".csv",
            initialfile="HashForge_History.csv",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as csv_file:

                writer = csv.writer(
                    csv_file
                )

                writer.writerow([
                    "Timestamp",
                    "Type",
                    "File Name",
                    "File Path",
                    "Algorithm",
                    "Hash Value",
                    "Expected Hash",
                    "Match",
                    "Case Name",
                    "Examiner"
                ])

                for entry in self.history:

                    entry_type = entry.get(
                        "type",
                        "scan"
                    )

                    match_value = entry.get(
                        "match"
                    )

                    match_text = (
                        ""
                        if match_value is None
                        else (
                            "MATCH"
                            if match_value
                            else "MISMATCH"
                        )
                    )

                    writer.writerow([
                        entry.get(
                            "timestamp",
                            ""
                        ),
                        (
                            "Verify"
                            if entry_type == "verify"
                            else "Scan"
                        ),
                        entry.get(
                            "file_name",
                            ""
                        ),
                        entry.get(
                            "file",
                            ""
                        ),
                        entry.get(
                            "algorithm",
                            ""
                        ),
                        entry.get(
                            "hash",
                            ""
                        ),
                        entry.get(
                            "expected_hash",
                            ""
                        ),
                        match_text,
                        self.case_information.get(
                            "case_name",
                            ""
                        ),
                        self.case_information.get(
                            "examiner_name",
                            ""
                        )
                    ])

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.recent_exports.insert(
                0,
                f"CSV • {os.path.basename(file_path)} • History • {timestamp}"
            )

            self.recent_exports = (
                self.recent_exports[:5]
            )

            messagebox.showinfo(
                "Export Complete",
                "History exported successfully.\n\n"
                f"{file_path}"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                f"Could not export history.\n\n{error}"
            )

    # ========================================================
    # DUPLICATES
    # ========================================================

    def show_duplicates(self):

        self.clear_main()
        self.set_active_nav("Duplicates")

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=35
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        header.pack(
            fill="x"
        )

        title_area = tk.Frame(
            header,
            bg=self.colors["bg"]
        )

        title_area.pack(
            side="left"
        )

        tk.Label(
            title_area,
            text="Duplicate Finder",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_area,
            text="Find files with matching cryptographic hashes",
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        button_area = tk.Frame(
            header,
            bg=self.colors["bg"]
        )

        button_area.pack(
            side="right"
        )

        tk.Button(
            button_area,
            text="⇩  Export CSV",
            command=self.export_duplicates_csv,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=18,
            pady=10,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="right"
        )

        tk.Button(
            button_area,
            text="⊕  Find Duplicates",
            command=self.find_duplicates,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=10,
            font=self.fonts["button"],
            cursor="hand2"
        ).pack(
            side="right",
            padx=(0, 10)
        )

        # ----------------------------------------------------
        # SOURCE TOOLBAR
        # ----------------------------------------------------

        toolbar = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        toolbar.pack(
            fill="x",
            pady=(25, 20)
        )

        toolbar_inner = tk.Frame(
            toolbar,
            bg=self.colors["white"]
        )

        toolbar_inner.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Button(
            toolbar_inner,
            text="📄  Add Files",
            command=self.select_duplicate_files,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=7,
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            side="left"
        )

        tk.Button(
            toolbar_inner,
            text="📁  Add Folder",
            command=self.select_duplicate_folder,
            bg=self.colors["white"],
            fg=self.colors["text"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=7,
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            side="left",
            padx=(8, 0)
        )

        tk.Button(
            toolbar_inner,
            text="🗑  Clear",
            command=self.clear_duplicate_selection,
            bg=self.colors["white"],
            fg=self.colors["danger"],
            activebackground=self.colors["hover"],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=7,
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            side="left",
            padx=(8, 0)
        )

        if self.duplicate_subfolders_var is None:

            self.duplicate_subfolders_var = tk.BooleanVar(
                value=True
            )

        tk.Checkbutton(
            toolbar_inner,
            text="Include subfolders",
            variable=self.duplicate_subfolders_var,
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            activebackground=self.colors["white"],
            selectcolor=self.colors["white"],
            font=self.fonts["small"],
            cursor="hand2"
        ).pack(
            side="left",
            padx=(15, 0)
        )

        tk.Label(
            toolbar_inner,
            text="Algorithm",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=self.fonts["small"]
        ).pack(
            side="left",
            padx=(20, 6)
        )

        if self.duplicate_algorithm_var is None:

            self.duplicate_algorithm_var = tk.StringVar(
                value="MD5"
            )

        algo_menu = ttk.Combobox(
            toolbar_inner,
            textvariable=self.duplicate_algorithm_var,
            values=list(self.algorithms.keys()),
            state="readonly",
            width=10
        )

        algo_menu.pack(
            side="left"
        )

        self.duplicate_selection_label = tk.Label(
            toolbar_inner,
            text=self.get_duplicate_selection_text(),
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=self.fonts["small"]
        )

        self.duplicate_selection_label.pack(
            side="right"
        )

        # ----------------------------------------------------
        # STAT CARDS
        # ----------------------------------------------------

        stats_row = tk.Frame(
            container,
            bg=self.colors["bg"]
        )

        stats_row.pack(
            fill="x",
            pady=(0, 20)
        )

        duplicate_file_count = sum(
            len(group["files"])
            for group in self.duplicate_groups
        )

        wasted_bytes = sum(
            group["size"] * (len(group["files"]) - 1)
            for group in self.duplicate_groups
        )

        self.create_stat_card(
            stats_row,
            "📄",
            "Files Scanned",
            str(len(self.duplicate_files)),
            0
        )

        self.create_stat_card(
            stats_row,
            "▣",
            "Duplicate Groups",
            str(len(self.duplicate_groups)),
            1
        )

        self.create_stat_card(
            stats_row,
            "⧉",
            "Duplicate Files",
            str(duplicate_file_count),
            2
        )

        self.create_stat_card(
            stats_row,
            "♻",
            "Space Reclaimable",
            self.format_file_size(wasted_bytes),
            3
        )

        # ----------------------------------------------------
        # RESULTS TABLE
        # ----------------------------------------------------

        result_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        result_card.pack(
            fill="both",
            expand=True
        )

        result_header = tk.Frame(
            result_card,
            bg=self.colors["white"]
        )

        result_header.pack(
            fill="x",
            padx=25,
            pady=(18, 10)
        )

        tk.Label(
            result_header,
            text="Duplicate Groups",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=self.fonts["section"]
        ).pack(
            side="left"
        )

        self.duplicate_count_label = tk.Label(
            result_header,
            text="Double-click a file to copy its full path",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 8)
        )

        self.duplicate_count_label.pack(
            side="right"
        )

        table_frame = tk.Frame(
            result_card,
            bg=self.colors["white"]
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        columns = (
            "size",
            "hash"
        )

        self.duplicate_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="tree headings",
            selectmode="browse"
        )

        self.duplicate_tree.heading(
            "#0",
            text="Group / File"
        )

        self.duplicate_tree.heading(
            "size",
            text="Size"
        )

        self.duplicate_tree.heading(
            "hash",
            text="Hash Value"
        )

        self.duplicate_tree.column(
            "#0",
            width=560,
            anchor="w"
        )

        self.duplicate_tree.column(
            "size",
            width=110,
            anchor="center"
        )

        self.duplicate_tree.column(
            "hash",
            width=360,
            anchor="w"
        )

        tree_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.duplicate_tree.yview
        )

        self.duplicate_tree.configure(
            yscrollcommand=tree_scroll.set
        )

        self.duplicate_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        tree_scroll.pack(
            side="right",
            fill="y"
        )

        self.duplicate_tree.bind(
            "<Double-1>",
            self.copy_duplicate_path
        )

        self.refresh_duplicate_tree()

    # ========================================================
    # DUPLICATES — HELPERS
    # ========================================================

    def get_duplicate_selection_text(self):

        return (
            f"{len(self.duplicate_files)} file(s) selected"
        )

    def format_file_size(self, size_bytes):

        size = float(size_bytes)

        for unit in ("B", "KB", "MB", "GB", "TB"):

            if size < 1024 or unit == "TB":

                return (
                    f"{size:.0f} {unit}"
                    if unit == "B"
                    else f"{size:.2f} {unit}"
                )

            size /= 1024

        return f"{size_bytes} B"

    # ========================================================
    # DUPLICATES — SELECT FILES / FOLDER
    # ========================================================

    def select_duplicate_files(self):

        files = filedialog.askopenfilenames(
            title="Select Files to Check for Duplicates"
        )

        if not files:
            return

        for file_path in files:

            if file_path not in self.duplicate_files:
                self.duplicate_files.append(file_path)

        self.show_duplicates()

    def select_duplicate_folder(self):

        directory = filedialog.askdirectory(
            title="Select Folder to Check for Duplicates"
        )

        if not directory:
            return

        include_subfolders = (
            self.duplicate_subfolders_var.get()
            if self.duplicate_subfolders_var is not None
            else True
        )

        if include_subfolders:

            for root, _dirs, files in os.walk(directory):

                for file_name in files:

                    file_path = os.path.join(
                        root,
                        file_name
                    )

                    if file_path not in self.duplicate_files:
                        self.duplicate_files.append(file_path)

        else:

            try:

                entries = os.listdir(directory)

            except OSError as error:

                messagebox.showerror(
                    "Folder Error",
                    f"Could not read folder:\n\n{error}"
                )

                return

            for entry in entries:

                file_path = os.path.join(
                    directory,
                    entry
                )

                if (
                    os.path.isfile(file_path)
                    and file_path not in self.duplicate_files
                ):
                    self.duplicate_files.append(file_path)

        self.show_duplicates()

    def clear_duplicate_selection(self):

        self.duplicate_files = []
        self.duplicate_groups = []

        self.show_duplicates()

    # ========================================================
    # DUPLICATES — FIND
    # ========================================================

    def find_duplicates(self):

        if not self.duplicate_files:

            messagebox.showwarning(
                "No Files Selected",
                "Please add files or a folder before searching "
                "for duplicates."
            )

            return

        algorithm = (
            self.duplicate_algorithm_var.get()
            if self.duplicate_algorithm_var is not None
            else "MD5"
        )

        hash_map = {}
        errors = 0

        if hasattr(
            self,
            "duplicate_count_label"
        ):

            self.duplicate_count_label.configure(
                text="Scanning files…",
                fg=self.colors["primary"]
            )

            self.update_idletasks()

        for file_path in self.duplicate_files:

            if not os.path.isfile(file_path):
                continue

            try:

                digest = self.calculate_file_hash(
                    file_path,
                    algorithm
                )

                size = os.path.getsize(
                    file_path
                )

                key = digest

                if key not in hash_map:

                    hash_map[key] = {
                        "hash": digest,
                        "size": size,
                        "files": []
                    }

                hash_map[key]["files"].append(
                    file_path
                )

            except (
                OSError,
                PermissionError
            ) as error:

                errors += 1

                messagebox.showerror(
                    "File Error",
                    f"Could not read:\n\n"
                    f"{file_path}\n\n"
                    f"Reason:\n{error}"
                )

            except Exception as error:

                errors += 1

                messagebox.showerror(
                    "Hashing Error",
                    f"An unexpected error occurred:\n\n{error}"
                )

        self.duplicate_groups = [
            group
            for group in hash_map.values()
            if len(group["files"]) > 1
        ]

        self.duplicate_groups.sort(
            key=lambda group: group["size"] * len(group["files"]),
            reverse=True
        )

        self.stats["last_scan"] = (
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )

        self.show_duplicates()

        if not self.duplicate_groups:

            messagebox.showinfo(
                "No Duplicates Found",
                f"Scanned {len(self.duplicate_files)} file(s) "
                f"using {algorithm} — no duplicates were found."
            )

        elif errors:

            messagebox.showwarning(
                "Scan Completed with Errors",
                f"Found {len(self.duplicate_groups)} duplicate "
                f"group(s), but {errors} file(s) could not be read."
            )

    # ========================================================
    # DUPLICATES — REFRESH TREE
    # ========================================================

    def refresh_duplicate_tree(self):

        if not hasattr(
            self,
            "duplicate_tree"
        ):
            return

        for item in self.duplicate_tree.get_children():
            self.duplicate_tree.delete(item)

        for index, group in enumerate(
            self.duplicate_groups,
            start=1
        ):

            group_label = (
                f"Group {index} • "
                f"{len(group['files'])} files • "
                f"{self.format_file_size(group['size'])} each"
            )

            group_id = self.duplicate_tree.insert(
                "",
                tk.END,
                text=group_label,
                values=(
                    "",
                    group["hash"]
                ),
                open=True
            )

            for file_path in group["files"]:

                self.duplicate_tree.insert(
                    group_id,
                    tk.END,
                    text=file_path,
                    values=(
                        self.format_file_size(group["size"]),
                        group["hash"]
                    )
                )

        if hasattr(
            self,
            "duplicate_selection_label"
        ):

            self.duplicate_selection_label.configure(
                text=self.get_duplicate_selection_text()
            )

    # ========================================================
    # DUPLICATES — COPY PATH
    # ========================================================

    def copy_duplicate_path(
        self,
        event=None
    ):

        if not hasattr(
            self,
            "duplicate_tree"
        ):
            return

        selected = self.duplicate_tree.selection()

        if not selected:
            return

        item_id = selected[0]

        if self.duplicate_tree.parent(item_id) == "":
            return

        file_path = self.duplicate_tree.item(
            item_id
        ).get(
            "text",
            ""
        )

        if not file_path:
            return

        self.clipboard_clear()
        self.clipboard_append(file_path)
        self.update()

        if hasattr(
            self,
            "duplicate_count_label"
        ):

            self.duplicate_count_label.configure(
                text="File path copied to clipboard",
                fg=self.colors["success"]
            )

    # ========================================================
    # DUPLICATES — EXPORT CSV
    # ========================================================

    def export_duplicates_csv(self):

        if not self.duplicate_groups:

            messagebox.showwarning(
                "No Duplicates",
                "There are no duplicate groups to export yet."
            )

            return

        file_path = filedialog.asksaveasfilename(
            title="Export Duplicates",
            defaultextension=".csv",
            initialfile="HashForge_Duplicates.csv",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as csv_file:

                writer = csv.writer(
                    csv_file
                )

                writer.writerow([
                    "Group",
                    "File Path",
                    "Size (bytes)",
                    "Hash"
                ])

                for index, group in enumerate(
                    self.duplicate_groups,
                    start=1
                ):

                    for file_item in group["files"]:

                        writer.writerow([
                            index,
                            file_item,
                            group["size"],
                            group["hash"]
                        ])

            messagebox.showinfo(
                "Export Complete",
                f"Duplicate report exported to:\n\n{file_path}"
            )

        except OSError as error:

            messagebox.showerror(
                "Export Error",
                f"Could not export duplicates:\n\n{error}"
            )

    # ========================================================
    # SETTINGS
    # ========================================================

    def show_settings(self):

        self.clear_main()
        self.set_active_nav("Settings")

        container = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )

        container.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=35
        )

        tk.Label(
            container,
            text="Settings",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.fonts["title"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            container,
            text="Customize the appearance of HashForge",
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
            font=self.fonts["subtitle"]
        ).pack(
            anchor="w",
            pady=(4, 30)
        )

        theme_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        theme_card.pack(
            fill="x"
        )

        tk.Label(
            theme_card,
            text="Appearance",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        tk.Label(
            theme_card,
            text="Choose a HashForge color theme.",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        themes_frame = tk.Frame(
            theme_card,
            bg=self.colors["white"]
        )

        themes_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 30)
        )

        theme_info = {
            "Emerald": (
                "#087F6B",
                "Professional teal"
            ),
            "Midnight": (
                "#20C997",
                "Dark mode"
            ),
            "Ocean": (
                "#087EA4",
                "Cool blue"
            ),
            "Royal": (
                "#6D28D9",
                "Purple accent"
            )
        }

        for index, theme_name in enumerate(
            theme_info
        ):

            color, description = theme_info[
                theme_name
            ]

            theme_button = tk.Frame(
                themes_frame,
                bg=self.colors["white"],
                highlightbackground=(
                    color
                    if theme_name == self.current_theme
                    else self.colors["border"]
                ),
                highlightthickness=2,
                cursor="hand2"
            )

            theme_button.grid(
                row=0,
                column=index,
                padx=7,
                sticky="nsew"
            )

            themes_frame.grid_columnconfigure(
                index,
                weight=1
            )

            color_box = tk.Canvas(
                theme_button,
                width=55,
                height=55,
                bg=self.colors["white"],
                highlightthickness=0
            )

            color_box.pack(
                pady=(18, 8)
            )

            color_box.create_oval(
                5,
                5,
                50,
                50,
                fill=color,
                outline=""
            )

            if theme_name == self.current_theme:

                color_box.create_text(
                    27,
                    27,
                    text="✓",
                    fill="white",
                    font=("Segoe UI", 17, "bold")
                )

            tk.Label(
                theme_button,
                text=theme_name,
                bg=self.colors["white"],
                fg=self.colors["text"],
                font=("Segoe UI", 10, "bold")
            ).pack()

            tk.Label(
                theme_button,
                text=description,
                bg=self.colors["white"],
                fg=self.colors["secondary"],
                font=("Segoe UI", 8)
            ).pack(
                pady=(3, 18)
            )

            for widget in (
                theme_button,
                color_box
            ):

                widget.bind(
                    "<Button-1>",
                    lambda event, t=theme_name:
                    self.change_theme(t)
                )

        # Developer information

        developer_card = tk.Frame(
            container,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        developer_card.pack(
            fill="x",
            pady=(20, 0)
        )

        tk.Label(
            developer_card,
            text="Developer Information",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        tk.Label(
            developer_card,
            text="About the developer of HashForge.",
            bg=self.colors["white"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 15)
        )

        developer_info = tk.Frame(
            developer_card,
            bg=self.colors["white"]
        )

        developer_info.pack(
            anchor="w",
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        detail_rows = [
            (
                "Name",
                "Nikhil Choudhary",
                None
            ),
            (
                "Course",
                "MCA",
                None
            ),
            (
                "GitHub",
                "github.com/GodNikhilYT",
                "https://github.com/GodNikhilYT"
            ),
            (
                "LinkedIn",
                "linkedin.com/in/nikhil-choudhary-mca-student-java-developer",
                "https://in.linkedin.com/in/nikhil-choudhary-mca-student-java-developer"
            )
        ]

        for label_text, value_text, url in detail_rows:

            row = tk.Frame(
                developer_info,
                bg=self.colors["white"]
            )

            row.pack(
                anchor="w",
                fill="x",
                pady=4
            )

            tk.Label(
                row,
                text=label_text,
                bg=self.colors["white"],
                fg=self.colors["secondary"],
                font=("Segoe UI", 9, "bold"),
                width=10,
                anchor="w"
            ).pack(
                side="left"
            )

            value_label = tk.Label(
                row,
                text=value_text,
                bg=self.colors["white"],
                fg=(
                    self.colors["primary"]
                    if url
                    else self.colors["text"]
                ),
                font=(
                    ("Segoe UI", 9, "underline")
                    if url
                    else ("Segoe UI", 9)
                ),
                cursor="hand2" if url else "arrow",
                anchor="w"
            )

            value_label.pack(
                side="left"
            )

            if url:

                value_label.bind(
                    "<Button-1>",
                    lambda event, link=url: self.open_developer_link(link)
                )

        # Current case

        case_card = tk.Frame(
            container,
            bg=self.colors["primary_light"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        case_card.pack(
            fill="x",
            pady=20
        )

        tk.Label(
            case_card,
            text="Current Case",
            bg=self.colors["primary_light"],
            fg=self.colors["text"],
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        current_case = (
            self.case_information.get(
                "case_name"
            )
            or "No case created yet"
        )

        tk.Label(
            case_card,
            text=current_case,
            bg=self.colors["primary_light"],
            fg=self.colors["secondary"],
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        tk.Button(
            case_card,
            text="Edit Case Information",
            command=self.show_case_information,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            relief="flat",
            padx=20,
            pady=8,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )


    # ========================================================
    # SETTINGS — OPEN DEVELOPER LINK
    # ========================================================

    def open_developer_link(self, url):

        try:

            webbrowser.open_new_tab(
                url
            )

        except Exception as error:

            messagebox.showerror(
                "Could Not Open Link",
                f"Unable to open the link:\n\n{error}"
            )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app = HashForgeApp()

    app.mainloop()
