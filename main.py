import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from file_organizer import sort_by_type, sort_by_date, sort_all, undo_sort
import os
import sys
import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

theme_colors = {
    "light": {
        "background": "#f5f5f7",     
        "foreground": "#333333",     
        "secondary_bg": "#e5e5e7",   
        "accent1": "#ffcf3e",        
        "accent2": "#ffaa37",        
        "accent3": "#ff7a5a",        
        "accent4": "#332b63",        
        "button_text": "#ffffff",    
        "entry_bg": "#ffffff",       
        "entry_fg": "#333333",       
        "log_bg": "#ffffff",        
        "log_fg": "#333333"          
    },
    "dark": {
        "background": "#1e1e2e",     
        "foreground": "#f5f5f7",     
        "secondary_bg": "#2d2d3d",   
        "accent1": "#C9A22F",        
        "accent2": "#ce8b2f",        
        "accent3": "#bd573e",        
        "accent4": "#332b63",        
        "button_text": "#ffffff",    
        "entry_bg": "#2d2d3d",       
        "entry_fg": "#f5f5f7",       
        "log_bg": "#2d2d3d",         
        "log_fg": "#f5f5f7"         
    }
}

current_theme = "dark"  # Default theme

def log_action(message):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, f"[{timestamp}] {message}\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder_path)
        log_action(f"Selected folder: {folder_path}")

def call_sort_by_type():
    path = entry_path.get()
    if path:
        try:
            sort_by_type(path)
            messagebox.showinfo("Success", "Sorted by file type.")
            log_action("Files sorted by type")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            log_action(f"Error sorting by type: {str(e)}")

def call_sort_by_date():
    path = entry_path.get()
    if path:
        try:
            sort_by_date(path)
            messagebox.showinfo("Success", "Sorted by date.")
            log_action("Files sorted by date")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            log_action(f"Error sorting by date: {str(e)}")

def call_undo():
    path = entry_path.get()
    if path:
        try:
            undo_sort(path)
            messagebox.showinfo("Success", "Unsorted all files and folders.")
            log_action("Unsorting complete - files and user folders restored to root directory")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            log_action(f"Error undoing sort: {str(e)}")

def call_sort_all():
    path = entry_path.get()
    if path:
        try:
            sort_all(path)
            messagebox.showinfo("Success", "Sorted by date and file type.")
            log_action("Files sorted by date and type with user folders in Others")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            log_action(f"Error in sort all: {str(e)}")

def toggle_theme():
    global current_theme
    
    current_theme = "light" if current_theme == "dark" else "dark"
    
    if current_theme == "dark":
        theme_button.config(text="🌙")
    else:
        theme_button.config(text="🔆")
    
    apply_theme(current_theme)
    log_action(f"Switched to {current_theme} mode")

def apply_theme(theme):
    colors = theme_colors[theme]
    
    app.configure(bg=colors["background"])
    
    style.configure("TFrame", background=colors["background"])
    style.configure("TLabel", background=colors["background"], foreground=colors["foreground"])
    style.configure("TEntry", fieldbackground=colors["entry_bg"], foreground=colors["entry_fg"])
    style.configure("TButton", background=colors["accent4"], foreground=colors["button_text"])
    
    style.configure("Type.TButton", background=colors["accent1"])
    style.map("Type.TButton", background=[("active", "#ffe07a")])
    
    style.configure("Date.TButton", background=colors["accent2"])
    style.map("Date.TButton", background=[("active", "#ffbc68")])
    
    style.configure("All.TButton", background=colors["accent3"])
    style.map("All.TButton", background=[("active", "#ff9a82")])
    
    style.configure("Undo.TButton", background=colors["accent4"])
    style.map("Undo.TButton", background=[("active", "#433b7d")])
    
    log_text.config(bg=colors["log_bg"], fg=colors["log_fg"])
    
    theme_button.config(bg=colors["accent4"], fg=colors["button_text"])

app = tk.Tk()
app.title("File Organizer")
app.geometry("600x550")
app.resizable(False, False)

icon_path = resource_path("icon.ico")
try:
    app.iconbitmap(icon_path)
except tk.TclError:
    print(f"Could not load icon from {icon_path}")

style = ttk.Style(app)
style.theme_use("clam")

main_frame = ttk.Frame(app)
main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

top_bar = ttk.Frame(main_frame)
top_bar.pack(fill=tk.X, pady=(0, 15))

theme_button = tk.Button(top_bar, text="🌙", width=3, command=toggle_theme,
                        relief="flat", cursor="hand2", font=("Segoe UI", 12))
theme_button.pack(side=tk.LEFT, padx=5)

title_label = ttk.Label(top_bar, text="Organize your files the easy way.", font=("Segoe UI", 16, "bold"))
title_label.pack(side=tk.LEFT, expand=False)

path_frame = ttk.Frame(main_frame)
path_frame.pack(fill=tk.X, pady=(0, 20))

entry_path = ttk.Entry(path_frame, width=75)
entry_path.pack(side=tk.LEFT, padx=(0, 10), ipady=3)

browse_btn = ttk.Button(path_frame, text="Browse", command=browse_folder)
browse_btn.pack(side=tk.LEFT)

buttons_frame = ttk.Frame(main_frame)
buttons_frame.pack(fill=tk.X, pady=(0, 20))

buttons_frame.columnconfigure(0, weight=1)
buttons_frame.columnconfigure(1, weight=1)

btn_type = ttk.Button(buttons_frame, text="Sort by Type", style="Type.TButton", command=call_sort_by_type)
btn_type.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", ipady=15, ipadx=15)

btn_date = ttk.Button(buttons_frame, text="Sort by Date", style="Date.TButton", command=call_sort_by_date)
btn_date.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", ipady=15, ipadx=15)

btn_all = ttk.Button(buttons_frame, text="Sort All", style="All.TButton", command=call_sort_all)
btn_all.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", ipady=15, ipadx=15)

btn_undo = ttk.Button(buttons_frame, text="Unsort", style="Undo.TButton", command=call_undo)
btn_undo.grid(row=1, column=1, padx=10, pady=10, sticky="nsew", ipady=15, ipadx=15)

log_frame = ttk.Frame(main_frame)
log_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(log_frame, text="Activity Log:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

log_text = scrolledtext.ScrolledText(log_frame, height=8, width=70, font=("Consolas", 9), state=tk.DISABLED)
log_text.pack(fill=tk.BOTH, expand=True)

apply_theme(current_theme)

log_action("Application started")

app.mainloop()