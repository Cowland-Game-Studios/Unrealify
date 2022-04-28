from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os

window = Tk()
window.geometry("300x300")
window["bg"] = "#292929"
window.title("Unreal Import Assistant")
window.resizable(False, False)

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename
def open_img():
    #x = openfn()
    img = Image.open(r"C:\Users\kingo\Documents\GitHub\UnrealCppImportHelper\SRC\Image\Splash.png")
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image=img, borderwidth=0)
    panel.image = img
    panel.pack()

open_img()

window.mainloop()