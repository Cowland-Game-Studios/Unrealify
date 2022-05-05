"""
following code not mine, sourced from: https://stackoverflow.com/questions/45682306/create-a-fix-button-with-scrollbar-in-tkinter
Thank you for the ScrollPane class.
"""

import tkinter as tk

class ScrollPane(tk.Frame):
    def __init__(self, root, Background = "#FFF"):
        tk.Frame.__init__(self, root)
        self.Canvas = tk.Canvas(root, borderwidth=0, background=Background)
        self.Frame = tk.Frame(self.Canvas, background=Background)
        self.VerticalScrollBar = tk.Scrollbar(root, orient="vertical", command=self.Canvas.yview)
        self.Canvas.configure(yscrollcommand=self.VerticalScrollBar.set)

        self.VerticalScrollBar.grid(row = 1, column = 1, sticky = "nsew")
        self.Canvas.grid(row = 1, column = 0, sticky = "nsew")
        self.Canvas.create_window((4,4), window=self.Frame, anchor="nw", tags="self.frame")

        self.Frame.bind("<Configure>", self.ConfigureHeight)

        self.row = 0

    def ConfigureHeight(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.Canvas.configure(scrollregion=self.Canvas.bbox("all"))
        
    def Add(self, NewLabel):
        NewLabel.grid(row=self.row, column=0)
        self.row += 1
        self.ConfigureHeight(None)

if __name__ == "__main__":
    from Slider import Slider
    from Incrementer import Incrementor

    root=tk.Tk()
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    A = ScrollPane(root, "#121212")

    for i in range(20):
        A.Add(Slider(A.Frame, (0, 30), bg="#121212"))
        A.Add(Incrementor(A.Frame, (0, 30), bg="#121212"))

    A.grid(row = 1)
    root.mainloop()