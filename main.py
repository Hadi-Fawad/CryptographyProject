# main.py

import tkinter as tk
from key_management import KeyManager
from gui import ChatApp
from utils import load_config


def main():
    # Load config settings
    config = load_config("file:/C:/Users/Hadi%20Fawad/CompSec_Project/venv/config.json")
    host = config.get("host", "localhost")
    port = config.get("port", 12345)

    # Initialize key manager with predefined password
    key_manager = KeyManager("SecurePassword")

    # Start chat application
    app = ChatApp(host, port, key_manager)
    app.mainloop()


if __name__ == "__main__":
    main()
