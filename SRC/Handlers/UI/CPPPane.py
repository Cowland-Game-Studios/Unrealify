import tkinter as tk
from PIL import ImageTk, Image
import os

import datetime

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.KeyStrokeWrapper import KeyStrokeWrapper

from Handlers.UIComponents.ToggleSwitch import ToggleSwitch
from Handlers.UIComponents.BottomBar import BottomBar

from Handlers.UIComponents.Usefuls import Usefuls

class CPPPane(TemplatePane):
    KeyHandler = None #make class variable so executes in background
    Texts = [] #same reason ^

    def __init__(self, Root, SettingsHandler, width=400, height=50, AllCPPClasses = None):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()
        self.AllCPPClasses = AllCPPClasses

        if CPPPane.KeyHandler is None:
            CPPPane.KeyHandler = KeyStrokeWrapper(AllCPPClasses, Settings=self.SettingsHandler, OnPopupFuncRef=lambda x : [self.UpdateHistoryBox(x)])

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
        FileName = str(datetime.datetime.now()).split(".")[0]

        if not os.path.isdir(Usefuls.DirectoryAbove + "/Outputs"):
            os.mkdir(Usefuls.DirectoryAbove + "/Outputs")

        with open(Usefuls.DirectoryAbove + f"""/Outputs/{FileName}.txt""".replace(" ", "_").replace(":", "_").replace("-", "_"), "w+") as f:
            f.writelines(CPPPane.Texts)

        BottomBar(self.Root, f"Saved successfully as {FileName}.txt")

    def ClearLog(self):
        CPPPane.Texts = []
        self.RefreshHistoryBoxDisplay()

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
            self.BitesPane = tk.Canvas(self.Frame, bg=Usefuls.LightBlack, highlightthickness=0)

            self.MiscBites = BitesTemplatePane(self.BitesPane, "C++", self.SettingsHandler, Width=720-170-10, Height=512-20)
            self.MiscBites.place(x=10, y=10)#.grid()

            self.Add(self.BitesPane, 10, 10)
            self.AllWidgets.append(self.BitesPane)


        if (self.Settings["C++"]["Type"]["Enabled"] and self.AllCPPClasses is not None):
            self.TrackerPane = tk.Canvas(self.Frame, bg=Usefuls.LightBlack, highlightthickness=0)

            self.TrackerTitleText = tk.Label(self.TrackerPane, text="Code Tracker", font=(Usefuls.FontAccented, 24), bg=Usefuls.LightBlack, foreground=Usefuls.Mint)
            self.TrackerTitleText.grid()

            self.TrackerBackgroundText = tk.Label(self.TrackerPane, text="Smart keystroke analyzer to predict code and suggest imports", font=(Usefuls.Font, 12), bg=Usefuls.LightBlack, foreground=Usefuls.White)
            self.TrackerBackgroundText.grid()

            self.TrackerSwitch = ToggleSwitch(self.TrackerPane, CPPPane.KeyHandler.Running, OnAnimDoneRef=lambda x: [self.StartKey(x)], bg=Usefuls.LightBlack, Width=50)
            self.TrackerSwitch.grid()

            if (self.Settings["C++"]["Type"]["LogTypeHistory"]):
                self.TrackHistory = tk.Text(self.TrackerPane, bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, highlightthickness=0, highlightbackground=Usefuls.LightGrey)
                self.TrackHistory.bind("<Key>", lambda e: "break")
                self.TrackHistory.insert(tk.INSERT, f"""{str(datetime.datetime.now()).split(".")[0]}: History Log:\n""")
                self.RefreshHistoryBoxDisplay()
                self.TrackHistory.grid()

                self.ButtonCanvas = tk.Canvas(self.TrackerPane, bg=Usefuls.LightBlack, highlightthickness=0)
                self.ButtonCanvas.grid(pady=5)

                self.SaveHistoryButton = tk.Button(self.ButtonCanvas, text="Save As .txt", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, command=self.SaveLog, highlightthickness=0)
                self.SaveHistoryButton.grid(row=0, column=1, padx=(0, 5))

                self.ClearHistoryButton = tk.Button(self.ButtonCanvas, text="Clear", bg=Usefuls.LightGrey, foreground=Usefuls.White, font=(Usefuls.Font, 10), borderwidth=0, command=self.ClearLog, highlightthickness=0)
                self.ClearHistoryButton.grid(row=0, column=2)

            self.Add(self.TrackerPane)
            self.AllWidgets.append(self.TrackerPane)

    def OnExit(self):
        if CPPPane.KeyHandler.Running:
            self.StartKey(False)