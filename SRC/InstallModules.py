import os

packages = [
    "bs4", 
    "pynput",
    "Events",
    "webbrowser",
    "pyperclip"
]

for package in packages:
    os.system(f"python3 -m pip install {package}")