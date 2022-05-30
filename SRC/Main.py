AllThreads = []
AllWindows = []
Splash = None

try:
  from Handlers import PopUpHandler
  from Handlers import SplashHandler

  from Handlers import BeautifulSoupHandler
  from Handlers import UIHandler
  import threading
  import time
  from events import Events
  import tkinter as tk

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

      AllCPPClasses = None

      try:
        AllCPPClasses = BeautifulSoupHandler.GetAllCPPClasses()
      except Exception as e:
        PopUpHandler.PopUp("No Wifi", "__CLOSE__", "No wifi connection detected, running on local mode- C++ CodeTracker is disabled.", False, 10)

      FakeUpdate.join()
      Splash.Update(100)

      time.sleep(0.25)

      Splash.Update(101)

      MainWindow = UIHandler.App(Splash.window, AllCPPClasses)

    NewWindow = threading.Thread(target=LoopProgress)
    NewWindow.start()
    AllThreads.append(NewWindow)

    Splash.Loop()
except Exception as e:
  from Handlers import PopUpHandler
  if type(e) == ModuleNotFoundError:
    import InstallModules
    PopUpHandler.PopUp("Installed Needed Dependencies", "__CLOSE__", "All required dependencies should have been installed, restart application to start Unrealify", False)
    exit()
  import traceback
  PopUpHandler.PopUp("ERROR", "__CLOSE__", str(traceback.format_exc()), True)