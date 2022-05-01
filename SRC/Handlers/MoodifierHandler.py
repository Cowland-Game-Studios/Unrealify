import tkinter as tk
import pyperclip

class BlueprintNode(tk.Frame):

    Counter = 0

    def __init__(self, Root, Information, OnClick, Width=50, Height=25):
        super().__init__(Root, width=Width, height=Height, bg="#2D2D2D", borderwidth=0)

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
        super().__init__(root, bg="#121212", height=height, width=width, highlightthickness=0)

        self.bind_all("<<Paste>>", self.HandlePaste)

        self.SideBar = tk.Canvas(root, bg="#2D2D2D", height=height, width=200, highlightthickness=0)
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
            On["bg"] = "#2D2D2D"

        Node["bg"] = "#FFF"

        for Detail in Node.ParsedInformation:
            Box = tk.Frame(self.SideBar, width=10, height=5, bg="#2D2D2D")
            Label = tk.Label(Box, text=Detail, bg="#2D2D2D", foreground="#FFF")
            A = tk.Text(Box, width=19, height=1, bg="#121212", foreground="#FFF", borderwidth=0)
            A.insert(tk.END, Node.ParsedInformation[Detail])
            Label.pack()
            A.pack()
            Box.pack()
            self.AllSideBar.append(Box)

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg="#2D2D2D"

    # create canvas
    myCanvas = Moodifier(root)

    # add to window and show
    myCanvas.pack()
    root.mainloop()