import subprocess
import os
import pygetwindow as gw
import win32gui
import win32con

def stop_process_by_name(process_name):
    # close
    windows = gw.getAllTitles()
    for title in windows:
        if "cmd.exe" in title:
            if (process_name in title) or ".py" not in title:
                # close the running script
                # also close all cmds not running a .py file... idle
                window = gw.getWindowsWithTitle(title)
                if window:
                    hwnd = window[0]._hWnd
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    print(f"Closed window: {title}")


def is_process_open(process_name):
    windows = gw.getAllTitles()
    for title in windows:
        if process_name in title:
            return True
    return False


def run_script_in_terminal(script_path):
    venv_python = 'python'
    # Start a new command prompt, run the script using the virtual environment's Python, and keep the window open
    subprocess.Popen(['start', 'cmd', '/k', venv_python, script_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)


def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
