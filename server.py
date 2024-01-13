from flask import Flask, send_file, request, make_response
import os
import zipfile
from os import path


app = Flask(__name__)

current_dir = path.abspath(path.dirname(__file__))
update_files_path = path.join(current_dir, "update")
main_file = "main.py" # the file to check for the current version
version_variable = '__version__'


if not os.path.exists(update_files_path):
    os.makedirs(update_files_path)


@app.route("/update", methods=["POST", "GET"])
def download_requires():
    data = request.json

    files_to_zip = []
    tmp_zip_name = f"_data.zip"

    for _file in os.listdir(update_files_path):
        _file_path = path.join(update_files_path, _file)
        if _file==tmp_zip_name:
            os.remove(_file_path)
        files_to_zip.append(_file_path)

    zip_filename = path.join(update_files_path, tmp_zip_name)
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file in files_to_zip:
            zip_file.write(file, os.path.basename(file))

    return send_file(zip_filename, as_attachment=True)


@app.route("/version", methods=["GET"])
def latest_core_version():
    _version = None

    # looking for lock file
    for _file in os.listdir(update_files_path):
        if "lock" in _file:
            return make_response(f"-1", 200)

    for _file in os.listdir(update_files_path):
        if _file!=main_file:
            continue

        with open(path.join(update_files_path, main_file), 'r') as file:
            for line in file:
                if version_variable in line:
                    # Assuming the version is in the format "code_version = x.x"
                    version = line.split('=')[-1].strip()
                    version = version.replace('"', '')
                    version = version.replace("'", "")
                    version = version.replace(" ", "")
                    _version = float(version)
                    break

    if not _version:
        return make_response("Invalid version", 404)

    return make_response(f"{version}", 200)

if __name__ == "__main__":
    app.run()
