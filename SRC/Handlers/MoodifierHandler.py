import tkinter as tk
import pyperclip

from Handlers.UIComponents.Usefuls import Usefuls

#Not released in V2.0, the following is WIP code for a in-house blueprint editor
class BlueprintNode(tk.Frame):

    Counter = 0

    def __init__(self, Root, Information, OnClick, Width=50, Height=25):
        super().__init__(Root, width=Width, height=Height, bg=Usefuls.LightGrey, borderwidth=0)

        self.ParsedInformation = self.ParseInformation(Information)

        self.place(x=BlueprintNode.Counter * 75, y=0, anchor="nw")
        BlueprintNode.Counter += 1
        self.bind("<1>", lambda x: [OnClick(self)])

    def ParseInformation(self, Information):
        Information = Information.split("\n")
        TestParser = {}

        for Info in Information:
            if ("=" not in Info):
                continue
            TestParser[Info.split("=")[0]] = "=".join(Info.split("=")[1:])

        return TestParser

class Moodifier(tk.Canvas):

    def __init__(self, root, width=500, height=300):
        super().__init__(root, bg=Usefuls.LightBlack, height=height, width=width, highlightthickness=0)

        self.bind_all("<<Paste>>", self.HandlePaste)

        self.SideBar = tk.Canvas(root, bg=Usefuls.LightGrey, height=height, width=200, highlightthickness=0)
        self.SideBar.pack(side=tk.RIGHT)

        self.AllSideBar = []
        self.AllNodes = []

    def HandlePaste(self, Event):
        self.AllNodes = []
        Content = pyperclip.paste()
        self.ParseUnrealCoding(Content)

    def ParseUnrealCoding(self, Code):
        Blueprints = Code.split("End Object")[:-1]
        
        for Blueprint in Blueprints:
            self.AllNodes.append(BlueprintNode(self, Blueprint, self.ShowDetailMenu))

    def ShowDetailMenu(self, Node):

        for PrevObj in self.AllSideBar:
            PrevObj.destroy()

        self.AllSideBar = []

        for On in self.AllNodes:
            On["bg"] = Usefuls.LightGrey

        Node["bg"] = Usefuls.White

        for Detail in Node.ParsedInformation:
            Box = tk.Frame(self.SideBar, width=10, height=5, bg=Usefuls.LightGrey)
            Label = tk.Label(Box, text=Detail, bg=Usefuls.LightGrey, foreground=Usefuls.White)
            A = tk.Text(Box, width=19, height=1, bg=Usefuls.LightBlack, foreground=Usefuls.White, borderwidth=0)
            A.insert(tk.END, Node.ParsedInformation[Detail])
            Label.pack()
            A.pack()
            Box.pack()
            self.AllSideBar.append(Box)

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg=Usefuls.LightGrey

    # create canvas
    myCanvas = Moodifier(root)

    # add to window and show
    myCanvas.pack()
    root.mainloop()