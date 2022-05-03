import tkinter as tk
from PIL import ImageTk, Image
import os

class ToggleSwitch(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, StartValue = False, OnToggleFuncRef = None, Width=67, Height=30):
        super().__init__(Root, width=Width, height=Height, bg="#2D2D2D", borderwidth=0, highlightthickness=0)

        self.ToggledImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/ToggledBackground.png").resize((67, 30), Image.ANTIALIAS))
        self.UntoggledImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/UntoggledBackground.png").resize((67, 30), Image.ANTIALIAS))
        self.SwitchBallImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/SwitchBall.png").resize((30, 30), Image.ANTIALIAS))

        self.OnToggle = OnToggleFuncRef

        self.IsToggled = StartValue
        self.Cooldown = False

        self.SetUpUI()

    def SetUpUI(self):

        self.ToggleButton = self.create_image(0, 0, image=self.ToggledImage, anchor="nw")
        self.tag_bind(self.ToggleButton, "<1>", lambda x: [self.Toggle()])
        self.SwitchBallButton = None

        self.Update()

    def Update(self, Lerp = 1, Ignore = False):

        if (self.SwitchBallButton):
            self.delete(self.SwitchBallButton)
        
        self.SwitchBallButton = self.create_image(38 * (Lerp if self.IsToggled else 1 - Lerp) + 15, 0, image=self.SwitchBallImage, anchor="n")
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
            self.OnToggle()
        

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = ToggleSwitch(root, False)

    # add to window and show
    myCanvas.place(relx=0.5, rely=0.5, anchor="center")
    root.mainloop()