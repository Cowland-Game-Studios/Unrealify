import tkinter as tk
from tkinter.ttk import Progressbar
import webbrowser
import pyperclip
import os
import sys
from PIL import ImageTk, Image
import random

from Handlers.UIComponents.Usefuls import Usefuls

class SplashScreen():

    SplashText = [
        "Mooing Cows...",
        "Loading Unreal Assets...",
        "Larry sucks at COD:Mobile..."
    ]

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window["bg"] = Usefuls.LightBlack
        self.window.title("Unrealify by Cowland Game Studios")
        self.window.resizable(False, False)
        self.window.focus_force()

        self.SetUpUI()
        self.window.focus_force()
        if sys.platform != "darwin":
            self.window.overrideredirect(True)
        #self.window.wm_attributes("-type", "splash")
        self.window.eval("tk::PlaceWindow . center")

    def Loop(self):
        self.window.mainloop()

    def SetUpUI(self) -> None:

        A = tk.Label(text="", font=(Usefuls.Font, 10), bg=Usefuls.LightBlack)
        A.pack()

        #load images
        CowImage = ImageTk.PhotoImage(Image.open(SplashScreen.DirectoryAbove + "/Image/Logo/Logo_DarkBG.png").resize((200, 200), Image.ANTIALIAS))
        SpinnerImage = ImageTk.PhotoImage(Image.open(SplashScreen.DirectoryAbove + "/Image/Splash/Spinner.png").resize((20, 20), Image.ANTIALIAS))

        self.IntroImage = tk.Label(self.window, image=CowImage, borderwidth=0, background=Usefuls.LightBlack)
        self.IntroImage.image = CowImage
        self.IntroImage.pack()

        self.HeaderLabel = tk.Label(master=self.window, text="Unrealify", bg=Usefuls.LightBlack, font=(Usefuls.FontLargest, 20), foreground=Usefuls.White)
        self.HeaderLabel.pack()

        self.CreditLabel = tk.Label(master=self.window, text="by Cowland Game Studios", bg=Usefuls.LightBlack, font=(Usefuls.FontLargest, 10), foreground=Usefuls.White)
        self.CreditLabel.place(relx=0.5, rely=0.89, anchor="center")

        self.SplashLabel = tk.Label(master=self.window, text=random.choice(SplashScreen.SplashText), bg=Usefuls.LightBlack, font=(Usefuls.FontLargest, 7), foreground=Usefuls.White)
        self.SplashLabel.place(x=1, rely=0.955, anchor="w")

        self.ProgressBarFormatter = tk.Frame(self.window, bg=Usefuls.DarkMint)
        self.ProgressBarFormatter.place(relx = 0.5, rely = 0.99, width=300, height=5, anchor="center")

        self.ProgressBar = tk.Frame(self.window, bg=Usefuls.Mint)
        self.ProgressBar.place(relx = 0, rely = 0.99, width=10, height=5, anchor="w")

        self.SpinImage = tk.Label(self.window, image=SpinnerImage, borderwidth=0, background=Usefuls.LightBlack)
        self.SpinImage.image = SpinnerImage
        self.SpinImage.place(relx=0.99, rely=0.97, anchor="se")

        self.AllWidgets = [self.IntroImage, self.HeaderLabel, self.ProgressBar, self.CreditLabel, self.ProgressBarFormatter, A, self.SplashLabel, self.SpinImage]

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