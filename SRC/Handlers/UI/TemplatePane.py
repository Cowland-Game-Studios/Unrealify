import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UIComponents.ScrollPane import ScrollPane

class TemplatePane(ScrollPane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, width=width, height=height, Background="#121212")

        self.AllWidgets = []
        self.SettingsHandler = SettingsHandler

    def Clear(self):
        for Widget in self.AllWidgets:
            if Widget is not None:
                Widget.destroy()
        self.AllWidgets = []

    def SetUpUI(self):
        self.Clear()

        ContentPane = tk.Canvas(width=self.Width - 125, height=self.Height, bg="#121212", highlightthickness=0)
        ContentPane.place(x = 125, y = 0, anchor = "nw")

        self.AllWidgets.append(ContentPane)

        return ContentPane

    def PlayAnimation(self, Lerp = 0, OgPosArray = [], WidgetOverride = []):

        if WidgetOverride == []:
            WidgetOverride = self.AllWidgets

        if (Lerp > 1):
            return

        if (Lerp == 0):
            for Widget in WidgetOverride:
                OgPosArray.append([float(Widget.place_info()["x"]), float(Widget.place_info()["y"]), float(Widget.place_info()["relx"]), float(Widget.place_info()["rely"])])

        for i in range(len(WidgetOverride)):
            WidgetOverride[i].place(x = Lerp*OgPosArray[i][0], y = Lerp*OgPosArray[i][1], relx=Lerp*OgPosArray[i][2], rely=Lerp*OgPosArray[i][3])

        self.after(10, lambda: [self.PlayAnimation(Lerp = Lerp + 0.1 * (1 - Lerp + 0.01), OgPosArray=OgPosArray, WidgetOverride=WidgetOverride)])

    # def PlayAnimation(self, Lerp = 0, OgPosArray = []):

    #     if (Lerp > 1):
    #         return

    #     if (Lerp == 0):
    #         for Widget in self.AllWidgets:
    #             OgPosArray.append([float(Widget.place_info()["x"]), float(Widget.place_info()["y"]), float(Widget.place_info()["relx"]), float(Widget.place_info()["rely"])])

    #     for i in range(len(self.AllWidgets)):
    #         self.AllWidgets[i].place(x = Lerp*OgPosArray[i][0], y = Lerp*OgPosArray[i][1], relx=Lerp*OgPosArray[i][2], rely=Lerp*OgPosArray[i][3])

    #     self.after(10, lambda: [self.PlayAnimation(Lerp = Lerp + 0.1 * (1 - Lerp + 0.01), OgPosArray=OgPosArray)])