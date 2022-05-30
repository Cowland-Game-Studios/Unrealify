import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UI.BitesTemplatePane import BitesTemplatePane

class MiscPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()

        self.SetUpMiscUI()

    def SetUpMiscUI(self):

        self.BitesPane = tk.Canvas(self.Frame, width=720-142, height=50, bg="#121212", highlightthickness=0)

        self.MiscBites = BitesTemplatePane(self.BitesPane, "Misc", self.SettingsHandler, Width=720-170-10, Height=512-20)
        self.MiscBites.place()

        self.Add(self.BitesPane, 10, 10)

        self.ToolPane = tk.Canvas(self.Frame, width=720-142, height=50, bg="#121212", highlightthickness=0)

        self.BitesBackgroundText = tk.Label(self.BitesPane, text="Tools", font=("Yu Gothic Bold", 24), bg="#121212", foreground="#92DDC8")
        self.BitesBackgroundText.grid()

        self.Add(self.ToolPane)