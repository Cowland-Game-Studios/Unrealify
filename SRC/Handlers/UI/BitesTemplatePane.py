import tkinter as tk
from PIL import ImageTk, Image
import os
import time

#Buttons... etc
from Handlers.UIComponents.IncrementSlider import IncrementSlider
from Handlers.UIComponents.ToggleSwitch import ToggleSwitch

from Handlers.UI.TemplatePane import TemplatePane

class BitesTemplatePane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, BitesDirectory, SettingsHandler, width=400, height=50):
        super().__init__(Root, SettingsHandler, width, height)

        self.Settings = self.SettingsHandler.GetAllData()
        self.BitesDirectory = BitesDirectory
        
        self.SetUpBitesUI()

    def SetUpBitesUI(self):
        for BiteName in os.listdir(BitesTemplatePane.DirectoryAbove + "/Bites/" + self.BitesDirectory):
            # if BiteName.startswith("_"):
            #     continue
            
            print(BiteName)
