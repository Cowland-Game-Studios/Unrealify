import tkinter as tk
from PIL import ImageTk, Image

import os
import platform
import subprocess
import webbrowser
import configparser
import json

from Handlers.SettingsHandler import YamlParser

from Handlers.UIComponents.Usefuls import Usefuls

class ProjectWindow(tk.Canvas):
    def __init__(self, Root, ProjectPath, Dashboard, ProjectNameRaw, Width=175, Height=175, bg=Usefuls.LightBlack):
        super().__init__(Root, width=Width, height=Height, bg=bg, borderwidth=2, highlightthickness=0)

        self.Dashboard = Dashboard

        self.ProjectPath = ProjectPath
        
        self.ProjectNameRaw = ProjectNameRaw.replace(".uproject", "")#x.replace(".uproject", "") for x in os.listdir(ProjectPath) if x.lower().endswith(".uproject")][0]

        self.ImagePath = f"{Usefuls.DirectoryAbove}/Image/Other/BadImage.png" 
        
        if os.path.isfile(f"{ProjectPath}/{self.ProjectNameRaw}.png"):
            self.ImagePath = f"{ProjectPath}//{self.ProjectNameRaw}.png" 
        elif os.path.isfile(f"{ProjectPath}/Saved/AutoScreenshot.png"):
            self.ImagePath = f"{ProjectPath}/Saved/AutoScreenshot.png" 

        self.Background = bg
        self.Data = YamlParser(ProjectPath + "/Unrealify/Properties.yaml").GetAllData()

        self.PreviewImage = ImageTk.PhotoImage(Image.open(self.ImagePath).resize((175, 175)), Image.ANTIALIAS)

        self.UProjectContent = {}
        self.UProjectPath = f"{ProjectPath}/{self.ProjectNameRaw}.uproject"
        with open(self.UProjectPath) as f:
            self.UProjectContent = json.loads(f.read())

        self.Version = self.UProjectContent["EngineAssociation"]
        self.ProjectDetails = configparser.ConfigParser(strict=False)
        self.ProjectDetails.read(f"{ProjectPath}/Config/DefaultGame.ini")

        self.SetUpUI()

    def SetUpUI(self):
        self.ImageLabel = tk.Label(self, image=self.PreviewImage, borderwidth=0, background=self.Background)
        self.ImageLabel.pack()

        self.VersionLabel = tk.Label(self, text=self.Version, foreground=Usefuls.LightBlack, borderwidth=0, background=Usefuls.Mint)
        self.VersionLabel.place(x=175, y=175, anchor="se")

        Name = ""
        if self.ProjectDetails.has_option("/Script/EngineSettings.GeneralProjectSettings", "ProjectName"):
            Name = self.ProjectDetails.get("/Script/EngineSettings.GeneralProjectSettings", "ProjectName")
        else:
            Name = self.ProjectNameRaw

        self.NameLabel = tk.Label(self, text=Name, foreground=Usefuls.White, borderwidth=0, background=self.Background, wraplengt=175)
        self.NameLabel.pack()

        self.NameLabel.bind("<Button-1>", lambda x : [self.Clicked()])

    def Clicked(self):
        self.Dashboard.Pather.delete("1.0", tk.END)
        self.Dashboard.Pather.insert(tk.INSERT, self.UProjectPath)

        self.Dashboard.OpenProject()

class ProjectExpanded(tk.Canvas):
    def __init__(self, CanvasToOpenOn, Data, Directory):
        super().__init__(CanvasToOpenOn, bg=Usefuls.LightBlack, borderwidth=0, highlightthickness=0)

        print(Data)
        print(Directory)

        self.TempWindow = ProjectWindow(None, Directory, None, Data["UPath"])

        self.ProjectImage = ImageTk.PhotoImage(Image.open(self.TempWindow.ImagePath).resize((275, 275)), Image.ANTIALIAS)

        self.SetUpUI()

    def SetUpUI(self):
        self.ImageLabel = tk.Label(self, image=self.ProjectImage, borderwidth=3, background=Usefuls.LightGrey)
        self.ImageLabel.place(x=10, y=10+25, width=275, height=275)

        self.VersionLabel = tk.Label(self, text=self.TempWindow.Version, font=(Usefuls.FontAccented, 12), foreground=Usefuls.LightBlack, borderwidth=0, background=Usefuls.Mint)
        self.VersionLabel.place(x=275 + 10, y=275 + 10+25, anchor="se")