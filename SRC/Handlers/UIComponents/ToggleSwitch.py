import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UIComponents.Usefuls import Usefuls

class ToggleSwitch(tk.Canvas):
    def __init__(self, Root, StartValue = False, OnToggleFuncRef = None, OnAnimDoneRef = None, Width=67, Height=50, Title="", bg=Usefuls.LightGrey):
        super().__init__(Root, width=Width, height=Height, bg=bg, borderwidth=0, highlightthickness=0)

        self.ToggledImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Toggle/ToggledBackground.png").resize((33, 15), Image.ANTIALIAS))
        self.UntoggledImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Toggle/UntoggledBackground.png").resize((33, 15), Image.ANTIALIAS))
        self.SwitchBallImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Toggle/SwitchBall.png").resize((15, 15), Image.ANTIALIAS))

        self.OnToggle = OnToggleFuncRef
        self.OnAnimDoneRef = OnAnimDoneRef
        self.Title = self.create_text(0, 0, text=Title, font=(Usefuls.FontAccented, 10), anchor="nw", fill=Usefuls.White)

        self.IsToggled = StartValue
        self.Cooldown = False

        self.SetUpUI()

    def SetUpUI(self):

        self.ToggleButton = self.create_image(0, 20, image=self.ToggledImage, anchor="nw")
        self.tag_bind(self.ToggleButton, "<1>", lambda x: [self.Toggle()])
        self.SwitchBallButton = None

        self.Update(SkipOnDoneFunc=True)

    def Update(self, Lerp = 1, SkipOnDoneFunc = False):

        if (self.SwitchBallButton):
            self.delete(self.SwitchBallButton)
        
        self.SwitchBallButton = self.create_image(19 * (Lerp if self.IsToggled else 1 - Lerp) + 7, 20, image=self.SwitchBallImage, anchor="n")
        self.tag_bind(self.SwitchBallButton, "<1>", lambda x: [self.Toggle()])

        if Lerp > 0.5:
            self.itemconfigure(self.ToggleButton, image=self.ToggledImage if self.IsToggled else self.UntoggledImage)

        if Lerp < 1:
            self.after(10, lambda: [self.Update(Lerp + 0.1 * (1 - Lerp + 0.1), SkipOnDoneFunc)])
        else:
            self.Cooldown = False
            if self.OnAnimDoneRef and not SkipOnDoneFunc:
                self.OnAnimDoneRef(self.IsToggled)
            

    def Toggle(self):
        if self.Cooldown:
            return

        self.Cooldown = True
        self.IsToggled = not self.IsToggled

        self.Update(0)

        if self.OnToggle:
            self.OnToggle(self.IsToggled)
        

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg=Usefuls.LightGrey

    def A(x):
        print("AAAAA")

    # create canvas
    myCanvas = ToggleSwitch(root, False, Title="Uhh", OnAnimDoneRef=A)

    # add to window and show
    myCanvas.pack()
    root.mainloop()