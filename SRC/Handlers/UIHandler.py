import tkinter as tk
import os
from PIL import ImageTk, Image
import threading
import webbrowser

if __name__ == "__main__":
  from SettingsHandler import YamlParser
  from KeyStrokeWrapper import KeyStrokeWrapper
else:
  from Handlers.SettingsHandler import YamlParser
  from Handlers.KeyStrokeWrapper import KeyStrokeWrapper

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
    self.window.iconphoto(False, ImageTk.PhotoImage(file = App.DirectoryAbove + "/Image/Icon.png"))

    #Load images
    self.CowImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Logo.png").resize((100, 100), Image.ANTIALIAS))
    self.CPPImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Cpp.png").resize((125, 25), Image.ANTIALIAS))
    self.BlueprintImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Blueprint.png").resize((125, 25), Image.ANTIALIAS))
    self.SettingImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Settings.png").resize((30, 30), Image.ANTIALIAS))
    self.InfoImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Info.png").resize((30, 30), Image.ANTIALIAS))

    self.CPPImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Cpp_Held.png").resize((125, 25), Image.ANTIALIAS))
    self.BlueprintImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Blueprint_Held.png").resize((125, 25), Image.ANTIALIAS))
    self.SettingImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Settings_Held.png").resize((30, 30), Image.ANTIALIAS))
    self.InfoImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Info_Held.png").resize((30, 30), Image.ANTIALIAS))

    #Handlers
    self.SettingsHandler = YamlParser(App.DirectoryAbove + "/Configuration.yaml")
    self.Settings = self.SettingsHandler.GetAllData()

    #Startup windows & processes
    self.KeyHandler = KeyStrokeWrapper(AllCPPClasses) #import isues
    self.__CPPKeyHandler(AllCPPClasses)
    self.SetUpSideBar()
    self.__ContinueLastLeft()

    #Last
    self.window.focus_force()

    self.window.protocol("WM_DELETE_WINDOW", self.Destroy)

  def __CPPKeyHandler(self, AllCPPClasses):
    
    if (not self.Settings["C++"]["Type"]["Enabled"]):
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
    self.InfoButton.bind("<1>", lambda x: [webbrowser.open("https://cowlandgames.studio/unrealify"), self.ResetSideBar()])
    self.InfoButton.place(x=125, y=self.Height, anchor="se")

    #self.AllWidgets.append(self.SideBar)
  
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

    Header = tk.Label(ContentPane, text="Settings", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    Header.place(rely=1, x = 10, anchor="sw")

  def SetUpBlueprintsMenu(self):
    ContentPane = self.SetUpUI()
    self.BlueprintButton["image"] = self.BlueprintImageHeld
    self.SettingsHandler.Write("App/LastLeft", "Blueprints")
    
    Header = tk.Label(ContentPane, text="Blueprints", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    Header.place(rely=1, x = 10, anchor="sw")

  def SetUpCPPMenu(self):
    ContentPane = self.SetUpUI()
    self.CPPButton["image"] = self.CPPImageHeld
    self.SettingsHandler.Write("App/LastLeft", "C++")
    
    Header = tk.Label(ContentPane, text="C++", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    Header.place(rely=1, x = 10, anchor="sw")

  def SetUpDashboardMenu(self):
    ContentPane = self.SetUpUI()
    self.SettingsHandler.Write("App/LastLeft", "Dashboard")
    
    Header = tk.Label(ContentPane, text="Dashbored", font=("Yu Gothic Bold", 50), bg="#121212", foreground="#2D2D2D")
    Header.place(rely=1, x = 10, anchor="sw")

  def SetUpUI(self):
    self.Clear()

    ContentPane = tk.Canvas(width=self.Width - 125, height=self.Height, bg="#121212", highlightthickness=0)
    ContentPane.place(x = 125, y = 0, anchor = "nw")

    self.AllWidgets.append(ContentPane)

    return ContentPane

if __name__ == "__main__":
  a = App(tk.Tk(), None).Loop()