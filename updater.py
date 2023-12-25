import requests
import zipfile
import schedule
import time
import os
from functions import *

# base_url = "https://mqlsupport.agent42.ir"
base_url = "http://127.0.0.1:5000"
download_endpoint = "/update" #download endpoint as zip
version_endpoint = "/version" #version endpoint as float
version_variable = "__version__" # version in main file which the version is stored

check_update_minute = 1
current_dir = os.path.abspath(os.path.dirname(__file__))
core_path = os.path.join(current_dir, "core")
ensure_directory_exists(core_path)


def request_core_files():
    data = {}
    url = f"{base_url}{download_endpoint}"
    res = requests.get(url, json=data, stream=True)
    if res.status_code!=200:
        print("error downloading files")
        print(res.text)
        return

    data_file = "_client_data.zip"
    with open(data_file, 'wb') as file:
        for chunk in res.iter_content(chunk_size=128):
            file.write(chunk)
    with zipfile.ZipFile(data_file, 'r') as zip_ref:
        zip_ref.extractall(core_path)
    os.remove(data_file)
    return True


def request_latest_version():
    url = f"{base_url}{version_endpoint}"
    res = requests.get(url)
    if res.status_code!=200:
        print("error downloading files")
        print(res.text)
        return
    return float(res.text)


def check_update():
    print("Checking for update...")
    main_file = "main.py"
    starter_file = "run.py"

    # reading latest version from server
    latest_version = request_latest_version()
    if not latest_version:
        print("invalid version file")
        return

    # in case the core folder is locked by server
    if latest_version==-1:
        return

    # current running version
    _version = None
    main_file_path = os.path.join(core_path, main_file)
    if os.path.exists(main_file_path):
        with open(main_file_path, 'r') as file:
            for line in file:
                if version_variable in line:
                    version = line.split('=')[-1].strip()
                    version = version.replace('"', '')
                    version = version.replace("'", "")
                    version = version.replace(" ", "")
                    _version = float(version)
                    break

    if not _version or _version<latest_version:
        print(f"New version available: {latest_version}")
        stop_process_by_name(starter_file)
        print(f"Downloading latest version {latest_version}")
        res = request_core_files()
        if not res:
            print(f"Error getting {main_file}")

        run_script_in_terminal(starter_file)
        # stop_process_by_name("updater.py")
    else:
        print("Currently the latest version")
        if not is_process_open(starter_file):
            run_script_in_terminal(starter_file)
    return True


if __name__=="__main__":
    schedule.every(check_update_minute).minutes.do(check_update)
    check_update()
    while True:
        schedule.run_pending()
        time.sleep(10)