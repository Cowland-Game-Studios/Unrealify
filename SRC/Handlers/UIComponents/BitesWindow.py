import tkinter as tk
from PIL import ImageTk, Image
import os

class BitesWindow(tk.Canvas):
    
    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, Title, Description, CodeSnippetToCopy, WebpageToOpen, FileToOpen, Image, Width=80, Height=20, bg="#2D2D2D"):
        super().__init__(Root, width=Width, height=Height, bg="#2D2D2D", borderwidth=0, highlightthickness=0)

        self.Title = Title
        self.Description = Description
        self.CodeSnippetToCopy = CodeSnippetToCopy
        self.WebpageToOpen = WebpageToOpen
        self.FileToOpen = FileToOpen
        self.Image = ImagezImage

        self.SetUpUI()

    def SetUpUI(self):
        self.TitleLabel = tk.Label(self, text=self.Title, font=("Yu Gothic Bold", 24), foreground="#FFF", bg="#2D2D2D")
        self.TitleLabel.pack()

        self.DescriptionLabel = tk.Label(self, text=self.Description, font=("Yu Gothic", 10), foreground="#FFF", bg="#2D2D2D")
        self.DescriptionLabel.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = BitesWindow(root, "Title", "Sub", "//test", "https://youtube.com", "a", "a")

    # add to window and show
    myCanvas.pack()
    root.mainloop()