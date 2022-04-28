import tkinter as tk
from tkinter.ttk import Progressbar
import webbrowser
import pyperclip
import os
from PIL import ImageTk, Image

class Progress():

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
    def __init__(self):
        self.SetUpUI()
        self.window.focus_force()
        self.window.overrideredirect(True)
        self.window.eval("tk::PlaceWindow . center")

    def Loop(self):
        self.window.mainloop()

    def SetUpUI(self) -> None:
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window["bg"] = "#292929"
        self.window.title("Unreal Import Assistant")
        self.window.resizable(False, False)
        self.window.focus_force()

        tk.Label(text="", font=("Helvetica", 5), bg="#292929").pack()

        img = ImageTk.PhotoImage(Image.open(Progress.DirectoryAbove + "/Image/Splash.png").resize((200, 200), Image.ANTIALIAS))
        self.IntroImage = tk.Label(self.window, image=img, borderwidth=0)
        self.IntroImage.image = img
        self.IntroImage.pack()

        tk.Label(text="", font=("Helvetica", 5), bg="#292929").pack()

        self.HeaderLabel = tk.Label(master=self.window, text="Unreal Coding Assistant", bg="#292929", font=("Helvetica", 15), foreground="white")
        self.HeaderLabel.pack()

        self.CopyrightLabel = tk.Label(master=self.window, text="Cowland Game Studios", bg="#292929", font=("Helvetica", 10), foreground="white")
        self.CopyrightLabel.pack()

        tk.Label(text="", font=("Helvetica", 30), bg="#292929").pack()
        
        self.Bar = Progressbar(self.window, length = 100)
        self.Bar.place(relx = 0.5, rely = 0.975, width = 400, height = 25, anchor="center")

        ProgressBarFormatter = tk.Frame(width=self.Width, height=self.Height, bg="#292929")

    def Update(self, Value):
        if Value != self.Bar["value"]:
            self.Bar["value"] = Value
        
        if Value > 100:
            #self.Bar.destroy()
            #self.HeaderLabel["text"] = "Loading Success! :)"
            #self.CopyrightLabel["text"] = "The application will now track what you type."
            #self.CopyrightLabel["font"] = ("Helvetica", 7)
            #self.LinkButton = tk.Button(master=self.window, text="Start Tracking!", command=lambda: [self.window.destroy()], bg="#0070e0", foreground="white", borderwidth=0, font=("Helvetica", 10))
            #self.LinkButton.place(relx=0.5, rely=1, width=300, height=20, anchor="s")
            self.window.destroy()

if __name__ == "__main__":
    a = Progress()
    a.Update(40)
    a.Loop()