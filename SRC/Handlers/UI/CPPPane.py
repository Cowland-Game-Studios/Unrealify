import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UI.BitesTemplatePane import BitesTemplatePane

class CPPPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()

        self.SetUpMiscUI()

    def SetUpMiscUI(self):

        self.BitesPane = tk.Canvas(self.Frame, bg="#121212", highlightthickness=0, height=500)

        self.BitesBackgroundText = tk.Label(self.BitesPane, text="Bites", font=("Yu Gothic Bold", 30), bg="#121212", foreground="#FFF")
        self.BitesBackgroundText.grid()

        self.MiscBites = BitesTemplatePane(self.BitesPane, "C++", self.SettingsHandler, Width=720-160, Height=300)
        self.MiscBites.grid()

        self.Add(self.BitesPane)

        self.TrackerPane = tk.Canvas(self.Frame, bg="#121212", highlightthickness=0, height=10, width=200)

        self.TrackerBackgroundText = tk.Label(self.TrackerPane, text="Import Tracker", font=("Yu Gothic Bold", 30), bg="#121212", foreground="#FFF")
        self.TrackerBackgroundText.grid()

        self.Add(self.TrackerPane)

        self.AllWidgets = [self.BitesPane, self.TrackerPane]

        #self.PlayAnimation()