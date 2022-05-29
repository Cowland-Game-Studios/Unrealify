import tkinter as tk
from PIL import ImageTk, Image

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = bg="#2D2D2D"
    root.geometry("600x200")

    # create canvas
    CowImage = ImageTk.PhotoImage(Image.open("/Users/mootbing/Desktop/Unrealify/SRC/Image/Logo/Icon.png").resize((100, 100), Image.ANTIALIAS))
    myCanvas = tk.Label(root, image=CowImage, relief=tk.FLAT, borderwidth=0)

    # add to window and show
    myCanvas.pack()
    root.mainloop()