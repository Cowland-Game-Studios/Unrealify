import tkinter as tk

from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.SettingsHandler import YamlParser
from Handlers.UIComponents.ScrollPane import ScrollPane
from Handlers.UI.TemplatePane import TemplatePane

from Handlers.UIComponents.ProjectWindow import ProjectWindow

root = tk.Tk()
root["bg"] = bg="#2D2D2D"

# create canvas
myCanvas = ScrollPane(root)

# add to window and show
myCanvas.grid(column=1, row=1)
myCanvas = ScrollPane(root)

# add to window and show
myCanvas.grid(column=1, row=2)
root.mainloop()