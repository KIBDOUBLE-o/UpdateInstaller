import json


class Config:
    _config = {}

    @classmethod
    def load(cls):
        with open("installer_config.json", encoding="utf-8") as f:
            cls._config = json.load(f)

    @classmethod
    def get_target(cls):
        return cls._config.get("target", [])

    @classmethod
    def get_source(cls):
        return cls._config.get("source", "")

    @classmethod
    def get_file_name(cls):
        return cls._config.get("fileName", "unnamed.txt")

    @classmethod
    def get_product_name(cls):
        return cls._config.get("productName", "Unnamed")

    @classmethod
    def get_downloaded_action(cls):
        return cls._config.get("downloadedAction", "none")

    @classmethod
    def get_current_version(cls):
        return cls._config.get("currentVersion", "unknown")

    @classmethod
    def get_new_version(cls):
        return cls._config.get("newVersion", "unknown")

    @classmethod
    def get_extract_target(cls):
        return cls._config.get("extractTarget", ".")
