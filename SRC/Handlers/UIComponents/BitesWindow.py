import tkinter as tk
from PIL import ImageTk, Image

import os
import platform
import subprocess
import webbrowser

from Handlers.SettingsHandler import YamlParser

class BitesWindow(tk.Canvas):
    
    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, BitePath, Width=150, Height=250, bg="#121212"):
        super().__init__(Root, width=Width, height=Height, bg=bg, borderwidth=2, highlightthickness=0)

        self.BitePath = BitePath

        self.Data = YamlParser(BitePath + "/Details.yaml").GetAllData()

        self.Background = bg

        self.Title = self.Data["Name"]
        self.Description = self.Data["Description"]
        self.CodeSnippetToCopy = self.Data["CodeSnippetToCopy"]
        self.WebpageToOpen = self.Data["WebpageToOpen"]
        self.FileToOpen = BitePath + "/" + self.Data["FileToOpen"]
        self.Tags = [x.strip() for x in self.Data["Tags"].split(",")] if self.Data["Tags"] != "NONE" else []
        ImagePath = BitePath + "/" + self.Data["Image"]["Link"]

        if (self.Data["Image"]["Link"] != "NONE"):
            #self.ImagePreviewSize = [int(x) for x in self.Data["Image"]["RescaleSize"].split("x")]
            self.ImageRescaleSize = [int(x) for x in self.Data["Image"]["RescaleSize"].split("x")]
            self.ImagePreviewSize = [150, int(self.ImageRescaleSize[1] * 150 / self.ImageRescaleSize[0])]
            self.PreviewImage = ImageTk.PhotoImage(Image.open(ImagePath).resize((self.ImagePreviewSize[0], self.ImagePreviewSize[1])), Image.ANTIALIAS)#.crop([0, 0, 150, 100]))
            self.ActualImage = ImageTk.PhotoImage(Image.open(ImagePath).resize((self.ImageRescaleSize[0], self.ImageRescaleSize[1]), Image.ANTIALIAS))
        else:
            self.ImagePreviewSize = [Width]
            self.PreviewImage = None

        self.SetUpUI()

    def SetUpUI(self):
        if self.PreviewImage:
            self.ImageLabel = tk.Label(self, image=self.PreviewImage, borderwidth=0, background=self.Background)
            self.ImageLabel.pack()
        
        self.TitleLabel = tk.Label(self, text=self.Title, font=("Yu Gothic Bold", 10), foreground="#92DDC8", bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        self.TitleLabel.pack()

        self.TitleLabel.bind("<Button-1>", lambda x : [self.CreateBiteDetail()])

        self.DescriptionLabel = tk.Label(self, text=self.Description, font=("Yu Gothic", 7), foreground="#FFF", bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        self.DescriptionLabel.pack()

        if self.Tags != []: #switch to display all
            self.TagLabel = tk.Label(self, text=self.Tags[0], font=("Yu Gothic", 7), foreground=self.Background, bg="#92DDC8", wraplengt=self.ImagePreviewSize[0])
            self.TagLabel.pack(pady=(5, 10))

    def CreateBiteDetail(self):
        DetailedBite = BitesExpanded(self)

class BitesExpanded(tk.Toplevel):

    def Open(path): #thanks to https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    
    def __init__(self, ParentBite):
        super().__init__(ParentBite)

        self.geometry("400x300")

        self.ParentBite = ParentBite

        self["bg"] = "#121212"
        self.title(f"Unrealify - {self.ParentBite.Title}")
        self.resizable(False, False)
        self.focus_force()
        self.iconphoto(False, ImageTk.PhotoImage(file = BitesWindow.DirectoryAbove + "/Image/Logo/Icon.png"))

        self.TitleLabel = tk.Label(self, text=self.ParentBite.Title, font=("Yu Gothic Bold", 18), foreground="#92DDC8", bg="#121212", wraplengt=380)
        self.TitleLabel.pack()

        if self.ParentBite.Tags != []:
            self.TagLabel = tk.Label(self, text=self.ParentBite.Tags[0], font=("Yu Gothic", 7), foreground="#121212", bg="#92DDC8", wraplengt=600)
            self.TagLabel.pack()

        self.DescriptionLabel = tk.Label(self, text=self.ParentBite.Description, font=("Yu Gothic", 10), foreground="#FFF", bg="#121212", wraplengt=380)
        self.DescriptionLabel.pack()

        if self.ParentBite.PreviewImage:
            self.ImageLabel = tk.Label(self, image=self.ParentBite.ActualImage, borderwidth=0, background="#121212")
            self.ImageLabel.pack(pady=5)

        if self.ParentBite.WebpageToOpen != "NONE":
            self.OpenFileButton = tk.Button(master=self, text="Open In Web", bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0, command= lambda: [webbrowser.open(self.ParentBite.WebpageToOpen)])
            self.OpenFileButton.pack(pady=5)
        
        if not self.ParentBite.FileToOpen.endswith("NONE"):
            self.OpenFileButton = tk.Button(master=self, text="Open In File Explorer", bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0, command= lambda: [BitesExpanded.Open(self.ParentBite.FileToOpen)])
            self.OpenFileButton.pack(pady=5)

        if self.ParentBite.CodeSnippetToCopy != "NONE" or (not self.ParentBite.FileToOpen.endswith("NONE") and self.ParentBite.PreviewImage is None):
            self.CopyLabel = tk.Text(master=self, bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0)
            self.CopyLabel.insert(tk.INSERT, self.ParentBite.CodeSnippetToCopy if self.ParentBite.CodeSnippetToCopy != "NONE" else "\n".join(open(self.ParentBite.FileToOpen, "r").readlines()))
            self.CopyLabel.pack(pady=(5, 0))
