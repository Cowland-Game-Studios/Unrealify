import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UI.BitesTemplatePane import BitesTemplatePane

from Handlers.UIComponents.Usefuls import Usefuls

class MiscPane(TemplatePane):
    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()

        self.SetUpMiscUI()

    def SetUpMiscUI(self):

        self.BitesPane = tk.Canvas(self.Frame, width=720-142, height=50, bg=Usefuls.LightBlack, highlightthickness=0)

        self.MiscBites = BitesTemplatePane(self.BitesPane, "Misc", self.SettingsHandler, Width=720-170-10, Height=512-20)
        self.MiscBites.place()

        self.Add(self.BitesPane, 10, 10)

        self.ToolPane = tk.Canvas(self.Frame, width=720-142, height=50, bg=Usefuls.LightBlack, highlightthickness=0)

        self.BitesBackgroundText = tk.Label(self.BitesPane, text="Tools", font=(Usefuls.FontAccented, 24), bg=Usefuls.LightBlack, foreground=Usefuls.Mint)
        self.BitesBackgroundText.grid()

        self.Add(self.ToolPane)