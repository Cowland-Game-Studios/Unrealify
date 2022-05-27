import tkinter as tk

from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.SettingsHandler import YamlParser
from Handlers.UIComponents.ScrollPane import ScrollPane
from Handlers.UI.TemplatePane import TemplatePane

root = tk.Tk()
root.geometry("1200x700")
root["bg"] = "#2D2D2D"

BitesPane = tk.Canvas(root, bg="#121212", highlightthickness=0, width=600, height=300)

BitesTemplatePane(BitesPane, "Misc", YamlParser(r"C:\Users\kingo\Documents\GitHub\UnrealCppImportHelper\SRC\Configuration.yaml"), 600, 300)#.place()#.grid()#.grid(columnspan=1, rowspan=1)
#ScrollPane(BitesPane, "#121212", 600, 300).grid()
#root.rowconfigure(1, weight=1)

BitesPane.grid()

root.mainloop()