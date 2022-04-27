from Handlers import KeyStrokeHandler
from Handlers import PopUpHandler
from Handlers import ProgressHandler
from Handlers import BeautifulSoupHandler
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

  def LoopProgress():
    global AllClasses

    ProgressBarToParse.Update(0)

    ProgressBarToParse.Update(50)

    time.sleep(0.1)

    AllClasses = BeautifulSoupHandler.GetAllClasses() #ProgressBarToParse

    ProgressBarToParse.Update(99)

    time.sleep(0.1)

    ProgressBarToParse.Update(100)


  NewWindow = threading.Thread(target=LoopProgress)
  NewWindow.start()

  ProgressBarToParse.Loop()

  PopUpHandler.PopUp(":)", ":)", "Unreal Classes Loaded Succesfully!")

  KeyHandler = KeyStrokeHandler.KeyHandler([PopUpAssistant], AllClasses)