#!/usr/bin/env python3
"""
EduContentTools GUI Application
A modern desktop interface for managing Minecraft Education content.
"""

import sys
import os

# Check tkinter availability before importing
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    TKINTER_AVAILABLE = True
    TKINTER_ERROR = None
except ImportError as e:
    TKINTER_AVAILABLE = False
    TKINTER_ERROR = str(e)
except Exception as e:
    TKINTER_AVAILABLE = False
    TKINTER_ERROR = f"Tkinter initialization error: {str(e)}"

import threading
from game_manager import GameManager
from settings import Settings


class EduContentToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EduContentTools")
        self.root.geometry("1200x800")
        
        # Initialize backend
        self.settings = Settings()
        self.game_manager = GameManager(self.settings)
        self.current_game = None
        
        # Configure style
        self.setup_style()
        
        # Create main layout
        self.create_layout()
        
        # Refresh game list
        self.refresh_game_list()
    
    def setup_style(self):
        """Configure ttk styles for a modern look."""
        style = ttk.Style()
        
        # Try to use a modern theme
        available_themes = style.theme_names()
        if 'aqua' in available_themes:  # macOS
            style.theme_use('aqua')
        elif 'vista' in available_themes:  # Windows
            style.theme_use('vista')
        elif 'clam' in available_themes:  # Cross-platform
            style.theme_use('clam')
        
        # Custom colors
        bg_color = "#f5f5f5"
        fg_color = "#333333"
        accent_color = "#007AFF"
        
        # Configure styles
        style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), foreground=accent_color)
        style.configure("Heading.TLabel", font=("Helvetica", 14, "bold"))
        style.configure("Info.TLabel", font=("Helvetica", 10))
        style.configure("Status.TLabel", font=("Helvetica", 10), foreground="green")
        
        # Button styles
        style.configure("Action.TButton", font=("Helvetica", 11), padding=10)
        style.configure("Primary.TButton", font=("Helvetica", 11, "bold"), padding=10)
    
    def create_layout(self):
        """Create the main application layout."""
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Create sections
        self.create_header(main_container)
        self.create_sidebar(main_container)
        self.create_main_panel(main_container)
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """Create the header section."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Title
        title = ttk.Label(header_frame, text="EduContentTools", style="Title.TLabel")
        title.grid(row=0, column=0, sticky=tk.W)
        
        # AI connection indicator
        self.ai_indicator = tk.Canvas(header_frame, width=12, height=12, highlightthickness=0)
        self.ai_indicator.grid(row=0, column=1, sticky=tk.E, padx=(0, 5))
        self.update_ai_indicator()
        
        ai_label = ttk.Label(header_frame, text="AI", font=("Helvetica", 10))
        ai_label.grid(row=0, column=2, sticky=tk.E, padx=(0, 15))
        
        # Settings button
        settings_btn = ttk.Button(header_frame, text="Settings", 
                                  command=self.open_settings, style="Action.TButton")
        settings_btn.grid(row=0, column=3, sticky=tk.E, padx=5)
        
        header_frame.columnconfigure(0, weight=1)
    
    def update_ai_indicator(self):
        """Update the AI connection status indicator."""
        self.ai_indicator.delete("all")
        if self.settings.is_configured():
            # Green light for connected
            self.ai_indicator.create_oval(2, 2, 10, 10, fill="#00CC00", outline="#009900")
        else:
            # Red light for disconnected
            self.ai_indicator.create_oval(2, 2, 10, 10, fill="#CC0000", outline="#990000")
    
    def create_sidebar(self, parent):
        """Create the left sidebar with game management."""
        sidebar_frame = ttk.LabelFrame(parent, text="Games", padding="10")
        sidebar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Game list
        list_frame = ttk.Frame(sidebar_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for game list
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.game_listbox = tk.Listbox(list_frame, height=20, width=30,
                                       yscrollcommand=scrollbar.set,
                                       font=("Helvetica", 11))
        self.game_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.game_listbox.yview)
        
        self.game_listbox.bind('<<ListboxSelect>>', self.on_game_select)
        
        # Game management buttons
        btn_frame = ttk.Frame(sidebar_frame)
        btn_frame.grid(row=1, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="New Game", 
                  command=self.create_new_game, style="Primary.TButton").grid(row=0, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(btn_frame, text="Refresh", 
                  command=self.refresh_game_list, style="Action.TButton").grid(row=1, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(btn_frame, text="Delete Game", 
                  command=self.delete_game, style="Action.TButton").grid(row=2, column=0, pady=2, sticky=(tk.W, tk.E))
        
        btn_frame.columnconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        sidebar_frame.columnconfigure(0, weight=1)
        sidebar_frame.rowconfigure(0, weight=1)
    
    def create_main_panel(self, parent):
        """Create the main content panel."""
        main_frame = ttk.Frame(parent)
        main_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_overview_tab()
        self.create_content_tab()
        self.create_creation_tab()
        self.create_export_tab()
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def create_overview_tab(self):
        """Create the overview tab."""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="Overview")
        
        # Game info display
        self.info_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, 
                                                   font=("Helvetica", 11),
                                                   height=25, width=70)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Action buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.grid(row=1, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="Upload World File", 
                  command=self.upload_world_file, style="Action.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Upload Documents", 
                  command=self.upload_documents, style="Action.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Extract Language Files", 
                  command=self.extract_language_files, style="Action.TButton").grid(row=0, column=2, padx=5)
        
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
    
    def create_content_tab(self):
        """Create the content editing tab."""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="Content")
        
        # Context section
        ttk.Label(tab, text="Game Context:", style="Heading.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.context_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=("Helvetica", 11))
        self.context_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Gameplay section
        ttk.Label(tab, text="Gameplay Description:", style="Heading.TLabel").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.gameplay_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=("Helvetica", 11))
        self.gameplay_text.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Objectives section
        ttk.Label(tab, text="Learning Objectives:", style="Heading.TLabel").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.objectives_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=("Helvetica", 11))
        self.objectives_text.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Save button
        ttk.Button(tab, text="Save All Content", 
                  command=self.save_content, style="Primary.TButton").grid(row=6, column=0, pady=(10, 0))
        
        tab.columnconfigure(0, weight=1)
    
    def create_creation_tab(self):
        """Create the content creation tab."""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="Create")
        
        # Student resources
        student_frame = ttk.LabelFrame(tab, text="Student Resources", padding="10")
        student_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(student_frame, text="Student Guide", 
                  command=lambda: self.create_content("student_guide"), 
                  style="Action.TButton").grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(student_frame, text="Student Workbook", 
                  command=lambda: self.create_content("student_workbook"), 
                  style="Action.TButton").grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(student_frame, text="Student Quiz", 
                  command=lambda: self.create_content("student_quiz"), 
                  style="Action.TButton").grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Parent & Teacher resources
        adult_frame = ttk.LabelFrame(tab, text="Parent & Teacher Resources", padding="10")
        adult_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(adult_frame, text="Parent Guide", 
                  command=lambda: self.create_content("parent_guide"), 
                  style="Action.TButton").grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(adult_frame, text="Teacher Guide", 
                  command=lambda: self.create_content("teacher_guide"), 
                  style="Action.TButton").grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Leadership resources
        leadership_frame = ttk.LabelFrame(tab, text="Leadership Resources", padding="10")
        leadership_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(leadership_frame, text="School Leadership Sheet", 
                  command=lambda: self.create_content("school_leadership"), 
                  style="Action.TButton").grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Curriculum & Analysis
        curriculum_frame = ttk.LabelFrame(tab, text="Curriculum & Analysis", padding="10")
        curriculum_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(curriculum_frame, text="Curriculum Standards", 
                  command=lambda: self.create_content("curriculum_standards"), 
                  style="Action.TButton").grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(curriculum_frame, text="Text Complexity Analysis", 
                  command=lambda: self.create_content("text_complexity"), 
                  style="Action.TButton").grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Progress display
        ttk.Label(tab, text="Creation Progress:", style="Heading.TLabel").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        self.progress_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=10, font=("Courier", 10))
        self.progress_text.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(5, weight=1)
        
        for frame in [student_frame, adult_frame, leadership_frame, curriculum_frame]:
            for i in range(3):
                frame.columnconfigure(i, weight=1)
    
    def create_export_tab(self):
        """Create the export tab."""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="Export")
        
        # Export options
        export_frame = ttk.LabelFrame(tab, text="Export All Creations", padding="20")
        export_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))
        
        ttk.Label(export_frame, text="Select export format:", 
                 font=("Helvetica", 12)).grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        ttk.Button(export_frame, text="Export as Markdown", 
                  command=lambda: self.export_all("md"), 
                  style="Action.TButton").grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(export_frame, text="Export as Word Document", 
                  command=lambda: self.export_all("docx"), 
                  style="Action.TButton").grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(export_frame, text="Export as PDF", 
                  command=lambda: self.export_all("pdf"), 
                  style="Action.TButton").grid(row=1, column=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Open folder button
        ttk.Button(export_frame, text="Open Exports Folder", 
                  command=self.open_exports_folder, 
                  style="Primary.TButton").grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Export info
        info_text = """
Export Information:

• Markdown (.md): Editable text format, works everywhere
• Word Document (.docx): Professional formatting for Microsoft Word
• PDF (.pdf): Print-ready, universal format

All exports include properly formatted tables and are organized by category.
Files will be saved to: games/[game-name]/exports/
        """
        
        info_label = ttk.Label(tab, text=info_text, font=("Helvetica", 11), 
                              justify=tk.LEFT, foreground="#666")
        info_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Export log
        ttk.Label(tab, text="Export Log:", style="Heading.TLabel").grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        self.export_log = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=10, font=("Courier", 10))
        self.export_log.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)
        
        for i in range(3):
            export_frame.columnconfigure(i, weight=1)
    
    def create_status_bar(self, parent):
        """Create the status bar."""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready", style="Info.TLabel")
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.current_game_label = ttk.Label(status_frame, text="No game loaded", style="Status.TLabel")
        self.current_game_label.grid(row=0, column=1, sticky=tk.E, padx=5)
        
        status_frame.columnconfigure(0, weight=1)
    
    # Event handlers
    
    def refresh_game_list(self):
        """Refresh the list of games."""
        self.game_listbox.delete(0, tk.END)
        games = self.game_manager.list_games()
        for game in games:
            self.game_listbox.insert(tk.END, game)
        
        if games:
            self.status_label.config(text=f"Found {len(games)} game(s)")
        else:
            self.status_label.config(text="No games found - create a new game to get started")
    
    def on_game_select(self, event):
        """Handle game selection."""
        selection = self.game_listbox.curselection()
        if selection:
            self.current_game = self.game_listbox.get(selection[0])
            self.load_game_info()
            self.current_game_label.config(text=f"Current: {self.current_game}")
    
    def create_new_game(self):
        """Create a new game."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Game")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter game name:", font=("Helvetica", 12)).pack(pady=20)
        
        name_entry = ttk.Entry(dialog, font=("Helvetica", 11), width=30)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def create():
            game_name = name_entry.get().strip()
            if not game_name:
                messagebox.showwarning("Invalid Name", "Please enter a game name.")
                return
            
            if self.game_manager.create_game_folder(game_name):
                messagebox.showinfo("Success", f"Game '{game_name}' created successfully!")
                dialog.destroy()
                self.refresh_game_list()
            else:
                messagebox.showerror("Error", f"Failed to create game '{game_name}'. It may already exist.")
        
        def cancel():
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Create", command=create, style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=cancel, style="Action.TButton").pack(side=tk.LEFT, padx=5)
        
        name_entry.bind('<Return>', lambda e: create())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def delete_game(self):
        """Delete the selected game."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game to delete.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{self.current_game}'?\n\n"
                                     "This will permanently remove all files and cannot be undone.")
        
        if confirm:
            if self.game_manager.delete_game_folder(self.current_game):
                messagebox.showinfo("Success", f"Game '{self.current_game}' deleted successfully.")
                self.current_game = None
                self.current_game_label.config(text="No game loaded")
                self.refresh_game_list()
                self.clear_displays()
            else:
                messagebox.showerror("Error", f"Failed to delete game '{self.current_game}'.")
    
    def load_game_info(self):
        """Load and display game information."""
        if not self.current_game:
            return
        
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        # Update overview tab
        self.info_text.delete(1.0, tk.END)
        
        output = f"Game: {self.current_game}\n"
        output += "=" * 60 + "\n\n"
        
        if info:
            if info.get("context"):
                output += "CONTEXT:\n" + info["context"] + "\n\n"
            if info.get("gameplay"):
                output += "GAMEPLAY:\n" + info["gameplay"] + "\n\n"
            if info.get("objectives"):
                objectives = info["objectives"]
                if isinstance(objectives, list):
                    output += "OBJECTIVES:\n" + "\n".join(f"• {obj}" for obj in objectives) + "\n\n"
                else:
                    output += "OBJECTIVES:\n" + objectives + "\n\n"
            
            if metadata and metadata.get("lang_file"):
                output += f"LANGUAGE FILE: {metadata['lang_file']}\n\n"
            
            if info.get("lang_analysis"):
                lang_analysis = info["lang_analysis"]
                if isinstance(lang_analysis, dict):
                    lang_analysis = str(lang_analysis)
                output += "LANGUAGE ANALYSIS:\n" + lang_analysis + "\n\n"
            
            if metadata and metadata.get("documents"):
                output += f"DOCUMENTS ({len(metadata['documents'])}):\n"
                for doc in metadata["documents"]:
                    output += f"  • {doc}\n"
                output += "\n"
        else:
            output += "No information available for this game.\n"
            output += "Upload a world file and documents to get started.\n"
        
        self.info_text.insert(1.0, output)
        
        # Update content tab
        if info:
            self.context_text.delete(1.0, tk.END)
            if info.get("context"):
                self.context_text.insert(1.0, info["context"])
            
            self.gameplay_text.delete(1.0, tk.END)
            if info.get("gameplay"):
                self.gameplay_text.insert(1.0, info["gameplay"])
            
            self.objectives_text.delete(1.0, tk.END)
            if info.get("objectives"):
                self.objectives_text.insert(1.0, info["objectives"])
    
    def clear_displays(self):
        """Clear all display areas."""
        self.info_text.delete(1.0, tk.END)
        self.context_text.delete(1.0, tk.END)
        self.gameplay_text.delete(1.0, tk.END)
        self.objectives_text.delete(1.0, tk.END)
        self.progress_text.delete(1.0, tk.END)
        self.export_log.delete(1.0, tk.END)
    
    def upload_world_file(self):
        """Upload a world file."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game first.")
            return
        
        filename = filedialog.askopenfilename(
            title="Select World File",
            filetypes=[("Minecraft World Files", "*.mcworld *.mctemplate"), ("All Files", "*.*")]
        )
        
        if filename:
            self.status_label.config(text="Uploading world file...")
            self.root.update()
            
            success = self.game_manager.upload_world_file(self.current_game, filename)
            if success:
                messagebox.showinfo("Success", "World file uploaded successfully!")
                self.load_game_info()
                self.status_label.config(text="World file uploaded")
            else:
                messagebox.showerror("Error", "Failed to upload world file.")
                self.status_label.config(text="Upload failed")
    
    def upload_documents(self):
        """Upload documents."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game first.")
            return
        
        filenames = filedialog.askopenfilenames(
            title="Select Documents",
            filetypes=[
                ("Supported Documents", "*.pdf *.docx *.pptx"),
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx"),
                ("PowerPoint Files", "*.pptx"),
                ("All Files", "*.*")
            ]
        )
        
        if filenames:
            self.status_label.config(text=f"Uploading {len(filenames)} document(s)...")
            self.root.update()
            
            success_count = 0
            for filename in filenames:
                if self.game_manager.upload_document(self.current_game, filename):
                    success_count += 1
            
            if success_count == len(filenames):
                messagebox.showinfo("Success", f"All {success_count} document(s) uploaded successfully!")
            else:
                messagebox.showwarning("Partial Success", 
                                      f"Uploaded {success_count} of {len(filenames)} document(s).")
            
            self.load_game_info()
            self.status_label.config(text=f"Uploaded {success_count} document(s)")
    
    def extract_language_files(self):
        """Extract and analyze language files."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game first.")
            return
        
        self.status_label.config(text="Extracting language files...")
        self.root.update()
        
        def extract():
            try:
                result = self.game_manager.extract_lang_files(self.current_game)
                
                self.root.after(0, lambda: self.status_label.config(text="Extraction complete"))
                
                if result:
                    self.root.after(0, lambda: messagebox.showinfo("Success", 
                                                                   "Language files extracted and analyzed successfully!"))
                    self.root.after(0, self.load_game_info)
                else:
                    self.root.after(0, lambda: messagebox.showwarning("No Files", 
                                                                      "No language files found in world file."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Extraction failed: {str(e)}"))
                self.root.after(0, lambda: self.status_label.config(text="Extraction failed"))
        
        threading.Thread(target=extract, daemon=True).start()
    
    def save_content(self):
        """Save content from the content tab."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game first.")
            return
        
        context = self.context_text.get(1.0, tk.END).strip()
        gameplay = self.gameplay_text.get(1.0, tk.END).strip()
        objectives = self.objectives_text.get(1.0, tk.END).strip()
        
        info = self.game_manager.load_game_info(self.current_game) or {}
        
        if context:
            info["context"] = context
        if gameplay:
            info["gameplay"] = gameplay
        if objectives:
            info["objectives"] = objectives
        
        self.game_manager.save_game_info(self.current_game, info)
        
        messagebox.showinfo("Success", "Content saved successfully!")
        self.status_label.config(text="Content saved")
        self.load_game_info()
    
    def create_content(self, content_type):
        """Create content using AI."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game first.")
            return
        
        # Switch to creation tab
        self.notebook.select(2)
        
        # Clear progress
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.insert(tk.END, f"Creating {content_type.replace('_', ' ').title()}...\n\n")
        self.root.update()
        
        def create():
            try:
                # Map content type to method
                method_map = {
                    "student_guide": self.game_manager.create_student_guide,
                    "student_workbook": self.game_manager.create_student_workbook,
                    "student_quiz": self.game_manager.create_student_quiz,
                    "parent_guide": self.game_manager.create_parent_guide,
                    "teacher_guide": self.game_manager.create_teacher_guide,
                    "school_leadership": self.game_manager.create_leadership_sheet,
                    "curriculum_standards": self.game_manager.create_curriculum_mapping,
                    "text_complexity": self.game_manager.create_text_complexity_analysis,
                }
                
                method = method_map.get(content_type)
                if not method:
                    self.root.after(0, lambda: self.progress_text.insert(tk.END, "Error: Unknown content type\n"))
                    return
                
                # For curriculum standards, need country and standards parameters
                if content_type == "curriculum_standards":
                    self.root.after(0, lambda: self.progress_text.insert(tk.END, "Using default: USA Common Core...\n"))
                    result = method(self.current_game, "USA", "Common Core")
                else:
                    result = method(self.current_game)
                
                if result:
                    self.root.after(0, lambda: self.progress_text.insert(tk.END, "\n[OK] Creation complete!\n"))
                    self.root.after(0, lambda: messagebox.showinfo("Success", 
                                                                   f"{content_type.replace('_', ' ').title()} created successfully!"))
                else:
                    self.root.after(0, lambda: self.progress_text.insert(tk.END, "\n[ERROR] Creation failed\n"))
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to create content."))
                
                self.root.after(0, lambda: self.status_label.config(text="Creation complete"))
            except Exception as e:
                self.root.after(0, lambda: self.progress_text.insert(tk.END, f"\n[ERROR] Error: {str(e)}\n"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Creation failed: {str(e)}"))
                self.root.after(0, lambda: self.status_label.config(text="Creation failed"))
        
        threading.Thread(target=create, daemon=True).start()
    
    def open_exports_folder(self):
        """Open the exports folder for the current game."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game first.")
            return
        
        exports_path = os.path.join(self.game_manager.games_dir, self.current_game, "exports")
        
        if not os.path.exists(exports_path):
            messagebox.showinfo("No Exports", "No exports folder found. Create some content and export it first.")
            return
        
        # Open folder in file explorer
        import subprocess
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", exports_path])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["explorer", exports_path])
            else:  # Linux
                subprocess.run(["xdg-open", exports_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def export_all(self, format_type):
        """Export all creations."""
        if not self.current_game:
            messagebox.showwarning("No Game Selected", "Please select a game first.")
            return
        
        # Switch to export tab
        self.notebook.select(3)
        
        # Clear log
        self.export_log.delete(1.0, tk.END)
        self.export_log.insert(tk.END, f"Exporting all creations as {format_type.upper()}...\n\n")
        self.root.update()
        
        def export():
            try:
                result = self.game_manager.export_all_creations(self.current_game, format_type)
                
                if result:
                    self.root.after(0, lambda: self.export_log.insert(tk.END, "\n[OK] Export complete!\n"))
                    self.root.after(0, lambda: self.export_log.insert(tk.END, f"Files saved to: games/{self.current_game}/exports/\n"))
                    self.root.after(0, lambda: messagebox.showinfo("Success", 
                                                                   f"All creations exported successfully as {format_type.upper()}!"))
                else:
                    self.root.after(0, lambda: self.export_log.insert(tk.END, "\n[ERROR] Export failed\n"))
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to export creations."))
                
                self.root.after(0, lambda: self.status_label.config(text="Export complete"))
            except Exception as e:
                self.root.after(0, lambda: self.export_log.insert(tk.END, f"\n[ERROR] Error: {str(e)}\n"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Export failed: {str(e)}"))
                self.root.after(0, lambda: self.status_label.config(text="Export failed"))
        
        threading.Thread(target=export, daemon=True).start()
    
    def open_settings(self):
        """Open settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings - Azure OpenAI Configuration")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create settings form
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Azure OpenAI Configuration", 
                 style="Heading.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # API Endpoint
        ttk.Label(frame, text="API Endpoint:").grid(row=1, column=0, sticky=tk.W, pady=5)
        endpoint_entry = ttk.Entry(frame, width=50)
        endpoint_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        endpoint_entry.insert(0, self.settings.get_api_endpoint())
        
        # API Key
        ttk.Label(frame, text="API Key:").grid(row=2, column=0, sticky=tk.W, pady=5)
        key_entry = ttk.Entry(frame, width=50, show="*")
        key_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        key_entry.insert(0, self.settings.get_api_key())
        
        # Deployment Name
        ttk.Label(frame, text="Deployment Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        deployment_entry = ttk.Entry(frame, width=50)
        deployment_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        deployment_entry.insert(0, self.settings.get_deployment_name())
        
        # API Version
        ttk.Label(frame, text="API Version:").grid(row=4, column=0, sticky=tk.W, pady=5)
        version_entry = ttk.Entry(frame, width=50)
        version_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        version_entry.insert(0, self.settings.get_api_version())
        
        def save_settings():
            self.settings.set_api_endpoint(endpoint_entry.get().strip())
            self.settings.set_api_key(key_entry.get().strip())
            self.settings.set_deployment_name(deployment_entry.get().strip())
            self.settings.set_api_version(version_entry.get().strip())
            self.settings.save()
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.update_ai_indicator()
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Save", command=save_settings, 
                  style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=cancel, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5)
        
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)


def main():
    """Main entry point for GUI application."""
    if not TKINTER_AVAILABLE:
        print("=" * 70)
        print("ERROR: GUI cannot start")
        print("=" * 70)
        print(f"\nTkinter is not available: {TKINTER_ERROR}")
        print("\nThis usually means:")
        print("  • Python tkinter module is not installed")
        print("  • System Tk/Tcl framework has compatibility issues")
        print("  • macOS version incompatibility with system Tk")
        print("\nSolutions:")
        print("  1. Use the CLI version instead:")
        print("     python main.py")
        print("\n  2. Install Python from python.org (includes working tkinter):")
        print("     https://www.python.org/downloads/")
        print("\n  3. Use homebrew Python:")
        print("     brew install python-tk")
        print("     brew install python@3.11")
        print("\n  4. Create a standalone executable on a compatible system")
        print("=" * 70)
        sys.exit(1)
    
    try:
        root = tk.Tk()
        app = EduContentToolsGUI(root)
        root.mainloop()
    except Exception as e:
        print("=" * 70)
        print("ERROR: GUI failed to start")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        print("\nThe GUI cannot run on this system.")
        print("\nPlease use the CLI version instead:")
        print("  python main.py")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
