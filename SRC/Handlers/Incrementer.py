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

        self.SetUpUI()

    def SetUpUI(self):
        self.IncrementButton = tk.Button(self, activebackground = "#2D2D2D", repeatdelay = 750, repeatinterval = 250, image=self.IncrementImage, bg="#2D2D2D", relief=tk.FLAT, borderwidth=0, command=lambda: [self.OnIncrement()])
        self.IncrementButton.place(relx=1, rely=0.5, anchor="e")
        #self.IncrementButton.bind("<Leave>", lambda x: [self.ResetButtons()])
        
        self.DecrementButton = tk.Button(self, activebackground = "#2D2D2D", repeatdelay = 750, repeatinterval = 250, image=self.DecrementImage, bg="#2D2D2D", relief=tk.FLAT, borderwidth=0, command=lambda: [self.OnDecrement()])
        self.DecrementButton.place(relx=0, rely=0.5, anchor="w")
        #self.DecrementButton.bind("<Leave>", lambda x: [self.ResetButtons()])

        self.ValueTextbox = tk.Text(self, relief=tk.FLAT, bg="#2D2D2D", borderwidth=0, foreground="#FFF", bd=0, highlightthickness=0, font=("Yu Gothic Bold", 10))
        self.ValueTextbox.bind("<Return>", self.ValidateValue)
        self.OnChanged()
        self.ValueTextbox.place(relx=0.5, rely=0.65, anchor="center", width=50, height=25)

    def TextboxAnimation(self, Pass = 0, Add = 1):
        if Pass > 3:
            self.after(10, self.TextboxAnimation(Pass - 1, -1))
            return
        if Pass < 0:
            self.ValueTextbox["font"] = ("Yu Gothic Bold", 10)
            return
        
        self.ValueTextbox["font"] = ("Yu Gothic Bold", 10 + Pass)

        self.after(10, lambda: [self.TextboxAnimation(Pass + Add, Add)])

    def OnChanged(self):
        self.ValueTextbox.insert(tk.END, " ")
        self.ValueTextbox.delete("1.0", tk.END)
        self.ValueTextbox.insert(tk.END, self.Value)
        self.ValueTextbox.tag_configure("center", justify="center")
        self.ValueTextbox.tag_add("center", 1.0, "end")

        self.TextboxAnimation()

    def ValidateValue(self, Event):
        NewValue = 0.0
        try:
            NewValue = float(self.ValueTextbox.get("1.0", tk.END))
        except:
            self.OnChanged()
            return "break"

        if NewValue >= self.Bounds[0] and NewValue <= self.Bounds[1]:
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

    def OnIncrement(self):

        if (self.Value + self.IncrementValue > self.Bounds[1]):
            return
        
        self.Value += self.IncrementValue
        self.OnChanged()

        if self.OnIncrement2:
            self.OnIncrement2()

    def OnDecrement(self):

        if (self.Value - self.IncrementValue < self.Bounds[0]):
            return

        self.Value -= self.IncrementValue
        self.OnChanged()

        if self.OnDecrement2:
            self.OnDecrement2()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = Incrementor(root, (0, 30), 10, 0.5)

    # add to window and show
    myCanvas.place(relx=0.5, rely=0.5, anchor="center")
    root.mainloop()