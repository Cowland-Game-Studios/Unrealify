import tkinter as tk
import os
from PIL import ImageTk, Image
import threading

if __name__ == "__main__":
  from SettingsHandler import YamlParser
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
    self.CowIcon = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Logo.png").resize((50, 50), Image.ANTIALIAS))
    self.CPPImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Cpp.png").resize((50, 50), Image.ANTIALIAS))
    self.BlueprintImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Blueprint.png").resize((50, 50), Image.ANTIALIAS))
    self.SettingImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Settings.png").resize((50, 50), Image.ANTIALIAS))

    self.CPPImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Cpp_Held.png").resize((50, 50), Image.ANTIALIAS))
    self.BlueprintImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Blueprint_Held.png").resize((50, 50), Image.ANTIALIAS))
    self.SettingImageHeld = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Settings_Held.png").resize((50, 50), Image.ANTIALIAS))

    #Handlers
    self.SettingsHandler = YamlParser(App.DirectoryAbove + "/Configuration.yaml")
    self.Settings = self.SettingsHandler.GetAllData()

    #Startup windows & processes
    self.__CPPKeyHandler(AllCPPClasses)
    self.__ContinueLastLeft()

    #Last
    self.window.focus_force()

  def __CPPKeyHandler(self, AllCPPClasses):
    self.KeyHandler = None
    
    if (not self.Settings["C++"]["Type"]["Enabled"] or __name__ == "__main__"):
      return
    
    self.KeyHandler = KeyStrokeWrapper(AllCPPClasses)
    self.KeyHandler.Start()

  def __ContinueLastLeft(self):
    if (self.Settings["App"]["LastLeft"] == "Blueprints"):
      self.SetUpBlueprintsMenu()
    elif (self.Settings["App"]["LastLeft"] == "C++"):
      self.SetUpCPPMenu()
    elif (self.Settings["App"]["LastLeft"] == "Settings"):
      self.SetUpSettingsMenu()
    else:
      self.SetUpUI()

  def Loop(self):
    self.window.mainloop()
    
  def SetUpSideBar(self):
    self.SideBar = tk.Frame(width=125, height=self.Height, bg="#2D2D2D")
    self.SideBar.place(x = 0, y = 0, anchor = "nw")

    #using tklabels because buttons shift down
    self.CPPButton = tk.Label(self.SideBar, image=self.CPPImage, relief=tk.FLAT, borderwidth=0)
    self.CPPButton.bind("<1>", lambda x: [self.SetUpCPPMenu()])
    self.CPPButton.place(x = 5, y = 10, anchor = "nw", width=50, height=50)

    self.BlueprintButton = tk.Label(self.SideBar, image=self.BlueprintImage, relief=tk.FLAT, borderwidth=0)
    self.BlueprintButton.bind("<1>", lambda x: [self.SetUpBlueprintsMenu()])
    self.BlueprintButton.place(x = 5, y = 70, anchor = "nw", width=50, height=50)

    self.SettingButton = tk.Label(self.SideBar, image=self.SettingImage, relief=tk.FLAT, borderwidth=0)
    self.SettingButton.bind("<1>", lambda x: [self.SetUpSettingsMenu()])
    self.SettingButton.place(x = 5, y = self.Height - 5, anchor = "sw", width=50, height=50)

  def Clear(self):
    self.window.overrideredirect(False)

    for Widget in self.AllWidgets:
      if Widget is not None:
        Widget.destroy()
    self.AllWidgets = []

  def __AddPadding(self, Parent, Size = 5):
    tk.Label(Parent, text="", font=("Helvetica", Size), bg="#121212").pack()

  def SetUpSettingsMenu(self):
    ContentPane = self.SetUpUI()
    self.SettingButton["image"] = self.SettingImageHeld
    self.SettingsHandler.Write("App/LastLeft", "Settings")

    self.__AddPadding(ContentPane)

    Header = tk.Label(ContentPane, text="Settings", font=("Helvetica", 20), bg="#121212", foreground="#FFF")
    Header.pack()

  def SetUpBlueprintsMenu(self):
    ContentPane = self.SetUpUI()
    self.BlueprintButton["image"] = self.BlueprintImageHeld
    self.SettingsHandler.Write("App/LastLeft", "Blueprints")

    self.__AddPadding(ContentPane)
    
    Header = tk.Label(ContentPane, text="Blueprints", font=("Helvetica", 20), bg="#121212", foreground="#FFF")
    Header.pack()

  def SetUpCPPMenu(self):
    ContentPane = self.SetUpUI()
    self.CPPButton["image"] = self.CPPImageHeld
    self.SettingsHandler.Write("App/LastLeft", "C++")

    self.__AddPadding(ContentPane)
    
    Header = tk.Label(ContentPane, text="C++", font=("Helvetica", 20), bg="#121212", foreground="#FFF")
    Header.pack()

  def SetUpUI(self):
    self.Clear()
    self.SetUpSideBar()

    ContentPane = tk.Frame(width=self.Width - 75, height=self.Height, bg="#121212")
    ContentPane.place(x = 75, y = 0, anchor = "nw")

    self.AllWidgets.append(ContentPane)

    return ContentPane

if __name__ == "__main__":
  import BeautifulSoupHandler
  a = App(tk.Tk(), BeautifulSoupHandler.GetAllCPPClasses()).Loop()