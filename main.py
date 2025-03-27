import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from tkinter import Toplevel
import subprocess
import threading
import platform
import json
import sys
import os

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip,
                          text=self.text,
                          background="#ffffe0",
                          relief="solid",
                          borderwidth=1)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def resource_path(self, relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DiscordStyleGitLabUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GitLab Manager v0.2.1")
        if platform.system() == "Windows":
            try:
                icon_path = resource_path(self, "logo.ico")
            except tk.TclError:
                print("Failed to load window icon")
        else:
            icon_path = "logo.ico"
        self.root.iconbitmap(icon_path)
        self.root.geometry("1000x800")

        # Farbpalette
        self.colors = {
            "background": "#36393f",
            "secondary": "#2f3136",
            "tertiary": "#40444b",
            "text": "#dcddde",
            "accent": "#5865f2",
            "input_bg": "#40444b"
        }

        self.setup_style()
        self.selected_files = []
        self.token_visible = False
        self.nav_buttons = []

        # Haupt-Frames
        self.main_frame = ttk.Frame(self.root, style="Secondary.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Linke Seitenleiste
        self.sidebar = ttk.Frame(self.main_frame, width=200, style="Secondary.TFrame")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Hauptinhalt
        self.content_frame = ttk.Frame(self.main_frame, style="Background.TFrame")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_widgets()
        self.create_sidebar()
        self.create_file_list()
        self.load_config()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TFrame", background=self.colors["background"])
        style.configure("Background.TFrame", background=self.colors["background"])
        style.configure("Secondary.TFrame", background=self.colors["secondary"])
        style.configure("TLabel",
                        background=self.colors["background"],
                        foreground=self.colors["text"],
                        font=("Helvetica", 10))

        style.configure("TEntry",
                        fieldbackground=self.colors["input_bg"],
                        foreground=self.colors["text"],
                        insertcolor=self.colors["text"],
                        borderwidth=1,
                        relief="flat")

        style.configure("Accent.TButton",
                        background=self.colors["accent"],
                        foreground="white",
                        borderwidth=0,
                        font=("Helvetica", 10, "bold"),
                        padding=10)
        style.map("Accent.TButton",
                  background=[("active", "#4752c4"), ("pressed", "#3c45a5")])

    def create_sidebar(self):
        logo_frame = ttk.Frame(self.sidebar, style="Secondary.TFrame")
        logo_frame.pack(pady=20)

        # Load and display logo
        try:
            if sys.platform == "windows":
                logo_path = resource_path(self, "logo.ico")
            else:
                logo_path = "logo.ico"
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((80, 80), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_photo = logo_photo

            logo_label = ttk.Label(logo_frame, image=logo_photo, style="Secondary.TLabel")
            logo_label.pack(pady=5)
            ttk.Label(logo_frame,
                      text="GitLab Manager",
                      style="TLabel",
                      font=("Helvetica", 14, "bold")).pack(pady=5)
        except Exception as e:
            print(f"Failed to load logo: {e}")
            ttk.Label(logo_frame,
                      text="GitLab Manager",
                      style="TLabel",
                      font=("Helvetica", 14, "bold")).pack(pady=10)

        nav_buttons = [
            ("Clone Repo", self.clone_repo),
            ("Commit", self.commit),
            ("Push", self.push),
            ("Pull", self.pull)
        ]

        for text, command in nav_buttons:
            btn = ttk.Button(self.sidebar,
                             text=text,
                             style="Accent.TButton",
                             command=command)
            btn.pack(fill=tk.X, padx=10, pady=5)
            self.nav_buttons.append(btn)

    def create_widgets(self):
        input_fields = [
            ("Repository URL", "repo_url"),
            ("Username", "username"),
            ("Token", "token"),
            ("Local Directory", "local_dir"),
            ("Commit Message", "commit_message"),
            ("Branch", "branch")
        ]

        self.vars = {
            "repo_url": tk.StringVar(),
            "username": tk.StringVar(),
            "token": tk.StringVar(),
            "local_dir": tk.StringVar(),
            "commit_message": tk.StringVar(),
            "branch": tk.StringVar(value="main")
        }

        for i, (label, var_name) in enumerate(input_fields):
            frame = ttk.Frame(self.content_frame, style="Background.TFrame")
            frame.pack(fill=tk.X, padx=20, pady=10)

            ttk.Label(frame,
                      text=label + ":",
                      style="TLabel",
                      width=15).pack(side=tk.LEFT)

            if var_name == "local_dir":
                entry = ttk.Entry(frame,
                                  textvariable=self.vars[var_name],
                                  style="TEntry",
                                  width=40)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                ttk.Button(frame,
                           text="Browse",
                           style="Accent.TButton",
                           command=self.browse_directory).pack(side=tk.RIGHT, padx=5)
            else:
                entry = ttk.Entry(frame,
                                  textvariable=self.vars[var_name],
                                  style="TEntry",
                                  width=50)
                if var_name == "token":
                    entry.configure(show="*")
                    self.entry_token = entry
                    ttk.Checkbutton(frame,
                                    text="Show",
                                    command=self.toggle_token).pack(side=tk.RIGHT, padx=5)
                    Tooltip(entry, "GitLab Personal Access Token")
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Console Ausgabe
        self.console = tk.Text(self.content_frame,
                               bg=self.colors["input_bg"],
                               fg=self.colors["text"],
                               insertbackground=self.colors["text"])
        self.console.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(self.content_frame, command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.config(yscrollcommand=scrollbar.set)

        # Statusleiste
        self.status = ttk.Label(self.content_frame,
                                text="Ready",
                                style="TLabel",
                                background=self.colors["secondary"],
                                padding=10)
        self.status.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

    def create_file_list(self):
        file_frame = ttk.Frame(self.content_frame, style="Background.TFrame")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Button(file_frame,
                   text="Select Files",
                   style="Accent.TButton",
                   command=self.select_files).pack(anchor=tk.W, pady=1)

        self.file_listbox = tk.Listbox(file_frame,
                                       bg=self.colors["input_bg"],
                                       fg=self.colors["text"],
                                       selectbackground=self.colors["accent"],
                                       height=6)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

    def toggle_token(self):
        self.token_visible = not self.token_visible
        show = "" if self.token_visible else "*"
        self.entry_token.config(show=show)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.vars["local_dir"].set(directory)

    def select_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for f in self.selected_files:
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def validate_inputs(self, required_fields):
        missing = [field for field in required_fields if not self.vars[field].get()]
        if missing:
            messagebox.showerror("Error", f"Missing required fields: {', '.join(missing)}")
            return False
        return True

    def is_git_repo(self, path):
        try:
            subprocess.run(['git', '-C', path, 'rev-parse', '--is-inside-work-tree'],
                           check=True,
                           capture_output=True,
                           text=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def toggle_buttons(self, state):
        for btn in self.nav_buttons:
            btn.state(['!disabled' if state else 'disabled'])

    def run_git_command(self, command, success_msg, error_msg):
        def wrapper():
            try:
                self.toggle_buttons(False)
                self.status.config(text="Processing...")
                self.console.delete(1.0, tk.END)

                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )

                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.console.insert(tk.END, output)
                        self.console.see(tk.END)

                return_code = process.poll()
                if return_code == 0:
                    self.status.config(text=success_msg)
                    messagebox.showinfo("Success", success_msg)
                else:
                    self.status.config(text="Error occurred")
                    messagebox.showerror("Error", error_msg)

            except Exception as e:
                self.status.config(text="Error occurred")
                messagebox.showerror("Error", str(e))
            finally:
                self.toggle_buttons(True)

        threading.Thread(target=wrapper, daemon=True).start()

    def clone_repo(self):
        if not self.validate_inputs(["repo_url", "local_dir"]):
            return

        url = self.vars["repo_url"].get()
        directory = self.vars["local_dir"].get()

        self.run_git_command(
            ["git", "clone", url, directory],
            "Repository cloned successfully",
            "Failed to clone repository"
        )

    def commit(self):
        if not self.validate_inputs(["local_dir", "commit_message"]) or not self.selected_files:
            messagebox.showerror("Error", "Select files to commit and enter commit message")
            return

        directory = self.vars["local_dir"].get()
        message = self.vars["commit_message"].get()

        if not self.is_git_repo(directory):
            messagebox.showerror("Error", "Selected directory is not a Git repository")
            return

        commands = [
            ["git", "-C", directory, "add", *self.selected_files],
            ["git", "-C", directory, "commit", "-m", message]
        ]

        for cmd in commands:
            self.run_git_command(
                cmd,
                "Commit successful",
                "Commit failed"
            )

    def push(self):
        if not self.validate_inputs(["local_dir"]):
            return

        directory = self.vars["local_dir"].get()

        if not self.is_git_repo(directory):
            messagebox.showerror("Error", "Selected directory is not a Git repository")
            return

        branch = self.vars["branch"].get() or "main"
        self.run_git_command(
            ["git", "-C", directory, "push", "origin", branch],
            "Push successful",
            "Push failed"
        )

    def pull(self):
        if not self.validate_inputs(["local_dir"]):
            return

        directory = self.vars["local_dir"].get()

        if not self.is_git_repo(directory):
            messagebox.showerror("Error", "Selected directory is not a Git repository")
            return

        branch = self.vars["branch"].get() or "main"
        self.run_git_command(
            ["git", "-C", directory, "pull", "origin", branch],
            "Pull successful",
            "Pull failed"
        )

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                for key in self.vars:
                    if key in config:
                        self.vars[key].set(config[key])
        except FileNotFoundError:
            pass

    def save_config(self):
        config = {key: var.get() for key, var in self.vars.items()}
        with open('config.json', 'w') as f:
            json.dump(config, f)

    def on_close(self):
        self.save_config()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordStyleGitLabUI(root)
    root.mainloop()