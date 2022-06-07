import os, platform

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

    def Open(path): #thanks to https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    # def ShowFileInExplorer(path):
    #     if platform.system() == "Windows":
    #         os.startfile(path)
    #     elif platform.system() == "Darwin":
    #         subprocess.Popen(["open", path])
    #     else:
    #         subprocess.Popen(["xdg-open", path])

if __name__ == '__main__':
    Usefuls.Open(r"D:\Unreal Projects\TrainSim\MobileTrainSimulator 5.0\Content\Materials")