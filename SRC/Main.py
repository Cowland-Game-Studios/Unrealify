from Handlers import PopUpHandler
from Handlers import ProgressHandler

AllThreads = []
AllWindows = []
ProgressBarToParse = None

try:
  from Handlers import BeautifulSoupHandler
  from Handlers import UIHandler
  import threading
  import time
  from events import Events
  import tkinter as tk

  AllCPPClasses = {}
  if __name__ == "__main__":
    ProgressBarToParse = ProgressHandler.Progress()
    AllWindows.append(ProgressBarToParse)

    def LoopProgress():
      global ProgressBarToParse

      ProgressBarToParse.Update(0)

      def UpdateFakeBar():
        for i in range(0, 100):
          ProgressBarToParse.Update(i)
          time.sleep(0.01)

      FakeUpdate = threading.Thread(target=UpdateFakeBar)
      FakeUpdate.start()
      AllThreads.append(FakeUpdate)

      AllCPPClasses = BeautifulSoupHandler.GetAllCPPClasses()

      FakeUpdate.join()
      ProgressBarToParse.Update(100)

      time.sleep(1)

      ProgressBarToParse.Update(101)

      MainWindow = UIHandler.App(ProgressBarToParse.window, AllCPPClasses)

    NewWindow = threading.Thread(target=LoopProgress)
    NewWindow.start()
    AllThreads.append(NewWindow)

    ProgressBarToParse.Loop()
except Exception as e:
  import traceback
  PopUpHandler.PopUp("ERROR", "__CLOSE__", str(traceback.format_exc()), True)