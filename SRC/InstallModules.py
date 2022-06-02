import os, sys

packages = [
    "pyyaml",
    "bs4", 
    "pynput",
    "Events",
    "requests",
    #"webbrowser",
    "pyperclip",
    "pillow"
    #"json" #Unreal uses this... yaml better imo
]

for package in packages:
    os.system(f"{sys.executable} -m pip install {package}")