#!/usr/bin/env python3
"""
DarkDork Modern - Professional Google Dorking Tool
Modern dark-themed tkinter interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font as tkfont
import webbrowser
import json
import csv
import datetime
import threading
import time
import urllib.parse
from typing import List, Dict, Optional
import os

# Try to load the library system
try:
    from darkdork_library import DorkLibrary
except ImportError:
    DorkLibrary = None


class ModernDarkDorkApp:
    """Modern dark-themed DarkDork application"""

    # Modern color scheme (dark theme like DorkNexus)
    COLORS = {
        'bg_dark': '#0a1628',      # Very dark blue background
        'bg_medium': '#1a2332',    # Medium dark blue
        'bg_light': '#2a3442',     # Lighter blue for cards
        'accent': '#00d4ff',       # Cyan accent color
        'accent_hover': '#00b8e6', # Darker cyan for hover
        'text_primary': '#ffffff', # White text
        'text_secondary': '#8b9db5', # Gray text
        'border': '#3a4452',       # Border color
        'success': '#00ff88',      # Green
        'warning': '#ffaa00',      # Orange
        'danger': '#ff4444',       # Red
        'info': '#4488ff',         # Blue
    }

    def __init__(self, root):
        self.root = root
        self.root.title("DarkDork Professional - Modern Interface")
        self.root.geometry("1400x900")

        # Configure root background
        self.root.configure(bg=self.COLORS['bg_dark'])

        # Try to load dork library
        self.library = DorkLibrary() if DorkLibrary else None
        if self.library and len(self.library.dorks) == 0:
            self.init_library()

        # Application state
        self.search_history = []
        self.current_category = "All Intelligence"
        self.target_domain = tk.StringVar()

        # Configure styles
        self.setup_styles()

        # Create modern fonts
        self.setup_fonts()

        # Create UI
        self.create_modern_ui()

    def init_library(self):
        """Initialize the dork library"""
        try:
            from darkdork_library import create_comprehensive_library
            self.library = create_comprehensive_library()
        except Exception as e:
            print(f"Could not initialize library: {e}")

    def setup_fonts(self):
        """Setup modern fonts"""
        self.fonts = {
            'title': tkfont.Font(family='Helvetica', size=24, weight='bold'),
            'heading': tkfont.Font(family='Helvetica', size=16, weight='bold'),
            'subheading': tkfont.Font(family='Helvetica', size=12, weight='bold'),
            'body': tkfont.Font(family='Helvetica', size=10),
            'small': tkfont.Font(family='Helvetica', size=9),
            'mono': tkfont.Font(family='Courier', size=9),
        }

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()

        # Configure dark theme
        style.theme_use('clam')

        # Configure general style
        style.configure('.',
            background=self.COLORS['bg_dark'],
            foreground=self.COLORS['text_primary'],
            fieldbackground=self.COLORS['bg_medium'],
            bordercolor=self.COLORS['border'],
            darkcolor=self.COLORS['bg_dark'],
            lightcolor=self.COLORS['bg_light'],
            troughcolor=self.COLORS['bg_medium'],
            selectbackground=self.COLORS['accent'],
            selectforeground=self.COLORS['text_primary']
        )

        # Frame styles
        style.configure('Card.TFrame',
            background=self.COLORS['bg_light'],
            relief='flat',
            borderwidth=1
        )

        style.configure('Sidebar.TFrame',
            background=self.COLORS['bg_medium']
        )

        # Label styles
        style.configure('Title.TLabel',
            font=('Helvetica', 18, 'bold'),
            background=self.COLORS['bg_dark'],
            foreground=self.COLORS['text_primary']
        )

        style.configure('Heading.TLabel',
            font=('Helvetica', 14, 'bold'),
            background=self.COLORS['bg_medium'],
            foreground=self.COLORS['text_primary']
        )

        style.configure('CardTitle.TLabel',
            font=('Helvetica', 11, 'bold'),
            background=self.COLORS['bg_light'],
            foreground=self.COLORS['text_primary']
        )

        style.configure('CardDesc.TLabel',
            font=('Helvetica', 9),
            background=self.COLORS['bg_light'],
            foreground=self.COLORS['text_secondary']
        )

        style.configure('Category.TLabel',
            font=('Helvetica', 9),
            background=self.COLORS['bg_light'],
            foreground=self.COLORS['info']
        )

        # Button styles
        style.configure('Accent.TButton',
            font=('Helvetica', 10, 'bold'),
            background=self.COLORS['accent'],
            foreground='#000000',
            borderwidth=0,
            focuscolor='none',
            padding=(20, 10)
        )

        style.map('Accent.TButton',
            background=[('active', self.COLORS['accent_hover'])],
            foreground=[('active', '#000000')]
        )

        style.configure('Category.TButton',
            font=('Helvetica', 10),
            background=self.COLORS['bg_medium'],
            foreground=self.COLORS['text_secondary'],
            borderwidth=0,
            focuscolor='none',
            padding=(15, 8),
            anchor='w'
        )

        style.map('Category.TButton',
            background=[('active', self.COLORS['bg_light'])],
            foreground=[('active', self.COLORS['text_primary'])]
        )

        # Entry style
        style.configure('Modern.TEntry',
            fieldbackground=self.COLORS['bg_medium'],
            foreground=self.COLORS['text_primary'],
            bordercolor=self.COLORS['border'],
            lightcolor=self.COLORS['bg_medium'],
            darkcolor=self.COLORS['bg_medium'],
            insertcolor=self.COLORS['text_primary']
        )

    def create_modern_ui(self):
        """Create modern UI layout"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Top bar with title and query builder
        self.create_top_bar(main_container)

        # Content area (sidebar + main)
        content = tk.Frame(main_container, bg=self.COLORS['bg_dark'])
        content.pack(fill=tk.BOTH, expand=True)

        # Sidebar (left)
        self.create_sidebar(content)

        # Main area (right)
        self.create_main_area(content)

    def create_top_bar(self, parent):
        """Create top bar with title and query builder"""
        top_bar = tk.Frame(parent, bg=self.COLORS['bg_dark'], height=200)
        top_bar.pack(fill=tk.X, padx=20, pady=20)
        top_bar.pack_propagate(False)

        # Title
        title_label = tk.Label(
            top_bar,
            text="DarkNexus",
            font=self.fonts['title'],
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary']
        )
        title_label.pack(anchor='w', pady=(0, 20))

        # Query builder card
        query_card = tk.Frame(top_bar, bg=self.COLORS['bg_light'], relief='flat', bd=1)
        query_card.pack(fill=tk.X)

        # Query builder padding
        query_inner = tk.Frame(query_card, bg=self.COLORS['bg_light'])
        query_inner.pack(fill=tk.BOTH, padx=20, pady=15)

        # Search input
        search_label = tk.Label(
            query_inner,
            text="Construct a query below or type here...",
            font=self.fonts['body'],
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_secondary']
        )
        search_label.pack(anchor='w', pady=(0, 10))

        # Input row
        input_frame = tk.Frame(query_inner, bg=self.COLORS['bg_light'])
        input_frame.pack(fill=tk.X)

        self.query_entry = tk.Entry(
            input_frame,
            font=self.fonts['body'],
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary'],
            insertbackground=self.COLORS['text_primary'],
            relief='flat',
            bd=0
        )
        self.query_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, ipadx=10)

        # Copy button
        copy_btn = tk.Button(
            input_frame,
            text="📋 Copy Query",
            font=self.fonts['body'],
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_primary'],
            activebackground=self.COLORS['bg_light'],
            activeforeground=self.COLORS['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            command=self.copy_query
        )
        copy_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Search button
        search_btn = tk.Button(
            input_frame,
            text="🔍 Search on Google",
            font=self.fonts['body'],
            bg=self.COLORS['accent'],
            fg='#000000',
            activebackground=self.COLORS['accent_hover'],
            activeforeground='#000000',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            command=self.execute_query
        )
        search_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Query builder fields
        builder_frame = tk.Frame(query_inner, bg=self.COLORS['bg_light'])
        builder_frame.pack(fill=tk.X, pady=(15, 0))

        # Create query builder fields
        self.create_query_builder(builder_frame)

    def create_query_builder(self, parent):
        """Create query builder input fields"""
        fields = [
            ("🎯 TARGET SITE", "site", "e.g., nasa.gov or .edu"),
            ("📁 FILE TYPE", "filetype", "e.g., pdf, xlsx, docx, log"),
            ("📝 IN TITLE", "intitle", "e.g., index of, login"),
            ("🔗 IN URL", "inurl", "e.g., admin, config"),
            ("📄 IN TEXT", "intext", "e.g., password, confidential"),
            ("✓ EXACT MATCH", "exact", "e.g., Top secret"),
        ]

        self.builder_vars = {}

        # Create two rows of three fields each
        for row in range(2):
            row_frame = tk.Frame(parent, bg=self.COLORS['bg_light'])
            row_frame.pack(fill=tk.X, pady=5)

            for col in range(3):
                idx = row * 3 + col
                if idx >= len(fields):
                    break

                label_text, field_name, placeholder = fields[idx]

                field_frame = tk.Frame(row_frame, bg=self.COLORS['bg_light'])
                field_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

                # Label
                label = tk.Label(
                    field_frame,
                    text=label_text,
                    font=self.fonts['small'],
                    bg=self.COLORS['bg_light'],
                    fg=self.COLORS['text_secondary']
                )
                label.pack(anchor='w', pady=(0, 5))

                # Entry
                var = tk.StringVar()
                self.builder_vars[field_name] = var

                entry = tk.Entry(
                    field_frame,
                    textvariable=var,
                    font=self.fonts['body'],
                    bg=self.COLORS['bg_dark'],
                    fg=self.COLORS['text_primary'],
                    insertbackground=self.COLORS['text_primary'],
                    relief='flat',
                    bd=0
                )
                entry.pack(fill=tk.X, ipady=6, ipadx=8)
                entry.bind('<KeyRelease>', lambda e: self.build_query_from_fields())

                # Placeholder
                entry.insert(0, placeholder)
                entry.config(fg=self.COLORS['text_secondary'])

                def on_focus_in(e, entry=entry, placeholder=placeholder):
                    if entry.get() == placeholder:
                        entry.delete(0, tk.END)
                        entry.config(fg=self.COLORS['text_primary'])

                def on_focus_out(e, entry=entry, placeholder=placeholder):
                    if not entry.get():
                        entry.insert(0, placeholder)
                        entry.config(fg=self.COLORS['text_secondary'])

                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<FocusOut>', on_focus_out)

    def create_sidebar(self, parent):
        """Create category sidebar"""
        sidebar = tk.Frame(parent, bg=self.COLORS['bg_medium'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Sidebar padding
        sidebar_inner = tk.Frame(sidebar, bg=self.COLORS['bg_medium'])
        sidebar_inner.pack(fill=tk.BOTH, padx=15, pady=20)

        # Search library
        search_label = tk.Label(
            sidebar_inner,
            text="Search library...",
            font=self.fonts['small'],
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_secondary']
        )
        search_label.pack(anchor='w', pady=(0, 5))

        search_entry = tk.Entry(
            sidebar_inner,
            font=self.fonts['body'],
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary'],
            insertbackground=self.COLORS['text_primary'],
            relief='flat',
            bd=0
        )
        search_entry.pack(fill=tk.X, ipady=6, ipadx=8, pady=(0, 20))

        # Categories
        categories = self.get_categories()

        for cat in categories:
            btn = tk.Button(
                sidebar_inner,
                text=f"  {cat['icon']} {cat['name']:<20} {cat['count']:>2}",
                font=self.fonts['body'],
                bg=self.COLORS['bg_medium'],
                fg=self.COLORS['text_secondary'],
                activebackground=self.COLORS['bg_light'],
                activeforeground=self.COLORS['text_primary'],
                relief='flat',
                bd=0,
                anchor='w',
                padx=10,
                pady=8,
                command=lambda c=cat['name']: self.select_category(c)
            )
            btn.pack(fill=tk.X, pady=2)

    def create_main_area(self, parent):
        """Create main dork display area"""
        main_area = tk.Frame(parent, bg=self.COLORS['bg_dark'])
        main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=0)

        # Scrollable canvas for dork cards
        canvas = tk.Canvas(main_area, bg=self.COLORS['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_area, orient="vertical", command=canvas.yview)

        self.dorks_frame = tk.Frame(canvas, bg=self.COLORS['bg_dark'])
        self.dorks_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.dorks_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Load initial dorks
        self.load_dorks("All Intelligence")

    def get_categories(self):
        """Get categories with icons and counts"""
        if self.library:
            cat_counts = {}
            for dork in self.library.dorks:
                cat = dork.get('category', 'Other')
                cat_counts[cat] = cat_counts.get(cat, 0) + 1

            total = len(self.library.dorks)

            categories = [
                {"name": "All Intelligence", "icon": "📚", "count": total},
            ]

            for cat, count in sorted(cat_counts.items()):
                icon = self.get_category_icon(cat)
                categories.append({"name": cat, "icon": icon, "count": count})

            return categories
        else:
            return [
                {"name": "All Intelligence", "icon": "📚", "count": 61},
                {"name": "Cloud Infrastructure", "icon": "☁️", "count": 9},
                {"name": "DevOps & CI/CD", "icon": "⚙️", "count": 10},
                {"name": "Databases", "icon": "💾", "count": 9},
                {"name": "Sensitive Files", "icon": "📁", "count": 9},
                {"name": "Vulnerabilities", "icon": "🔓", "count": 8},
                {"name": "IoT & Cameras", "icon": "📷", "count": 8},
                {"name": "Network Admin", "icon": "🌐", "count": 4},
                {"name": "Misc & OSINT", "icon": "🔍", "count": 4},
            ]

    def get_category_icon(self, category):
        """Get icon for category"""
        icons = {
            "Exposed Documents": "📄",
            "Login Pages": "🔐",
            "Configuration": "⚙️",
            "Databases": "💾",
            "API & Secrets": "🔑",
            "Cloud Storage": "☁️",
            "Network Devices": "🌐",
            "Source Code": "💻",
            "Web Applications": "🌍",
            "CI/CD": "🔧",
            "Error Messages": "⚠️",
            "OSINT": "🔍",
            "Mobile": "📱",
            "Financial": "💰",
            "Healthcare": "⚕️",
        }
        return icons.get(category, "📌")

    def select_category(self, category):
        """Select a category and load its dorks"""
        self.current_category = category
        self.load_dorks(category)

    def load_dorks(self, category):
        """Load dorks for selected category"""
        # Clear existing
        for widget in self.dorks_frame.winfo_children():
            widget.destroy()

        # Get dorks
        if self.library:
            if category == "All Intelligence":
                dorks = self.library.dorks
            else:
                dorks = [d for d in self.library.dorks if d.get('category') == category]
        else:
            # Mock dorks for display
            dorks = self.get_mock_dorks(category)

        # Create dork cards in grid layout (3 columns)
        row = 0
        col = 0
        for dork in dorks:
            card = self.create_dork_card(self.dorks_frame, dork)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')

            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Configure column weights
        for i in range(3):
            self.dorks_frame.columnconfigure(i, weight=1)

    def create_dork_card(self, parent, dork):
        """Create a modern dork card"""
        card = tk.Frame(parent, bg=self.COLORS['bg_light'], relief='flat', bd=0)

        # Card padding
        card_inner = tk.Frame(card, bg=self.COLORS['bg_light'])
        card_inner.pack(fill=tk.BOTH, padx=15, pady=15)

        # Category badge
        category = dork.get('category', 'Other')
        category_label = tk.Label(
            card_inner,
            text=category.upper(),
            font=self.fonts['small'],
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['info'],
            padx=8,
            pady=3
        )
        category_label.pack(anchor='w', pady=(0, 8))

        # Title/Name
        name = dork.get('name', dork.get('query', 'Unknown'))[:50]
        title_label = tk.Label(
            card_inner,
            text=name,
            font=self.fonts['subheading'],
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_primary'],
            anchor='w',
            justify='left',
            wraplength=300
        )
        title_label.pack(anchor='w', fill=tk.X, pady=(0, 8))

        # Description
        desc = dork.get('description', 'No description')[:100]
        desc_label = tk.Label(
            card_inner,
            text=desc,
            font=self.fonts['small'],
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_secondary'],
            anchor='w',
            justify='left',
            wraplength=300
        )
        desc_label.pack(anchor='w', fill=tk.X, pady=(0, 10))

        # Query (monospace)
        query = dork.get('query', '')
        query_frame = tk.Frame(card_inner, bg=self.COLORS['bg_dark'])
        query_frame.pack(fill=tk.X, pady=(0, 10))

        query_label = tk.Label(
            query_frame,
            text=query[:60] + ('...' if len(query) > 60 else ''),
            font=self.fonts['mono'],
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent'],
            anchor='w',
            padx=10,
            pady=8
        )
        query_label.pack(fill=tk.X)

        # Copy button
        copy_btn = tk.Button(
            card_inner,
            text="📋 Copy",
            font=self.fonts['small'],
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_primary'],
            activebackground=self.COLORS['bg_dark'],
            activeforeground=self.COLORS['text_primary'],
            relief='flat',
            bd=0,
            padx=10,
            pady=5,
            command=lambda q=query: self.copy_to_clipboard(q)
        )
        copy_btn.pack(side=tk.LEFT)

        # Execute button
        exec_btn = tk.Button(
            card_inner,
            text="🔍 Execute",
            font=self.fonts['small'],
            bg=self.COLORS['accent'],
            fg='#000000',
            activebackground=self.COLORS['accent_hover'],
            activeforeground='#000000',
            relief='flat',
            bd=0,
            padx=10,
            pady=5,
            command=lambda q=query: self.execute_dork(q)
        )
        exec_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Hover effect
        def on_enter(e):
            card.configure(bg=self.COLORS['border'])

        def on_leave(e):
            card.configure(bg=self.COLORS['bg_light'])

        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)

        return card

    def get_mock_dorks(self, category):
        """Get mock dorks for display"""
        return [
            {
                "name": "Exposed .env configuration",
                "query": 'filetype:env "DB_PASSWORD"',
                "category": "Configuration",
                "description": "Find exposed .env files with database credentials"
            },
            {
                "name": "Error logs with stack traces",
                "query": 'filetype:log "fatal error"',
                "category": "Error Messages",
                "description": "Locate error log files with detailed stack traces"
            },
            {
                "name": "Leaked SSH keys",
                "query": 'intitle:"index of" "id_rsa"',
                "category": "API & Secrets",
                "description": "Find accidentally exposed SSH private keys"
            }
        ]

    def build_query_from_fields(self):
        """Build query from builder fields"""
        parts = []

        for field, var in self.builder_vars.items():
            value = var.get().strip()
            # Skip if placeholder or empty
            if not value or value.startswith('e.g.,'):
                continue

            if field == 'site':
                parts.append(f"site:{value}")
            elif field == 'filetype':
                parts.append(f"filetype:{value}")
            elif field == 'intitle':
                if ' ' in value:
                    parts.append(f'intitle:"{value}"')
                else:
                    parts.append(f"intitle:{value}")
            elif field == 'inurl':
                parts.append(f"inurl:{value}")
            elif field == 'intext':
                if ' ' in value:
                    parts.append(f'intext:"{value}"')
                else:
                    parts.append(f"intext:{value}")
            elif field == 'exact':
                parts.append(f'"{value}"')

        query = ' '.join(parts)
        self.query_entry.delete(0, tk.END)
        self.query_entry.insert(0, query)

    def copy_query(self):
        """Copy query to clipboard"""
        query = self.query_entry.get()
        if query:
            self.root.clipboard_clear()
            self.root.clipboard_append(query)
            messagebox.showinfo("Copied", "Query copied to clipboard!")

    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.query_entry.delete(0, tk.END)
        self.query_entry.insert(0, text)

    def execute_query(self):
        """Execute current query"""
        query = self.query_entry.get()
        if query:
            self.execute_dork(query)

    def execute_dork(self, query):
        """Execute a dork query"""
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)

        # Record in history
        self.search_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'query': query,
            'status': 'executed'
        })


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernDarkDorkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
