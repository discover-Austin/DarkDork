#!/usr/bin/env python3
"""
DarkDork - Professional Google Dorking Tool
For Forensic and Cybersecurity Organizations

Copyright 2026
Licensed under the Apache License, Version 2.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import webbrowser
import json
import csv
import datetime
import threading
import time
import urllib.parse
from typing import List, Dict, Optional
import os


class DorkCategory:
    """Represents a category of Google dorks for security research"""

    CATEGORIES = {
        "Exposed Documents": [
            'filetype:pdf "confidential"',
            'filetype:xls "password"',
            'filetype:doc "internal use only"',
            'filetype:csv "email"',
            'filetype:txt "password"',
            'filetype:docx "confidential"',
            'filetype:xlsx "budget"',
            'filetype:pptx "confidential presentation"'
        ],
        "Login Pages": [
            'inurl:admin intitle:login',
            'inurl:wp-admin',
            'inurl:login.php',
            'intitle:"Index of" "admin"',
            'inurl:admin/login.php',
            'intitle:"phpMyAdmin" "Welcome to phpMyAdmin"',
            'inurl:administrator',
            'inurl:auth_user_file.txt'
        ],
        "Vulnerable Servers": [
            'intitle:"Index of" .bash_history',
            'intitle:"Index of" "database.sql"',
            'intitle:"Index of" "backup"',
            'intitle:"Index of" "config"',
            'intitle:"Index of" "mysql"',
            'intitle:"Index of" ".env"',
            'intitle:"Index of" "wp-config.php"',
            'filetype:env "DB_PASSWORD"'
        ],
        "Network Devices": [
            'intitle:"Network Camera" inurl:ViewerFrame',
            'inurl:8080 intitle:"Surveillance"',
            'intitle:"netcam live image"',
            'intitle:"Network Device" inurl:login.asp',
            'intitle:"NAS" inurl:login',
            'intext:"Powered by Webcamxp"',
            'inurl:":8080" intitle:"DVR"'
        ],
        "SQL Errors": [
            'intext:"SQL syntax" site:',
            'intext:"mysql_fetch" site:',
            'intext:"Warning: mysql" site:',
            'intext:"Error Occurred While Processing Request" site:',
            'intext:"Microsoft OLE DB Provider for SQL Server" site:',
            'intext:"Unclosed quotation mark" site:',
            'intext:"ODBC Driver error" site:'
        ],
        "Sensitive Directories": [
            'intitle:"Index of" "parent directory"',
            'intitle:"Index of" "/private"',
            'intitle:"Index of" "/logs"',
            'intitle:"Index of" "/admin"',
            'intitle:"Index of" "/backup"',
            'intitle:"Index of" "/db"',
            'intitle:"Index of" "credentials"'
        ],
        "Exposed Credentials": [
            'filetype:log username password',
            'filetype:sql "password" | "pwd"',
            'filetype:ini intext:env("DB_PASSWORD")',
            'intext:"connectionString" "password"',
            'filetype:config "connectionString"',
            'filetype:properties "password"',
            '"BEGIN RSA PRIVATE KEY" site:'
        ],
        "Vulnerable Web Apps": [
            'inurl:shell.php',
            'inurl:backdoor',
            'inurl:r57.php',
            'inurl:c99.php',
            'inurl:cmd.php',
            'inurl:webshell',
            'inurl:security.txt'
        ],
        "IoT Devices": [
            'inurl:camera intitle:"Home"',
            'intitle:"smart home" inurl:web',
            'inurl:sonos',
            'intitle:"Dashboard" "smart meter"',
            'inurl:8080 intitle:"control panel"',
            'intitle:"Device Management" inurl:8080'
        ],
        "API Keys & Tokens": [
            'filetype:env "API_KEY"',
            'filetype:env "SECRET_KEY"',
            '"authorization: Bearer" site:',
            'filetype:json "api_key"',
            'filetype:yml "access_token"',
            '"x-api-key" site:',
            'filetype:config "apikey"'
        ]
    }


class DarkDorkApp:
    """Main application class for DarkDork"""

    def __init__(self, root):
        self.root = root
        self.root.title("DarkDork - Professional Google Dorking Tool v1.0")
        self.root.geometry("1200x800")

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Application state
        self.search_history = []
        self.current_results = []
        self.config = self.load_config()

        # Create UI
        self.create_menu()
        self.create_ui()

        # Status
        self.status_var = tk.StringVar(value="Ready")
        self.create_status_bar()

    def load_config(self) -> Dict:
        """Load configuration from file"""
        config_file = "darkdork_config.json"
        default_config = {
            "rate_limit_seconds": 2,
            "results_per_page": 10,
            "auto_export": False,
            "default_export_format": "csv",
            "search_engine": "google"
        }

        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return {**default_config, **json.load(f)}
            except:
                return default_config
        return default_config

    def save_config(self):
        """Save configuration to file"""
        try:
            with open("darkdork_config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")

    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_command(label="Export History", command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Clear History", command=self.clear_history)
        tools_menu.add_command(label="Batch Search", command=self.batch_search)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)

    def create_ui(self):
        """Create main user interface"""
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_container, text="DarkDork - Professional Google Dorking Tool",
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Create notebook for tabs
        notebook = ttk.Notebook(main_container)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Tab 1: Dork Categories
        self.categories_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.categories_frame, text="Dork Categories")
        self.create_categories_tab()

        # Tab 2: Custom Dork Builder
        self.custom_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.custom_frame, text="Custom Dork Builder")
        self.create_custom_tab()

        # Tab 3: Search History
        self.history_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.history_frame, text="Search History")
        self.create_history_tab()

        # Results area
        results_frame = ttk.LabelFrame(main_container, text="Search Results", padding="10")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_frame, height=15,
                                                      font=('Courier', 10))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_categories_tab(self):
        """Create the dork categories tab"""
        # Category selection
        cat_select_frame = ttk.Frame(self.categories_frame)
        cat_select_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(cat_select_frame, text="Category:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, padx=5, sticky=tk.W)

        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(cat_select_frame, textvariable=self.category_var,
                                          values=list(DorkCategory.CATEGORIES.keys()),
                                          state='readonly', width=40)
        self.category_combo.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
        cat_select_frame.columnconfigure(1, weight=1)

        # Dork selection listbox
        list_frame = ttk.Frame(self.categories_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.categories_frame.rowconfigure(1, weight=1)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.dork_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       font=('Courier', 9), selectmode=tk.SINGLE)
        self.dork_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.dork_listbox.yview)

        # Target domain input
        target_frame = ttk.Frame(self.categories_frame)
        target_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        target_frame.columnconfigure(1, weight=1)

        ttk.Label(target_frame, text="Target Domain (optional):").grid(
            row=0, column=0, padx=5, sticky=tk.W)
        self.target_domain_var = tk.StringVar()
        ttk.Entry(target_frame, textvariable=self.target_domain_var).grid(
            row=0, column=1, padx=5, sticky=(tk.W, tk.E))

        # Buttons
        button_frame = ttk.Frame(self.categories_frame)
        button_frame.grid(row=3, column=0, pady=10)

        ttk.Button(button_frame, text="Execute Dork",
                  command=self.execute_selected_dork).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Execute All in Category",
                  command=self.execute_category).grid(row=0, column=1, padx=5)

    def create_custom_tab(self):
        """Create the custom dork builder tab"""
        # Instructions
        ttk.Label(self.custom_frame,
                 text="Build custom Google dorks using the operators below:",
                 font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=2,
                                                      pady=5, sticky=tk.W)

        # Operators reference
        operators_frame = ttk.LabelFrame(self.custom_frame, text="Google Dork Operators",
                                        padding="10")
        operators_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        operators_text = """
site:           Limit results to specific domain (e.g., site:example.com)
filetype:       Search for specific file types (e.g., filetype:pdf)
intitle:        Search page titles (e.g., intitle:"index of")
inurl:          Search URLs (e.g., inurl:admin)
intext:         Search page content (e.g., intext:password)
ext:            File extension (e.g., ext:sql)
cache:          View Google's cached version of a page
link:           Find pages linking to a URL
related:        Find related websites
info:           Get information about a page
"""

        ttk.Label(operators_frame, text=operators_text, font=('Courier', 9),
                 justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)

        # Custom dork input
        input_frame = ttk.LabelFrame(self.custom_frame, text="Build Your Dork", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(0, weight=1)

        self.custom_dork_var = tk.StringVar()
        custom_entry = ttk.Entry(input_frame, textvariable=self.custom_dork_var,
                                font=('Courier', 10))
        custom_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Quick insert buttons
        quick_frame = ttk.Frame(input_frame)
        quick_frame.grid(row=1, column=0, pady=5)

        operators = [
            ("site:", "site:"),
            ("filetype:", "filetype:"),
            ("intitle:", "intitle:"),
            ("inurl:", "inurl:"),
            ("intext:", "intext:"),
            ("ext:", "ext:")
        ]

        for idx, (label, op) in enumerate(operators):
            ttk.Button(quick_frame, text=label, width=10,
                      command=lambda o=op: self.insert_operator(o)).grid(
                          row=0, column=idx, padx=2)

        # Execute button
        ttk.Button(input_frame, text="Execute Custom Dork",
                  command=self.execute_custom_dork).grid(row=2, column=0, pady=10)

        # Saved custom dorks
        saved_frame = ttk.LabelFrame(self.custom_frame, text="Saved Custom Dorks",
                                    padding="10")
        saved_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S),
                        pady=5)
        saved_frame.columnconfigure(0, weight=1)
        saved_frame.rowconfigure(0, weight=1)

        self.custom_frame.rowconfigure(3, weight=1)

        self.saved_dorks_listbox = tk.Listbox(saved_frame, font=('Courier', 9))
        self.saved_dorks_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        saved_buttons = ttk.Frame(saved_frame)
        saved_buttons.grid(row=1, column=0, pady=5)

        ttk.Button(saved_buttons, text="Save Current",
                  command=self.save_custom_dork).grid(row=0, column=0, padx=2)
        ttk.Button(saved_buttons, text="Load Selected",
                  command=self.load_custom_dork).grid(row=0, column=1, padx=2)
        ttk.Button(saved_buttons, text="Delete Selected",
                  command=self.delete_custom_dork).grid(row=0, column=2, padx=2)

        self.load_saved_dorks()

    def create_history_tab(self):
        """Create the search history tab"""
        # History table
        columns = ('timestamp', 'dork', 'status')
        self.history_tree = ttk.Treeview(self.history_frame, columns=columns,
                                        show='headings', height=20)

        self.history_tree.heading('timestamp', text='Timestamp')
        self.history_tree.heading('dork', text='Dork Query')
        self.history_tree.heading('status', text='Status')

        self.history_tree.column('timestamp', width=150)
        self.history_tree.column('dork', width=400)
        self.history_tree.column('status', width=100)

        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.history_frame.columnconfigure(0, weight=1)
        self.history_frame.rowconfigure(0, weight=1)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL,
                                 command=self.history_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = ttk.Frame(self.history_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Repeat Search",
                  command=self.repeat_search).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear History",
                  command=self.clear_history).grid(row=0, column=1, padx=5)

    def create_status_bar(self):
        """Create status bar at bottom of window"""
        status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        ttk.Label(status_bar, textvariable=self.status_var,
                 anchor=tk.W).grid(row=0, column=0, sticky=(tk.W, tk.E))
        status_bar.columnconfigure(0, weight=1)

    def on_category_selected(self, event):
        """Handle category selection"""
        category = self.category_var.get()
        if category in DorkCategory.CATEGORIES:
            self.dork_listbox.delete(0, tk.END)
            for dork in DorkCategory.CATEGORIES[category]:
                self.dork_listbox.insert(tk.END, dork)

    def insert_operator(self, operator: str):
        """Insert operator into custom dork entry"""
        current = self.custom_dork_var.get()
        if current and not current.endswith(' '):
            current += ' '
        self.custom_dork_var.set(current + operator)

    def build_search_url(self, dork: str) -> str:
        """Build Google search URL from dork"""
        target_domain = self.target_domain_var.get().strip()

        if target_domain:
            if 'site:' not in dork.lower():
                dork = f'site:{target_domain} {dork}'

        encoded_query = urllib.parse.quote(dork)
        return f"https://www.google.com/search?q={encoded_query}"

    def execute_dork(self, dork: str):
        """Execute a single dork query"""
        self.status_var.set(f"Executing: {dork}")

        try:
            url = self.build_search_url(dork)

            # Add to results
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = f"\n{'='*80}\n"
            result += f"[{timestamp}] Dork: {dork}\n"
            result += f"Search URL: {url}\n"
            result += f"{'='*80}\n"

            self.results_text.insert(tk.END, result)
            self.results_text.see(tk.END)

            # Add to history
            self.add_to_history(dork, "Executed")

            # Open in browser
            webbrowser.open(url)

            # Rate limiting
            time.sleep(self.config.get('rate_limit_seconds', 2))

            self.status_var.set(f"Completed: {dork}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute dork: {str(e)}")
            self.add_to_history(dork, "Error")

    def execute_selected_dork(self):
        """Execute the selected dork from listbox"""
        selection = self.dork_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a dork to execute")
            return

        dork = self.dork_listbox.get(selection[0])
        threading.Thread(target=self.execute_dork, args=(dork,), daemon=True).start()

    def execute_category(self):
        """Execute all dorks in selected category"""
        category = self.category_var.get()
        if not category:
            messagebox.showwarning("Warning", "Please select a category")
            return

        dorks = DorkCategory.CATEGORIES.get(category, [])
        if not dorks:
            return

        response = messagebox.askyesno(
            "Confirm Batch Execution",
            f"Execute all {len(dorks)} dorks in category '{category}'?\n\n"
            f"This will open {len(dorks)} browser tabs with rate limiting."
        )

        if response:
            threading.Thread(target=self.execute_dorks_batch,
                           args=(dorks,), daemon=True).start()

    def execute_dorks_batch(self, dorks: List[str]):
        """Execute multiple dorks with rate limiting"""
        for dork in dorks:
            self.execute_dork(dork)

    def execute_custom_dork(self):
        """Execute custom built dork"""
        dork = self.custom_dork_var.get().strip()
        if not dork:
            messagebox.showwarning("Warning", "Please enter a custom dork")
            return

        threading.Thread(target=self.execute_dork, args=(dork,), daemon=True).start()

    def add_to_history(self, dork: str, status: str):
        """Add search to history"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.search_history.append({
            'timestamp': timestamp,
            'dork': dork,
            'status': status
        })

        self.history_tree.insert('', 0, values=(timestamp, dork, status))

    def repeat_search(self):
        """Repeat selected search from history"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a search from history")
            return

        item = self.history_tree.item(selection[0])
        dork = item['values'][1]

        threading.Thread(target=self.execute_dork, args=(dork,), daemon=True).start()

    def clear_history(self):
        """Clear search history"""
        response = messagebox.askyesno("Confirm", "Clear all search history?")
        if response:
            self.search_history.clear()
            self.history_tree.delete(*self.history_tree.get_children())
            self.status_var.set("History cleared")

    def save_custom_dork(self):
        """Save current custom dork"""
        dork = self.custom_dork_var.get().strip()
        if not dork:
            messagebox.showwarning("Warning", "No dork to save")
            return

        saved_dorks = self.load_saved_dorks_list()
        if dork not in saved_dorks:
            saved_dorks.append(dork)
            self.save_saved_dorks_list(saved_dorks)
            self.saved_dorks_listbox.insert(tk.END, dork)
            messagebox.showinfo("Success", "Custom dork saved")

    def load_custom_dork(self):
        """Load selected custom dork"""
        selection = self.saved_dorks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a saved dork")
            return

        dork = self.saved_dorks_listbox.get(selection[0])
        self.custom_dork_var.set(dork)

    def delete_custom_dork(self):
        """Delete selected custom dork"""
        selection = self.saved_dorks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a saved dork to delete")
            return

        dork = self.saved_dorks_listbox.get(selection[0])
        saved_dorks = self.load_saved_dorks_list()
        if dork in saved_dorks:
            saved_dorks.remove(dork)
            self.save_saved_dorks_list(saved_dorks)
            self.saved_dorks_listbox.delete(selection[0])

    def load_saved_dorks(self):
        """Load saved custom dorks into listbox"""
        saved_dorks = self.load_saved_dorks_list()
        self.saved_dorks_listbox.delete(0, tk.END)
        for dork in saved_dorks:
            self.saved_dorks_listbox.insert(tk.END, dork)

    def load_saved_dorks_list(self) -> List[str]:
        """Load saved dorks from file"""
        if os.path.exists("saved_dorks.json"):
            try:
                with open("saved_dorks.json", 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_saved_dorks_list(self, dorks: List[str]):
        """Save dorks list to file"""
        try:
            with open("saved_dorks.json", 'w') as f:
                json.dump(dorks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save dorks: {str(e)}")

    def export_results(self):
        """Export current results"""
        if not self.results_text.get("1.0", tk.END).strip():
            messagebox.showwarning("Warning", "No results to export")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("HTML files", "*.html"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                content = self.results_text.get("1.0", tk.END)

                if file_path.endswith('.html'):
                    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DarkDork Results</title>
    <style>
        body {{ font-family: monospace; margin: 20px; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>DarkDork Search Results</h1>
    <pre>{content}</pre>
</body>
</html>
"""
                    with open(file_path, 'w') as f:
                        f.write(html_content)
                else:
                    with open(file_path, 'w') as f:
                        f.write(content)

                messagebox.showinfo("Success", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_history(self):
        """Export search history"""
        if not self.search_history:
            messagebox.showwarning("Warning", "No history to export")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as f:
                        json.dump(self.search_history, f, indent=2)
                else:
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=['timestamp', 'dork', 'status'])
                        writer.writeheader()
                        writer.writerows(self.search_history)

                messagebox.showinfo("Success", f"History exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def batch_search(self):
        """Open batch search dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Batch Search")
        dialog.geometry("600x400")

        ttk.Label(dialog, text="Enter dorks (one per line):",
                 font=('Helvetica', 10, 'bold')).pack(pady=10)

        text_area = scrolledtext.ScrolledText(dialog, height=15)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def execute_batch():
            dorks = [line.strip() for line in text_area.get("1.0", tk.END).split('\n')
                    if line.strip()]
            if dorks:
                dialog.destroy()
                threading.Thread(target=self.execute_dorks_batch,
                               args=(dorks,), daemon=True).start()

        ttk.Button(dialog, text="Execute All", command=execute_batch).pack(pady=10)

    def show_settings(self):
        """Show settings dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("500x300")

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Rate limit
        ttk.Label(frame, text="Rate Limit (seconds):").grid(row=0, column=0,
                                                             sticky=tk.W, pady=5)
        rate_var = tk.IntVar(value=self.config.get('rate_limit_seconds', 2))
        ttk.Spinbox(frame, from_=1, to=10, textvariable=rate_var, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=5)

        # Results per page
        ttk.Label(frame, text="Results Per Page:").grid(row=1, column=0,
                                                         sticky=tk.W, pady=5)
        results_var = tk.IntVar(value=self.config.get('results_per_page', 10))
        ttk.Spinbox(frame, from_=5, to=100, textvariable=results_var,
                   width=10).grid(row=1, column=1, sticky=tk.W, pady=5)

        def save_settings():
            self.config['rate_limit_seconds'] = rate_var.get()
            self.config['results_per_page'] = results_var.get()
            self.save_config()
            messagebox.showinfo("Success", "Settings saved")
            dialog.destroy()

        ttk.Button(frame, text="Save", command=save_settings).grid(
            row=2, column=0, columnspan=2, pady=20)

    def show_documentation(self):
        """Show documentation"""
        doc_text = """
DarkDork - Professional Google Dorking Tool

FEATURES:
- Pre-built dork categories for common security research tasks
- Custom dork builder with operator quick-insert
- Search history tracking and export
- Batch search capabilities
- Configurable rate limiting
- Export results to multiple formats

USAGE:
1. Select a category and dork from the Categories tab
2. Optionally specify a target domain
3. Click 'Execute Dork' to open the search in your browser
4. Build custom dorks using the Custom Dork Builder tab
5. View and export search history from the History tab

GOOGLE DORK OPERATORS:
- site: Limit to specific domain
- filetype: Search for file types
- intitle: Search in page titles
- inurl: Search in URLs
- intext: Search in page content
- cache: View cached pages

LEGAL NOTICE:
This tool is intended for authorized security testing, penetration
testing, bug bounty programs, and security research only. Users must
obtain proper authorization before conducting any security testing.
Unauthorized access to computer systems is illegal.
"""

        dialog = tk.Toplevel(self.root)
        dialog.title("Documentation")
        dialog.geometry("700x500")

        text = scrolledtext.ScrolledText(dialog, font=('Courier', 9), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert("1.0", doc_text)
        text.config(state=tk.DISABLED)

    def show_about(self):
        """Show about dialog"""
        about_text = """
DarkDork v1.0
Professional Google Dorking Tool

For Forensic and Cybersecurity Organizations

Copyright 2026
Licensed under the Apache License, Version 2.0

This tool is designed for professional security researchers,
forensic analysts, and cybersecurity organizations to conduct
authorized security assessments and OSINT investigations.

DISCLAIMER:
This tool must only be used for authorized security testing.
Unauthorized access to computer systems is illegal. Users are
responsible for ensuring they have proper authorization before
conducting any security testing activities.
"""

        messagebox.showinfo("About DarkDork", about_text)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DarkDorkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
