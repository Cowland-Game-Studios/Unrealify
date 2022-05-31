"""
following code not mine, sourced from: https://stackoverflow.com/questions/45682306/create-a-fix-button-with-scrollbar-in-tkinter
Thank you for the ScrollPane class.
"""

import tkinter as tk

class ScrollPane(tk.Canvas):
    def __init__(self, root, Background = "#FFF", width=400, height=50):
        tk.Canvas.__init__(self, root, bg=Background, width=width, height=height, borderwidth=0, highlightthickness=0)
        self.Canvas = tk.Canvas(root, bg=Background, width=width, height=height, borderwidth=0, highlightthickness=0)

        self.Frame = tk.Frame(self.Canvas, background=Background)
        self.Root = self.Frame

        self.VerticalScrollBar = tk.Scrollbar(root, orient="vertical", command=self.Canvas.yview)
        self.Canvas.configure(yscrollcommand=self.VerticalScrollBar.set)

        self.VerticalScrollBar.grid(row = 1, column = 1, sticky = "nsew")
        self.Canvas.grid(row = 1, column = 0, sticky = "nsew")
        self.Canvas.create_window((4,4), window=self.Frame, anchor="nw", tags="self.frame")

        self.Frame.bind("<Configure>", self.ConfigureHeight)
        #self.Canvas.bind("<MouseWheel>", self.MouseWheel)

        self.row = 0

    def MouseWheel(self, event):
        if (self.Canvas):
            self.Canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def ConfigureHeight(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.Canvas.configure(scrollregion=self.Canvas.bbox("all"))
        
    def Add(self, NewLabel, Padx=0, Pady=0, RowOverride = -1, ColOverride = -1):
        NewLabel.grid(row=(self.row if RowOverride == -1 else RowOverride), column=(0 if ColOverride == -1 else ColOverride), padx=Padx, pady=Pady)
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