import tkinter as tk

class App():
  
  def __init__(self):
    self.window = tk.Tk()
    self.window.geometry("800x600")
    self.window["bg"] = "#292929"
    self.window.title("Unreal Coding Assistant")
    self.window.resizable(False, False)
    
    self.SetUpUI()
    self.window.focus_force()

    self.window.mainloop()
    
  def SetUpUI(self):
    print("ui")

if __name__ == "__main__":
  a = App()