import tkinter as tk
from PIL import ImageTk, Image
import os

class TemplatePane(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, width=width, height=height, bg="#121212", borderwidth=0, highlightthickness=0)

        self.AllWidgets = []
        self.SettingsHandler = SettingsHandler

    def Clear(self):
        for Widget in self.AllWidgets:
            if Widget is not None:
                Widget.destroy()
        self.AllWidgets = []

    def SetUpUI(self):
        self.Clear()

        ContentPane = tk.Canvas(width=self.Width - 125, height=self.Height, bg="#121212", highlightthickness=0)
        ContentPane.place(x = 125, y = 0, anchor = "nw")

        self.AllWidgets.append(ContentPane)

        return ContentPane