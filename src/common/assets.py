import os
import sys

def getAsset(relative_path):
    cleaned_path = relative_path.lstrip("/").replace("/", os.sep)
    base_path = os.path.join(sys._MEIPASS, "assets") if hasattr(sys, "_MEIPASS") else os.path.join(os.path.abspath("."), "assets")
    return os.path.join(base_path, cleaned_path)