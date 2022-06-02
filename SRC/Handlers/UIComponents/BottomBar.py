import os
import tkinter as tk

from Handlers.UIComponents.Usefuls import Usefuls

class BottomBar(tk.Canvas):
    def __init__(self, Root, Text, bg=Usefuls.Mint, fg=Usefuls.White, Height=25, Relx=0.45):
        super().__init__(Root, bg=bg, borderwidth=0, highlightthickness=0, width=800-125)

        self.DisplayText = tk.Label(self, text=Text, font=(Usefuls.FontAccented, int(Height/2)), bg=Usefuls.Mint, foreground=Usefuls.White)
        self.DisplayText.place(relx=Relx, y=0, anchor="n")

        self.place(x=0, rely=1, anchor="sw", height=Height, width=800-125)

        self.PlayAnimation()

        #self.after(2000, lambda : [self.destroy()])

    def PlayAnimation(self, Lerp=0, Reverse = False):
        if Lerp <= 0 and Reverse:
            self.destroy()
            return

        if Lerp >= 1 and not Reverse:
            self.after(1500, self.PlayAnimation(1, True))
            return

        self.place(x=0, rely=1.1 - 0.1 * Lerp)

        self.after(10, lambda: [self.PlayAnimation(Lerp + 0.025 if not Reverse else Lerp - 0.025, Reverse)])


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg="#2D2D2D"

    A = BottomBar(root, "Cow", Usefuls.Mint)
    #A
    root.mainloop()