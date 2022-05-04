import tkinter as tk
from PIL import ImageTk, Image
import os

#Buttons... etc
from UIComponents.IncrementSlider import IncrementSlider
from UIComponents.ToggleSwitch import ToggleSwitch

from UI.TemplatePane import TemplatePane

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
        Ref = tk.Label(CSettings, text="C++", font=("Yu Gothic Bold", 30), foreground="#FFF", bg="#121212")
        Ref.pack(padx=10)

        Ref = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Enabled"])
        Ref.place(relx=1, y=10, anchor="ne")

        if (self.Settings["C++"]["Enabled"]):
            Ref = tk.Label(CSettings, text="Bites", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            Ref.pack(padx=10, anchor="w")

            Ref = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Bites/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Bites"]["Enabled"])
            Ref.pack(padx=30, anchor="w")

            Ref = tk.Label(CSettings, text="Pop Ups", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            Ref.pack(padx=10, anchor="w")

            Ref = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/PopUps/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["PopUps"]["Enabled"])
            Ref.pack(padx=30, anchor="w")

            if (self.Settings["C++"]["PopUps"]["Enabled"]):
                Ref = IncrementSlider(CSettings, (0, 10), Title="Autoclose After Seconds (0 to not autoclose)", StartValue = self.Settings["C++"]["PopUps"]["AutoCloseAfter"], IncrementValue = 1, OnChangeFuncRef = lambda x : [SettingsWriteSlider(x, "C++/PopUps/AutoCloseAfter")], SnapTo = [], SnapThreashold = 1, bg="#121212")
                Ref.pack(padx=30)

            Ref = tk.Label(CSettings, text="Type", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            Ref.pack(padx=10, anchor="w")

            Ref = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Type/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Type"]["Enabled"])
            Ref.pack(padx=30, anchor="w")

            if (self.Settings["C++"]["Type"]["Enabled"]):
                Ref = ToggleSwitch(CSettings, Title="History?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Type/LogTypeHistory")], bg="#121212", StartValue = self.Settings["C++"]["Type"]["LogTypeHistory"])
                Ref.pack(padx=30, anchor="w")

                Ref = IncrementSlider(CSettings, (0.1, 1), Title="Delay (Seconds) after last key pressed to check", StartValue = self.Settings["C++"]["Type"]["DelayBetweenCharacters"], IncrementValue = 0.05, OnChangeFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Type/DelayBetweenCharacters")], SnapTo = [0.25, 0.5], SnapThreashold = 0.05, bg="#121212")
                Ref.pack(padx=30, pady=3)
            
        tk.Label(CSettings, text="", bg="#121212").pack(padx=210)

        CSettings.pack()

        #Blueprints

        BPSettings = tk.Canvas( self.Root, width=400, height=50, bg="#121212", highlightthickness=0)
        Ref = tk.Label(BPSettings, text="Blueprints", font=("Yu Gothic Bold", 30), foreground="#FFF", bg="#121212")
        Ref.pack(padx=10)

        Ref = ToggleSwitch(BPSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "Blueprints/Enabled")], bg="#121212", StartValue=self.Settings["Blueprints"]["Enabled"])
        Ref.place(relx=1, y=10, anchor="ne")

        Ref = ToggleSwitch(BPSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "Blueprints/Enabled")], bg="#121212", StartValue=self.Settings["Blueprints"]["Enabled"])
        Ref.place(relx=1, y=10, anchor="ne")

        if (self.Settings["Blueprints"]["Enabled"]):
            Ref = tk.Label(BPSettings, text="Bites", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            Ref.pack(padx=10, anchor="w")

            Ref = ToggleSwitch(BPSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "Blueprints/Bites/Enabled")], bg="#121212", StartValue=self.Settings["Blueprints"]["Bites"]["Enabled"])
            Ref.pack(padx=30, anchor="w")

            Ref = tk.Label(BPSettings, text="Moodifier", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
            Ref.pack(padx=10, anchor="w")

            Ref = ToggleSwitch(BPSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "Blueprints/Moodifier/Enabled")], bg="#121212", StartValue=self.Settings["Blueprints"]["Moodifier"]["Enabled"])
            Ref.pack(padx=30, anchor="w")

        tk.Label(BPSettings, text="", bg="#121212").pack(padx=210)

        BPSettings.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg="#2D2D2D"

    SettingsPane(root, 400, 50).pack()

    root.mainloop()