import json

from protected_data_operator import PDOperator


class WebConstructor:
    __slots__ = ('_index', '_style', '_scripts')

    def __init__(self):
        self._index = []
        self._style = []
        self._scripts = []

    def include_index(self, index: str):
        pass

    def include_style(self, style: str):
        pass

    def include_script(self, script: str):
        pass

    def build(self) -> str:
        pass

    def create_dump(self, path: str):
        pass

    def load_dump(self, path: str):
        pass
