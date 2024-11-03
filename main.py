import tkinter as tk
from tkinter import messagebox
import winreg

def get_installed_software():
    software_list = []
    uninstall_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                    display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                    # Use try-except to check for InstallDate
                    try:
                        install_date = winreg.QueryValueEx(subkey, 'InstallDate')[0]
                    except FileNotFoundError:
                        install_date = None
                    software_list.append((display_name, install_date, subkey_name))
            except OSError:
                continue

    return software_list

def update_install_date(subkey_name, new_date):
    uninstall_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{uninstall_key}\\{subkey_name}", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, 'InstallDate', 0, winreg.REG_SZ, new_date)
        messagebox.showinfo("Success", "Installation date updated successfully.")

def display_software():
    for widget in software_frame.winfo_children():
        widget.destroy()

    software_list = get_installed_software()
    
    for display_name, install_date, subkey_name in software_list:
        row = tk.Frame(software_frame)
        row.pack(fill=tk.X)

        name_label = tk.Label(row, text=display_name, width=50)
        name_label.pack(side=tk.LEFT)

        date_label = tk.Label(row, text=install_date if install_date else "Not Set", width=20)
        date_label.pack(side=tk.LEFT)

        edit_button = tk.Button(row, text="Edit Date", command=lambda name=subkey_name: edit_date(name, install_date))
        edit_button.pack(side=tk.LEFT)

def edit_date(subkey_name, current_date):
    def save_date():
        new_date = date_entry.get()
        update_install_date(subkey_name, new_date)
        edit_window.destroy()
        display_software()

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Install Date")
    
    tk.Label(edit_window, text="New Install Date (YYYYMMDD):").pack()
    date_entry = tk.Entry(edit_window)
    date_entry.pack()
    date_entry.insert(0, current_date if current_date else "")  # Pre-fill if exists
    
    tk.Button(edit_window, text="Save", command=save_date).pack()

root = tk.Tk()
root.title("Edit 'InstallDate'")  # Updated title

software_frame = tk.Frame(root)
software_frame.pack(pady=10)

refresh_button = tk.Button(root, text="Refresh Software List", command=display_software)
refresh_button.pack()

display_software()

root.mainloop()
