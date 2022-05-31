import tkinter as tk
from PIL import ImageTk, Image
import os
import sys
import datetime

from tkinter import filedialog
from tkinter import messagebox

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UIComponents.ScrollPane import ScrollPane
from Handlers.UIComponents.BottomBar import BottomBar

from Handlers.UIComponents.ProjectWindow import ProjectWindow

from Handlers.SettingsHandler import YamlParser

class DashboardPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50, bg = "#2D2D2D"):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()
        self.DataParser = YamlParser(DashboardPane.DirectoryAbove + "/Data/Projects.yaml")
        self.Background = bg

        self.AllProjects = []

        self.SetUpMiscUI()

    def OpenProject(self):

        if not self.Pather:
            return

        Path = self.Pather.get("1.0", tk.END).replace("\n", "")

        if Path.strip() == "":
            return

        try:
            open(Path, "r")
        except:
            return

        RootDir = "/".join(Path.replace("\\", "/").split("/")[:-1])

        if not os.path.isfile(RootDir + "/Unrealify/Properties.yaml"):
            PromptCreate = tk.messagebox.askquestion("Create Unrealify Project", "This Unreal Engine Project has not been associated with Unrealify yet, link? (Will create an /Unrealify/ directory and Unrealify files within project")

            if PromptCreate == "no":
                return

            if not os.path.isdir(RootDir + "/Unrealify"):
                os.mkdir(RootDir + "/Unrealify")

            with open(RootDir + "/Unrealify/Properties.yaml", "w+") as w:
                w.write("\n".join(open(DashboardPane.DirectoryAbove + "/Data/UnrealifyProjectTemplate.yaml", "r").readlines()))
        
        Data = self.DataParser.GetAllData()

        self.DataParser.Write("LastLeft", str(RootDir))

        if Data["Projects"] is None:
            Data["Projects"] = []

        PathAndPlatform = RootDir + "\t" + str(sys.platform) + "\t" + str(str(datetime.datetime.now()).split(".")[0])
        
        if PathAndPlatform not in Data["Projects"]:
            self.DataParser.Write("Projects", Data["Projects"] + [PathAndPlatform])

        BottomBar(self.Root, ".uproject file found!")

    def SetUpMiscUI(self):

        self.ProjectPane = tk.Canvas(self.Frame, width=720-142, height=512-150, bg=self.Background, highlightthickness=0)

        self.BitesBackgroundText = tk.Label(self.ProjectPane, text="Unrealify Projects", font=("Yu Gothic Bold", 24), bg=self.Background, foreground="#FFF")
        self.BitesBackgroundText.grid(pady=10)

        self.BrowserPane = ScrollPane(self.ProjectPane, self.Background, 720-167, 512-150)
        self.BrowserPane.place(y=50)

        Column = 0
        Row = 0

        if self.DataParser.GetAllData()["Projects"]:
            for Project in self.DataParser.GetAllData()["Projects"]:
                if Project.split("\t")[1] != sys.platform:
                    continue

                if not os.path.isfile(Project.split("\t")[0] + "/Unrealify/Properties.yaml"):
                    continue

                if Column >= 3:
                    Column = 0
                    Row += 1
                NewBite = ProjectWindow(self.BrowserPane.Frame, Project.split("\t")[0])
                self.BrowserPane.Add(NewBite, Padx=3, Pady=3, RowOverride=Row, ColOverride=Column)
                Column += 1
                self.AllProjects.append(NewBite)

        self.Add(self.ProjectPane, 10, (10, 0))

        self.BottomPane = tk.Canvas(self.Frame, width=720-142, height=75, bg="#121212", highlightthickness=0)

        self.Pather = tk.Text(self.BottomPane, bg="#2D2D2D", foreground="#FFF", font=("Yu Gothic", 16), borderwidth=0, highlightthickness=0)
        self.Pather.place(x=0, y=10, width=505, height=25)
        self.Pather.insert("1.0", r"/Users/mootbing/Desktop/LoneCity/LoneCity/LoneCity.uproject")
        self.Pather.bind("<Return>", lambda e: "break")

        def SetFile():
            File = filedialog.askopenfilename(initialdir = DashboardPane.DirectoryAbove,
            title = "Select Unreal Project",
            filetypes = (("Unreal Project",
                "*.uproject"),
                )
            )
            self.Pather.delete("1.0", tk.END)
            self.Pather.insert(tk.INSERT, str(File))

        self.OpenExplorerButton = tk.Button(self.BottomPane, text="...", bg="#292929", foreground="#FFF", font=("Yu Gothic", 14), borderwidth=0, highlightthickness=0, command=SetFile)
        self.OpenExplorerButton.place(x=500, y=10, width=50, height=25, anchor="nw")

        self.ButtonCanvas = tk.Canvas(self.BottomPane, bg="#121212", highlightthickness=0)
        self.ButtonCanvas.place(relx=1, rely=0.875, anchor="se")

        self.OpenButton = tk.Button(self.ButtonCanvas, text="Open", bg="#292929", foreground="#FFF", font=("Yu Gothic", 10), borderwidth=0, highlightthickness=0, command=lambda : [self.OpenProject()])
        self.OpenButton.grid(row=0, column=1, padx=(0, 10))

        self.CreateButton = tk.Button(self.ButtonCanvas, text="Properties", bg="#292929", foreground="#FFF", font=("Yu Gothic", 10), borderwidth=0, highlightthickness=0)
        self.CreateButton.grid(row=0, column=2, padx=(0, 30))

        self.Add(self.BottomPane)

        #self.VerticalScrollBar.destroy() #for now no need