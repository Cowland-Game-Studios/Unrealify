import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.UIComponents.ToggleSwitch import ToggleSwitch
from Handlers.KeyStrokeWrapper import KeyStrokeWrapper

class CPPPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    KeyHandler = None 

    def __init__(self, Root, SettingsHandler, width=400, height=50, AllCPPClasses = None):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()
        self.AllCPPClasses = AllCPPClasses

        if CPPPane.KeyHandler is None:
            CPPPane.KeyHandler = KeyStrokeWrapper(AllCPPClasses)

        self.SetUpMiscUI()

    def StartKey(self, Event):
        if CPPPane.KeyHandler is None:
            return
        
        if (not self.Settings["C++"]["Type"]["Enabled"] or not Event):
            CPPPane.KeyHandler.Stop()
            return
    
        if Event:
            CPPPane.KeyHandler.Start()

    def SetUpMiscUI(self):

        if (self.Settings["C++"]["Bites"]["Enabled"]):
            self.BitesPane = tk.Canvas(self.Frame, bg="#121212", highlightthickness=0)

            self.BitesBackgroundText = tk.Label(self.BitesPane, text="Bites", font=("Yu Gothic Bold", 24), bg="#121212", foreground="#92DDC8")
            self.BitesBackgroundText.grid()

            self.MiscBites = BitesTemplatePane(self.BitesPane, "C++", self.SettingsHandler, Width=720-160, Height=300)
            self.MiscBites.grid()

            self.Add(self.BitesPane)
            self.AllWidgets.append(self.BitesPane)


        if (self.Settings["C++"]["PopUps"]["Enabled"] and self.AllCPPClasses is not None):
            self.TrackerPane = tk.Canvas(self.Frame, bg="#121212", highlightthickness=0)

            self.TrackerTitleText = tk.Label(self.TrackerPane, text="Code Tracker", font=("Yu Gothic Bold", 24), bg="#121212", foreground="#92DDC8")
            self.TrackerTitleText.grid()

            self.TrackerBackgroundText = tk.Label(self.TrackerPane, text="Smart keystroke analyzer to predict code and suggest imports", font=("Yu Gothic", 12), bg="#121212", foreground="#FFF")
            self.TrackerBackgroundText.grid()

            self.TrackerSwitch = ToggleSwitch(self.TrackerPane, CPPPane.KeyHandler.Running, OnAnimDoneRef=lambda x: [self.StartKey(x)], bg="#121212", Width=50)
            self.TrackerSwitch.grid()

            self.Add(self.TrackerPane)
            self.AllWidgets.append(self.TrackerPane)

    def OnExit(self):
        if CPPPane.KeyHandler.Running:
            self.StartKey(False)