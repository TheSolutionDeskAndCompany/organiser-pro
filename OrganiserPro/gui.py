#!/usr/bin/env python3
"""
OrganiserPro GUI - Linux Edition
A modern Tkinter-based GUI for file organization on Linux desktops.
"""

import os
import sys
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import sys
import platform
from pathlib import Path

# Import our core modules
from .sorter import sort_by_type, sort_by_date
from .dedupe import find_duplicates, handle_duplicates

# OrganiserPro Modern Theme Colors
COLORS = {
    'background': '#0f0f1a',    # Dark Navy Background
    'pink': '#f35ca6',         # Softer Pink Accent (was #ff43b9)
    'turquoise': '#21d0ff',    # Bright Turquoise Accent
    'purple': '#a86af7',       # Softer Purple (was #8432f5)
    'text': '#ffffff',         # Pure White text
    'text_secondary': '#c8c8ff', # Brighter secondary text
    'hover_pink': '#ff7eb9',   # Lighter pink for hover
    'hover_turquoise': '#4dd8ff', # Lighter turquoise for hover
    'hover_purple': '#c18fff', # Lighter purple for hover
    'dark_purple': '#7b4ae2',  # Darker purple for pressed
    'card_bg': '#1a1a2e',      # Card background
    'card_highlight': '#24243e', # Card highlight
    'border': '#2a2a4a',       # Border color
    'shadow': '#00000040',     # Shadow with transparency
    'glow': '#f35ca640',       # Glow effect (with alpha)
    'success': '#4caf50',      # Success green
    'warning': '#ff9800',      # Warning orange
    'error': '#f44336'         # Error red
}

# Modern soft font configuration with safe fallbacks
FONTS = {
    'default': ('Arial', 10),
    'header': ('Arial', 18, 'normal'),
    'subheader': ('Arial', 12, 'normal'),
    'button': ('Arial', 10, 'normal'),
    'small': ('Arial', 9)
}


class OrganiserProGUI:
    """Main GUI application for OrganiserPro Linux Edition."""

    def __init__(self):
        # Check if running on Linux
        if platform.system() != "Linux":
            messagebox.showerror(
                "OrganiserPro Linux Edition - Unsupported Platform",
                f"This version of OrganiserPro is designed specifically for Linux desktop environments.\n\n"
                f"Your system: {platform.system()} {platform.release()}\n\n"
                f"What you can do:\n"
                f"• Windows and Mac versions are coming in future releases\n"
                f"• Check our GitHub repository for updates\n"
                f"• Consider using a Linux virtual machine or dual-boot setup\n\n"
                f"We appreciate your interest in OrganiserPro!"
            )
            sys.exit(1)

        self.root = tk.Tk()
        self.root.title("OrganiserPro - Linux Edition")

        # Set window size and position - perfect fit for all content
        window_width = 520
        window_height = 630
        min_width = 500
        min_height = 600

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Apply window settings
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(min_width, min_height)
        self.root.option_add('*Font', 'Arial 10')

        # Set window icon (if available)
        try:
            # Try to set window icon - will work if icon file exists
            icon_path = Path(__file__).parent.parent / "assets" / "icon.png"
            if icon_path.exists():
                self.root.iconphoto(True, tk.PhotoImage(file=str(icon_path)))
        except Exception:
            pass  # Continue without icon if not available

        # Configure modern styling
        self.setup_styles()

        # Set background color
        self.root.configure(bg=COLORS['background'])

        # Variables
        self.selected_folder = tk.StringVar()
        self.operation_mode = tk.StringVar(value="sort_type")
        self.preview_mode = tk.BooleanVar(value=True)
        self.recursive_scan = tk.BooleanVar(value=True)

        # Progress tracking
        self.progress_queue = queue.Queue()
        self.is_running = False

        self.setup_ui()
        self.setup_drag_drop()

    def setup_styles(self):
        """Configure modern professional TTK styles with enhanced theming."""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure modern button styles with glow effects
        self.style.configure('Neon.TButton',
                           background=COLORS['pink'],
                           foreground=COLORS['text'],
                           font=FONTS['button'],
                           padding=(25, 12),
                           relief='flat',
                           borderwidth=2,
                           focuscolor=COLORS['glow'])

        self.style.map('Neon.TButton',
                      background=[('active', COLORS['hover_pink']),
                                ('pressed', COLORS['dark_purple']),
                                ('focus', COLORS['pink'])],
                      foreground=[('active', COLORS['text']),
                                ('pressed', COLORS['text']),
                                ('focus', COLORS['text'])],
                      bordercolor=[('active', COLORS['hover_pink']),
                                 ('pressed', COLORS['dark_purple']),
                                 ('focus', COLORS['glow'])])

        # Configure secondary button style
        self.style.configure('Secondary.TButton',
                           background=COLORS['card_bg'],
                           foreground=COLORS['text_secondary'],
                           font=FONTS['button'],
                           padding=(20, 10),
                           relief='flat',
                           borderwidth=1)

        self.style.map('Secondary.TButton',
                      background=[('active', COLORS['card_highlight']),
                                ('pressed', COLORS['border'])],
                      foreground=[('active', COLORS['text']),
                                ('pressed', COLORS['text'])],
                      bordercolor=[('active', COLORS['border']),
                                 ('pressed', COLORS['text_secondary'])])

        # Configure warning button style (for undo)
        self.style.configure('Warning.TButton',
                           background=COLORS['warning'],
                           foreground=COLORS['text'],
                           font=FONTS['button'],
                           padding=(20, 10),
                           relief='flat',
                           borderwidth=1)

        self.style.map('Warning.TButton',
                      background=[('active', '#ffb74d'),
                                ('pressed', '#f57c00')],
                      foreground=[('active', COLORS['text']),
                                ('pressed', COLORS['text'])])

        self.style.configure('Turquoise.TButton',
                           background=COLORS['turquoise'],
                           foreground=COLORS['background'],
                           font=FONTS['button'],
                           padding=(20, 10),
                           relief='flat',
                           borderwidth=0)

        self.style.map('Turquoise.TButton',
                      background=[('active', COLORS['hover_turquoise']),
                                ('pressed', COLORS['purple'])],
                      foreground=[('active', COLORS['background']),
                                ('pressed', COLORS['text'])])

        # Configure dark frame styles
        self.style.configure('Dark.TFrame',
                           background=COLORS['background'],
                           relief='flat',
                           borderwidth=0)

        self.style.configure('Purple.TFrame',
                           background=COLORS['purple'],
                           relief='flat',
                           borderwidth=2)

        # Configure neon label styles
        self.style.configure('NeonHeader.TLabel',
                           background=COLORS['background'],
                           foreground=COLORS['pink'],
                           font=FONTS['header'])

        self.style.configure('NeonSubheader.TLabel',
                           background=COLORS['background'],
                           foreground=COLORS['turquoise'],
                           font=FONTS['subheader'])

        self.style.configure('NeonText.TLabel',
                           background=COLORS['background'],
                           foreground=COLORS['text'],
                           font=FONTS['default'])

        self.style.configure('Purple.TLabel',
                           background=COLORS['purple'],
                           foreground=COLORS['text'],
                           font=FONTS['subheader'])

        # Configure neon entry styles
        self.style.configure('Neon.TEntry',
                           fieldbackground=COLORS['background'],
                           foreground=COLORS['text'],
                           borderwidth=2,
                           relief='solid',
                           insertcolor=COLORS['pink'])

        # Configure neon radiobutton styles
        self.style.configure('Neon.TRadiobutton',
                           background=COLORS['background'],
                           foreground=COLORS['text'],
                           font=FONTS['default'],
                           focuscolor=COLORS['turquoise'],
                           indicatorcolor=COLORS['turquoise'])

        # Configure neon checkbutton styles
        self.style.configure('Neon.TCheckbutton',
                           background=COLORS['background'],
                           foreground=COLORS['text'],
                           font=FONTS['default'],
                           focuscolor=COLORS['turquoise'],
                           indicatorcolor=COLORS['turquoise'])

    def setup_ui(self):
        """Set up the main user interface with compact scrollable layout."""
        # Create main canvas and scrollbar for scrolling functionality
        canvas = tk.Canvas(self.root, bg=COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Main container with reduced padding for compactness
        main_frame = ttk.Frame(self.scrollable_frame, padding="20", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsive design
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Header section with compact styling
        header_frame = tk.Frame(main_frame, bg=COLORS['background'], pady=10)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(0, weight=1)

        # Clean title without emoji
        title_label = tk.Label(
            header_frame,
            text="OrganiserPro",
            bg=COLORS['background'],
            fg=COLORS['pink'],
            font=FONTS['header']
        )
        title_label.grid(row=0, column=0, pady=(0, 5))

        # Clean subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Linux Edition • File Organization Made Simple",
            bg=COLORS['background'],
            fg=COLORS['turquoise'],
            font=FONTS['subheader']
        )
        subtitle_label.grid(row=1, column=0)

        # Content area with compact card-like panels
        content_frame = tk.Frame(main_frame, bg=COLORS['background'])
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        content_frame.columnconfigure(0, weight=1)

        # CARD 1: Folder Selection with compact styling
        folder_card = tk.Frame(content_frame, bg=COLORS['card_bg'], relief='solid', bd=1, padx=15, pady=12)
        folder_card.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10), padx=5)
        folder_card.columnconfigure(1, weight=1)

        # Card header with neon accent
        folder_header = tk.Label(
            folder_card,
            text="📁 SELECT FOLDER",
            bg=COLORS['card_bg'],
            fg=COLORS['pink'],
            font=FONTS['subheader']
        )
        folder_header.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))

        # Folder path input with custom styling
        path_label = tk.Label(
            folder_card,
            text="Folder Path:",
            bg=COLORS['card_bg'],
            fg=COLORS['text'],
            font=FONTS['default']
        )
        path_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 15))

        self.folder_entry = tk.Entry(
            folder_card,
            textvariable=self.selected_folder,
            width=50,
            bg=COLORS['background'],
            fg=COLORS['text'],
            font=FONTS['default'],
            relief='solid',
            bd=2,
            insertbackground=COLORS['pink']
        )
        self.folder_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 15), ipady=5)

        # Browse button with neon styling
        browse_btn = tk.Button(
            folder_card,
            text="Browse",
            command=self.browse_folder,
            bg=COLORS['turquoise'],
            fg=COLORS['background'],
            font=FONTS['button'],
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        browse_btn.grid(row=1, column=2)

        # Helpful hint with turquoise accent
        hint_label = tk.Label(
            folder_card,
            text="💡 Tip: Drag and drop a folder or type the path directly",
            bg=COLORS['card_bg'],
            fg=COLORS['turquoise'],
            font=FONTS['default']
        )
        hint_label.grid(row=2, column=0, columnspan=3, pady=(15, 0), sticky=tk.W)

        # CARD 2: Operation Selection with compact styling
        operation_card = tk.Frame(content_frame, bg=COLORS['card_bg'], relief='solid', bd=1, padx=15, pady=12)
        operation_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10), padx=5)

        # Card header with neon accent
        operation_header = tk.Label(
            operation_card,
            text="⚡ CHOOSE OPERATION",
            bg=COLORS['card_bg'],
            fg=COLORS['turquoise'],
            font=FONTS['subheader']
        )
        operation_header.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))

        # Custom radio buttons with neon styling
        self.create_neon_radiobutton(
            operation_card,
            "🗂️ Sort by File Type",
            "sort_type",
            1, 0
        )

        self.create_neon_radiobutton(
            operation_card,
            "📅 Sort by Date",
            "sort_date",
            2, 0
        )

        self.create_neon_radiobutton(
            operation_card,
            "🔍 Find Duplicates",
            "dedupe",
            3, 0
        )

        # CARD 3: Options with stunning styling
        options_card = tk.Frame(content_frame, bg=COLORS['card_bg'], relief='solid', bd=2, padx=25, pady=20)
        options_card.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 30), padx=10)

        # Card header with neon accent
        options_header = tk.Label(
            options_card,
            text="⚙️ OPTIONS",
            bg=COLORS['card_bg'],
            fg=COLORS['purple'],
            font=FONTS['subheader']
        )
        options_header.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))

        # Custom checkboxes with neon styling
        self.create_neon_checkbox(
            options_card,
            "🔍 Preview Mode (see changes before applying)",
            self.preview_mode,
            1, 0
        )

        self.create_neon_checkbox(
            options_card,
            "📁 Recursive scan (include subdirectories)",
            self.recursive_scan,
            2, 0
        )

        # ACTION BUTTON - Compact styling
        action_frame = tk.Frame(main_frame, bg=COLORS['background'])
        action_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        action_frame.columnconfigure(0, weight=1)

        # Create the clean action button
        self.action_button = tk.Button(
            action_frame,
            text="Start Organizing",
            command=self.execute_operation,
            bg=COLORS['turquoise'],
            fg=COLORS['background'],
            font=FONTS['button'],
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            borderwidth=0,
            activebackground=COLORS['hover_turquoise'],
            activeforeground=COLORS['background']
        )
        self.action_button.grid(row=0, column=0, pady=20)

        # Add hover effects to the action button
        self.action_button.bind('<Enter>', self.on_action_button_enter)
        self.action_button.bind('<Leave>', self.on_action_button_leave)

        # Progress bar with neon styling
        progress_frame = tk.Frame(main_frame, bg=COLORS['background'])
        progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 20))
        progress_frame.columnconfigure(0, weight=1)

        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            style='Modern.Horizontal.TProgressbar'
        )
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=20)

        # Results section with neon styling
        results_frame = tk.Frame(main_frame, bg=COLORS['card_bg'], relief='solid', bd=2, padx=25, pady=20)
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)

        results_header = tk.Label(
            results_frame,
            text="📊 RESULTS",
            bg=COLORS['card_bg'],
            fg=COLORS['turquoise'],
            font=FONTS['subheader']
        )
        results_header.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        main_frame.rowconfigure(4, weight=1)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=10,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=COLORS['background'],
            fg=COLORS['text'],
            font=FONTS['default'],
            relief='solid',
            borderwidth=1
        )
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Status bar with modern styling
        status_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="10")
        status_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.status_var = tk.StringVar(value="Ready to organize your files")
        status_bar = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            style='Card.TLabel'
        )
        status_bar.grid(row=0, column=0, sticky=tk.W)

    def create_neon_radiobutton(self, parent, text, value, row, col):
        """Create a custom neon-styled radio button."""
        radio_frame = tk.Frame(parent, bg=COLORS['card_bg'])
        radio_frame.grid(row=row, column=col, sticky=tk.W, pady=8, padx=(20, 0))

        # Custom radio button using tkinter
        radio_var = tk.Radiobutton(
            radio_frame,
            text=text,
            variable=self.operation_mode,
            value=value,
            bg=COLORS['card_bg'],
            fg=COLORS['text'],
            font=FONTS['default'],
            selectcolor=COLORS['pink'],
            activebackground=COLORS['card_bg'],
            activeforeground=COLORS['turquoise'],
            cursor='hand2'
        )
        radio_var.pack(anchor=tk.W)

    def create_neon_checkbox(self, parent, text, variable, row, col):
        """Create a custom neon-styled checkbox."""
        check_frame = tk.Frame(parent, bg=COLORS['card_bg'])
        check_frame.grid(row=row, column=col, sticky=tk.W, pady=8, padx=(20, 0))

        # Custom checkbox using tkinter
        check_var = tk.Checkbutton(
            check_frame,
            text=text,
            variable=variable,
            bg=COLORS['card_bg'],
            fg=COLORS['text'],
            font=FONTS['default'],
            selectcolor=COLORS['turquoise'],
            activebackground=COLORS['card_bg'],
            activeforeground=COLORS['pink'],
            cursor='hand2'
        )
        check_var.pack(anchor=tk.W)

    def on_action_button_enter(self, event):
        """Handle action button hover enter."""
        self.action_button.config(bg=COLORS['hover_turquoise'], relief='raised')

    def on_action_button_leave(self, event):
        """Handle action button hover leave."""
        self.action_button.config(bg=COLORS['turquoise'], relief='flat')

    def setup_drag_drop(self):
        """Set up drag and drop functionality for folder selection."""
        # Note: Basic drag-drop support - can be enhanced with tkinterdnd2 if available
        def on_drop(event):
            # This is a simplified version - full drag-drop would require tkinterdnd2
            pass

        self.folder_entry.bind('<Button-1>', lambda e: self.folder_entry.focus())

    def browse_folder(self):
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(
            title="Select folder to organize",
            initialdir=os.path.expanduser("~")
        )
        if folder:
            self.selected_folder.set(folder)

    def log_message(self, message: str, level: str = "info"):
        """Add a message to the results area."""
        self.results_text.config(state=tk.NORMAL)

        # Add timestamp and format message
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        if level == "error":
            formatted_msg = f"[{timestamp}] ❌ {message}\n"
        elif level == "success":
            formatted_msg = f"[{timestamp}] ✅ {message}\n"
        elif level == "warning":
            formatted_msg = f"[{timestamp}] ⚠️ {message}\n"
        else:
            formatted_msg = f"[{timestamp}] ℹ️ {message}\n"

        # Insert the message
        self.results_text.insert(tk.END, formatted_msg)
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def preview_operation(self):
        """Preview the selected operation without making changes."""
        if not self.validate_inputs():
            return

        self.log_message("Starting preview operation...")
        self.status_var.set("Previewing...")

        # Run preview in separate thread to avoid blocking UI
        thread = threading.Thread(target=self._run_preview, daemon=True)
        thread.start()

    def execute_operation(self):
        """Execute the selected operation with safety features."""
        if not self.validate_inputs():
            return

        # Enhanced safety confirmation
        folder = self.selected_folder.get()
        operation = self.operation_mode.get()
        
        # Check if this operation was recently run (idempotence check)
        if self._check_recent_operation(folder, operation):
            result = messagebox.askyesno(
                "Operation Already Performed",
                f"It appears this {operation.replace('_', ' ')} operation was recently performed on this folder.\n\n"
                f"Running it again might not produce meaningful changes.\n\n"
                f"Do you want to continue anyway?",
                icon='warning'
            )
            if not result:
                return

        if not self.preview_mode.get():
            # Enhanced confirmation without preview
            result = messagebox.askyesno(
                "Confirm Operation",
                f"You are about to {operation.replace('_', ' ')} files without previewing changes first.\n\n"
                f"This will modify your files. A backup will be created for safety.\n\n"
                f"Are you sure you want to continue?",
                icon='warning'
            )
            if not result:
                return
        else:
            # Confirmation even with preview
            result = messagebox.askyesno(
                "Execute Operation",
                f"Ready to {operation.replace('_', ' ')} files in:\n{folder}\n\n"
                f"A backup will be created before making changes.\n\n"
                f"Continue with the operation?"
            )
            if not result:
                return

        self.log_message("Creating backup before operation...")
        self.status_var.set("Creating backup...")
        self.progress.start()

        # Disable buttons during operation
        self.preview_button.config(state=tk.DISABLED)
        self.execute_button.config(state=tk.DISABLED)
        
        # Add undo button if it doesn't exist
        if not hasattr(self, 'undo_button'):
            self._add_undo_button()

        # Run operation in separate thread
        thread = threading.Thread(target=self._run_operation_with_backup, daemon=True)
        thread.start()

    def _run_preview(self):
        """Run preview operation in background thread."""
        try:
            folder = Path(self.selected_folder.get())
            operation = self.operation_mode.get()

            if operation == "sort_type":
                self._preview_sort_by_type(folder)
            elif operation == "sort_date":
                self._preview_sort_by_date(folder)
            elif operation == "dedupe":
                self._preview_dedupe(folder)

        except Exception as e:
            self.log_message(f"Preview failed: {str(e)}", "error")
        finally:
            self.status_var.set("Ready")

    def _run_operation_with_backup(self):
        """Run actual operation with backup creation in background thread."""
        backup_path = None
        try:
            folder = Path(self.selected_folder.get())
            operation = self.operation_mode.get()

            # Create backup
            backup_path = self._create_backup(folder)
            if backup_path:
                self.log_message(f"Backup created: {backup_path}", "success")
                self.last_backup_path = backup_path
                self.last_operation_folder = str(folder)
                self.last_operation_type = operation
            
            self.log_message("Starting operation...")
            self.status_var.set("Processing...")

            if operation == "sort_type":
                self._execute_sort_by_type(folder)
            elif operation == "sort_date":
                self._execute_sort_by_date(folder)
            elif operation == "dedupe":
                self._execute_dedupe(folder)

            # Record successful operation
            self._record_operation(folder, operation)
            
            self.log_message("Operation completed successfully!", "success")
            
            # Enable undo button
            if hasattr(self, 'undo_button'):
                self.undo_button.config(state=tk.NORMAL)

        except Exception as e:
            self.log_message(f"Operation failed: {str(e)}", "error")
            # If operation failed and we have a backup, offer to restore
            if backup_path and backup_path.exists():
                result = messagebox.askyesno(
                    "Operation Failed",
                    f"The operation failed: {str(e)}\n\n"
                    f"Would you like to restore from the backup?"
                )
                if result:
                    self._restore_from_backup(backup_path, folder)
        finally:
            self.progress.stop()
            self.preview_button.config(state=tk.NORMAL)
            self.execute_button.config(state=tk.NORMAL)
            self.status_var.set("Ready")

    def _run_operation(self):
        """Run actual operation in background thread (legacy method)."""
        try:
            folder = Path(self.selected_folder.get())
            operation = self.operation_mode.get()

            if operation == "sort_type":
                self._execute_sort_by_type(folder)
            elif operation == "sort_date":
                self._execute_sort_by_date(folder)
            elif operation == "dedupe":
                self._execute_dedupe(folder)

            self.log_message("Operation completed successfully!", "success")

        except Exception as e:
            self.log_message(f"Operation failed: {str(e)}", "error")
        finally:
            self.progress.stop()
            self.preview_button.config(state=tk.NORMAL)
            self.execute_button.config(state=tk.NORMAL)
            self.status_var.set("Ready")

    def _preview_sort_by_type(self, folder: Path):
        """Preview sort by type operation."""
        # Get file counts by type
        files_by_type = {}
        for file_path in folder.rglob("*") if self.recursive_scan.get() else folder.iterdir():
            if file_path.is_file() and not file_path.name.startswith("."):
                ext = file_path.suffix.lower() or "no_extension"
                files_by_type[ext] = files_by_type.get(ext, 0) + 1

        self.log_message(f"Preview: Sort by Type in {folder}")
        self.log_message(f"Found {sum(files_by_type.values())} files")

        for ext, count in sorted(files_by_type.items()):
            folder_name = ext[1:] if ext.startswith('.') else ext
            self.log_message(f"  → {folder_name}/ ({count} files)")

    def _check_recent_operation(self, folder: str, operation: str) -> bool:
        """Check if this operation was recently performed on this folder."""
        try:
            # Check for operation history file
            history_file = Path(folder) / '.organiserpro_history.json'
            if not history_file.exists():
                return False
            
            import json
            import time
            
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            # Check if same operation was run in last 5 minutes
            current_time = time.time()
            for record in history.get('operations', []):
                if (record.get('operation') == operation and 
                    current_time - record.get('timestamp', 0) < 300):  # 5 minutes
                    return True
            
            return False
        except Exception:
            return False

    def _preview_sort_by_date(self, folder: Path):
        """Preview sort by date operation."""
        self.log_message(f"Preview: Sort by Date in {folder}")
        # Implementation would analyze files by date and show preview
        self.log_message("Date sorting preview - feature coming soon!")

    def _preview_dedupe(self, folder: Path):
        """Preview duplicate detection."""
        self.log_message(f"Preview: Find Duplicates in {folder}")

        duplicates = find_duplicates(str(folder), recursive=self.recursive_scan.get())

        if duplicates:
            # Convert dict to list of groups for display
            duplicate_groups = [files for files in duplicates.values() if len(files) > 1]
            self.log_message(f"Found {len(duplicate_groups)} groups of duplicate files:")
            for i, group in enumerate(duplicate_groups[:5], 1):  # Show first 5 groups
                self.log_message(f"  Group {i}: {len(group)} duplicates")
                for file_path in group[:3]:  # Show first 3 files in group
                    self.log_message(f"    • {file_path}")
                if len(group) > 3:
                    self.log_message(f"    ... and {len(group) - 3} more")
            if len(duplicate_groups) > 5:
                self.log_message(f"  ... and {len(duplicate_groups) - 5} more groups")
        else:
            self.log_message("No duplicate files found!", "success")

    def _execute_sort_by_type(self, folder: Path):
        """Execute sort by type operation."""
        try:
            sort_by_type(str(folder), dry_run=False)
            self.log_message("Files sorted by type successfully!")
        except Exception as e:
            self.log_message(f"Error sorting files: {str(e)}", "error")

    def _execute_sort_by_date(self, folder: Path):
        """Execute sort by date operation."""
        try:
            sort_by_date(str(folder), dry_run=False)
            self.log_message("Files sorted by date successfully!")
        except Exception as e:
            self.log_message(f"Error sorting files by date: {str(e)}", "error")

    def _execute_dedupe(self, folder: Path):
        """Execute duplicate removal."""
        duplicates = find_duplicates(str(folder), recursive=self.recursive_scan.get())

        if duplicates:
            # Convert dict to list of groups for counting
            duplicate_groups = [files for files in duplicates.values() if len(files) > 1]
            total_duplicates = sum(len(group) - 1 for group in duplicate_groups)  # Keep one from each group
            self.log_message(f"Found {total_duplicates} duplicate files that could be removed")
            self.log_message("Automatic duplicate removal coming in future update!")
        else:
            self.log_message("No duplicates found - your files are already organized!", "success")

    def run(self):
        """Start the GUI application."""
        self.log_message("OrganiserPro Linux Edition started")
        self.log_message("Select a folder and choose an operation to begin")

        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    app = OrganiserProGUI()
    app.run()


if __name__ == "__main__":
    main()
