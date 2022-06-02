import tkinter as tk
from PIL import ImageTk, Image

import os
import platform
import subprocess
import webbrowser
import pyperclip

import shutil

from Handlers.SettingsHandler import YamlParser

from Handlers.UIComponents.Usefuls import Usefuls

from Handlers.UIComponents.BottomBar import BottomBar

class BitesWindow(tk.Canvas):
    def __init__(self, Root, BitePath, CanvasToOpenOn, Width=155, Height=250, bg=Usefuls.LightBlack):
        super().__init__(Root, width=Width, height=Height, bg=bg, borderwidth=2, highlightthickness=0)

        self.BitePath = BitePath

        self.Data = YamlParser(BitePath + "/Details.yaml").GetAllData()

        self.Background = bg

        self.CanvasToOpenOn = CanvasToOpenOn

        self.Title = self.Data["Name"]
        self.Description = self.Data["Description"]
        self.CodeSnippetToCopy = self.Data["CodeSnippetToCopy"]
        self.WebpageToOpen = self.Data["WebpageToOpen"]
        self.FileToOpen = BitePath + "/" + self.Data["FileToOpen"]

        self.ProjectData = YamlParser(Usefuls.DirectoryAbove + "/Data/Projects.yaml").GetAllData()
        self.ProjectPath = self.ProjectData["Opened"]
        self.ApplyPath = self.Data["ApplyLocation"].replace("__ROOT__", self.ProjectPath)

        self.Tags = [x.strip() for x in self.Data["Tags"].split(",")] if self.Data["Tags"] != "NONE" else []
        ImagePath = BitePath + "/" + self.Data["Image"]["Link"]

        if (self.Data["Image"]["Link"] != "NONE"):
            #self.ImagePreviewSize = [int(x) for x in self.Data["Image"]["RescaleSize"].split("x")]
            self.ImageRescaleSize = [int(x) for x in self.Data["Image"]["RescaleSize"].split("x")]
            self.ImagePreviewSize = [155, int(self.ImageRescaleSize[1] * 155 / self.ImageRescaleSize[0])]
            self.PreviewImage = ImageTk.PhotoImage(Image.open(ImagePath).resize((self.ImagePreviewSize[0] + 10, self.ImagePreviewSize[1] + 10)), Image.ANTIALIAS)#.crop([0, 0, 155, 100]))
            self.ActualImage = ImageTk.PhotoImage(Image.open(ImagePath).resize((self.ImageRescaleSize[0], self.ImageRescaleSize[1]), Image.ANTIALIAS))
        else:
            self.ImagePreviewSize = [Width + 10, Width + 10]
            self.PreviewImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Other/BadImage.png").resize((self.ImagePreviewSize[0] + 10, self.ImagePreviewSize[1] + 10)), Image.ANTIALIAS)#.crop([0, 0, 155, 100]))
            self.ActualImage = None

        self.SetUpUI()

    def SetUpUI(self):
        if self.PreviewImage:
            self.ImageLabel = tk.Label(self, image=self.PreviewImage, borderwidth=0, background=self.Background)
            self.ImageLabel.pack()
        
        self.TitleLabel = tk.Label(self, text=self.Title, font=(Usefuls.Font, 10), foreground=Usefuls.White, bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        self.TitleLabel.pack()

        self.TitleLabel.bind("<Button-1>", lambda x : [self.CreateBiteDetail()])

        # self.DescriptionLabel = tk.Label(self, text=self.Description, font=(Usefuls.Font, 10), foreground=Usefuls.White, bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        # self.DescriptionLabel.pack()

        if self.Tags != []: #switch to display all
            self.TagLabel = tk.Label(self, text=self.Tags[0], font=(Usefuls.Font, 7), foreground=self.Background, bg=Usefuls.Mint, wraplengt=self.ImagePreviewSize[0])
            if len(self.ImagePreviewSize) > 1:
                self.TagLabel.place(relx=1, y=self.ImagePreviewSize[1], anchor="e")

    def CreateBiteDetail(self):
        DetailedBite = BitesExpanded(self)
        DetailedBite.place(x=0, y=0, width=720-142, height=512)

class BitesExpanded(tk.Canvas):

    def Open(path): #thanks to https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def Apply(self):

        StashPath = ""
        if os.path.isfile(self.ParentBite.ApplyPath):
            StashPath = f"{self.ParentBite.ProjectPath}/Unrealify/Temp"

            if self.ParentBite.Data["ApplyLocation"].replace("__ROOT__", "") != "":
                StashPath += self.ParentBite.Data["ApplyLocation"].replace("__ROOT__", "")
                StashPath = "/".join(StashPath.split("/")[:-1]) if "." in StashPath.split("/")[-1] else StashPath

            if not os.path.isdir(StashPath):
                os.makedirs(StashPath)
            
            #print(f"Copying {self.ParentBite.ApplyPath} to {StashPath} for backup")
        
            shutil.copy2(self.ParentBite.ApplyPath, StashPath)

        shutil.copy2(self.ParentBite.FileToOpen, self.ParentBite.ApplyPath)

        #print(f"Copying {self.ParentBite.FileToOpen} to {self.ParentBite.ApplyPath} for application")

        BottomBar(self, f"Applied!" + f" Old moved to '/Unrealify/Temp/' folder" if StashPath != "" else "", Relx=0.3)
    
    def __init__(self, ParentBite):
        super().__init__(ParentBite.CanvasToOpenOn, bg=Usefuls.LightBlack, borderwidth=0, highlightthickness=0)

        #self.geometry("400x300")

        self.ParentBite = ParentBite
        self.TitleLabel = tk.Label(self, text=self.ParentBite.Title, font=(Usefuls.FontAccented, 18), foreground=Usefuls.Mint, bg=Usefuls.LightBlack, wraplengt=380)
        self.TitleLabel.pack()

        if self.ParentBite.Tags != []:
            self.TagLabel = tk.Label(self, text=self.ParentBite.Tags[0], font=(Usefuls.Font, 7), foreground=Usefuls.LightBlack, bg=Usefuls.Mint, wraplengt=600)
            self.TagLabel.pack()

        self.DescriptionLabel = tk.Label(self, text=self.ParentBite.Description, font=(Usefuls.Font, 10), foreground=Usefuls.White, bg=Usefuls.LightBlack, wraplengt=380)
        self.DescriptionLabel.pack()

        if self.ParentBite.PreviewImage and self.ParentBite.ActualImage:
            self.ImageLabel = tk.Label(self, image=self.ParentBite.ActualImage, borderwidth=0, background=Usefuls.LightBlack)
            self.ImageLabel.pack(pady=5)

        self.ButtonCanvas = tk.Canvas(self, bg=Usefuls.LightBlack, highlightthickness=0)
        self.ButtonCanvas.pack()

        if self.ParentBite.WebpageToOpen != "NONE":
            self.OpenFileButton = tk.Button(master=self.ButtonCanvas, text="Open In Web", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, command= lambda: [webbrowser.open(self.ParentBite.WebpageToOpen)])
            self.OpenFileButton.grid(column=0, row=0, padx=5)
        
        if not self.ParentBite.FileToOpen.endswith("NONE"):
            self.OpenFileButton = tk.Button(master=self.ButtonCanvas, text="Open File", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, command= lambda: [BitesExpanded.Open(self.ParentBite.FileToOpen)])
            self.OpenFileButton.grid(column=1, row=0, padx=5)

            if self.ParentBite.ProjectPath != "" and self.ParentBite.ProjectPath != "NONE" and not self.ParentBite.ApplyPath.endswith("NONE"):
                self.OpenFileButton = tk.Button(master=self.ButtonCanvas, text=f"""Apply to {self.ParentBite.ProjectData["Projects"][self.ParentBite.ProjectPath]["UPath"]}""", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, command= lambda: [self.Apply()])
                self.OpenFileButton.grid(column=2, row=0, padx=5)

        if self.ParentBite.CodeSnippetToCopy != "NONE":
            self.CopyButton = tk.Button(master=self.ButtonCanvas, text=f"""Copy Code""", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, command= lambda: [pyperclip.copy( self.ParentBite.CodeSnippetToCopy)])
            self.CopyButton.grid(column=3, row=0, padx=5)

        self.CloseButton = tk.Button(master=self, text=f"""Close Bite""", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, command= lambda: [self.destroy()])
        self.CloseButton.pack(pady=5)

        if self.ParentBite.CodeSnippetToCopy != "NONE" or not self.ParentBite.FileToOpen.endswith("NONE"):
            tk.Label(self, text=("  Copy" if self.ParentBite.CodeSnippetToCopy != "NONE" else "File") + " Preview:", bg=Usefuls.LightBlack, foreground=Usefuls.White, borderwidth=0, font=(Usefuls.Font, 12), justify=tk.LEFT).pack(padx=(0, 475))
            self.CopyLabel = tk.Text(master=self, bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0)
            self.CopyLabel.insert(tk.INSERT, self.ParentBite.CodeSnippetToCopy if self.ParentBite.CodeSnippetToCopy != "NONE" else "\n".join(open(self.ParentBite.FileToOpen, "r").readlines()))
            self.CopyLabel.pack(pady=(5, 0))