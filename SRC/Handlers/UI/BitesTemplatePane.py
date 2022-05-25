import tkinter as tk
from PIL import ImageTk, Image
import os
import time

#Buttons... etc
from Handlers.UIComponents.IncrementSlider import IncrementSlider
from Handlers.UIComponents.ToggleSwitch import ToggleSwitch
from Handlers.UIComponents.BitesWindow import BitesWindow

from Handlers.UI.TemplatePane import TemplatePane

class BitesTemplatePane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, BitesDirectory, SettingsHandler, Width=400, Height=50):
        super().__init__(Root, SettingsHandler, Width, Height)

        tk.Label(self.Root, text="", font=("Yu Gothic Bold", 1), foreground="#92DDC8", bg="#121212", width=Width).pack()

        self.Settings = self.SettingsHandler.GetAllData()
        self.BitesDirectory = BitesDirectory

        self.AllBites = []
        
        self.SetUpBitesUI()

    def SetUpBitesUI(self):

        Bites = [x for x in os.listdir(BitesTemplatePane.DirectoryAbove + "/Bites/" + self.BitesDirectory) if not x.startswith("_")]

        if len(Bites) == 0:
            tk.Label(self.Root, text="No bites yet... Check later.", font=("Yu Gothic Bold", 15), foreground="#92DDC8", bg="#121212").pack()
            return

        for BiteName in Bites:
            NewBite = BitesWindow(self.Root, BitesTemplatePane.DirectoryAbove + "/Bites/" + self.BitesDirectory + "/" + BiteName)
            NewBite.pack(anchor="center")
            self.AllBites.append(NewBite)
        
