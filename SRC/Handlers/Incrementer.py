import tkinter as tk
from PIL import ImageTk, Image
import os

class Incrementor(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])

    def __init__(self, Root, Bounds, StartValue = 0, IncrementValue = 1, OnIncrement2 = None, OnDecrement2 = None, Width=100, Height=25):
        super().__init__(Root, width=Width, height=Height, bg="#2D2D2D", borderwidth=0)

        self.IncrementImage = ImageTk.PhotoImage(Image.open(Incrementor.DirectoryAbove + "/Image/Slider/Increment.png").resize((25, 25), Image.ANTIALIAS))
        self.DecrementImage = ImageTk.PhotoImage(Image.open(Incrementor.DirectoryAbove + "/Image/Slider/Decrement.png").resize((25, 25), Image.ANTIALIAS))

        self.IncrementImageHeld = ImageTk.PhotoImage(Image.open(Incrementor.DirectoryAbove + "/Image/Slider/Increment_Held.png").resize((25, 25), Image.ANTIALIAS))
        self.DecrementImageHeld = ImageTk.PhotoImage(Image.open(Incrementor.DirectoryAbove + "/Image/Slider/Decrement_Held.png").resize((25, 25), Image.ANTIALIAS))

        self.OnIncrement2 = OnIncrement2
        self.OnDecrement2 = OnDecrement2

        self.Value = StartValue
        self.IncrementValue = IncrementValue
        self.Bounds = Bounds

        self.IncrementPressed = False
        self.DecrementPressed = False

        self.SetUpUI()

    def SetUpUI(self):
        self.IncrementButton = tk.Label(self, image=self.IncrementImage, bg="#2D2D2D", relief=tk.FLAT, borderwidth=0)
        self.IncrementButton.bind("<1>", lambda x: [self.OnIncrement()])
        self.IncrementButton.bind("<ButtonRelease-1>", lambda x: [self.ResetButtons()])
        self.IncrementButton.place(relx=1, rely=0.5, anchor="e")
        
        self.DecrementButton = tk.Label(self, image=self.DecrementImage, bg="#2D2D2D", relief=tk.FLAT, borderwidth=0)
        self.DecrementButton.bind("<1>", lambda x: [self.OnDecrement()])
        self.DecrementButton.bind("<ButtonRelease-1>", lambda x: [self.ResetButtons()])
        self.DecrementButton.place(relx=0, rely=0.5, anchor="w")

        self.ValueTextbox = tk.Text(self, relief=tk.FLAT, bg="#2D2D2D", borderwidth=0, foreground="#FFF")
        self.ValueTextbox.bind("<Return>", self.ValidateValue)
        self.OnChanged()
        self.ValueTextbox.place(relx=0.5, rely=0.65, anchor="center", width=50, height=25)

    def OnChanged(self):
        self.ValueTextbox.insert(tk.END, " ")
        self.ValueTextbox.delete("1.0", tk.END)
        self.ValueTextbox.insert(tk.END, self.Value)
        self.ValueTextbox.tag_configure("center", justify="center")
        self.ValueTextbox.tag_add("center", 1.0, "end")

    def ValidateValue(self, Event):

        NewValue = int(self.ValueTextbox.get("1.0", tk.END))

        if NewValue <= self.Bounds[1] and NewValue >= self.Bounds[1]:
            self.Value = NewValue
        elif NewValue > self.Bounds[1]:
            self.Value = self.Bounds[1]
        elif NewValue < self.Bounds[0]:
            self.Value = self.Bounds[0]

        self.OnChanged()

        return "break"

    def ResetButtons(self):
        self.DecrementButton["image"] = self.DecrementImage
        self.IncrementButton["image"] = self.IncrementImage

        self.IncrementPressed = False
        self.DecrementPressed = False

    def OnIncrement(self, Recur = False):

        if not Recur:
            self.IncrementPressed = True

        if (self.Value >= self.Bounds[1] or not self.IncrementPressed):
            return
        
        self.Value += self.IncrementValue
        self.OnChanged()
        self.IncrementButton["image"] = self.IncrementImageHeld

        if self.OnIncrement2:
            self.OnIncrement2()

        #self.after(500, self.OnIncrement(True))

    def OnDecrement(self, Recur = False):

        if not Recur:
            self.DecrementPressed = True

        if (self.Value <= self.Bounds[0] or not self.DecrementPressed):
            return

        self.Value -= self.IncrementValue
        self.OnChanged()
        self.DecrementButton["image"] = self.DecrementImageHeld

        if self.OnDecrement2:
            self.OnDecrement2()

        #self.after(500, self.OnDecrement(True))

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = Incrementor(root, (0, 30), 10, 0.5)

    # add to window and show
    myCanvas.pack()
    root.mainloop()