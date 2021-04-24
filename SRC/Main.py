from Handlers import KeyStrokeHandler
from Handlers import PopUpHandler
from Handlers import ProgressHandler
from Handlers import BeautifulSoupHandler
import threading
import time
from events import Events

ProgressBarToParse = None

def PopUpAssistant(Keyword, URL, Include):
  def MakePopUp():
    PopUpHandler.PopUp(Keyword, URL, Include)

  NewWindow = threading.Thread(target=MakePopUp)
  NewWindow.start()

def LoadingProgressMenu():

  def MakeProgressBar():
    global ProgressBarToParse

    ProgressBarToParse = ProgressHandler.Progress()
    ProgressBarToParse.Loop()
  
  NewWindow = threading.Thread(target=MakeProgressBar)
  NewWindow.start()

if __name__ == "__main__":
  LoadingProgressMenu()
  while ProgressBarToParse == None: #wait for thing to load
    time.sleep(0.5)
  AllClasses = BeautifulSoupHandler.GetAllClasses() #ProgressBarToParse
  KeyHandler = KeyStrokeHandler.KeyHandler([PopUpAssistant], AllClasses)