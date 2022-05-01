from Handlers import PopUpHandler
from Handlers import SplashHandler

AllThreads = []
AllWindows = []
Splash = None

try:
  from Handlers import BeautifulSoupHandler
  from Handlers import UIHandler
  import threading
  import time
  from events import Events
  import tkinter as tk

  AllCPPClasses = {}
  if __name__ == "__main__":
    Splash = SplashHandler.SplashScreen()
    AllWindows.append(Splash)

    def LoopProgress():
      global Splash

      Splash.Update(0)

      def UpdateFakeBar():
        for i in range(0, 100):
          Splash.Update(i)
          time.sleep(0.01)

      FakeUpdate = threading.Thread(target=UpdateFakeBar)
      FakeUpdate.start()
      AllThreads.append(FakeUpdate)

      AllCPPClasses = BeautifulSoupHandler.GetAllCPPClasses()

      FakeUpdate.join()
      Splash.Update(100)

      time.sleep(1)

      Splash.Update(101)

      MainWindow = UIHandler.App(Splash.window, AllCPPClasses)

    NewWindow = threading.Thread(target=LoopProgress)
    NewWindow.start()
    AllThreads.append(NewWindow)

    Splash.Loop()
except Exception as e:
  import traceback
  PopUpHandler.PopUp("ERROR", "__CLOSE__", str(traceback.format_exc()), True)