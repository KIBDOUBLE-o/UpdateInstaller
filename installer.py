from pathlib import Path
from time import sleep

import requests
from config import Config

import os
import shutil
import zipfile


class Installer:
    @staticmethod
    def download():
        url = Config.get_source()
        name = Config.get_file_name()

        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(name, 'wb') as file:
            chunks = response.iter_content(chunk_size=8192)
            for chunk in chunks:
                if chunk:
                    file.write(chunk)

    @staticmethod
    def remove_old(ui, progress: int):
        cost = 30
        targets = Config.get_target()
        for i in range(len(targets)):
            target = targets[i]
            if not os.path.exists(target): continue
            ui.set_status(f"Removing {target}...")
            ui.set_progress(progress + cost * (i / len(targets)))
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
            print(f"Removed: {target}")
            sleep(1)

    @staticmethod
    def finalize(ui):
        action = Config.get_downloaded_action()
        name = Config.get_file_name()

        if action == "none":
            ui.set_status("Finalizing...")
            ui.set_progress(99)
            sleep(2)
        elif action == "unzip":
            ui.set_status("Extracting...")
            with zipfile.ZipFile(name, "r") as archive:
                for item in archive.infolist():
                    path = Path(item.filename)

                    if path.exists():
                        continue

                    archive.extract(item, Config.get_extract_target())
            ui.set_progress(99)
            sleep(2)

        sleep(1)

    @staticmethod
    def install(ui):
        ui.set_status("Downloading...")
        Installer.download()
        ui.set_progress(50)
        sleep(3)

        Installer.remove_old(ui, 50)

        Installer.finalize(ui)

        ui.complete()
