import tkinter as tk

from Handlers.UI.BitesTemplatePane import BitesTemplatePane
from Handlers.SettingsHandler import YamlParser

root = tk.Tk()
root.geometry("600x500")
root["bg"] = "#2D2D2D"

BitesTemplatePane(root, "Misc", YamlParser(r"C:\Users\kingo\Documents\GitHub\UnrealCppImportHelper\SRC\Configuration.yaml"), Width=600, Height=300).place(x=0, y=0)

tk.Text(root).place(x=0, y=0)

root.mainloop()