import tkinter as tk

from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.SettingsHandler import YamlParser
from Handlers.UIComponents.ScrollPane import ScrollPane
from Handlers.UI.TemplatePane import TemplatePane

from Handlers.UIComponents.ProjectWindow import ProjectWindow

root = tk.Tk()
root["bg"] = bg="#2D2D2D"

# create canvas
myCanvas = ProjectWindow(root, "/Users/mootbing/Desktop/LoneCity/LoneCity")

# add to window and show
myCanvas.pack()
root.mainloop()