import tkinter as tk
from PIL import ImageTk, Image
import os

class ToggleSwitch(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])

    def __init__(self, Root, StartValue = False, OnToggleFuncRef = None, Width=67, Height=25):
        super().__init__(Root, width=Width, height=Height, bg="#2D2D2D", borderwidth=0)

        self.ToggledImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/ToggledBackground.png").resize((67, 30), Image.ANTIALIAS))
        self.UntoggledImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/UntoggledBackground.png").resize((67, 30), Image.ANTIALIAS))
        self.SwitchBallImage = ImageTk.PhotoImage(Image.open(ToggleSwitch.DirectoryAbove + "/Image/Toggle/SwitchBall.png").resize((30, 30), Image.ANTIALIAS))

        self.OnToggle = OnToggleFuncRef

        self.IsToggled = StartValue

        self.SetUpUI()

    def SetUpUI(self):
        # self.ToggleButton = tk.Button(self, activebackground = "#2D2D2D", bg="#2D2D2D", relief=tk.FLAT, borderwidth=0, command=self.Toggle)
        # self.ToggleButton.pack()
        self.ToggleButton = self.create_image(0, 0, image=self.ToggledImage, anchor="nw")
        self.SwitchBallButton = self.create_image(0, 0, image=self.SwitchBallImage, anchor="nw")
        self.tag_bind(self.ToggleButton, "<1>", lambda x: [self.Toggle()])
        #self.tag_bind(B, "<1>", lambda x: [self.Toggle()])

        self.Update()

    def Update(self):
        print(self.IsToggled)
        self.itemconfigure(self.ToggleButton, image=self.ToggledImage if self.IsToggled else self.UntoggledImage)
        pass
        #self.ToggleButton["image"] = self.ToggledImage if self.IsToggled else self.UntoggledImage

    def Toggle(self):
        self.IsToggled = not self.IsToggled

        self.Update()

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