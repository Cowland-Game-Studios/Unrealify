import tkinter as tk
import os
from PIL import ImageTk, Image

class App():

  DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
  def __init__(self):
    self.window = tk.Tk()
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
    
    self.SetUpUI()
    self.window.focus_force()

  def Loop(self):
    self.window.mainloop()
    
  def SetUpSideBar(self):
    self.SideBar = tk.Frame(width=60, height=self.Height, bg="#585858")
    self.SideBar.place(x = 0, y = 0, anchor = "nw")

    self.CPPButton = tk.Button(self.SideBar, image=self.CPPImage, highlightbackground="#585858", borderwidth=0)
    self.CPPButton.place(x = 5, y = 10, anchor = "nw", width=50, height=50)

    self.BlueprintButton = tk.Button(self.SideBar, image=self.BlueprintImage, highlightbackground="#585858", borderwidth=0)
    self.BlueprintButton.place(x = 5, y = 70, anchor = "nw", width=50, height=50)

    self.SettingButton = tk.Button(self.SideBar, image=self.SettingImage, highlightbackground="#585858", borderwidth=0)
    self.SettingButton.place(x = 5, y = self.Height - 5, anchor = "sw", width=50, height=50)

  def SetUpUI(self):
    self.SetUpSideBar()

    self.ContentPane = tk.Frame(width=self.Width, height=self.Height, bg="#292929")
    self.ContentPane.place(x = 75, y = 0, anchor = "nw")

if __name__ == "__main__":
  a = App().Loop()