import tkinter as tk
from PIL import ImageTk, Image

import os
import platform
import subprocess
import webbrowser

import shutil

from Handlers.SettingsHandler import YamlParser

from Handlers.UIComponents.BottomBar import BottomBar

class BitesWindow(tk.Canvas):
    
    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, BitePath, Width=155, Height=250, bg="#121212"):
        super().__init__(Root, width=Width, height=Height, bg=bg, borderwidth=2, highlightthickness=0)

        self.BitePath = BitePath

        self.Data = YamlParser(BitePath + "/Details.yaml").GetAllData()

        self.Background = bg

        self.Title = self.Data["Name"]
        self.Description = self.Data["Description"]
        self.CodeSnippetToCopy = self.Data["CodeSnippetToCopy"]
        self.WebpageToOpen = self.Data["WebpageToOpen"]
        self.FileToOpen = BitePath + "/" + self.Data["FileToOpen"]

        self.ProjectData = YamlParser(BitesWindow.DirectoryAbove + "/Data/Projects.yaml").GetAllData()
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
            self.PreviewImage = ImageTk.PhotoImage(Image.open(BitesWindow.DirectoryAbove + "/Image/Other/BadImage.png").resize((self.ImagePreviewSize[0] + 10, self.ImagePreviewSize[1] + 10)), Image.ANTIALIAS)#.crop([0, 0, 155, 100]))
            self.ActualImage = None

        self.SetUpUI()

    def SetUpUI(self):
        if self.PreviewImage:
            self.ImageLabel = tk.Label(self, image=self.PreviewImage, borderwidth=0, background=self.Background)
            self.ImageLabel.pack()
        
        self.TitleLabel = tk.Label(self, text=self.Title, font=("Helvetica", 10), foreground="#FFF", bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        self.TitleLabel.pack()

        self.TitleLabel.bind("<Button-1>", lambda x : [self.CreateBiteDetail()])

        # self.DescriptionLabel = tk.Label(self, text=self.Description, font=("Yu Gothic", 10), foreground="#FFF", bg=self.Background, wraplengt=self.ImagePreviewSize[0])
        # self.DescriptionLabel.pack()

        if self.Tags != []: #switch to display all
            self.TagLabel = tk.Label(self, text=self.Tags[0], font=("Yu Gothic", 7), foreground=self.Background, bg="#92DDC8", wraplengt=self.ImagePreviewSize[0])
            if len(self.ImagePreviewSize) > 1:
                self.TagLabel.place(relx=1, y=self.ImagePreviewSize[1], anchor="e")

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

        if self.ParentBite.PreviewImage and self.ParentBite.ActualImage:
            self.ImageLabel = tk.Label(self, image=self.ParentBite.ActualImage, borderwidth=0, background="#121212")
            self.ImageLabel.pack(pady=5)

        if self.ParentBite.WebpageToOpen != "NONE":
            self.OpenFileButton = tk.Button(master=self, text="Open In Web", bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0, command= lambda: [webbrowser.open(self.ParentBite.WebpageToOpen)])
            self.OpenFileButton.pack(pady=5)
        
        if not self.ParentBite.FileToOpen.endswith("NONE"):
            self.OpenFileButton = tk.Button(master=self, text="Open File", bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0, command= lambda: [BitesExpanded.Open(self.ParentBite.FileToOpen)])
            self.OpenFileButton.pack(pady=5)

            if self.ParentBite.ProjectPath != "" and self.ParentBite.ProjectPath != "NONE" and not self.ParentBite.ApplyPath.endswith("NONE"):
                self.OpenFileButton = tk.Button(master=self, text=f"""Apply to {self.ParentBite.ProjectData["Projects"][self.ParentBite.ProjectPath]["UPath"]}""", bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0, command= lambda: [self.Apply()])
                self.OpenFileButton.pack(pady=5)

        if self.ParentBite.CodeSnippetToCopy != "NONE" or (not self.ParentBite.FileToOpen.endswith("NONE") and self.ParentBite.PreviewImage is None):
            self.CopyLabel = tk.Text(master=self, bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0)
            self.CopyLabel.insert(tk.INSERT, self.ParentBite.CodeSnippetToCopy if self.ParentBite.CodeSnippetToCopy != "NONE" else "\n".join(open(self.ParentBite.FileToOpen, "r").readlines()))
            self.CopyLabel.pack(pady=(5, 0))
