import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading

# Import the core extractor logic
from core_extractor import extract_xd_data

# --- Colors and Styling ---
COLOR_BG = "#F0F0F0"
COLOR_WIDGET_BG = "#fdfdfd"
COLOR_TEXT = "#222222"
COLOR_BTN = "#fdfdfd"
COLOR_BTN_ACTIVE = "#EAEAEA"
FONT_NORMAL = ("Arial", 10)
FONT_BOLD = ("Arial", 10, "bold")


class ExtractorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XD Extractor")
        self.geometry("500x250")
        self.config(bg=COLOR_BG)
        self.resizable(False, False)

        self.xd_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self):
        main_frame = tk.Frame(self, bg=COLOR_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input file selection widgets ---
        tk.Label(main_frame, text="Adobe XD File (.xd):", font=FONT_BOLD, bg=COLOR_BG, fg=COLOR_TEXT).grid(row=0,
                                                                                                           column=0,
                                                                                                           sticky="w",
                                                                                                           pady=(0, 5))

        in_frame = tk.Frame(main_frame, bg=COLOR_BG)
        in_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        in_entry = tk.Entry(in_frame, textvariable=self.xd_file_path, state="readonly", width=50, bg=COLOR_WIDGET_BG,
                            fg=COLOR_TEXT, relief=tk.SOLID, borderwidth=1)
        in_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        in_btn = tk.Button(in_frame, text="Browse...", command=self.select_xd_file, font=FONT_NORMAL, bg=COLOR_BTN,
                           fg=COLOR_TEXT, activebackground=COLOR_BTN_ACTIVE, relief=tk.SOLID, borderwidth=1, padx=5)
        in_btn.pack(side=tk.LEFT, padx=(10, 0))

        # --- Output directory selection widgets ---
        tk.Label(main_frame, text="Output Directory:", font=FONT_BOLD, bg=COLOR_BG, fg=COLOR_TEXT).grid(row=2, column=0,
                                                                                                        sticky="w",
                                                                                                        pady=(0, 5))

        out_frame = tk.Frame(main_frame, bg=COLOR_BG)
        out_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        out_entry = tk.Entry(out_frame, textvariable=self.output_dir_path, state="readonly", width=50,
                             bg=COLOR_WIDGET_BG, fg=COLOR_TEXT, relief=tk.SOLID, borderwidth=1)
        out_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        out_btn = tk.Button(out_frame, text="Browse...", command=self.select_output_dir, font=FONT_NORMAL, bg=COLOR_BTN,
                            fg=COLOR_TEXT, activebackground=COLOR_BTN_ACTIVE, relief=tk.SOLID, borderwidth=1, padx=5)
        out_btn.pack(side=tk.LEFT, padx=(10, 0))

        # --- Extraction button ---
        self.extract_btn = tk.Button(main_frame, text="Extract", command=self.run_extraction_thread, font=FONT_BOLD,
                                     bg=COLOR_BTN, fg=COLOR_TEXT, activebackground=COLOR_BTN_ACTIVE, relief=tk.SOLID,
                                     borderwidth=1, padx=10, pady=5)
        self.extract_btn.grid(row=4, column=0, columnspan=2)

    def select_xd_file(self):
        """Opens a file dialog to select an .xd file."""
        file_path = filedialog.askopenfilename(
            title="Select Adobe XD File",
            filetypes=[("Adobe XD files", "*.xd")]
        )
        if file_path:
            self.xd_file_path.set(file_path)

    def select_output_dir(self):
        """Opens a directory dialog to select an output folder."""
        dir_path = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if dir_path:
            self.output_dir_path.set(dir_path)

    def run_extraction_thread(self):
        """Validates paths and starts the extraction process in a new thread."""
        if not self.xd_file_path.get() or not self.output_dir_path.get():
            messagebox.showwarning("Warning", "Both input file and output directory must be selected.")
            return

        self.extract_btn.config(state="disabled", text="Extracting...")
        # Run extraction in a separate thread to keep the GUI responsive
        thread = threading.Thread(target=self.perform_extraction)
        thread.start()

    def perform_extraction(self):
        """Calls the core extraction function and shows the result."""
        result = extract_xd_data(self.xd_file_path.get(), self.output_dir_path.get())

        # Show result message box
        if result["status"] == "success":
            messagebox.showinfo("Success", result["message"])
        else:
            messagebox.showerror("Error", result["message"])

        # Re-enable the button
        self.extract_btn.config(state="normal", text="Extract")


if __name__ == "__main__":
    app = ExtractorApp()
    app.mainloop()