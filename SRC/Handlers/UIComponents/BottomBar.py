import os
import tkinter as tk

class BottomBar(tk.Canvas):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, Text, bg="#92DDC8", fg="#FFF", Height=25):
        super().__init__(Root, bg=bg, borderwidth=0, highlightthickness=0, width=800)

        self.DisplayText = tk.Label(self, text=Text, font=("Yu Gothic Bold", int(Height/2)), bg="#92DDC8", foreground="#FFF")
        self.DisplayText.place(relx=0.42, y=0, anchor="n")

        self.place(relx=0, rely=1, anchor="sw", height=Height)

        self.after(2000, lambda : [self.destroy()])

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg="#2D2D2D"

    A = BottomBar(root, "Cow", "#92DDC8")
    #A
    root.mainloop()