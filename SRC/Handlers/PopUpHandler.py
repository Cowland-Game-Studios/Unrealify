import tkinter as tk
import webbrowser
import pyperclip

class PopUp():
  
    def __init__(self, Header, Link, TextToCopy):
        self.SetUpUI(Header, Link, TextToCopy)
        self.window.focus_force()

        self.window.mainloop()
    
    def OpenLink(self, link):
        if (link == "__CLOSE__"):
            self.window.destroy()
        else:
            webbrowser.open_new_tab(link)

    def SetUpUI(self, Header, Link, TextToCopy) -> None:
        self.window = tk.Tk()
        self.window.geometry("300x150")
        self.window["bg"] = "#292929"
        self.window.title("Unreal Import Assistant")
        self.window.resizable(False, False)

        self.HeaderLabel = tk.Label(master=self.window, text=Header, bg="#292929", font=("Courier", 30), foreground="white")
        self.HeaderLabel.pack()
        
        self.DescriptionLabel = tk.Text(master=self.window, bg="#585858", foreground="white", font=("Courier", 15), borderwidth=0)
        self.DescriptionLabel.insert(tk.INSERT, TextToCopy)
        self.DescriptionLabel.place(x=10, y=50, width=220, height=50)

        self.LinkButton = tk.Button(master=self.window, text="Copy", command=lambda: [pyperclip.copy(TextToCopy)], bg="#adf7eb", foreground="white", borderwidth=0)
        self.LinkButton.place(x=290, rely=0.5, width=50, height=50, anchor="e")
        
        LinkButtonText = "Show In Browser"
        if (Link == "__CLOSE__"):
            LinkButtonText = "Close"

        self.LinkButton = tk.Button(master=self.window, text=LinkButtonText, command=lambda: [self.OpenLink(Link)], bg="#adf7eb", foreground="white", borderwidth=0)
        self.LinkButton.place(relx=0.5, rely=1, width=300, height=25, anchor="s")
    

if __name__ == "__main__":
    a2 = PopUp("Test", "Lol", "XD")
    a2 = PopUp("Testasdfasd", "Lolasdfasd", "XDasdf")