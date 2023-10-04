import os
import pyuac
import win32com.client
from tkinter import messagebox
cur_di = os.path.dirname(os.path.abspath(__file__))


def main():
    try:
        path = os.path.join(
            "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/M.K Player.lnk")
        target = f"{cur_di}/M.K Player.exe"
        icon = f"{cur_di}/M_ico.ico"
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.save()
    except:
        messagebox.showerror(
            title="Shortcut Error", message="Program has a problem during make shortcut!")


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin()
        except:
            messagebox.showerror(
                title="Shortcut Error", message="Program has a problem during adding the shortcut!")
    else:
        main()
