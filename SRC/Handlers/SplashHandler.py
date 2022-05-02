import tkinter as tk
from tkinter.ttk import Progressbar
import webbrowser
import pyperclip
import os
from PIL import ImageTk, Image
import random

class SplashScreen():

    SplashText = [
        "Mooing Cows...",
        "Loading Unreal Assets..."
    ]

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window["bg"] = "#121212"
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

        A = tk.Label(text="", font=("Yu Gothic", 10), bg="#121212")
        A.pack()

        img = ImageTk.PhotoImage(Image.open(SplashScreen.DirectoryAbove + "/Image/Logo/Logo_DarkBG.png").resize((200, 200), Image.ANTIALIAS))
        self.IntroImage = tk.Label(self.window, image=img, borderwidth=0)
        self.IntroImage.image = img
        self.IntroImage.pack()

        self.HeaderLabel = tk.Label(master=self.window, text="Unrealify", bg="#121212", font=("Yu Gothic Bold", 20), foreground="white")
        self.HeaderLabel.pack()

        self.CreditLabel = tk.Label(master=self.window, text="by Cowland Game Studios", bg="#121212", font=("Yu Gothic", 10), foreground="white")
        self.CreditLabel.place(relx=0.5, rely=0.89, anchor="center")

        self.SplashLabel = tk.Label(master=self.window, text=random.choice(SplashScreen.SplashText), bg="#121212", font=("Yu Gothic Bold", 7), foreground="white")
        self.SplashLabel.place(x=1, rely=0.96, anchor="w")

        self.ProgressBarFormatter = tk.Frame(self.window, bg="#5AA17F")
        self.ProgressBarFormatter.place(relx = 0.5, rely = 0.99, width=300, height=5, anchor="center")

        self.ProgressBar = tk.Frame(self.window, bg="#92DDC8")
        self.ProgressBar.place(relx = 0, rely = 0.99, width=10, height=5, anchor="w")

        self.AllWidgets = [self.IntroImage, self.HeaderLabel, self.ProgressBar, self.CreditLabel, self.ProgressBarFormatter, A, self.SplashLabel]

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
    a = SplashScreen()
    a.Update(10)
    a.Loop()