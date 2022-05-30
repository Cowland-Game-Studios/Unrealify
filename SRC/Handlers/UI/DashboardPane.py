import tkinter as tk
from PIL import ImageTk, Image
import os

from tkinter import filedialog

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UIComponents.ScrollPane import ScrollPane

from Handlers.SettingsHandler import YamlParser

class DashboardPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50, bg = "#2D2D2D"):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()
        self.Background = bg

        self.SetUpMiscUI()

    def OpenProject(self, Path):
        Parser = YamlParser(DashboardPane.DirectoryAbove + "/Data/Projects.yaml")
        Data = Parser.GetAllData()
        Parser.Write("LastLeft", Path)

        if Path not in Data["Projects"]:
            Parser.Write("Projects", Data["Projects"].append(Path))

        print(f"opening {Path}")

    def SetUpMiscUI(self):

        self.ProjectPane = tk.Canvas(self.Frame, width=720-142, height=512-150, bg=self.Background, highlightthickness=0)

        self.BitesBackgroundText = tk.Label(self.ProjectPane, text="Unrealify Projects", font=("Yu Gothic Bold", 24), bg=self.Background, foreground="#FFF")
        self.BitesBackgroundText.grid(pady=10)

        self.BrowserPane = ScrollPane(self.ProjectPane, self.Background, 720-142, 512-150)
        self.BrowserPane.place(y=50)

        self.Add(self.ProjectPane, 10, (10, 0))

        self.BottomPane = tk.Canvas(self.Frame, width=720-142, height=75, bg="#121212", highlightthickness=0)

        self.Pather = tk.Text(self.BottomPane, bg="#2D2D2D", foreground="#FFF", font=("Yu Gothic", 16), borderwidth=0, highlightthickness=0)
        self.Pather.place(x=0, y=10, width=505, height=25)
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

        self.OpenButton = tk.Button(self.ButtonCanvas, text="Open", bg="#292929", foreground="#FFF", font=("Yu Gothic", 10), borderwidth=0, highlightthickness=0, command=lambda : [self.OpenProject(self.Pather.get("1.0", tk.END))])
        self.OpenButton.grid(row=0, column=1, padx=(0, 10))

        self.CreateButton = tk.Button(self.ButtonCanvas, text="Create Unrealify Project", bg="#292929", foreground="#FFF", font=("Yu Gothic", 10), borderwidth=0, highlightthickness=0)
        self.CreateButton.grid(row=0, column=2, padx=(0, 30))

        self.Add(self.BottomPane)

        #self.VerticalScrollBar.destroy() #for now no need