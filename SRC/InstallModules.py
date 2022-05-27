import os, sys

packages = [
    "bs4", 
    "pynput",
    "Events",
    "webbrowser",
    "pyperclip"
]

for package in packages:
    os.system(f"{sys.executable} -m pip install {package}")