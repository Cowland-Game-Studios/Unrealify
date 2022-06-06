import tkinter as tk
from PIL import ImageTk, Image

import os
import datetime
import platform
import subprocess
import webbrowser
import configparser
import json
import shutil

from tkinter import messagebox

from Handlers.SettingsHandler import YamlParser

from Handlers.UIComponents.Usefuls import Usefuls
from Handlers.UIComponents.BottomBar import BottomBar

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

        self.Name = ""
        if self.ProjectDetails.has_option("/Script/EngineSettings.GeneralProjectSettings", "ProjectName"):
            self.Name = self.ProjectDetails.get("/Script/EngineSettings.GeneralProjectSettings", "ProjectName")
        else:
            self.Name = self.ProjectNameRaw

        self.NameLabel = tk.Label(self, text=self.Name, foreground=Usefuls.White, borderwidth=0, background=self.Background, wraplengt=175)
        self.NameLabel.pack()

        self.NameLabel.bind("<Button-1>", lambda x : [self.Clicked()])
        self.ImageLabel.bind("<Button-1>", lambda x : [self.Clicked()])

    def Clicked(self):
        self.Dashboard.Pather.delete("1.0", tk.END)
        self.Dashboard.Pather.insert(tk.INSERT, self.UProjectPath)

        self.Dashboard.OpenProject()

class ProjectExpanded(tk.Canvas):
    def __init__(self, CanvasToOpenOn, Data, Directory, DataParser, OnDestroyFunction = None):
        super().__init__(CanvasToOpenOn, bg=Usefuls.LightBlack, borderwidth=0, highlightthickness=0)

        self.OnDestroyFunction = OnDestroyFunction

        self.Data = Data
        self.Directory = Directory
        self.DataParser = DataParser

        self.TempWindow = ProjectWindow(None, Directory, None, Data["UPath"])

        ButtonRenderScale = 1.25

        self.ProjectImage = ImageTk.PhotoImage(Image.open(self.TempWindow.ImagePath).resize((250, 250)), Image.ANTIALIAS)
        self.CloseImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/CloseProject.png").resize((int(100 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)
        self.UnlinkImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/UnlinkFromUnrealify.png").resize((int(134 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)
        self.DeleteImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/DeleteUnrealProject.png").resize((int(133 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)

        self.OpenInUnrealImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/OpenInUnreal.png").resize((int(104 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)
        self.OpenInCPPImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/OpenInCPP.png").resize((int(119 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)
        self.OpenInGitImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/OpenInGit.png").resize((int(101 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)

        self.OpenBloatManagerImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/BloatManager.png").resize((int(100 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)
        self.AutoSortContentsImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/AutoSortContents.png").resize((int(134 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)
        self.DeleteCachedFoldersImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/ProjectMenu/DeleteCachedFolders.png").resize((int(138 * ButtonRenderScale), int(25 * ButtonRenderScale))), Image.ANTIALIAS)

        self.SetUpUI()

    def SetUpUI(self):
        self.ImageLabel = tk.Label(self, image=self.ProjectImage, borderwidth=3, background=Usefuls.LightGrey)
        self.ImageLabel.place(x=10, y=45, width=250, height=250)

        self.VersionLabel = tk.Label(self, text=self.TempWindow.Version, font=(Usefuls.FontLargest, 12), foreground=Usefuls.LightBlack, borderwidth=0, background=Usefuls.Mint)
        self.VersionLabel.place(x=250 + 10, y=250 + 45, anchor="se")

        self.TitleLabel = tk.Label(self, text=self.TempWindow.Name, bg=Usefuls.LightBlack, fg=Usefuls.Mint, font=(Usefuls.FontLargest, 20))
        self.TitleLabel.place(relx=0.4, y=0, anchor="nw")

        #ty 
        #https://www.geeksforgeeks.org/how-to-get-size-of-folder-using-python/
        #https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder
        Size = 0
        LastModified = 0
        for Path, Directory, Files in os.walk(self.Directory):
            for F in Files:
                Joined = os.path.join(Path, F)
                Size += os.path.getsize(Joined)
                if os.path.getctime(Joined) > LastModified:
                    LastModified = os.path.getctime(Joined)

        Size = int((Size / (1024 * 1024 * 1024)) * 1000) / 1000

        LastModified = datetime.datetime.fromtimestamp(os.path.getmtime(self.Directory)).strftime("%m/%d/%Y %I:%M%p")
        
        tk.Label(self, text="Last Modified ", bg=Usefuls.LightBlack, fg=Usefuls.White, font=(Usefuls.Font, 16)).place(x=250 + 10 + 10, y=40)
        tk.Label(self, text=LastModified, bg=Usefuls.LightBlack, fg=Usefuls.White, font=(Usefuls.FontAccented, 14)).place(x=250 + 10 + 10, y=45 + 25)

        tk.Label(self, text="Project Size ", bg=Usefuls.LightBlack, fg=Usefuls.White, font=(Usefuls.Font, 16)).place(x=250 + 10 + 10, y=45 + 30 + 35)
        tk.Label(self, text=f"{Size}GB" if Size > 1 else f"{Size * 1000}MB", bg=Usefuls.LightBlack, fg=Usefuls.White, font=(Usefuls.FontAccented, 14)).place(x=250 + 10 + 10, y=45 + 30 + 20 + 50)

        Platforms = "All" if "TargetPlatforms" not in self.TempWindow.UProjectContent else ", ".join(self.TempWindow.UProjectContent["TargetPlatforms"])

        tk.Label(self, text="Project Platforms ", bg=Usefuls.LightBlack, fg=Usefuls.White, font=(Usefuls.Font, 16)).place(x=250 + 10 + 10, y=45 + 60 + 75)
        tk.Label(self, text=Platforms, bg=Usefuls.LightBlack, fg=Usefuls.White, font=(Usefuls.FontAccented, 14), wraplengt=300, justify="left").place(x=250 + 10 + 10, y=45 + 60 + 20 + 85)

        self.ButtonCanvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=Usefuls.LightBlack)
        self.ButtonCanvas.place(x=10, rely=0.65, anchor="sw")

        def OpenInUnreal(x):
            pass
        
        self.OpenInUnrealButton = tk.Label(self.ButtonCanvas, image=self.OpenInUnrealImage, borderwidth=0, highlightthickness=0)
        self.OpenInUnrealButton.grid(row=0, column=1, padx=(0, 5))
        self.OpenInUnrealButton.bind("<Button-1>", OpenInUnreal)

        def OpenInCPP(x):
            pass
        
        self.OpenInCPPButton = tk.Label(self.ButtonCanvas, image=self.OpenInCPPImage, borderwidth=0, highlightthickness=0)
        self.OpenInCPPButton.grid(row=0, column=2, padx=(0, 5))
        self.OpenInCPPButton.bind("<Button-1>", OpenInCPP)

        def OpenInGit(Github):
            with open(f"{Github}/config") as f:
                URL = "".join(f.readlines()).split("""url =""")[1].split("""fetch =""")[0].strip().replace(".git", "")
                webbrowser.open(URL)
        
        GitHubDir = None
        if os.path.isdir(f"{self.Directory}/.git"):
            GitHubDir = f"{self.Directory}/.git"
        elif os.path.isdir(f"""{"/".join(self.Directory.split("/")[:-1])}/.git"""):
            GitHubDir = f"""{"/".join(self.Directory.split("/")[:-1])}/.git"""

        if GitHubDir:
            self.OpenInGitButton = tk.Label(self.ButtonCanvas, image=self.OpenInGitImage, borderwidth=0, highlightthickness=0)
            self.OpenInGitButton.grid(row=0, column=3)
            self.OpenInGitButton.bind("<Button-1>", lambda x: [OpenInGit(GitHubDir)])

        self.ButtonCanvas2 = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=Usefuls.LightBlack)
        self.ButtonCanvas2.place(x=10, rely=0.725, anchor="sw")

        def OpenBloat(x):
            pass #write bloater window here
        
        self.BloatManagerButton = tk.Label(self.ButtonCanvas2, image=self.OpenBloatManagerImage, borderwidth=0, highlightthickness=0)
        self.BloatManagerButton.grid(row=0, column=1, padx=(0, 5))
        self.BloatManagerButton.bind("<Button-1>", OpenBloat)

        def AutoSortContents(x):
            Confirm = messagebox.askyesno(title="Confirm Sort", message="This action will sort all .uasset files in every subdirectory of the Content folder into their own folders based on file type (eg. Textures Sounds Blueprints etc)\nThis action can not be undone!")
            if Confirm:
                pass
        
        self.AutoSortContentsButton = tk.Label(self.ButtonCanvas2, image=self.AutoSortContentsImage, borderwidth=0, highlightthickness=0)
        self.AutoSortContentsButton.grid(row=0, column=2, padx=(0, 5))
        self.AutoSortContentsButton.bind("<Button-1>", AutoSortContents)

        def DeleteCachedFolders(x):

            DelList = [
                "/Binaries",
                "/Intermediate",
                "/DerivedDataCache",
                "/Saved"
            ]

            Confirm = messagebox.askyesno(title="Confirm Deletion", message="This action will delete the following folders (Please ensure Unreal is closed during the process):\n - Binaries \n - Intermediate \n - Saved (Except /Config) \n - DerivedDataCache\nThis action can not be undone!")

            if Confirm:
                for SubDir in DelList:

                    if not os.path.isdir(self.Directory + SubDir):
                        continue

                    if SubDir == "/Saved":
                        for SubSubDir in os.listdir(self.Directory + SubDir):
                            if SubSubDir == "Config":
                                continue

                            if os.path.isdir(self.Directory + SubDir + "/" + SubSubDir):
                                shutil.rmtree(self.Directory + SubDir + "/" + SubSubDir)
                            elif os.path.isfile(self.Directory + SubDir + "/" + SubSubDir):
                                os.remove(self.Directory + SubDir + "/" + SubSubDir)
                    else:
                        shutil.rmtree(self.Directory + SubDir)

                BottomBar(self, "Successfully Deleted Directories!")
        
        self.DeleteCachedFoldersButton = tk.Label(self.ButtonCanvas2, image=self.DeleteCachedFoldersImage, borderwidth=0, highlightthickness=0)
        self.DeleteCachedFoldersButton.grid(row=0, column=3, padx=(0, 5))
        self.DeleteCachedFoldersButton.bind("<Button-1>", DeleteCachedFolders)

        self.ButtonCanvas3 = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=Usefuls.LightBlack)
        self.ButtonCanvas3.place(relx=1, rely=0.985, anchor="se")

        def UnlinkFromUnrealify(x):
            Confirm = messagebox.askyesno(title="Confirm Unlink", message="This will unlink the project from Unrealify, and delete the /Unrealify/ folder. \nThis action can not be undone, you will have to find the project again in the selector to link it.")

            if Confirm:

                if os.path.isdir(self.Directory + "/Unrealify"):
                    shutil.rmtree(self.Directory + "/Unrealify")

                NewDict = self.DataParser.GetAllData()["Projects"]
                del NewDict[self.Directory]

                self.DataParser.Write("Projects", NewDict)
                self.DataParser.Write("LastLeft", "")

                self.CloseProject()
        
        self.UnlinkFromUnrealifyButton = tk.Label(self.ButtonCanvas3, image=self.UnlinkImage, borderwidth=0, highlightthickness=0)
        self.UnlinkFromUnrealifyButton.grid(row=0, column=1, padx=(0, 5))
        self.UnlinkFromUnrealifyButton.bind("<Button-1>", UnlinkFromUnrealify)

        def DeleteUnrealProject(x):
            pass
        
        self.DeleteUnrealProject = tk.Label(self.ButtonCanvas3, image=self.DeleteImage, borderwidth=0, highlightthickness=0)
        self.DeleteUnrealProject.grid(row=0, column=2, padx=(0, 5))
        self.DeleteUnrealProject.bind("<Button-1>", DeleteUnrealProject)

        self.CloseButton = tk.Label(self.ButtonCanvas3, image=self.CloseImage, borderwidth=0, highlightthickness=0)
        self.CloseButton.grid(row=0, column=0, padx=(0, 100))
        self.CloseButton.bind("<Button-1>", lambda x: [self.CloseProject()])

    def CloseProject(self):
        self.DataParser.Write("Opened", "")
        if self.OnDestroyFunction:
           self.OnDestroyFunction()
        self.destroy()