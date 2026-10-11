from pathlib import Path
import os
import shutil
import zipfile

import requests
from config import Config


class Installer:
    @staticmethod
    def set_progress(ui, value: float):
        ui.set_progress(round(value, 1))

    @staticmethod
    def download(ui, start: float = 0, end: float = 33):
        url = Config.get_source()
        name = Config.get_file_name()

        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()

            total = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if not chunk:
                        continue

                    file.write(chunk)
                    downloaded += len(chunk)

                    if total > 0:
                        progress = start + (end - start) * downloaded / total
                        Installer.set_progress(ui, min(progress, end))

        Installer.set_progress(ui, end)

    @staticmethod
    def remove_old(ui, start: float = 33, end: float = 63):
        targets = [
            target
            for target in Config.get_target()
            if os.path.exists(target)
        ]

        if not targets:
            Installer.set_progress(ui, end)
            return

        step = (end - start) / len(targets)

        for i, target in enumerate(targets):
            ui.set_status(f"Removing {target}...")
            Installer.set_progress(ui, start + step * i)

            Installer.remove(target)

            Installer.set_progress(ui, start + step * (i + 1))

    @staticmethod
    def cleanup(ui, start: float = 80, end: float = 99):
        targets = [
            target
            for target in Config.get_cleanup_targets()
            if os.path.exists(target)
        ]

        if not targets:
            Installer.set_progress(ui, end)
            return

        step = (end - start) / len(targets)

        for i, target in enumerate(targets):
            ui.set_status(f"Cleanup {target}...")
            Installer.set_progress(ui, start + step * i)

            Installer.remove(target)

            Installer.set_progress(ui, start + step * (i + 1))

    @staticmethod
    def remove(target: str):
        if os.path.isdir(target) and not os.path.islink(target):
            shutil.rmtree(target)
        else:
            os.remove(target)

        print(f"Removed: {target}")

    @staticmethod
    def finalize(ui, start: float = 63, end: float = 80):
        action = Config.get_downloaded_action()
        name = Config.get_file_name()

        if action == "none":
            ui.set_status("Finalizing...")
            Installer.set_progress(ui, end)
            return

        if action == "unzip":
            target = Config.get_extract_target()
            os.makedirs(target, exist_ok=True)

            ui.set_status("Extracting...")

            with zipfile.ZipFile(name, "r") as archive:
                items = archive.infolist()
                total = len(items)

                if total == 0:
                    Installer.set_progress(ui, end)
                    return

                step = (end - start) / total

                for i, item in enumerate(items):
                    destination = Path(target) / item.filename

                    if not destination.exists():
                        archive.extract(item, target)

                    Installer.set_progress(
                        ui,
                        start + step * (i + 1)
                    )

            return

        raise ValueError(f"Unknown downloaded action: {action}")

    @staticmethod
    def install(ui):
        ui.set_status("Downloading...")
        Installer.set_progress(ui, 0)
        Installer.download(ui)

        Installer.remove_old(ui)

        Installer.finalize(ui)

        Installer.cleanup(ui)

        Installer.set_progress(ui, 100)
        ui.complete()
