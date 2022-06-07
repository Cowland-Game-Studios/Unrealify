import tkinter as tk
from PIL import ImageTk, Image
import os
import time
import webbrowser

#Buttons... etc
from Handlers.UIComponents.IncrementSlider import IncrementSlider
from Handlers.UIComponents.ToggleSwitch import ToggleSwitch
from Handlers.UIComponents.BitesWindow import BitesWindow
from Handlers.SettingsHandler import YamlParser

from Handlers.UIComponents.ScrollPane import ScrollPane
from Handlers.UI.TemplatePane import TemplatePane

from Handlers.UIComponents.Usefuls import Usefuls

class BitesTemplatePane(TemplatePane):
    def __init__(self, Root, BitesDirectory, SettingsHandler, Width=400, Height=50, Background=Usefuls.LightGrey, Title="Bites"):
        super().__init__(Root, SettingsHandler, Width, Height, Background=Background)

        tk.Label(self.Root, text="a", font=(Usefuls.FontAccented, 1), foreground=Usefuls.White, bg=Background, width=Width).pack()

        self.StackImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Search/SearchOnStack.png").resize((25, 25), Image.ANTIALIAS))
        self.GoogleImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Search/SearchOnGoogle.png").resize((25, 25), Image.ANTIALIAS))

        self.Settings = self.SettingsHandler.GetAllData()
        self.BitesDirectory = BitesDirectory

        self.Background = Background

        self.AllBites = []

        self.SearchBar = tk.Text(master=self.Canvas, bg=Usefuls.DarkWhite, foreground=Usefuls.White, font=(Usefuls.Font, 12), borderwidth=0, highlightthickness=0)
        self.SearchBar.place(x=10, y=60, width=250, height=25, anchor="nw")
        self.SearchBar.bind("<KeyRelease>", lambda x: [self.FilterFeed()])

        self.SearchBar.insert(1.0, "Search By Tag/Keyword")

        self.SearchOnStackButton = tk.Label(self.Canvas, relief=tk.FLAT, image=self.StackImage, highlightthickness=0, borderwidth=0)
        self.SearchOnStackButton.place(x=250, y=60, anchor="nw")
        self.SearchOnStackButton.bind("<Button-1>", lambda x: [webbrowser.open(f"""https://stackoverflow.com/search?q={self.SearchBar.get("1.0", tk.END)}""")])

        self.SearchOnGoogleButton = tk.Label(self.Canvas, relief=tk.FLAT, image=self.GoogleImage, highlightthickness=0, borderwidth=0)
        self.SearchOnGoogleButton.place(x=275, y=60, anchor="nw")
        self.SearchOnGoogleButton.bind("<Button-1>", lambda x: [webbrowser.open(f"""https://www.google.com/search?q={self.SearchBar.get("1.0", tk.END)}""")])

        tk.Label(self.Canvas, text="Bites", font=(Usefuls.FontAccented, 25), foreground=Usefuls.White, bg=Background).place(x=10, y=10, anchor="nw")
        
        self.SetUpBitesUI()

    def SetUpBitesUI(self, Context = ""):

        Context = Context.strip().lower()

        Pad = tk.Label(self.Root, text="", font=(Usefuls.FontAccented, 50), foreground=Usefuls.White, bg=self.Background, borderwidth=0)
        self.AllBites.append(Pad)
        Pad.pack(pady=10)

        Bites = []
        for Bite in os.listdir(Usefuls.DirectoryAbove + "/Bites/" + self.BitesDirectory):            
            if (Bite.startswith("_") or Bite.startswith(".")):
                continue

            Data = YamlParser(Usefuls.DirectoryAbove + "/Bites/" + self.BitesDirectory + "/" + Bite + "/Details.yaml").GetAllData()

            if Context == "" or \
                Context in Data["Name"].lower() or \
                any([Context.lower() in x.lower() for x in Data["Tags"].split(",")]):
                Bites.append(Bite)

        if len(Bites) == 0:
            A = tk.Label(self.Root, text="No bites yet.", font=(Usefuls.FontLargest, 24), foreground=Usefuls.White, bg=self.Background)
            self.AllBites.append(A)
            A.pack()
            return

        Column = 3 #rst
        CurrentPane = None 

        for BiteName in Bites:
            if Column >= 3:
                Column = 0
                CurrentPane = tk.Canvas(self.Root, bg=Usefuls.LightGrey, borderwidth=0, highlightthickness=0)
                CurrentPane.pack(pady=5)
            NewBite = BitesWindow(CurrentPane, Usefuls.DirectoryAbove + "/Bites/" + self.BitesDirectory + "/" + BiteName, self.Canvas)
            NewBite.grid(column=Column, row=0, padx=5)
            Column += 1
            self.AllBites.append(CurrentPane)

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