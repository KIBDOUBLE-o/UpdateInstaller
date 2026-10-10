import json
import os
import threading

import webview
from webview import Window

from config import Config
from installer import Installer
from web_constructor import WebConstructor


class UI:
    def __init__(self):
        self.window: Window | None = None

    def call(self, func: str, *args):
        js_args = ", ".join(json.dumps(arg) for arg in args)
        self.window.evaluate_js(f"{func}({js_args});")


    def set_progress(self, percent: int):
        self.call("window.Installer.setProgress", percent)

    def set_status(self, status: str):
        self.call("window.Installer.setStatus", status)

    def set_versions(self, current: str, new: str):
        self.call("window.Installer.setCurrentVersion", current)
        self.call("window.Installer.setNewVersion", new)

    def on_loaded(self):
        self.set_versions(Config.get_current_version(), Config.get_new_version())

    def complete(self):
        self.call("window.Installer.complete")

    def run(self):
        class Api:
            def start_install(api):
                threading.Thread(target=Installer.install, args=(self,), daemon=True).start()

            def quit(api):
                self.window.destroy()

        constructor = WebConstructor()
        if os.path.exists("ui"):
            constructor.include_index(open("ui/index.html", encoding="utf-8").read())
            constructor.include_style(open("ui/style.css", encoding="utf-8").read())
            constructor.include_script(open("ui/script.js", encoding="utf-8").read())
            constructor.create_dump("uinstaller.uinterface")
        else:
            constructor.load_dump("uinstaller.uinterface")

        self.window = webview.create_window(f"{Config.get_product_name()} installer", html=constructor.build(), js_api=Api(), text_select=True, width=640, height=430, resizable=False, frameless=True)
        webview.start(func=self.on_loaded)