import tkinter as tk
import os
from PIL import ImageTk, Image

class App():

  DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
  def __init__(self, SplashRef):
    self.window = SplashRef
    self.Height = 300
    self.Width = 400
    self.window.geometry(f"{self.Width}x{self.Height}")
    self.window["bg"] = "#292929"
    self.window.title("Unreal Coding Assistant - Dashboard")
    self.window.resizable(False, False)
    self.window.focus_force()

    self.window.iconphoto(False, ImageTk.PhotoImage(file = App.DirectoryAbove + "/Image/Logo.png"))

    #Load images
    self.CPPImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Cpp.png").resize((50, 50), Image.ANTIALIAS))
    self.BlueprintImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Blueprint.png").resize((50, 50), Image.ANTIALIAS))
    self.SettingImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Settings.png").resize((50, 50), Image.ANTIALIAS))
    
    self.AllWidgets = []

    self.SetUpUI()
    self.SetUpSettings()
    #self.SetUpSelection()

    self.window.focus_force()

  def Loop(self):
    self.window.mainloop()

  def SetUpSelection(self):
    self.CPPButton = tk.Button(self.window, image=self.CPPImage, highlightbackground="#585858", borderwidth=0, command=lambda:[self.SetUpCPPMenu()])
    self.CPPButton.place(relx = 0.27, rely = 0.5, anchor = "center", width=150, height=150)
    self.AllWidgets.append(self.CPPButton)

    self.BlueprintButton = tk.Button(self.window, image=self.BlueprintImage, highlightbackground="#585858", borderwidth=0, command=lambda:[self.SetUpBlueprintsMenu()])
    self.BlueprintButton.place(relx = 0.73, rely = 0.5, anchor = "center", width=150, height=150)
    self.AllWidgets.append(self.BlueprintButton)
    
  def SetUpSideBar(self):
    self.SideBar = tk.Frame(width=60, height=self.Height, bg="#585858")
    self.SideBar.place(x = 0, y = 0, anchor = "nw")

    self.CPPButton = tk.Button(self.SideBar, image=self.CPPImage, highlightbackground="#585858", borderwidth=0)
    self.CPPButton.place(x = 5, y = 10, anchor = "nw", width=50, height=50)

    self.BlueprintButton = tk.Button(self.SideBar, image=self.BlueprintImage, highlightbackground="#585858", borderwidth=0)
    self.BlueprintButton.place(x = 5, y = 70, anchor = "nw", width=50, height=50)

    self.SettingButton = tk.Button(self.SideBar, image=self.SettingImage, highlightbackground="#585858", borderwidth=0)
    self.SettingButton.place(x = 5, y = self.Height - 5, anchor = "sw", width=50, height=50)

  def Clear(self):
    self.window.overrideredirect(False)

    for Widget in self.AllWidgets:
      if Widget is not None:
        Widget.destroy()
    self.AllWidgets = []

  def SetUpSettings(self):
    ContentPane = self.SetUpUI()
    pass

  def SetUpBlueprintsMenu(self):
    ContentPane = self.SetUpUI()
    pass

  def SetUpCPPMenu(self):
    ContentPane = self.SetUpUI()
    pass

  def SetUpUI(self):
    self.Clear()
    self.SetUpSideBar()

    ContentPane = tk.Frame(width=self.Width, height=self.Height, bg="#292929")
    ContentPane.place(x = 75, y = 0, anchor = "nw")

    self.AllWidgets.append(ContentPane)

    return ContentPane

if __name__ == "__main__":
  a = App().Loop()