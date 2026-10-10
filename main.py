from config import Config
from ui import UI

if __name__ == '__main__':
    Config.load()
    UI().run()
