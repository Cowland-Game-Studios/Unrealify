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
            self.ImagePreviewSize = [Width, Width]
            self.PreviewImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Other/BadImage.png").resize((self.ImagePreviewSize[0] + 10, self.ImagePreviewSize[1] + 10)), Image.ANTIALIAS)#.crop([0, 0, 155, 100]))
            self.ActualImage = None

        self.SetUpUI()

    def SetUpUI(self):
        self.ImageLabel = tk.Label(self, image=self.PreviewImage, borderwidth=0, background=self.Background)
        self.ImageLabel.pack()
            
        
        self.TitleLabel = tk.Label(self, text=self.Title, font=(Usefuls.Font, 10), foreground=Usefuls.White, bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        self.TitleLabel.pack()

        self.ImageLabel.bind("<Button-1>", lambda x : [self.CreateBiteDetail()])
        self.TitleLabel.bind("<Button-1>", lambda x : [self.CreateBiteDetail()])

        # self.DescriptionLabel = tk.Label(self, text=self.Description, font=(Usefuls.Font, 10), foreground=Usefuls.White, bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        # self.DescriptionLabel.pack()

        if self.Tags != []: #switch to display all
            self.TagLabel = tk.Label(self, text=self.Tags[0], foreground=self.Background, bg=Usefuls.Mint, wraplengt=self.ImagePreviewSize[0])
            if len(self.ImagePreviewSize) > 1:
                self.TagLabel.place(relx=1, y=self.ImagePreviewSize[1] + 1, anchor="e")

    def CreateBiteDetail(self):
        DetailedBite = BitesExpanded(self)
        DetailedBite.place(x=0, y=0, width=720-142, height=512)

class BitesExpanded(tk.Canvas):

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

        BottomBar(self, f"Applied!" + f" Old moved to '/Unrealify/Temp/' folder" if StashPath != "" else "", Relx=0.3, Rely=0.96)
    
    def __init__(self, ParentBite):
        super().__init__(ParentBite.CanvasToOpenOn, bg=Usefuls.LightBlack, borderwidth=0, highlightthickness=0)

        self.ApplyToProjectImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/BitesMenu/ApplyToProject.png").resize((109, 25), Image.ANTIALIAS))
        self.CopyImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/BitesMenu/Copy.png").resize((55, 25), Image.ANTIALIAS))
        self.OpenFileImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/BitesMenu/OpenFile.png").resize((75, 25), Image.ANTIALIAS))
        self.OpenOnWebImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/BitesMenu/OpenOnWeb.png").resize((95, 25), Image.ANTIALIAS))
        self.OpenInExplorerImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/OpenInExplorer.png").resize((101, 25), Image.ANTIALIAS))
        self.ReturnImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/BitesMenu/Return.png").resize((25, 25), Image.ANTIALIAS))

        self.ParentBite = ParentBite
        self.TitleLabel = tk.Label(self, text=self.ParentBite.Title, font=(Usefuls.FontAccented, 18), foreground=Usefuls.Mint, bg=Usefuls.LightBlack, wraplengt=380)
        self.TitleLabel.pack()

        if self.ParentBite.Tags != []:
            self.TagLabel = tk.Label(self, text=self.ParentBite.Tags[0], foreground=Usefuls.LightBlack, bg=Usefuls.Mint, wraplengt=600)
            self.TagLabel.pack()

        self.DescriptionLabel = tk.Label(self, text=self.ParentBite.Description, font=(Usefuls.Font, 10), foreground=Usefuls.White, bg=Usefuls.LightBlack, wraplengt=380)
        self.DescriptionLabel.pack()

        if self.ParentBite.PreviewImage and self.ParentBite.ActualImage:
            self.ImageLabel = tk.Label(self, image=self.ParentBite.ActualImage, borderwidth=0, background=Usefuls.LightBlack)
            self.ImageLabel.pack(pady=5)

        self.ButtonCanvas = tk.Canvas(self, bg=Usefuls.LightBlack, highlightthickness=0)
        self.ButtonCanvas.pack(pady=5)

        if self.ParentBite.WebpageToOpen != "NONE":
            self.OpenInWebButton = tk.Label(master=self.ButtonCanvas, image=self.OpenOnWebImage, highlightthickness=0, borderwidth=0)
            self.OpenInWebButton.grid(column=0, row=0, padx=5)
            self.OpenInWebButton.bind("<Button-1>", lambda x: [webbrowser.open(self.ParentBite.WebpageToOpen)])
        
        if not self.ParentBite.FileToOpen.endswith("NONE"):
            self.OpenFileButton = tk.Label(master=self.ButtonCanvas, image=self.OpenFileImage, highlightthickness=0, borderwidth=0)
            self.OpenFileButton.grid(column=1, row=0, padx=5)
            self.OpenFileButton.bind("<Button-1>", lambda x: [Usefuls.Open(self.ParentBite.FileToOpen)])

            self.OpenInExplorerButton = tk.Label(master=self.ButtonCanvas, image=self.OpenInExplorerImage, highlightthickness=0, borderwidth=0)
            self.OpenInExplorerButton.grid(column=2, row=0, padx=5)
            self.OpenInExplorerButton.bind("<Button-1>", lambda x: [Usefuls.ShowFileInExplorer(self.ParentBite.FileToOpen)])

            if self.ParentBite.ProjectPath != "" and self.ParentBite.ProjectPath != "NONE" and not self.ParentBite.ApplyPath.endswith("NONE"):
                self.ApplyButton = tk.Label(master=self.ButtonCanvas, image=self.ApplyToProjectImage, highlightthickness=0, borderwidth=0)
                self.ApplyButton.grid(column=3, row=0, padx=5)
                self.ApplyButton.bind("<Button-1>", lambda x: [self.Apply()])

        if self.ParentBite.CodeSnippetToCopy != "NONE":
            self.CopyButton = tk.Label(master=self.ButtonCanvas, image=self.CopyImage, highlightthickness=0, borderwidth=0)
            self.CopyButton.grid(column=4, row=0, padx=5)
            self.CopyButton.bind("<Button-1>", lambda x: [pyperclip.copy(self.ParentBite.CodeSnippetToCopy if self.ParentBite.CodeSnippetToCopy != "__FILE__" else "\n".join(open(self.ParentBite.FileToOpen, "r").readlines())), BottomBar(self, f"Copied!", Rely=0.96)])

        self.CloseButton = tk.Label(master=self, image=self.ReturnImage, highlightthickness=0, borderwidth=0)
        self.CloseButton.place(x=5, y=5, anchor="nw")
        self.CloseButton.bind("<Button-1>", lambda x: [self.destroy()])

        if self.ParentBite.CodeSnippetToCopy != "NONE" or not self.ParentBite.FileToOpen.endswith("NONE"):
            tk.Label(self, text=("  Copy" if self.ParentBite.CodeSnippetToCopy != "NONE" else "File") + " Preview:", bg=Usefuls.LightBlack, foreground=Usefuls.White, borderwidth=0, font=(Usefuls.Font, 12), justify=tk.LEFT).pack(padx=(0, 475))
            self.CopyLabel = tk.Text(master=self, bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0)
            self.CopyLabel.insert(tk.INSERT, self.ParentBite.CodeSnippetToCopy if self.ParentBite.CodeSnippetToCopy != "NONE" and self.ParentBite.CodeSnippetToCopy != "__FILE__" else "\n".join(open(self.ParentBite.FileToOpen, "r").readlines()))
            self.CopyLabel.pack(pady=(5, 0))