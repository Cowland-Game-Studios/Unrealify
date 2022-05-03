import tkinter as tk
from PIL import ImageTk, Image
import os

if __name__ == "__main__":
    from Slider import Slider
    from Incrementer import Incrementor
else:
    from UIComponents.Slider import Slider
    from UIComponents.Incrementer import Incrementor

class IncrementSlider(tk.Canvas):
    def __init__(self, Root, Bounds, Title="Uhh", StartValue = 0, IncrementValue = 1, OnChangeFuncRef = None, SnapTo = [], SnapThreashold = 1, bg="#2D2D2D"):
        super().__init__(Root, width=355, height=50, bg=bg, borderwidth=0, highlightthickness=0)

        self.Slider = Slider(self, Bounds, StartValue, self.OnChangeRef, SnapTo, SnapThreashold, bg=bg)
        self.Incrementor = Incrementor(self, Bounds, StartValue, IncrementValue, self.OnChangeRef, bg=bg)

        self.Slider.place(relx=0, rely=0.75, anchor="w")
        self.Incrementor.place(relx=1, rely=0.975, anchor="se")
        
        self.Title = self.create_text(0, 5, text=Title, font=("Yu Gothic Bold", 10), anchor="nw", fill="white")
        
        self.OnChangeFuncRef = OnChangeFuncRef

        self.Value = StartValue
        self.Bounds = Bounds
        self.SnapTo = SnapTo + [self.Bounds[0], self.Bounds[1]]
        self.SnapThreashold = SnapThreashold

    def OnChangeRef(self, Value):
        self.Incrementor.ValidateValue(None, Value)
        self.Slider.OnClicked(None, Value)

        if (self.OnChangeFuncRef):
            self.OnChangeFuncRef(Value)

        self.Value = Value

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = IncrementSlider(root, (-20, 30), "Ch", 0, SnapTo=[ -10, 5, 0, 10, 15], SnapThreashold=2)

    # add to window and show
    myCanvas.pack()
    root.mainloop()