import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UIComponents.Usefuls import Usefuls

class Incrementor(tk.Canvas):
    def __init__(self, Root, Bounds, StartValue = 0, IncrementValue = 1, OnChangedFuncRef = None, Width=80, Height=21, bg=Usefuls.LightGrey):
        super().__init__(Root, width=Width, height=Height, bg=Usefuls.LightBlack, borderwidth=0, highlightthickness=0)

        self.bg = bg

        self.IncrementImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Incrementer/Increment.png").resize((20, 20), Image.ANTIALIAS))
        self.DecrementImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Incrementer/Decrement.png").resize((20, 20), Image.ANTIALIAS))

        self.OnChangedFuncRef = OnChangedFuncRef

        self.Value = StartValue
        self.IncrementValue = IncrementValue
        self.Bounds = Bounds

        self.SetUpUI()

    def SetUpUI(self):
        self.ValueTextbox = tk.Text(self, relief=tk.FLAT, bg=Usefuls.LightGrey, borderwidth=0, foreground=Usefuls.Mint, bd=0, highlightthickness=0, font=(Usefuls.FontAccented, 10))
        self.ValueTextbox.bind("<Return>", self.ValidateValue)
        self.UpdateTextboxAlignment()
        self.ValueTextbox.place(relx=0.5, rely=0.65, anchor="center", width=50, height=25)

        self.IncrementButton = tk.Button(self, activebackground = self.bg, bg  = self.bg, repeatdelay = 750, repeatinterval = 250, image=self.IncrementImage, relief=tk.FLAT, borderwidth=0, command=lambda: [self.OnIncrement()], border=0, fg=self.bg, highlightthickness=0, highlightbackground=self.bg)
        self.IncrementButton.place(relx=1, rely=0.5, anchor="e")
        
        self.DecrementButton = tk.Button(self, activebackground = self.bg, bg  = self.bg, repeatdelay = 750, repeatinterval = 250, image=self.DecrementImage, relief=tk.FLAT, borderwidth=0, command=lambda: [self.OnDecrement()], border=0, fg=self.bg, highlightthickness=0, highlightbackground=self.bg)
        self.DecrementButton.place(relx=0, rely=0.5, anchor="w")

    def TextboxAnimation(self, Pass = 0, Add = 1):
        if Pass > 3:
            self.after(10, self.TextboxAnimation(Pass - 1, -1))
            return
        if Pass < 0:
            self.ValueTextbox["font"] = (Usefuls.FontAccented, 10)
            return
        
        self.ValueTextbox["font"] = (Usefuls.FontAccented, 10 + Pass)

        self.after(10, lambda: [self.TextboxAnimation(Pass + Add, Add)])

    def UpdateTextboxAlignment(self):
        self.ValueTextbox.insert(tk.END, " ")
        self.ValueTextbox.delete("1.0", tk.END)
        self.ValueTextbox.insert(tk.END, self.Value)
        self.ValueTextbox.tag_configure("center", justify="center")
        self.ValueTextbox.tag_add("center", 1.0, "end")

    def OnChanged(self):

        self.UpdateTextboxAlignment()

        if self.OnChangedFuncRef:
            self.OnChangedFuncRef(self.Value)

        self.TextboxAnimation()

    def ValidateValue(self, Event, ValueOverride = None):
        NewValue = 0.0
        if ValueOverride is None:
            try:
                NewValue = float(self.ValueTextbox.get("1.0", tk.END))
            except:
                self.OnChanged()
                return "break"
        else:
            NewValue = ValueOverride
        NewValue = round(NewValue * 1e3) / 1e3

        if NewValue == self.Value:
            return

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

    def OnDecrement(self):

        if (self.Value - self.IncrementValue < self.Bounds[0]):
            return

        self.Value -= self.IncrementValue
        self.OnChanged()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg=Usefuls.LightGrey

    def Update(Value):
        IC.ValidateValue(None, Value)
        SL.OnClicked(None, Value)

    # create canvas
    IC = Incrementor(root, (-10, 10), 0, 0.5, Update)

    # add to window and show
    IC.pack()

    from Slider import Slider

    SL = Slider(root, (-10, 10), 0, Update, SnapTo=[0, 5], SnapThreashold=1)
    SL.pack()

    root.mainloop()