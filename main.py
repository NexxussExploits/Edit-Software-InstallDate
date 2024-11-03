import tkinter as tk
from tkinter import messagebox
import winreg

def get_installed_software():
    software_list = []
    uninstall_keys = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
    
    for uninstall_key in uninstall_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                            try:
                                install_date = winreg.QueryValueEx(subkey, 'InstallDate')[0]
                            except FileNotFoundError:
                                install_date = None
                            software_list.append((display_name, install_date, subkey_name))
                    except OSError:
                        continue
        except FileNotFoundError:
            continue

    # Get installed apps from current user as well
    uninstall_key_user = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, uninstall_key_user) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                        try:
                            install_date = winreg.QueryValueEx(subkey, 'InstallDate')[0]
                        except FileNotFoundError:
                            install_date = None
                        software_list.append((display_name, install_date, subkey_name))
                except OSError:
                    continue
    except FileNotFoundError:
        pass

    return software_list

def update_install_date(subkey_name, new_date):
    # Check both HKEY_LOCAL_MACHINE and HKEY_CURRENT_USER for the subkey
    uninstall_keys = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
    
    for uninstall_key in uninstall_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{uninstall_key}\\{subkey_name}", 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, 'InstallDate', 0, winreg.REG_SZ, new_date)
                messagebox.showinfo("Success", "Installation date updated successfully.")
                return
        except FileNotFoundError:
            continue

    # Also check the current user's uninstall key
    uninstall_key_user = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"{uninstall_key_user}\\{subkey_name}", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, 'InstallDate', 0, winreg.REG_SZ, new_date)
            messagebox.showinfo("Success", "Installation date updated successfully.")
            return
    except FileNotFoundError:
        messagebox.showwarning("Error", "Failed to update installation date. Key not found.")

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
    
    tk.Label(edit_window, text="New Install Date (YYYYMM
