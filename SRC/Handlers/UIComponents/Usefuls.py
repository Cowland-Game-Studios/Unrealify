import os

class Usefuls:
    LightBlack = "#121212"
    LightGrey = "#2D2D2D"
    LightGray = LightGrey
    DarkWhite = "#4B4B4B"
    Mint = "#92DDC8"
    DarkMint = "#5AA17F"
    White = "#FFF"

    Font = "@Yu Gothic UI"
    FontAccented = "@Yu Gothic"
    FontLargest = "@Yu Gothic Bold"
    
    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])