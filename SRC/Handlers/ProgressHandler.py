import tkinter as tk
from tkinter.ttk import Progressbar
import webbrowser
import pyperclip
import os
from PIL import ImageTk, Image

class Progress():

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window["bg"] = "#2D2D2D"
        self.window.title("Unrealify by Cowland Game Studios")
        self.window.resizable(False, False)
        self.window.focus_force()

        self.SetUpUI()
        self.window.focus_force()
        self.window.overrideredirect(True)
        self.window.eval("tk::PlaceWindow . center")

    def Loop(self):
        self.window.mainloop()

    def SetUpUI(self) -> None:

        tk.Label(text="", font=("Yu Gothic", 10), bg="#2D2D2D").pack()

        img = ImageTk.PhotoImage(Image.open(Progress.DirectoryAbove + "/Image/Logo.png").resize((200, 200), Image.ANTIALIAS))
        self.IntroImage = tk.Label(self.window, image=img, borderwidth=0)
        self.IntroImage.image = img
        self.IntroImage.pack()

        self.HeaderLabel = tk.Label(master=self.window, text="Unrealify", bg="#2D2D2D", font=("Yu Gothic Bold", 20), foreground="white")
        self.HeaderLabel.pack()

        self.CopyrightLabel = tk.Label(master=self.window, text="by Cowland Game Studios", bg="#2D2D2D", font=("Yu Gothic", 10), foreground="white")
        self.CopyrightLabel.pack()

        tk.Label(text="", font=("Yu Gothic", 35), bg="#2D2D2D").pack()

        self.ProgressBarFormatter = tk.Frame(self.window, bg="#5AA17F")
        self.ProgressBarFormatter.place(relx = 0.5, rely = 0.99, width=300, height=5, anchor="center")

        self.ProgressBar = tk.Frame(self.window, bg="#92DDC8")
        self.ProgressBar.place(relx = 0, rely = 0.99, width=10, height=5, anchor="w")

        self.AllWidgets = [self.IntroImage, self.HeaderLabel, self.ProgressBar, self.CopyrightLabel, self.ProgressBarFormatter]

        self.Update(100)

    def Clear(self):
        for Widget in self.AllWidgets:
            if Widget is not None:
                Widget.destroy()
            self.AllWidgets = []

    def Update(self, Value):
        self.ProgressBar.place(relx = 0, rely = 0.99, width=Value / 100 * 300, height=5, anchor="w")
        
        if Value > 100:
            self.Clear()

if __name__ == "__main__":
    a = Progress()
    a.Update(10)
    a.Loop()