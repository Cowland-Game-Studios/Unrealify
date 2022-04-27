import tkinter as tk
from Handlers.PopUpHandler import PopUp
from tkinter.ttk import Progressbar
import webbrowser
import pyperclip
import os

class Progress():

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
    def __init__(self):
        self.SetUpUI()
        self.window.focus_force()

    def Loop(self):
        self.window.mainloop()

    def SetUpUI(self) -> None:
        self.window = tk.Tk()
        self.window.geometry("300x100")
        self.window["bg"] = "#292929"
        self.window.title("Unreal Import Assistant")
        self.window.resizable(False, False)

        self.window.iconphoto(True, tk.PhotoImage(file = PopUp.DirectoryAbove + "/Image/Logo.png"))

        self.HeaderLabel = tk.Label(master=self.window, text="Loading Unreal Classes", bg="#292929", font=("Courier", 15), foreground="white")
        self.HeaderLabel.pack()
        
        self.Bar = Progressbar(self.window, length = 100)
        self.Bar.place(relx = 0.5, rely = 0.5, width = 280, height = 25, anchor="center")

    def Update(self, Value):
        if Value != self.Bar["value"]:
            self.Bar["value"] = Value
        
        if Value == 100:
            self.window.destroy()
            

if __name__ == "__main__":
    a = Progress()