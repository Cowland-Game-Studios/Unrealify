import os, platform, subprocess, sys

class Usefuls:
    LightBlack = "#121212"
    LightGrey = "#2D2D2D"
    LightGray = LightGrey
    DarkWhite = "#4B4B4B"
    Mint = "#92DDC8"
    DarkMint = "#5AA17F"
    White = "#FFF"

    Font = "@Yu Gothic UI" if platform.system() != "Darwin" else "YuGothic" 
    FontAccented = "@Yu Gothic" if platform.system() != "Darwin" else Font
    FontLargest = "@Yu Gothic Bold" if platform.system() != "Darwin" else Font
    
    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])
    if getattr(sys, 'frozen', False):
        DirectoryAbove = "/".join(os.path.dirname(sys.executable).replace("\\", "/").split("/")[:-1])

    def Open(path): #thanks to https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def ShowFileInExplorer(path):
        if os.path.isfile(path):
            path = "/".join(path.replace("\\", "/").split("/")[:-1])
        Usefuls.Open(path)
