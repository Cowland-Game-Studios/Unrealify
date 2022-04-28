from Handlers import PopUpHandler
from Handlers import ProgressHandler

AllThreads = []
AllWindows = []
ProgressBarToParse = None

try:
  from Handlers import KeyStrokeHandler
  from Handlers import BeautifulSoupHandler
  from Handlers import UIHandler
  import threading
  import time
  from events import Events

  def PopUpAssistant(Keyword, URL, Include):
    def MakePopUp():
      PopUpHandler.PopUp(Keyword, URL, Include)

    NewWindow = threading.Thread(target=MakePopUp)
    NewWindow.start()

  AllClasses = {}
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

      AllClasses = BeautifulSoupHandler.GetAllClasses() #ProgressBarToParse

      FakeUpdate.join()
      ProgressBarToParse.Update(100)

      time.sleep(1)

      ProgressBarToParse.Update(101)
      ProgressBarToParse = None

    NewWindow = threading.Thread(target=LoopProgress)
    NewWindow.start()
    AllThreads.append(NewWindow)

    ProgressBarToParse.Loop()

    KeyHandler = threading.Thread(target = lambda: [KeyStrokeHandler.KeyHandler([PopUpAssistant], AllClasses)]) 
    KeyHandler.start()
    AllThreads.append(KeyHandler)

    MainWindow = UIHandler.App()
    AllWindows.append(MainWindow)
except Exception as e:
  import traceback
  PopUpHandler.PopUp("ERROR", "__CLOSE__", str(traceback.format_exc()), True)