import tkinter as tk
from PIL import ImageTk, Image
import os

class Slider(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, Bounds, StartValue = 0, OnChangeFuncRef = None):
        super().__init__(Root, width=400, height=30, bg="#2D2D2D", borderwidth=0, highlightthickness=0)

        self.BackgroundImage = ImageTk.PhotoImage(Image.open(Slider.DirectoryAbove + "/Image/Slider/SliderBackground.png").resize((250, 4), Image.ANTIALIAS))
        self.DotButtonImage = ImageTk.PhotoImage(Image.open(Slider.DirectoryAbove + "/Image/Slider/SliderButton.png").resize((15, 15), Image.ANTIALIAS))
        self.DotButtonImageHeld = ImageTk.PhotoImage(Image.open(Slider.DirectoryAbove + "/Image/Slider/SliderButton_Held.png").resize((15, 15), Image.ANTIALIAS))
        
        self.OnChangeFuncRef = OnChangeFuncRef

        self.Value = StartValue
        self.Bounds = Bounds

        self.SetUpUI()

    def SetUpUI(self):
        self.Background = self.create_image(7, 15, image=self.BackgroundImage, anchor="w")
        self.tag_bind(self.Background, "<B1-Motion>", lambda x: [self.OnClicked(x)])
        self.tag_bind(self.Background, "<ButtonRelease-1>", lambda x: [self.OnClicked(x), self.OnChanged()])
        self.Button = None
        self.BackgroundOverlay = None
        
        self.UpdateButtonPos()

    def UpdateButtonPos(self):
        if self.Button:
            self.delete(self.Button)

        if self.BackgroundOverlay:
            self.delete(self.BackgroundOverlay)
        
        self.BackgroundOverlay = self.create_rectangle(0, 13, (self.Value + abs(self.Bounds[0])) / (abs(self.Bounds[0]) + self.Bounds[1]) * 250 + 7, 17, outline="", fill="#92DDC8")
        self.Button = self.create_image((self.Value + abs(self.Bounds[0])) / (abs(self.Bounds[0]) + self.Bounds[1]) * 250 + 7, 7, image=self.DotButtonImage, anchor="n")

    def OnChanged(self):
        if self.OnChangeFuncRef:
            self.OnChangeFuncRef()

        print(self.Value)

    def OnClicked(self, Event):
        NewValue = ((Event.x - 7) / 250) * (abs(self.Bounds[0]) + self.Bounds[1]) - abs(self.Bounds[0])

        if NewValue >= self.Bounds[0] and NewValue <= self.Bounds[1]:
            self.Value = NewValue
        elif NewValue > self.Bounds[1]:
            self.Value = self.Bounds[1]
        elif NewValue < self.Bounds[0]:
            self.Value = self.Bounds[0]

        self.UpdateButtonPos()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = Slider(root, (0, 30), 0)

    # add to window and show
    myCanvas.place(x=10, y=0, width=375, height=30, anchor="nw")
    root.mainloop()