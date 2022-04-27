from Handlers import PopUpHandler
from Handlers import ProgressHandler

try:
  from Handlers import KeyStrokeHandler
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

      for i in range(0, 99):
        ProgressBarToParse.Update(i)
        time.sleep(0.01)

      AllClasses = BeautifulSoupHandler.GetAllClasses() #ProgressBarToParse

      time.sleep(0.1)

      ProgressBarToParse.Update(100)


    NewWindow = threading.Thread(target=LoopProgress)
    NewWindow.start()

    ProgressBarToParse.Loop()

    PopUpHandler.PopUp(":)", "__CLOSE__", "Unreal Classes Loaded Succesfully!", False)

    KeyHandler = KeyStrokeHandler.KeyHandler([PopUpAssistant], AllClasses)
except Exception as e:
  PopUpHandler.PopUp(":(", "__CLOSE__", "Error: " + str(e), False)