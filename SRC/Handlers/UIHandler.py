import tkinter as tk
import os
from PIL import ImageTk, Image
import threading
import webbrowser

if __name__ == "__main__":
  from SettingsHandler import YamlParser
  #from KeyStrokeWrapper import KeyStrokeWrapper
  from UI.SettingsPane import SettingsPane
  from UI.InfoPane import InfoPane
  from UIComponents.TransitionalButton import TransitionalButton
else:
  from Handlers.SettingsHandler import YamlParser
  from Handlers.KeyStrokeWrapper import KeyStrokeWrapper
  from Handlers.UIComponents.IncrementSlider import IncrementSlider
  from Handlers.UIComponents.ToggleSwitch import ToggleSwitch
  from Handlers.UI.SettingsPane import SettingsPane
  from Handlers.UI.InfoPane import InfoPane

class App():

  DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
  def __init__(self, SplashRef, AllCPPClasses):
    self.window = SplashRef
    self.Width = 720
    self.Height = 512
    self.AllWidgets = []
    self.IsAnimating = False

    #Setup window
    self.window.geometry(f"{self.Width}x{self.Height}")
    self.window["bg"] = "#121212"
    self.window.title("Unrealify by Cowland Game Studios")
    self.window.resizable(False, False)
    self.window.focus_force()
    self.window.iconphoto(False, ImageTk.PhotoImage(file = App.DirectoryAbove + "/Image/Logo/Icon.png"))

    #Load images
    self.CowImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Logo/Logo.png").resize((100, 100), Image.ANTIALIAS))
    self.CPPImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Cpp.png").resize((125, 37), Image.ANTIALIAS))
    self.BlueprintImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Blueprint.png").resize((125, 37), Image.ANTIALIAS))
    self.SettingImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Settings.png").resize((30, 30), Image.ANTIALIAS))
    self.InfoImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Info.png").resize((30, 30), Image.ANTIALIAS))

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

    self.CPPButton = TransitionalButton(self.SideBar, OnClickFuncRef=self.SetUpCPPMenu, OverlayImage=self.CPPImage)
    self.CPPButton.pack(pady=5)

    self.BlueprintButton = TransitionalButton(self.SideBar, OnClickFuncRef=self.SetUpBlueprintsMenu, OverlayImage=self.BlueprintImage)
    self.BlueprintButton.pack(pady=5)

    self.SettingButton = TransitionalButton(self.SideBar, Mode="BL", OnClickFuncRef=self.SetUpSettingsMenu, OverlayImage=self.SettingImage)
    self.SettingButton.place(x=0, y=self.Height, anchor="sw")

    self.InfoButton = TransitionalButton(self.SideBar, Mode="BR", OnClickFuncRef=self.SetUpInformationMenu, OverlayImage=self.InfoImage)
    self.InfoButton.place(x=125, y=self.Height, anchor="se")

  def SetNotAnimating(self):
    self.IsAnimating = False
  
  def ResetSideBar(self, SkipAnimations=False):

    if self.IsAnimating:
      return

    self.CowButton["image"] = self.CowImage
    self.CPPButton.PlayAnimation(False, 0, self.SetNotAnimating)
    self.BlueprintButton.PlayAnimation(False, 0, self.SetNotAnimating)
    self.SettingButton.PlayAnimation(False, 0, self.SetNotAnimating)
    self.InfoButton.PlayAnimation(False, 0, self.SetNotAnimating)
    self.IsAnimating = True

  def Clear(self, SkipAnimations=False):
    self.window.overrideredirect(False)

    for Widget in self.AllWidgets:
      if Widget is not None:
        Widget.destroy()
    self.AllWidgets = []

    self.ResetSideBar(SkipAnimations)

  def __AddPadding(self, Parent, Size = 3):
    tk.Label(Parent, text="", font=("Yu Gothic", Size), bg="#121212").pack()

  def SetUpSettingsMenu(self):
    self.SettingButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()

    self.SettingsHandler.Write("App/LastLeft", "Settings")

    BackgroundText = tk.Label(ContentPane, text="Settings", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")

    SettingsMenu = SettingsPane(ContentPane, self.SettingsHandler)
    SettingsMenu.pack()

    self.AllWidgets.append(
      ContentPane
    )

  def SetUpBlueprintsMenu(self):
    self.BlueprintButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()
    
    self.SettingsHandler.Write("App/LastLeft", "Blueprints")
    
    BackgroundText = tk.Label(ContentPane, text="Blueprints", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")

  def SetUpCPPMenu(self):
    self.CPPButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()
    self.SettingsHandler.Write("App/LastLeft", "C++")
    
    BackgroundText = tk.Label(ContentPane, text="C++", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")
  
  def SetUpInformationMenu(self):
    self.InfoButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()
    
    self.SettingsHandler.Write("App/LastLeft", "Info")

    InfoMenu = InfoPane(ContentPane, self.SettingsHandler, 720-125, 512)
    InfoMenu.pack(fill="both")

    self.AllWidgets.append(
      ContentPane
    )

  def SetUpDashboardMenu(self):
    ContentPane = self.SetUpUI()
    self.SettingsHandler.Write("App/LastLeft", "Dashboard")
    
    BackgroundText = tk.Label(ContentPane, text="Dashbored", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    BackgroundText.place(rely=1, x = 10, anchor="sw")

  def SetUpUI(self):
    self.Clear()

    ContentPane = tk.Canvas(width=self.Width - 125, height=self.Height, bg="#121212", highlightthickness=0)
    ContentPane.place(x = 125, y = 0, anchor = "nw")

    self.AllWidgets.append(ContentPane)

    return ContentPane

if __name__ == "__main__":
  a = App(tk.Tk(), None).Loop()