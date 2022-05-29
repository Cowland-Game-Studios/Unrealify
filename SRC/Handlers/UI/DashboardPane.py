import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UIComponents.ScrollPane import ScrollPane

class DashboardPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50, bg = "#2D2D2D"):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()
        self.Background = bg

        self.SetUpMiscUI()

    def SetUpMiscUI(self):

        self.ProjectPane = tk.Canvas(self.Frame, width=720-142, height=512, bg=self.Background, highlightthickness=0)

        self.BitesBackgroundText = tk.Label(self.ProjectPane, text="Unrealify Projects", font=("Yu Gothic Bold", 24), bg=self.Background, foreground="#FFF")
        self.BitesBackgroundText.grid(pady=5)

        self.BrowserPane = ScrollPane(self.ProjectPane, self.Background, 720-142, 512)
        self.BrowserPane.grid(pady=5)

        self.Add(self.ProjectPane, 5, 5)