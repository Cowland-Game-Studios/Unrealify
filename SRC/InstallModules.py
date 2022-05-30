import os, sys

packages = [
    "pyyaml",
    "bs4", 
    "pynput",
    "Events",
    "webbrowser",
    "pyperclip",
    "PIL"
]

for package in packages:
    os.system(f"{sys.executable} -m pip install {package}")