import tkinter as tk
from Handlers.UI.SettingsPane import SettingsPane
from Handlers.UI.InfoPane import InfoPane
from Handlers.SettingsHandler import YamlParser

root = tk.Tk()
#root.geometry("300x150")
root["bg"] = "#2D2D2D"

SettingsPane(root, YamlParser(r"C:\Users\kingo\Documents\GitHub\UnrealCppImportHelper\SRC\Configuration.yaml"), width=600, height=400).grid(row=1)

root.mainloop()