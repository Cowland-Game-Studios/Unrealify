import tkinter as tk
from PIL import ImageTk, Image
import os
import webbrowser

from Handlers.UI.TemplatePane import TemplatePane

from Handlers.UIComponents.Usefuls import Usefuls

class InfoPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()

        #Socials
        self.LogoDark = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Logo/Logo_DarkBG.png").resize((200, 200), Image.ANTIALIAS))
        self.YoutubeImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Socials/Socials_Youtube.png").resize((100, 100), Image.ANTIALIAS))
        self.ItchImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Socials/Socials_Itch.png").resize((100, 100), Image.ANTIALIAS))
        self.GithubImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Socials/Socials_Github.png").resize((100, 100), Image.ANTIALIAS))

        self.SetUpInfoUI()

    def SetUpInfoUI(self):
        self.BackgroundText = tk.Label( self.Root, text="Info", font=(Usefuls.FontAccented, 50), bg=Usefuls.LightBlack, foreground=Usefuls.LightGrey)
        self.BackgroundText.place(rely=1, x = 10, anchor="sw")

        self.InfoIcon = tk.Label( self.Root, image=self.LogoDark, borderwidth=0, background=Usefuls.LightBlack)
        self.InfoIcon.place(relx=0.5, y=20, anchor="n")

        self.Title = tk.Label( self.Root, text="Unrealify", font=(Usefuls.FontAccented, 40), bg=Usefuls.LightBlack, foreground=Usefuls.White)
        self.Title.place(relx=0.5, rely=0.51, anchor="center")

        self.Version = tk.Label(self.Root, text=self.Settings["App"]["Version"], font=(Usefuls.FontAccented, 12), bg=Usefuls.LightBlack, foreground=Usefuls.White)
        self.Version.place(relx=0.725, rely=0.505, anchor="n")

        self.Sub1 = tk.Label( self.Root, text="Streamline", font=(Usefuls.FontAccented, 12), bg=Usefuls.LightBlack, foreground=Usefuls.White)
        self.Sub1.place(relx=0.375, rely=0.56, anchor="n")

        self.Sub2 = tk.Label( self.Root, text="your UE5 experiance", font=(Usefuls.Font, 12), bg=Usefuls.LightBlack, foreground=Usefuls.White)
        self.Sub2.place(relx=0.45, rely=0.56, anchor="nw")

        # Credit = tk.Label( self.Root, text="Cowland Game Studios", font=(Usefuls.Font, 12), bg=Usefuls.LightBlack, foreground=Usefuls.White)
        # Credit.place(relx=0.5, rely=0.9, anchor="s")

        self.Socials_Youtube = tk.Label( self.Root, image=self.YoutubeImage, relief=tk.FLAT, borderwidth=0, background=Usefuls.LightBlack)
        self.Socials_Youtube.bind("<1>", lambda x: [webbrowser.open("https://www.youtube.com/channel/UCMcfj1Phz3G9xH0fUF_o9Jw")])
        self.Socials_Youtube.place(relx=0.7, rely=0.725, anchor="center")

        self.Socials_Itch = tk.Label( self.Root, image=self.ItchImage, relief=tk.FLAT, borderwidth=0, background=Usefuls.LightBlack)
        self.Socials_Itch.bind("<1>", lambda x: [webbrowser.open("https://cowlandgamestudios.itch.io/")])
        self.Socials_Itch.place(relx=0.5, rely=0.725, anchor="center")

        self.Socials_Github = tk.Label( self.Root, image=self.GithubImage, relief=tk.FLAT, borderwidth=0, background=Usefuls.LightBlack)
        self.Socials_Github.bind("<1>", lambda x: [webbrowser.open("https://github.com/Cowland-Game-Studios/Unrealify")])
        self.Socials_Github.place(relx=0.3, rely=0.725, anchor="center")

        self.AllWidgets = [self.BackgroundText, self.InfoIcon, self.Title, self.Version, self.Sub1, self.Sub2, self.Socials_Youtube, self.Socials_Github, self.Socials_Itch]

        self.PlayAnimation()
        