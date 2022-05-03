import tkinter as tk
import os
from PIL import ImageTk, Image
import threading
import webbrowser

if __name__ == "__main__":
  from SettingsHandler import YamlParser
  from UIComponents.IncrementSlider import IncrementSlider
  from UIComponents.ToggleSwitch import ToggleSwitch
  #from KeyStrokeWrapper import KeyStrokeWrapper
else:
  from Handlers.SettingsHandler import YamlParser
  from Handlers.KeyStrokeWrapper import KeyStrokeWrapper
  from Handlers.UIComponents.IncrementSlider import IncrementSlider
  from Handlers.UIComponents.ToggleSwitch import ToggleSwitch

class App():

  DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
  def __init__(self, SplashRef, AllCPPClasses):
    self.window = SplashRef
    self.Width = 720
    self.Height = 512
    self.AllWidgets = []

    #Setup window
    self.window.geometry(f"{self.Width}x{self.Height}")
    self.window["bg"] = "#121212"
    self.window.title("Unrealify by Cowland Game Studios")
    self.window.resizable(False, False)
    self.window.focus_force()
    self.window.iconphoto(False, ImageTk.PhotoImage(file = App.DirectoryAbove + "/Image/Logo/Icon.png"))

    #Load images
    self.CowImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Logo/Logo.png").resize((100, 100), Image.ANTIALIAS))
    self.CowImageDark = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Logo/Logo_DarkBG.png").resize((200, 200), Image.ANTIALIAS))
    self.CPPImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Cpp.png").resize((125, 37), Image.ANTIALIAS))
    self.BlueprintImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Blueprint.png").resize((125, 37), Image.ANTIALIAS))
    self.SettingImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Settings.png").resize((30, 30), Image.ANTIALIAS))
    self.InfoImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Info.png").resize((30, 30), Image.ANTIALIAS))

    self.CPPImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Cpp_Held.png").resize((125, 37), Image.ANTIALIAS))
    self.BlueprintImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Blueprint_Held.png").resize((125, 37), Image.ANTIALIAS))
    self.SettingImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Settings_Held.png").resize((30, 30), Image.ANTIALIAS))
    self.InfoImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Info_Held.png").resize((30, 30), Image.ANTIALIAS))

    #Socials
    self.YoutubeImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Socials/Socials_Youtube.png").resize((100, 100), Image.ANTIALIAS))
    self.ItchImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Socials/Socials_Itch.png").resize((100, 100), Image.ANTIALIAS))
    self.GithubImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Socials/Socials_Github.png").resize((100, 100), Image.ANTIALIAS))

    #Handlers
    self.SettingsHandler = YamlParser(App.DirectoryAbove + "/Configuration.yaml")
    self.Settings = self.SettingsHandler.GetAllData()

    #Startup windows & processes
    self.KeyHandler = None #KeyStrokeWrapper(AllCPPClasses) #import isues
    self.__CPPKeyHandler(AllCPPClasses)
    self.SetUpSideBar()
    self.__ContinueLastLeft()

    #Last
    self.window.focus_force()

    self.window.protocol("WM_DELETE_WINDOW", self.Destroy)

  def __CPPKeyHandler(self, AllCPPClasses):
    
    if (not self.Settings["C++"]["Type"]["Enabled"] or self.KeyHandler is None):
      return
    
    self.KeyHandler.Start()

  def __ContinueLastLeft(self):
    if (self.Settings["App"]["LastLeft"] == "Blueprints"):
      self.SetUpBlueprintsMenu()
    elif (self.Settings["App"]["LastLeft"] == "C++"):
      self.SetUpCPPMenu()
    elif (self.Settings["App"]["LastLeft"] == "Settings"):
      self.SetUpSettingsMenu()
    elif (self.Settings["App"]["LastLeft"] == "Dashboard"):
      self.SetUpDashboardMenu()
    elif (self.Settings["App"]["LastLeft"] == "Info"):
      self.SetUpInformationMenu()
    else:
      self.SetUpUI()

  def Loop(self):
    self.window.mainloop()

  def Destroy(self):
    if self.KeyHandler:
      self.KeyHandler.Stop()

    self.window.destroy()
    
  def SetUpSideBar(self):
    self.SideBar = tk.Frame(width=125, height=self.Height, bg="#2D2D2D")
    self.SideBar.pack(side=tk.LEFT, fill="y")

    #using tklabels because buttons shift down
    self.CowButton = tk.Label(self.SideBar, image=self.CowImage, relief=tk.FLAT, borderwidth=0)
    self.CowButton.bind("<1>", lambda x: [self.SetUpDashboardMenu()])
    self.CowButton.pack(pady=10)

    self.CPPButton = tk.Label(self.SideBar, image=self.CPPImage, relief=tk.FLAT, borderwidth=0)
    self.CPPButton.bind("<1>", lambda x: [self.SetUpCPPMenu()])
    self.CPPButton.pack(pady=5)

    self.BlueprintButton = tk.Label(self.SideBar, image=self.BlueprintImage, relief=tk.FLAT, borderwidth=0)
    self.BlueprintButton.bind("<1>", lambda x: [self.SetUpBlueprintsMenu()])
    self.BlueprintButton.pack(pady=5)

    self.SettingButton = tk.Label(self.SideBar, image=self.SettingImage, relief=tk.FLAT, borderwidth=0)
    self.SettingButton.bind("<1>", lambda x: [self.SetUpSettingsMenu()])
    self.SettingButton.place(x=0, y=self.Height, anchor="sw")

    self.InfoButton = tk.Label(self.SideBar, image=self.InfoImage, relief=tk.FLAT, borderwidth=0)
    self.InfoButton.bind("<1>", lambda x: [self.SetUpInformationMenu()])
    self.InfoButton.place(x=125, y=self.Height, anchor="se")
  
  def ResetSideBar(self):
    self.CowButton["image"] = self.CowImage
    self.CPPButton["image"] = self.CPPImage
    self.BlueprintButton["image"] = self.BlueprintImage
    self.SettingButton["image"] = self.SettingImage
    self.InfoButton["image"] = self.InfoImage

  def Clear(self):
    self.window.overrideredirect(False)

    for Widget in self.AllWidgets:
      if Widget is not None:
        Widget.destroy()
    self.AllWidgets = []

    self.ResetSideBar()

  def __AddPadding(self, Parent, Size = 3):
    tk.Label(Parent, text="", font=("Yu Gothic", Size), bg="#121212").pack()

  def SetUpSettingsMenu(self):
    ContentPane = self.SetUpUI()
    self.SettingButton["image"] = self.SettingImageHeld
    self.SettingsHandler.Write("App/LastLeft", "Settings")

    BackgroundText = tk.Label(ContentPane, text="Settings", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")

    self.Settings = self.SettingsHandler.GetAllData()

    def SettingsWriteSlider(Value, Dir):
      #print(f"Writing to {Dir} at {Value}")
      self.SettingsHandler.Write(Dir, Value)

    CSettings = tk.Canvas(ContentPane, width=400, height=50, bg="#121212", highlightthickness=0)
    Ref = tk.Label(CSettings, text="C++", font=("Yu Gothic Bold", 30), foreground="#FFF", bg="#121212")
    Ref.pack(padx=10)

    Ref = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Enabled"])
    Ref.place(relx=1, y=10, anchor="ne")

    if (self.Settings["C++"]["Enabled"]):
      Ref = tk.Label(CSettings, text="Bites", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
      Ref.pack(padx=10, anchor="w")

      Ref = ToggleSwitch(CSettings, Title="Enabled?", OnToggleFuncRef = lambda x : [SettingsWriteSlider(x, "C++/Bites/Enabled")], bg="#121212", StartValue=self.Settings["C++"]["Bites"]["Enabled"])
      Ref.pack(padx=30, anchor="w")

      Ref = tk.Label(CSettings, text="Popups", font=("Yu Gothic", 15), foreground="#FFF", bg="#121212")
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
    
    CSettings.pack()

    BPSettings = tk.Canvas(ContentPane, width=400, height=50, bg="#121212", highlightthickness=0)
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

    BPSettings.pack()

  def SetUpBlueprintsMenu(self):
    ContentPane = self.SetUpUI()
    self.BlueprintButton["image"] = self.BlueprintImageHeld
    self.SettingsHandler.Write("App/LastLeft", "Blueprints")
    
    BackgroundText = tk.Label(ContentPane, text="Blueprints", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")

  def SetUpCPPMenu(self):
    ContentPane = self.SetUpUI()
    self.CPPButton["image"] = self.CPPImageHeld
    self.SettingsHandler.Write("App/LastLeft", "C++")
    
    BackgroundText = tk.Label(ContentPane, text="C++", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")

  def SetUpDashboardMenu(self):
    ContentPane = self.SetUpUI()
    self.SettingsHandler.Write("App/LastLeft", "Dashboard")
    
    BackgroundText = tk.Label(ContentPane, text="Dashbored", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")
  
  def SetUpInformationMenu(self):
    ContentPane = self.SetUpUI()
    self.InfoButton["image"] = self.InfoImageHeld
    self.SettingsHandler.Write("App/LastLeft", "Info")

    BackgroundText = tk.Label(ContentPane, text="Info", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")

    InfoIcon = tk.Label(ContentPane, image=self.CowImageDark, relief=tk.FLAT, borderwidth=0)
    InfoIcon.place(relx=0.5, y=20, anchor="n")

    Title = tk.Label(ContentPane, text="Unrealify", font=("Yu Gothic Bold", 40), bg="#121212", foreground="#FFF")
    Title.place(relx=0.5, rely=0.51, anchor="center")

    Version = tk.Label(ContentPane, text=self.Settings["App"]["Version"], font=("Yu Gothic Bold", 12), bg="#121212", foreground="#FFF")
    Version.place(relx=0.725, rely=0.505, anchor="n")

    Sub = tk.Label(ContentPane, text="Streamline", font=("Yu Gothic Bold", 12), bg="#121212", foreground="#FFF")
    Sub.place(relx=0.375, rely=0.56, anchor="n")

    Sub = tk.Label(ContentPane, text="your UE5 experiance", font=("Yu Gothic", 12), bg="#121212", foreground="#FFF")
    Sub.place(relx=0.45, rely=0.56, anchor="nw")

    # Credit = tk.Label(ContentPane, text="Cowland Game Studios", font=("Yu Gothic", 12), bg="#121212", foreground="#FFF")
    # Credit.place(relx=0.5, rely=0.9, anchor="s")

    Socials_Youtube = tk.Label(ContentPane, image=self.YoutubeImage, relief=tk.FLAT, borderwidth=0)
    Socials_Youtube.bind("<1>", lambda x: [webbrowser.open("https://www.youtube.com/channel/UCMcfj1Phz3G9xH0fUF_o9Jw")])
    Socials_Youtube.place(relx=0.7, rely=0.725, anchor="center")

    Socials_Itch = tk.Label(ContentPane, image=self.ItchImage, relief=tk.FLAT, borderwidth=0)
    Socials_Itch.bind("<1>", lambda x: [webbrowser.open("https://cowlandgamestudios.itch.io/")])
    Socials_Itch.place(relx=0.5, rely=0.725, anchor="center")

    Socials_Github = tk.Label(ContentPane, image=self.GithubImage, relief=tk.FLAT, borderwidth=0)
    Socials_Github.bind("<1>", lambda x: [webbrowser.open("https://github.com/Cowland-Game-Studios/Unrealify")])
    Socials_Github.place(relx=0.3, rely=0.725, anchor="center")

  def SetUpUI(self):
    self.Clear()

    ContentPane = tk.Canvas(width=self.Width - 125, height=self.Height, bg="#121212", highlightthickness=0)
    ContentPane.place(x = 125, y = 0, anchor = "nw")

    self.AllWidgets.append(ContentPane)

    return ContentPane

if __name__ == "__main__":
  a = App(tk.Tk(), None).Loop()