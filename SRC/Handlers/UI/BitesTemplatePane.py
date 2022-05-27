import tkinter as tk
from PIL import ImageTk, Image
import os
import time

#Buttons... etc
from Handlers.UIComponents.IncrementSlider import IncrementSlider
from Handlers.UIComponents.ToggleSwitch import ToggleSwitch
from Handlers.UIComponents.BitesWindow import BitesWindow
from Handlers.SettingsHandler import YamlParser

from Handlers.UI.TemplatePane import TemplatePane

class BitesTemplatePane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, BitesDirectory, SettingsHandler, Width=400, Height=50, Background="#262626"):
        super().__init__(Root, SettingsHandler, Width, Height, Background=Background)

        tk.Label(self.Root, text="", font=("Yu Gothic Bold", 1), foreground="#92DDC8", bg=Background, width=Width).pack()

        self.Settings = self.SettingsHandler.GetAllData()
        self.BitesDirectory = BitesDirectory

        self.Background = Background

        self.AllBites = []

        self.SearchBar = tk.Text(master=self.Root, bg="#2D2D2D", foreground="#FFF", font=("Yu Gothic", 10), borderwidth=0)
        self.SearchBar.place(x=10, y=10, width=160, height=20, anchor="nw")
        self.SearchBar.bind("<KeyRelease>", lambda x: [self.FilterFeed()])

        self.SearchBar.insert(1.0, "Search By Tag/Keyword")
        
        self.SetUpBitesUI()

    def SetUpBitesUI(self, Context = ""):

        Context = Context.strip().lower()

        Pad = tk.Label(self.Root, text="", font=("Yu Gothic Bold", 15), foreground="#92DDC8", bg=self.Background)
        self.AllBites.append(Pad)
        Pad.pack()

        Bites = []
        for Bite in os.listdir(BitesTemplatePane.DirectoryAbove + "/Bites/" + self.BitesDirectory):            
            if (Bite.startswith("_")):
                continue

            Data = YamlParser(BitesTemplatePane.DirectoryAbove + "/Bites/" + self.BitesDirectory + "/" + Bite + "/Details.yaml").GetAllData()

            if Context == "" or \
                Context in Data["Name"].lower() or \
                any([Context.lower() in x.lower() for x in Data["Tags"].split(",")]):
                Bites.append(Bite)

        if len(Bites) == 0:
            A = tk.Label(self.Root, text="No bites yet.", font=("Yu Gothic Bold", 15), foreground="#92DDC8", bg=self.Background)
            self.AllBites.append(A)
            A.pack()
            return

        for BiteName in Bites:
            NewBite = BitesWindow(self.Root, BitesTemplatePane.DirectoryAbove + "/Bites/" + self.BitesDirectory + "/" + BiteName)
            NewBite.pack(anchor="center")
            self.AllBites.append(NewBite)

    def ClearBites(self):
        for Widget in self.AllBites:
            if Widget:
                Widget.destroy()
        self.AllBites = []
        
    def FilterFeed(self):
        if not self.SearchBar:
            return

        self.ClearBites()

        self.SetUpBitesUI(Context = self.SearchBar.get("1.0", tk.END))