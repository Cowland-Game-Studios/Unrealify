import tkinter as tk
from PIL import ImageTk, Image
import os

class ToggleSwitch(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, StartValue = False, OnToggleFuncRef = None, Width=67, Height=50, Title="", bg="#2d2d2d"):
        super().__init__(Root, width=Width, height=Height, bg=bg, borderwidth=0, highlightthickness=0)

        self.ToggledImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/ToggledBackground.png").resize((33, 15), Image.ANTIALIAS))
        self.UntoggledImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/UntoggledBackground.png").resize((33, 15), Image.ANTIALIAS))
        self.SwitchBallImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/SwitchBall.png").resize((15, 15), Image.ANTIALIAS))

        self.OnToggle = OnToggleFuncRef
        self.Title = self.create_text(0, 0, text=Title, font=("Yu Gothic Bold", 10), anchor="nw", fill="white")

        self.IsToggled = StartValue
        self.Cooldown = False

        self.SetUpUI()

    def SetUpUI(self):

        self.ToggleButton = self.create_image(0, 20, image=self.ToggledImage, anchor="nw")
        self.tag_bind(self.ToggleButton, "<1>", lambda x: [self.Toggle()])
        self.SwitchBallButton = None

        self.Update()

    def Update(self, Lerp = 1, Ignore = False):

        if (self.SwitchBallButton):
            self.delete(self.SwitchBallButton)
        
        self.SwitchBallButton = self.create_image(19 * (Lerp if self.IsToggled else 1 - Lerp) + 7, 20, image=self.SwitchBallImage, anchor="n")
        self.tag_bind(self.SwitchBallButton, "<1>", lambda x: [self.Toggle()])

        if Lerp > 0.5:
            self.itemconfigure(self.ToggleButton, image=self.ToggledImage if self.IsToggled else self.UntoggledImage)

        if Lerp < 1:
            self.after(10, lambda: [self.Update(Lerp + 0.1 * (1 - Lerp + 0.1), True)])
        else:
            self.Cooldown = False
            

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
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = ToggleSwitch(root, False, Title="Uhh")

    # add to window and show
    myCanvas.pack()
    root.mainloop()