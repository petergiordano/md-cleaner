# Import necessary libraries from Python's standard library.
# - tkinter is the standard GUI (Graphical User Interface) library for Python.
# - filedialog provides dialogs to open and save files.
# - messagebox is for showing standard dialog boxes (like errors or info).
# - scrolledtext provides a text widget with a linked scrollbar.
# - ttk is the themed widget set for tkinter, which gives a more modern look.
# - re is for regular expression operations, used for the cleaning logic.
# - os is for interacting with the operating system, used here to get file basenames.
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import os
from markdown_cleaner import MarkdownCleaner

# --- GUI Application Class ---
class MarkdownCleanerApp(tk.Tk):
    """
    The main application class, which inherits from tkinter's root window (tk.Tk).
    It sets up the entire graphical user interface and handles user interactions.
    """
    def __init__(self):
        """
        Initializes the main application window and its components.
        """
        super().__init__()  # Call the constructor of the parent class (tk.Tk).
        self.title("Markdown Cleaner")  # Set the window title.
        self.geometry("1000x700")  # Set the initial size of the window.

        # Configure the visual style of the application's widgets.
        self.style = ttk.Style(self)
        try:
            # 'aqua' provides the native macOS look and feel.
            self.style.theme_use("aqua") 
        except tk.TclError:
            # If 'aqua' is not available (e.g., on Windows or Linux), use the default theme.
            self.style.theme_use("default")

        # Create an instance of the MarkdownCleaner to handle the cleaning logic.
        self.cleaner = MarkdownCleaner()
        # Call the method to create all the widgets (buttons, text areas, etc.).
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges all the GUI elements within the main window.
        """
        # Create a main frame to hold all other widgets. Padding adds space around the edges.
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True) # Make the frame fill the entire window.

        # A PanedWindow is a container that allows the user to resize its child widgets.
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashwidth=8)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # --- Input Pane (Left Side) ---
        input_frame = ttk.Frame(paned_window, padding="5")
        ttk.Label(input_frame, text="Original Markdown", font=("Helvetica", 14, "bold")).pack(pady=(0, 5), anchor="w")
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, width=50, font=("Helvetica", 12), relief="solid", bd=1)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        paned_window.add(input_frame) # Add the input frame to the PanedWindow.
        
        # --- Output Pane (Right Side) ---
        output_frame = ttk.Frame(paned_window, padding="5")
        ttk.Label(output_frame, text="Cleaned Markdown", font=("Helvetica", 14, "bold")).pack(pady=(0, 5), anchor="w")
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10, width=50, font=("Helvetica", 12), state="disabled", relief="solid", bd=1)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        paned_window.add(output_frame) # Add the output frame to the PanedWindow.

        # --- Bottom Control Area ---
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0)) # Fills the width at the bottom.

        # A container for the action buttons.
        button_container = ttk.Frame(bottom_frame)
        button_container.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Create and place the buttons, linking them to their respective methods.
        ttk.Button(button_container, text="Open File...", command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_container, text="Clean Text", command=self.clean_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_container, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_container, text="Save As...", command=self.save_file).pack(side=tk.RIGHT, padx=5)

        # A status bar at the very bottom to provide feedback to the user.
        self.status_label = ttk.Label(main_frame, text="Ready", anchor="w", padding=(5,2))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def open_file(self):
        """Handles the 'Open File...' button click. Opens a file dialog and loads content."""
        file_path = filedialog.askopenfilename(
            title="Open Markdown File",
            filetypes=(("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*"))
        )
        # If the user cancels the dialog, file_path will be empty.
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.input_text.delete('1.0', tk.END) # Clear existing text.
                self.input_text.insert('1.0', content) # Insert new content.
                self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
                self.clean_text() # Automatically clean the text after loading a file.
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            self.status_label.config(text="Error opening file")

    def clean_text(self):
        """Handles the 'Clean Text' button click. Cleans the text from the input area."""
        original_content = self.input_text.get("1.0", tk.END)
        if not original_content.strip():
            self.status_label.config(text="Input is empty. Nothing to clean.")
            return

        # Call the cleaner logic.
        cleaned_content, changes_made = self.cleaner.clean_escaped_markdown(original_content)

        # Update the output text area. It must be temporarily enabled to modify it.
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", cleaned_content)
        self.output_text.config(state="disabled") # Disable it again to prevent user edits.

        # Provide feedback in the status bar.
        if changes_made > 0:
            self.status_label.config(text=f"Successfully cleaned {changes_made} types of markdown patterns.")
        else:
            self.status_label.config(text="No escaped markdown patterns were found.")

    def copy_to_clipboard(self):
        """Handles the 'Copy to Clipboard' button click."""
        cleaned_content = self.output_text.get("1.0", tk.END)
        if cleaned_content.strip():
            self.clipboard_clear()  # Clear the system clipboard.
            self.clipboard_append(cleaned_content) # Add the new content.
            self.status_label.config(text="Cleaned text copied to clipboard!")
        else:
            self.status_label.config(text="Nothing to copy.")

    def save_file(self):
        """Handles the 'Save As...' button click. Opens a save file dialog."""
        cleaned_content = self.output_text.get("1.emacs", tk.END)
        if not cleaned_content.strip():
            self.status_label.config(text="Nothing to save.")
            return

        # Ask the user where to save the file.
        file_path = filedialog.asksaveasfilename(
            title="Save Cleaned Markdown",
            defaultextension=".md",
            filetypes=(("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*"))
        )
        # If the user cancels, do nothing.
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            self.status_label.config(text=f"File saved to: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
            self.status_label.config(text="Error saving file")

# --- Main Execution Block ---
if __name__ == "__main__":
    """
    This block runs only when the script is executed directly (not imported).
    It creates an instance of the app and starts the main event loop.
    """
    app = MarkdownCleanerApp()
    app.mainloop() # This call blocks and keeps the application window open.
