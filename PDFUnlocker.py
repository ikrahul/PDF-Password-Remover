# Author: Rahul Ban
'''About: This script is a masterpiece of coding art. 
It's so good, you'll wonder how you ever lived without it. XD
JK Just a simple minimal PDF Password Remover created 
because I did not like the idea of sharing my files
to websites that unlock the files for you and probably sell your data.'''

import os
import pikepdf
import logging
import coloredlogs
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import webbrowser
import ttkbootstrap as ttkb  


script_name = os.path.basename(__file__)
logging.basicConfig(level=logging.DEBUG, filename=script_name + ".log", filemode="a", encoding='utf-8',
                    format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG, logger=logger, fmt='[%(asctime)s] [%(levelname)s] %(message)s')

def is_pdf_file(file_path):
    return file_path.lower().endswith('.pdf')

def validate_file_path():
    file_path = file_path_entry.get()
    if not is_pdf_file(file_path):
        show_error("Please select a valid PDF file.")
        return
    if not os.path.exists(file_path):
        show_error("File does not exist.")
        return
    if not check_pdf_password_required(file_path):
        messagebox.showinfo("Info", "This PDF file is not locked.")
        return

def show_error(message):
    messagebox.showerror("Error", message)
    file_path_entry.delete(0, tk.END)  

def browse_file():
    open_file_button.config(state=tk.DISABLED)  
    open_folder_button.config(state=tk.DISABLED)  
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_entry.config(state=tk.NORMAL)
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)
        file_path_entry.config(state=tk.DISABLED)
        validate_file_path()

def check_pdf_password_required(file_path):
    try:
        with pikepdf.open(file_path):
            return False
    except pikepdf.PasswordError:
        return True
    except Exception as e:
        show_error(f"Error checking password requirement for {file_path}: {e}")
        show_error(f"Error checking password requirement: {e}")
        return None

unlocked_file_path = None

def remove_pdf_password():
    global unlocked_file_path
    file_path = file_path_entry.get()
    file_password = password_entry.get()
    if not file_path:
        show_error("No file selected. Please select a PDF file first to unlock.")
        return
    try:
        with pikepdf.open(file_path, password=file_password, allow_overwriting_input=True) as pdf_document:
            unlocked_file_path = os.path.splitext(file_path)[0] + "_unlocked.pdf"
            pdf_document.save(unlocked_file_path)
            messagebox.showinfo("Success", "Password successfully removed!")
            open_file_button.config(state=tk.NORMAL)
            open_folder_button.config(state=tk.NORMAL)
    except pikepdf.PasswordError:
        show_error(f"Incorrect password for {file_path}")
        show_error("Incorrect password!")
    except Exception as e:
        show_error(f"Error removing password from {file_path}: {e}")
        show_error(f"Error removing password: {e}")


def open_unlocked_file():
    if unlocked_file_path:
        os.startfile(unlocked_file_path)

def open_folder():
    if unlocked_file_path:
        os.startfile(os.path.dirname(unlocked_file_path))

def open_about():
    about_message = (
        "PDF Password Remover\n"
        "Version 1.0\n\n"
        "This application allows users to remove passwords from PDF files.\n"
        "Simply browse for a locked PDF, enter the password, and unlock it.\n"
        "For more information, visit our GitHub repository.\n\n"
        "Developed by Rahul Ban\n"
        "rahulban@live.in"
    )
    messagebox.showinfo("About", about_message)

def open_github():
    webbrowser.open("Placeholderrepo")


root = tk.Tk()
root.title("PDF Password Remover")
root.iconbitmap('icon.ico')
root.resizable(False, False)

style = ttkb.Style()  
style.theme_use("darkly")  
style.configure('TLabel', font=('Helvetica', 12))  
style.configure('TButton', font=('Helvetica', 12))  


ttk.Label(root, text="PDF Password Remover", font=('Helvetica', 16, 'bold')).pack(pady=20)  # Added title

ttk.Label(root, text="PDF File Path:").pack(pady=5)
file_path_entry = ttk.Entry(root, width=50)
file_path_entry.pack(pady=5)
file_path_entry.config(state=tk.DISABLED)

ttk.Button(root, text="Browse", command=browse_file).pack(pady=5)
ttk.Label(root, text="Password:").pack(pady=5)
password_entry = ttk.Entry(root, show="*", width=50)
password_entry.pack(pady=5)
ttk.Button(root, text="Unlock", command=remove_pdf_password).pack(pady=10)
ttk.Button(root, text="About", command=open_about).pack(side=tk.LEFT, padx=10, pady=10)

open_file_button = ttk.Button(root, text="Open Unlocked File", command=open_unlocked_file)
open_file_button.pack(side=tk.LEFT, padx=10, pady=10)  

open_folder_button = ttk.Button(root, text="Open Folder", command=open_folder)
open_folder_button.pack(side=tk.LEFT, padx=10, pady=10)  
open_file_button.config(state=tk.DISABLED)  
open_folder_button.config(state=tk.DISABLED)  

ttk.Button(root, text="Open Source", command=open_github).pack(side=tk.RIGHT, padx=10, pady=10)
root.mainloop()