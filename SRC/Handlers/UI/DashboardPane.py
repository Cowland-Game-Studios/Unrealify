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

from Handlers.UIComponents.Usefuls import Usefuls

from Handlers.UIComponents.ProjectWindow import ProjectWindow

from Handlers.SettingsHandler import YamlParser

class DashboardPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50, bg = Usefuls.LightGrey):
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
        self.DataParser.Write("Opened", str(RootDir))

        if Data["Projects"] is None:
            Data["Projects"] = {}
        
        if RootDir not in Data["Projects"].keys():
            DataToMod = Data["Projects"]
            DataToMod.update({RootDir : {"Platform" : sys.platform, "LastModif" : datetime.datetime.now().timestamp(), "UPath" : Path.replace("\\", "/").split("/")[-1]}})
            self.DataParser.Write("Projects", DataToMod)
        else:
            self.DataParser.Write(f"Projects:::{RootDir}:::LastModif", str(str(datetime.datetime.now().timestamp())), ":::")

        BottomBar(self.Root, ".uproject file found!")

    def SetUpMiscUI(self):

        self.ProjectPane = tk.Canvas(self.Frame, width=720-142, height=512-150, bg=self.Background, highlightthickness=0)

        self.BitesBackgroundText = tk.Label(self.ProjectPane, text="Unrealify Projects", font=(Usefuls.FontAccented, 24), bg=self.Background, foreground=Usefuls.White)
        self.BitesBackgroundText.grid(pady=10)

        self.BrowserPane = ScrollPane(self.ProjectPane, self.Background, 720-167, 512-150)
        self.BrowserPane.place(y=50)

        Column = 0
        Row = 0

        ProjectData = self.DataParser.GetAllData()["Projects"]

        if ProjectData:
            #tysm https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
            ProjectData = {k: v for k, v in sorted(ProjectData.items(), key=lambda item: float(item[1]["LastModif"]) * -1)}

            for ProjectPath in ProjectData:

                Project = ProjectData[ProjectPath]

                if Project["Platform"] != sys.platform:
                    continue

                if not os.path.isfile(ProjectPath + "/Unrealify/Properties.yaml"):
                    continue

                if Column >= 3:
                    Column = 0
                    Row += 1
                NewBite = ProjectWindow(self.BrowserPane.Frame, ProjectPath, self)
                self.BrowserPane.Add(NewBite, Padx=3, Pady=3, RowOverride=Row, ColOverride=Column)
                Column += 1
                self.AllProjects.append(NewBite)

        self.Add(self.ProjectPane, 10, (10, 0))

        self.BottomPane = tk.Canvas(self.Frame, width=720-142, height=75, bg=Usefuls.LightBlack, highlightthickness=0)

        self.Pather = tk.Text(self.BottomPane, bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 12), borderwidth=0, highlightthickness=0)
        self.Pather.place(x=5, y=10, width=505, height=25)

        if self.DataParser.GetAllData()["LastLeft"] != "":
            Left = self.DataParser.GetAllData()["LastLeft"]
            self.Pather.insert("1.0", Left + "/" + self.DataParser.GetAllData()["Projects"][Left]["UPath"])
        self.Pather.bind("<Return>", lambda x: "break")

        def SetFile():
            File = filedialog.askopenfilename(initialdir = DashboardPane.DirectoryAbove,
            title = "Select Unreal Project",
            filetypes = (("Unreal Project",
                "*.uproject"),
                )
            )
            self.Pather.delete("1.0", tk.END)
            self.Pather.insert(tk.INSERT, str(File))

        self.OpenExplorerButton = tk.Button(self.BottomPane, text="...", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 14), borderwidth=0, highlightthickness=0, command=SetFile)
        self.OpenExplorerButton.place(x=500, y=10, width=50, height=25, anchor="nw")

        self.ButtonCanvas = tk.Canvas(self.BottomPane, bg=Usefuls.LightBlack, highlightthickness=0)
        self.ButtonCanvas.place(relx=1, rely=0.875, anchor="se")

        self.OpenButton = tk.Button(self.ButtonCanvas, text="Open", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, highlightthickness=0, command=lambda : [self.OpenProject()])
        self.OpenButton.grid(row=0, column=1, padx=(0, 10))

        self.CreateButton = tk.Button(self.ButtonCanvas, text="Properties", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, highlightthickness=0)
        self.CreateButton.grid(row=0, column=2, padx=(0, 30))

        self.Add(self.BottomPane, Padx=10)

        #self.VerticalScrollBar.destroy() #for now no need