import tkinter as tk

from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.SettingsHandler import YamlParser

root = tk.Tk()
#root.geometry("300x150")
root["bg"] = "#2D2D2D"

BitesTemplatePane(root, "Blueprints", YamlParser(r"C:\Users\kingo\Documents\GitHub\UnrealCppImportHelper\SRC\Configuration.yaml"), width=600, height=400).grid(row=1)

root.mainloop()