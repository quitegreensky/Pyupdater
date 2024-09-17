import subprocess
import psutil
import os


def stop_process_by_name(process_name):
    for process in psutil.process_iter(['pid', 'name', 'cmdline', "status"]):

        cmd_lines = process.info.get('cmdline', [])
        if not cmd_lines:
            continue
        if process_name in cmd_lines:
            psutil.Process(process.info['pid']).terminate()


def is_process_open(process_name):
    for process in psutil.process_iter(['pid', 'name', 'cmdline', "status"]):

        cmd_lines = process.info.get('cmdline', [])
        if not cmd_lines:
            continue
        if process_name in cmd_lines:
            return True
    return False


def run_script_in_terminal(script_path):
    venv_python = os.path.join('env', 'Scripts', 'python.exe')
    if not os.path.exists(venv_python):
        print("env not found.")
        venv_python = 'python'

    # Start a new command prompt, run the script using the virtual environment's Python, and keep the window open
    subprocess.Popen(['start', 'cmd', '/k', venv_python, script_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)


def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
