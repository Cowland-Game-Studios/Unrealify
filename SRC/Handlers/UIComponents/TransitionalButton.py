import tkinter as tk
from PIL import ImageTk, Image
import os

class TransitionalButton(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, OnClickFuncRef = None, bg="#2d2d2d", Mode="Side", OverlayImage = None):

        self.Width = 125 if (Mode == "Side") else 50
        self.Height = 37 if (Mode == "Side") else 50

        super().__init__(Root, width=self.Width, height=self.Height, bg=bg, borderwidth=0, highlightthickness=0)

        self.Mode = Mode

        self.SideBarImage = ImageTk.PhotoImage(Image.open(TransitionalButton.DirectoryAbove + "/Image/TransitionalButton/SideBar.png").resize((125, 37), Image.ANTIALIAS))
        self.BottomBarImage = ImageTk.PhotoImage(Image.open(TransitionalButton.DirectoryAbove + "/Image/TransitionalButton/BottomBar.png").resize((50, 50), Image.ANTIALIAS))

        self.OverlayImage = OverlayImage
        self.OnClickFuncRef = OnClickFuncRef

        self.IsHighlighted = False
        self.Cooldown = False

        self.SetUpUI()

    def OnClick(self):

        if (self.Cooldown):
            return
        
        self.Cooldown = True

        if (self.OnClickFuncRef):
            self.OnClickFuncRef()

        self.PlayAnimation(not self.IsHighlighted)

    def SetUpUI(self):
        self.SlideImage = self.create_image(self.Width, 0, image=self.SideBarImage if self.Mode == "Side" else self.BottomBarImage, anchor="nw")
        ButtonID = self.create_image(0, 0, image=self.OverlayImage, anchor="nw")
        self.tag_bind(ButtonID, "<1>", lambda x :[self.OnClick()])
    
    def PlayAnimation(self, Reversed = False, Lerp = 0):

        if Lerp > 1:
            self.IsHighlighted = Reversed
            self.Cooldown = False
            return #self.PlayAnimation(not Reversed, 0)

        LerpFlipped = Lerp * (-1 if Reversed else 1)

        self.moveto(self.SlideImage, ((LerpFlipped * self.Width) + (self.Width if Reversed else 0)) if self.Mode == "Side" else 0, ((LerpFlipped * self.Height) + (self.Height if Reversed else 0)) if self.Mode != "Side" else 0)

        self.after(10, lambda: [self.PlayAnimation(Reversed, Lerp = Lerp + 0.1 * (1 - Lerp + 0.01))])

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = TransitionalButton(root, Mode="Bottom", OverlayImage=ImageTk.PhotoImage(Image.open(TransitionalButton.DirectoryAbove + "/Image/TransitionalButton/Info.png").resize((50, 50), Image.ANTIALIAS)))
    myCanvas.pack()
    
    myCanvas = TransitionalButton(root, Mode="Side", OverlayImage=ImageTk.PhotoImage(Image.open(TransitionalButton.DirectoryAbove + "/Image/TransitionalButton/CPP.png").resize((125, 37), Image.ANTIALIAS)))
    myCanvas.pack()
    # add to window and show
    root.mainloop()