import tkinter as tk
from PIL import ImageTk, Image
import os

#Buttons... etc
from Handlers.UIComponents.IncrementSlider import IncrementSlider
from Handlers.UIComponents.ToggleSwitch import ToggleSwitch

from Handlers.UI.TemplatePane import TemplatePane

class SettingsPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root

        self.Settings = self.SettingsHandler.GetAllData()

        self.SetUpSettingsUI()

    def SetUpSettingsUI(self):

        self.Settings = self.SettingsHandler.GetAllData()

        def SettingsWriteSlider(Value, Dir):
            self.SettingsHandler.Write(Dir, Value)

        #C++

        CSettings = tk.Canvas( self.Root, width=400, height=50, bg="#121212", highlightthickness=0)
        CPPText = tk.Label(CSettings, text="C++", font=("Yu Gothic Bold", 30), foreground="#FFF", bg="#121212")
        CPPText.pack(padx=10)
        self.AllWidgets.append(CPPText)

        CPPToggle = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Enabled"])
        CPPToggle.place(relx=1, y=10, anchor="ne")
        self.AllWidgets.append(CPPToggle)

        if (self.Settings["C++"]["Enabled"]):
            CPPBitesText = tk.Label(CSettings, text="Bites", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            CPPBitesText.pack(padx=10, anchor="w")
            self.AllWidgets.append(CPPBitesText)

            CPPBitesToggle = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Bites/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Bites"]["Enabled"])
            CPPBitesToggle.pack(padx=30, anchor="w")
            self.AllWidgets.append(CPPBitesToggle)

            CPPPopupText = tk.Label(CSettings, text="Pop Ups", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            CPPPopupText.pack(padx=10, anchor="w")
            self.AllWidgets.append(CPPPopupText)

            CPPPopupToggle = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/PopUps/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["PopUps"]["Enabled"])
            CPPPopupToggle.pack(padx=30, anchor="w")
            self.AllWidgets.append(CPPPopupToggle)

            if (self.Settings["C++"]["PopUps"]["Enabled"]):
                CPPPopupAutocloseSlide = IncrementSlider(CSettings, (0, 10), Title="Autoclose After Seconds (0 to not autoclose)", StartValue = self.Settings["C++"]["PopUps"]["AutoCloseAfter"], IncrementValue = 1, OnChangeFuncRef = lambda x : [SettingsWriteSlider(x, "C++/PopUps/AutoCloseAfter")], SnapTo = [], SnapThreashold = 1, bg="#121212")
                CPPPopupAutocloseSlide.pack(padx=30)
                self.AllWidgets.append(CPPPopupAutocloseSlide)

            CPPTypeText = tk.Label(CSettings, text="Type", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            CPPTypeText.pack(padx=10, anchor="w")
            self.AllWidgets.append(CPPTypeText)

            CPPTypeToggle = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Type/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Type"]["Enabled"])
            CPPTypeToggle.pack(padx=30, anchor="w")
            self.AllWidgets.append(CPPTypeToggle)

            if (self.Settings["C++"]["Type"]["Enabled"]):
                CPPTypeHistoryToggle = ToggleSwitch(CSettings, Title="History?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Type/LogTypeHistory")], bg="#121212", StartValue = self.Settings["C++"]["Type"]["LogTypeHistory"])
                CPPTypeHistoryToggle.pack(padx=30, anchor="w")
                self.AllWidgets.append(CPPTypeHistoryToggle)

                CPPTypeDelaySlide = IncrementSlider(CSettings, (0.1, 1), Title="Delay (Seconds) after last key pressed to check", StartValue = self.Settings["C++"]["Type"]["DelayBetweenCharacters"], IncrementValue = 0.05, OnChangeFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Type/DelayBetweenCharacters")], SnapTo = [0.25, 0.5], SnapThreashold = 0.05, bg="#121212")
                CPPTypeDelaySlide.pack(padx=30, pady=3)
                self.AllWidgets.append(CPPTypeDelaySlide)
            
        tk.Label(CSettings, text="", bg="#121212").pack(padx=210)

        CSettings.pack()

        #Blueprints

        BPSettings = tk.Canvas( self.Root, width=400, height=50, bg="#121212", highlightthickness=0)
        BPText = tk.Label(BPSettings, text="Blueprints", font=("Yu Gothic Bold", 30), foreground="#FFF", bg="#121212")
        BPText.pack(padx=10)
        self.AllWidgets.append(BPText)

        BPToggle = ToggleSwitch(BPSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "Blueprints/Enabled")], bg="#121212", StartValue=self.Settings["Blueprints"]["Enabled"])
        BPToggle.place(relx=1, y=10, anchor="ne")
        self.AllWidgets.append(BPToggle)

        if (self.Settings["Blueprints"]["Enabled"]):
            BPBitesText = tk.Label(BPSettings, text="Bites", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            BPBitesText.pack(padx=10, anchor="w")
            self.AllWidgets.append(BPBitesText)

            BPBitesToggle = ToggleSwitch(BPSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "Blueprints/Bites/Enabled")], bg="#121212", StartValue=self.Settings["Blueprints"]["Bites"]["Enabled"])
            BPBitesToggle.pack(padx=30, anchor="w")
            self.AllWidgets.append(BPBitesToggle)

            BPMoodifierText = tk.Label(BPSettings, text="Moodifier", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            BPMoodifierText.pack(padx=10, anchor="w")
            self.AllWidgets.append(BPMoodifierText)

            BPMoodifierToggle = ToggleSwitch(BPSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "Blueprints/Moodifier/Enabled")], bg="#121212", StartValue=self.Settings["Blueprints"]["Moodifier"]["Enabled"])
            BPMoodifierToggle.pack(padx=30, anchor="w")
            self.AllWidgets.append(BPMoodifierToggle)

        tk.Label(BPSettings, text="", bg="#121212").pack(padx=210)

        BPSettings.pack()

        #self.PlayAnimation()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg="#2D2D2D"

    SettingsPane(root, 400, 50).pack()

    root.mainloop()