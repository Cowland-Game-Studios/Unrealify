import tkinter as tk
from PIL import ImageTk, Image
import os

import datetime

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.UIComponents.ToggleSwitch import ToggleSwitch
from Handlers.KeyStrokeWrapper import KeyStrokeWrapper

class CPPPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    KeyHandler = None 
    Texts = []

    def __init__(self, Root, SettingsHandler, width=400, height=50, AllCPPClasses = None):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()
        self.AllCPPClasses = AllCPPClasses

        if CPPPane.KeyHandler is None:
            CPPPane.KeyHandler = KeyStrokeWrapper(AllCPPClasses, EnablePopup=self.Settings["C++"]["PopUps"]["Enabled"], OnPopupFuncRef=lambda x : [self.UpdateHistoryBox(x)])

        self.SetUpMiscUI()

    def UpdateHistoryBox(self, Detail):
        if (self.Settings["C++"]["Type"]["LogTypeHistory"]):
            CPPPane.Texts.append(f"""\n{str(datetime.datetime.now()).split(".")[0]}: {Detail}""")
        
        self.RefreshHistoryBoxDisplay()
    
    def RefreshHistoryBoxDisplay(self):
        try:
            self.TrackHistory.delete("1.0", tk.END)
            for Text in CPPPane.Texts:
                self.TrackHistory.insert(tk.INSERT, Text)
        except:
            return

    def SaveLog(self):
        with open(CPPPane.DirectoryAbove + f"""/Outputs/{str(datetime.datetime.now()).split(".")[0]}.txt""".replace(" ", "_").replace(":", "_").replace("-", "_"), "w+") as f:
            f.writelines(CPPPane.Texts)

    def StartKey(self, Event):
        if CPPPane.KeyHandler is None:
            return
        
        if (not self.Settings["C++"]["Type"]["Enabled"] or not Event):
            CPPPane.KeyHandler.Stop()
            self.UpdateHistoryBox("Stopped Logging")
            return
    
        if Event:
            CPPPane.KeyHandler.Start()
            self.UpdateHistoryBox("Started Logging")

    def SetUpMiscUI(self):

        if (self.Settings["C++"]["Bites"]["Enabled"]):
            self.BitesPane = tk.Canvas(self.Frame, bg="#121212", highlightthickness=0)

            self.BitesBackgroundText = tk.Label(self.BitesPane, text="Bites", font=("Yu Gothic Bold", 24), bg="#121212", foreground="#92DDC8")
            self.BitesBackgroundText.grid()

            self.MiscBites = BitesTemplatePane(self.BitesPane, "C++", self.SettingsHandler, Width=720-170, Height=300)
            self.MiscBites.grid()

            self.Add(self.BitesPane)
            self.AllWidgets.append(self.BitesPane)


        if (self.Settings["C++"]["Type"]["Enabled"] and self.AllCPPClasses is not None):
            self.TrackerPane = tk.Canvas(self.Frame, bg="#121212", highlightthickness=0)

            self.TrackerTitleText = tk.Label(self.TrackerPane, text="Code Tracker", font=("Yu Gothic Bold", 24), bg="#121212", foreground="#92DDC8")
            self.TrackerTitleText.grid()

            self.TrackerBackgroundText = tk.Label(self.TrackerPane, text="Smart keystroke analyzer to predict code and suggest imports", font=("Yu Gothic", 12), bg="#121212", foreground="#FFF")
            self.TrackerBackgroundText.grid()

            self.TrackerSwitch = ToggleSwitch(self.TrackerPane, CPPPane.KeyHandler.Running, OnAnimDoneRef=lambda x: [self.StartKey(x)], bg="#121212", Width=50)
            self.TrackerSwitch.grid()

            if (self.Settings["C++"]["Type"]["LogTypeHistory"]):
                self.TrackHistory = tk.Text(self.TrackerPane, bg="#262626", foreground="#FFF", font=("Yu Gothic", 10), borderwidth=0)
                self.TrackHistory.bind("<Key>", lambda e: "break")
                self.TrackHistory.insert(tk.INSERT, f"""{str(datetime.datetime.now()).split(".")[0]}: History Log:\n""")
                self.RefreshHistoryBoxDisplay()
                self.TrackHistory.grid()

                self.SaveHistoryButton = tk.Button(self.TrackerPane, text="Save As .txt", bg="#292929", foreground="white", font=("Yu Gothic", 10), borderwidth=0, command=self.SaveLog)
                self.SaveHistoryButton.grid(pady=5)

                #also clear button on same canvas

            self.Add(self.TrackerPane)
            self.AllWidgets.append(self.TrackerPane)

    def OnExit(self):
        if CPPPane.KeyHandler.Running:
            self.StartKey(False)