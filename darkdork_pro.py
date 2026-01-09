#!/usr/bin/env python3
"""
DarkDork Professional - Unified Modern Interface
Exponentially better UI with all features integrated
Built with PyQt6 for maximum polish and performance
"""

import sys
import webbrowser
import urllib.parse
import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QListWidget,
        QScrollArea, QFrame, QSplitter, QTabWidget, QTableWidget, QTableWidgetItem,
        QMessageBox, QFileDialog, QProgressBar, QSystemTrayIcon, QMenu
    )
    from PyQt6.QtCore import (
        Qt, QTimer, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
        QPoint, QSize, pyqtSignal, QThread
    )
    from PyQt6.QtGui import (
        QIcon, QFont, QPalette, QColor, QLinearGradient, QPainter,
        QBrush, QPen, QPixmap, QCursor
    )
except ImportError:
    print("PyQt6 not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *

# Import existing modules
try:
    from darkdork_library import DorkLibrary, create_comprehensive_library
    from darkdork_db import DarkDorkDatabase
    from darkdork_exports import DarkDorkExporter
except ImportError:
    DorkLibrary = None
    DarkDorkDatabase = None
    DarkDorkExporter = None


class DarkTheme:
    """Modern dark theme with DarkNexus-inspired colors"""

    # Color palette
    BG_DARK = "#0a1628"
    BG_MEDIUM = "#1a2332"
    BG_LIGHT = "#2a3442"
    BG_CARD = "#1e2936"

    ACCENT = "#00d4ff"
    ACCENT_HOVER = "#00e6ff"
    ACCENT_PRESSED = "#00b8e6"

    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#8b9db5"
    TEXT_MUTED = "#5a6b7d"

    SUCCESS = "#00ff88"
    WARNING = "#ffaa00"
    DANGER = "#ff4444"
    INFO = "#4488ff"

    BORDER = "#3a4452"
    SHADOW = "rgba(0, 0, 0, 0.5)"

    @classmethod
    def get_stylesheet(cls):
        """Get complete stylesheet for the application"""
        return f"""
        * {{
            font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
        }}

        QMainWindow {{
            background-color: {cls.BG_DARK};
        }}

        QWidget {{
            background-color: transparent;
            color: {cls.TEXT_PRIMARY};
        }}

        /* Sidebar styling */
        #sidebar {{
            background-color: {cls.BG_MEDIUM};
            border-right: 1px solid {cls.BORDER};
        }}

        /* Card styling */
        .card {{
            background-color: {cls.BG_CARD};
            border-radius: 8px;
            padding: 16px;
            border: 1px solid {cls.BORDER};
        }}

        .card:hover {{
            border-color: {cls.ACCENT};
            background-color: {cls.BG_LIGHT};
        }}

        /* Button styling */
        QPushButton {{
            background-color: {cls.BG_LIGHT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
        }}

        QPushButton:hover {{
            background-color: {cls.BG_MEDIUM};
            border-color: {cls.ACCENT};
        }}

        QPushButton:pressed {{
            background-color: {cls.BG_DARK};
        }}

        QPushButton#accent {{
            background-color: {cls.ACCENT};
            color: #000000;
            border: none;
            font-weight: 600;
        }}

        QPushButton#accent:hover {{
            background-color: {cls.ACCENT_HOVER};
        }}

        QPushButton#accent:pressed {{
            background-color: {cls.ACCENT_PRESSED};
        }}

        QPushButton#sidebar {{
            background-color: transparent;
            border: none;
            text-align: left;
            padding: 12px 20px;
            border-radius: 0px;
        }}

        QPushButton#sidebar:hover {{
            background-color: {cls.BG_LIGHT};
        }}

        QPushButton#sidebar:pressed {{
            background-color: {cls.BG_DARK};
        }}

        /* Input styling */
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {cls.BG_DARK};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border-color: {cls.ACCENT};
        }}

        /* Scrollbar styling */
        QScrollBar:vertical {{
            background: {cls.BG_DARK};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background: {cls.BG_LIGHT};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {cls.ACCENT};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}

        /* Label styling */
        QLabel {{
            color: {cls.TEXT_PRIMARY};
        }}

        QLabel#heading {{
            font-size: 24px;
            font-weight: 700;
            color: {cls.TEXT_PRIMARY};
        }}

        QLabel#subheading {{
            font-size: 16px;
            font-weight: 600;
            color: {cls.TEXT_PRIMARY};
        }}

        QLabel#muted {{
            color: {cls.TEXT_SECONDARY};
            font-size: 12px;
        }}

        /* Table styling */
        QTableWidget {{
            background-color: {cls.BG_CARD};
            border: 1px solid {cls.BORDER};
            border-radius: 8px;
            gridline-color: {cls.BORDER};
        }}

        QTableWidget::item {{
            padding: 8px;
            color: {cls.TEXT_PRIMARY};
        }}

        QTableWidget::item:selected {{
            background-color: {cls.ACCENT};
            color: #000000;
        }}

        QHeaderView::section {{
            background-color: {cls.BG_LIGHT};
            color: {cls.TEXT_PRIMARY};
            padding: 8px;
            border: none;
            font-weight: 600;
        }}

        /* Tab widget styling */
        QTabWidget::pane {{
            border: 1px solid {cls.BORDER};
            border-radius: 8px;
            background-color: {cls.BG_CARD};
        }}

        QTabBar::tab {{
            background-color: {cls.BG_MEDIUM};
            color: {cls.TEXT_SECONDARY};
            padding: 10px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 4px;
        }}

        QTabBar::tab:selected {{
            background-color: {cls.BG_CARD};
            color: {cls.TEXT_PRIMARY};
            border-bottom: 2px solid {cls.ACCENT};
        }}

        QTabBar::tab:hover {{
            background-color: {cls.BG_LIGHT};
        }}

        /* Progress bar styling */
        QProgressBar {{
            background-color: {cls.BG_DARK};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            text-align: center;
            color: {cls.TEXT_PRIMARY};
        }}

        QProgressBar::chunk {{
            background-color: {cls.ACCENT};
            border-radius: 6px;
        }}

        /* List widget styling */
        QListWidget {{
            background-color: {cls.BG_CARD};
            border: 1px solid {cls.BORDER};
            border-radius: 8px;
        }}

        QListWidget::item {{
            padding: 12px;
            border-bottom: 1px solid {cls.BORDER};
        }}

        QListWidget::item:selected {{
            background-color: {cls.ACCENT};
            color: #000000;
        }}

        QListWidget::item:hover {{
            background-color: {cls.BG_LIGHT};
        }}
        """


class ToastNotification(QFrame):
    """Toast notification widget"""

    def __init__(self, message: str, type: str = "info", parent=None):
        super().__init__(parent)
        self.message = message
        self.type = type
        self.setup_ui()
        self.animate_in()

    def setup_ui(self):
        """Setup toast UI"""
        self.setFixedHeight(60)
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)

        colors = {
            "info": DarkTheme.INFO,
            "success": DarkTheme.SUCCESS,
            "warning": DarkTheme.WARNING,
            "error": DarkTheme.DANGER
        }
        color = colors.get(self.type, DarkTheme.INFO)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {DarkTheme.BG_CARD};
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 12px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        # Icon
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        icon_label = QLabel(icons.get(self.type, "ℹ️"))
        icon_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(icon_label)

        # Message
        msg_label = QLabel(self.message)
        msg_label.setStyleSheet(f"color: {DarkTheme.TEXT_PRIMARY}; font-size: 13px;")
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label, 1)

    def animate_in(self):
        """Animate toast appearing"""
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Will be positioned by parent, just fade in via opacity
        self.setWindowOpacity(0.0)
        QTimer.singleShot(50, lambda: self.setWindowOpacity(1.0))

        # Auto-hide after 3 seconds
        QTimer.singleShot(3000, self.animate_out)

    def animate_out(self):
        """Animate toast disappearing"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()


class LoadingSpinner(QWidget):
    """Animated loading spinner"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)  # Update every 50ms

    def rotate(self):
        """Rotate the spinner"""
        self.angle = (self.angle + 10) % 360
        self.update()

    def paintEvent(self, event):
        """Paint the spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw spinning arc
        rect = self.rect().adjusted(10, 10, -10, -10)
        painter.setPen(QPen(QColor(DarkTheme.ACCENT), 3))
        painter.drawArc(rect, self.angle * 16, 120 * 16)


class DorkCard(QFrame):
    """Animated dork card widget"""

    execute_clicked = pyqtSignal(dict)
    copy_clicked = pyqtSignal(dict)

    def __init__(self, dork: Dict, parent=None):
        super().__init__(parent)
        self.dork = dork
        self.setObjectName("card")
        self.is_hovered = False
        self.setup_ui()
        self.setup_animations()
        self.animate_in()

    def setup_ui(self):
        """Setup card UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Category badge
        category = self.dork.get('category', 'Other')
        category_label = QLabel(category.upper())
        category_label.setObjectName("muted")
        category_label.setStyleSheet(f"""
            background-color: {DarkTheme.BG_DARK};
            padding: 4px 12px;
            border-radius: 4px;
            color: {DarkTheme.INFO};
            font-size: 10px;
            font-weight: 600;
        """)
        layout.addWidget(category_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Title
        name = self.dork.get('name', 'Unknown')
        title_label = QLabel(name[:60])
        title_label.setObjectName("subheading")
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(title_label)

        # Description
        desc = self.dork.get('description', 'No description')[:100]
        desc_label = QLabel(desc)
        desc_label.setObjectName("muted")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY}; font-size: 12px;")
        layout.addWidget(desc_label)

        # Query display
        query = self.dork.get('query', '')
        query_frame = QFrame()
        query_frame.setStyleSheet(f"""
            background-color: {DarkTheme.BG_DARK};
            border-radius: 4px;
            padding: 8px;
        """)
        query_layout = QVBoxLayout(query_frame)
        query_layout.setContentsMargins(8, 8, 8, 8)

        query_label = QLabel(query[:70] + ('...' if len(query) > 70 else ''))
        query_label.setStyleSheet(f"""
            color: {DarkTheme.ACCENT};
            font-family: 'Courier New', monospace;
            font-size: 11px;
        """)
        query_layout.addWidget(query_label)
        layout.addWidget(query_frame)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        copy_btn = QPushButton("📋 Copy")
        copy_btn.setStyleSheet(f"""
            padding: 6px 12px;
            font-size: 11px;
            background-color: {DarkTheme.BG_MEDIUM};
        """)
        copy_btn.clicked.connect(lambda: self.copy_clicked.emit(self.dork))
        btn_layout.addWidget(copy_btn)

        exec_btn = QPushButton("🔍 Execute")
        exec_btn.setObjectName("accent")
        exec_btn.setStyleSheet(f"""
            padding: 6px 12px;
            font-size: 11px;
            background-color: {DarkTheme.ACCENT};
            color: #000000;
            font-weight: 600;
            border: none;
            border-radius: 4px;
        """)
        exec_btn.clicked.connect(lambda: self.execute_clicked.emit(self.dork))
        btn_layout.addWidget(exec_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Style the frame
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {DarkTheme.BG_CARD};
                border: 1px solid {DarkTheme.BORDER};
                border-radius: 8px;
            }}
            QFrame#card:hover {{
                border-color: {DarkTheme.ACCENT};
                background-color: {DarkTheme.BG_LIGHT};
            }}
        """)

    def animate_in(self):
        """Animate card appearing"""
        self.setWindowOpacity(0.0)

        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(400)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_animation.start()

    def setup_animations(self):
        """Setup hover animations"""
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(200)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        """Animate on mouse enter"""
        self.is_hovered = True
        # Subtle scale effect on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Animate on mouse leave"""
        self.is_hovered = False
        super().leaveEvent(event)


class DarkDorkPro(QMainWindow):
    """Unified DarkDork Professional Application"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DarkDork Professional")
        self.setGeometry(100, 100, 1600, 1000)

        # Initialize data
        self.library = None
        self.database = None
        self.exporter = None
        self.search_history = []
        self.current_category = "All Intelligence"
        self.toasts = []  # Track active toasts

        # Load modules
        self.load_modules()

        # Setup UI
        self.setup_ui()

        # Apply theme
        self.setStyleSheet(DarkTheme.get_stylesheet())

        # Show welcome toast
        QTimer.singleShot(500, lambda: self.show_toast("Welcome to DarkDork Professional!", "success"))

    def load_modules(self):
        """Load darkdork modules"""
        try:
            if DorkLibrary:
                self.library = create_comprehensive_library()
            if DarkDorkDatabase:
                self.database = DarkDorkDatabase()
            if DarkDorkExporter:
                self.exporter = DarkDorkExporter()
        except Exception as e:
            print(f"Error loading modules: {e}")

    def setup_ui(self):
        """Setup main UI"""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar
        self.create_top_bar(main_layout)

        # Splitter for sidebar and main area
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet(f"QSplitter::handle {{ background-color: {DarkTheme.BORDER}; }}")

        # Sidebar
        self.create_sidebar(splitter)

        # Main content area with tabs
        self.create_main_area(splitter)

        # Set splitter sizes
        splitter.setSizes([250, 1350])

        main_layout.addWidget(splitter)

        # Status bar
        self.create_status_bar()

    def create_top_bar(self, parent_layout):
        """Create top bar with branding and quick actions"""
        top_bar = QFrame()
        top_bar.setStyleSheet(f"""
            background-color: {DarkTheme.BG_DARK};
            border-bottom: 1px solid {DarkTheme.BORDER};
        """)
        top_bar.setFixedHeight(70)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)

        # Logo/Title
        title = QLabel("⚡ DarkDork Professional")
        title.setObjectName("heading")
        title.setStyleSheet(f"color: {DarkTheme.TEXT_PRIMARY}; font-size: 22px; font-weight: 700;")
        layout.addWidget(title)

        layout.addStretch()

        # Quick action buttons
        new_project_btn = QPushButton("📁 New Project")
        new_project_btn.clicked.connect(self.new_project)
        layout.addWidget(new_project_btn)

        export_btn = QPushButton("📊 Export")
        export_btn.clicked.connect(self.export_results)
        layout.addWidget(export_btn)

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn)

        parent_layout.addWidget(top_bar)

    def create_sidebar(self, parent):
        """Create sidebar with navigation"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(200)
        sidebar.setMaximumWidth(300)

        layout = QVBoxLayout(sidebar)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 20, 0, 20)

        # Section label
        section_label = QLabel("  CATEGORIES")
        section_label.setStyleSheet(f"""
            color: {DarkTheme.TEXT_MUTED};
            font-size: 11px;
            font-weight: 600;
            padding: 12px 20px;
        """)
        layout.addWidget(section_label)

        # Category buttons
        categories = self.get_categories()
        for cat in categories:
            btn = QPushButton(f"  {cat['icon']}  {cat['name']}")
            btn.setObjectName("sidebar")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, c=cat['name']: self.select_category(c))
            layout.addWidget(btn)

        layout.addStretch()

        # Stats section
        stats_label = QLabel("  STATISTICS")
        stats_label.setStyleSheet(f"""
            color: {DarkTheme.TEXT_MUTED};
            font-size: 11px;
            font-weight: 600;
            padding: 12px 20px;
        """)
        layout.addWidget(stats_label)

        if self.library:
            dork_count = QLabel(f"  📊  {len(self.library.dorks)} Dorks")
            dork_count.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY}; padding: 8px 20px;")
            layout.addWidget(dork_count)

        parent.addWidget(sidebar)

    def create_main_area(self, parent):
        """Create main content area with tabs"""
        main_area = QWidget()
        layout = QVBoxLayout(main_area)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Tab 1: Dork Browser
        self.create_dork_browser_tab()

        # Tab 2: Query Builder
        self.create_query_builder_tab()

        # Tab 3: Search History
        self.create_history_tab()

        # Tab 4: Database/Projects
        self.create_projects_tab()

        layout.addWidget(self.tabs)

        parent.addWidget(main_area)

    def create_dork_browser_tab(self):
        """Create dork browser tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)

        # Search bar
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search dorks...")
        search_input.setFixedHeight(40)
        search_input.textChanged.connect(self.filter_dorks)
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)

        # Scroll area for dork cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.dork_container = QWidget()
        self.dork_layout = QVBoxLayout(self.dork_container)
        self.dork_layout.setSpacing(12)

        scroll.setWidget(self.dork_container)
        layout.addWidget(scroll)

        self.tabs.addTab(tab, "🎯 Dork Browser")

        # Load initial dorks
        self.load_dorks("All Intelligence")

    def create_query_builder_tab(self):
        """Create query builder tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)

        # Title
        title = QLabel("Build Custom Query")
        title.setObjectName("subheading")
        layout.addWidget(title)

        # Query fields
        fields = [
            ("🎯 Target Site", "site", "e.g., nasa.gov or .edu"),
            ("📁 File Type", "filetype", "e.g., pdf, xlsx, docx"),
            ("📝 In Title", "intitle", "e.g., index of, login"),
            ("🔗 In URL", "inurl", "e.g., admin, config"),
            ("📄 In Text", "intext", "e.g., password, confidential"),
            ("✓ Exact Match", "exact", "e.g., Top secret"),
        ]

        self.query_fields = {}

        for label, field, placeholder in fields:
            field_layout = QVBoxLayout()
            field_layout.setSpacing(8)

            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY}; font-size: 12px; font-weight: 600;")
            field_layout.addWidget(lbl)

            entry = QLineEdit()
            entry.setPlaceholderText(placeholder)
            entry.setFixedHeight(40)
            entry.textChanged.connect(self.build_query)
            self.query_fields[field] = entry
            field_layout.addWidget(entry)

            layout.addLayout(field_layout)

        # Generated query display
        layout.addSpacing(20)
        gen_label = QLabel("Generated Query:")
        gen_label.setStyleSheet(f"color: {DarkTheme.TEXT_SECONDARY}; font-size: 12px; font-weight: 600;")
        layout.addWidget(gen_label)

        self.generated_query = QTextEdit()
        self.generated_query.setFixedHeight(80)
        self.generated_query.setReadOnly(True)
        self.generated_query.setStyleSheet(f"""
            background-color: {DarkTheme.BG_DARK};
            color: {DarkTheme.ACCENT};
            font-family: 'Courier New', monospace;
            font-size: 13px;
            padding: 12px;
        """)
        layout.addWidget(self.generated_query)

        # Action buttons
        btn_layout = QHBoxLayout()

        copy_btn = QPushButton("📋 Copy Query")
        copy_btn.clicked.connect(self.copy_generated_query)
        btn_layout.addWidget(copy_btn)

        execute_btn = QPushButton("🔍 Execute on Google")
        execute_btn.setObjectName("accent")
        execute_btn.clicked.connect(self.execute_generated_query)
        btn_layout.addWidget(execute_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()

        self.tabs.addTab(tab, "🔧 Query Builder")

    def create_history_tab(self):
        """Create search history tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Title
        title = QLabel("Search History")
        title.setObjectName("subheading")
        layout.addWidget(title)

        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "Query", "Status", "Actions"])
        layout.addWidget(self.history_table)

        self.tabs.addTab(tab, "📜 History")

    def create_projects_tab(self):
        """Create projects/database tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Title
        title = QLabel("Projects & Database")
        title.setObjectName("subheading")
        layout.addWidget(title)

        # Projects list
        self.projects_list = QListWidget()
        layout.addWidget(self.projects_list)

        self.tabs.addTab(tab, "📁 Projects")

    def create_status_bar(self):
        """Create status bar"""
        status = self.statusBar()
        status.setStyleSheet(f"""
            background-color: {DarkTheme.BG_MEDIUM};
            color: {DarkTheme.TEXT_SECONDARY};
            border-top: 1px solid {DarkTheme.BORDER};
            padding: 5px;
        """)

        dork_count = len(self.library.dorks) if self.library else 0
        status.showMessage(f"Ready | {dork_count} dorks loaded")

    def get_categories(self):
        """Get categories for sidebar"""
        if self.library:
            cat_counts = {}
            for dork in self.library.dorks:
                cat = dork.get('category', 'Other')
                cat_counts[cat] = cat_counts.get(cat, 0) + 1

            categories = [{"name": "All Intelligence", "icon": "📚"}]

            icons = {
                "Exposed Documents": "📄",
                "Login Pages": "🔐",
                "Configuration": "⚙️",
                "Databases": "💾",
                "API & Secrets": "🔑",
                "Cloud Storage": "☁️",
                "Network Devices": "🌐",
                "Source Code": "💻",
            }

            for cat in sorted(cat_counts.keys()):
                icon = icons.get(cat, "📌")
                categories.append({"name": cat, "icon": icon})

            return categories

        return [{"name": "All Intelligence", "icon": "📚"}]

    def select_category(self, category):
        """Select category and load dorks"""
        self.current_category = category
        self.load_dorks(category)

    def load_dorks(self, category):
        """Load dorks for category"""
        # Clear existing
        while self.dork_layout.count():
            child = self.dork_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Get dorks
        if self.library:
            if category == "All Intelligence":
                dorks = self.library.dorks
            else:
                dorks = [d for d in self.library.dorks if d.get('category') == category]
        else:
            dorks = []

        # Create grid layout for cards
        row_widget = None
        row_layout = None
        col = 0

        for i, dork in enumerate(dorks):
            if col == 0:
                row_widget = QWidget()
                row_layout = QHBoxLayout(row_widget)
                row_layout.setSpacing(12)
                row_layout.setContentsMargins(0, 0, 0, 0)

            card = DorkCard(dork)
            card.execute_clicked.connect(self.execute_dork)
            card.copy_clicked.connect(self.copy_dork)
            row_layout.addWidget(card)

            col += 1
            if col >= 3:
                self.dork_layout.addWidget(row_widget)
                col = 0
                row_widget = None
                row_layout = None

        # Add last row if incomplete
        if row_widget:
            row_layout.addStretch()
            self.dork_layout.addWidget(row_widget)

        self.dork_layout.addStretch()

    def filter_dorks(self, text):
        """Filter dorks by search text"""
        # TODO: Implement filtering
        pass

    def build_query(self):
        """Build query from fields"""
        parts = []

        for field, entry in self.query_fields.items():
            value = entry.text().strip()
            if not value:
                continue

            if field == 'site':
                parts.append(f"site:{value}")
            elif field == 'filetype':
                parts.append(f"filetype:{value}")
            elif field == 'intitle':
                parts.append(f'intitle:"{value}"' if ' ' in value else f"intitle:{value}")
            elif field == 'inurl':
                parts.append(f"inurl:{value}")
            elif field == 'intext':
                parts.append(f'intext:"{value}"' if ' ' in value else f"intext:{value}")
            elif field == 'exact':
                parts.append(f'"{value}"')

        query = ' '.join(parts)
        self.generated_query.setText(query)

    def copy_generated_query(self):
        """Copy generated query to clipboard"""
        query = self.generated_query.toPlainText()
        if query:
            QApplication.clipboard().setText(query)
            self.show_toast("Query copied to clipboard!", "success")
            self.statusBar().showMessage("Query copied to clipboard!", 3000)
        else:
            self.show_toast("No query to copy!", "warning")

    def execute_generated_query(self):
        """Execute generated query"""
        query = self.generated_query.toPlainText()
        if query:
            self.execute_search(query)

    def execute_dork(self, dork):
        """Execute a dork"""
        query = dork.get('query', '')
        self.execute_search(query)

    def show_toast(self, message: str, type: str = "info"):
        """Show a toast notification"""
        toast = ToastNotification(message, type, self)
        toast.setParent(self)
        toast.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Position toast in bottom-right corner
        padding = 20
        toast_spacing = 70
        y_offset = padding + (len(self.toasts) * toast_spacing)

        toast.move(
            self.width() - toast.width() - padding,
            self.height() - toast.height() - y_offset
        )
        toast.show()

        self.toasts.append(toast)
        toast.destroyed.connect(lambda: self.toasts.remove(toast) if toast in self.toasts else None)

    def copy_dork(self, dork):
        """Copy dork to clipboard"""
        query = dork.get('query', '')
        QApplication.clipboard().setText(query)
        self.show_toast(f"Copied: {query[:50]}...", "success")
        self.statusBar().showMessage("Dork copied to clipboard!", 3000)

    def execute_search(self, query):
        """Execute Google search"""
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)

        # Record in history
        self.search_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'query': query,
            'status': 'executed'
        })

        self.show_toast(f"Executed: {query[:40]}...", "info")
        self.statusBar().showMessage(f"Executed: {query[:50]}...", 5000)

    def new_project(self):
        """Create new project"""
        # TODO: Implement project creation dialog
        QMessageBox.information(self, "New Project", "Project creation coming soon!")

    def export_results(self):
        """Export results"""
        # TODO: Implement export dialog
        QMessageBox.information(self, "Export", "Export functionality coming soon!")

    def show_settings(self):
        """Show settings dialog"""
        # TODO: Implement settings dialog
        QMessageBox.information(self, "Settings", "Settings coming soon!")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("DarkDork Professional")

    window = DarkDorkPro()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
