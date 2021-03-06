
from pynput.keyboard import Key, Listener
import re
from Handlers import BeautifulSoupHandler
from events import Events
import datetime
import time
import threading

KeyIgnores = [
  "key.enter",
  "key.space"
]

class KeyHandler():

  #optional parameters, event params are just for what functions to call when matched, the dictionairy can be parsed in to save recalling of a latent function
  def __init__(self, AEventParams = [], AClassDict = BeautifulSoupHandler.GetAllClasses()) -> None:
    
    print("Tracking Started (Exit terminal to stop)")

    self.Keys = []
    self.UnrealClassesDict = AClassDict
    self.TriggeredStamp = datetime.datetime.now().timestamp()

    self.EventHandler = Events()
    if len(AEventParams) == 0:
      self.EventHandler.on_change += self.DummyEvent
    else:
      for Event in AEventParams:
        self.EventHandler.on_change += Event

    Checker = threading.Thread(target=self.CheckStrokes)
    Checker.start()

    with Listener(on_press = self.ProcessStrokes) as listener:   
      listener.join()

  def IsNotBlackListedKeys(self, Key) -> bool:
    return Key.lower() in KeyIgnores or "\\" in Key.lower() #to rid key.space, key.backspace

  def IsNotCharacter(self, Key) -> bool:
    return "key" in Key.lower() #to rid key.anything

  def DummyEvent(self, Keyword, URL, Include) -> None: #dummy event if no event is put in the EventParams
    print("%s %s %s" % (Keyword, URL, Include))

  def ProcessStrokes(self, Key) -> None:
    
    Key = str(Key).replace("\'", "")

    if Key.lower() == "key.backspace" and len(self.Keys) > 0:
      self.Keys.pop()
      return

    if self.IsNotBlackListedKeys(Key): #on blacklisted key pressed flush characters
      self.Keys = []
      return

    if self.IsNotCharacter(Key):#ignore shift keys
      return
    
    self.Keys.append(Key) #add character into Keys
    TriggeredStamp = datetime.datetime.now().timestamp()

    print(self.Keys)

  def CheckStrokes(self):

    Delay = 0.5

    while True:

      time.sleep(Delay)

      if (datetime.datetime.now().timestamp() - self.TriggeredStamp > Delay / 2):
        Joined = "".join(self.Keys).lower().replace(";", "")
              
        if Joined in list(self.UnrealClassesDict.keys()): 
          self.EventHandler.on_change(
            Joined,
            self.UnrealClassesDict[Joined],
              BeautifulSoupHandler.GetClassInclude(self.UnrealClassesDict[Joined])
              ) #event dispatches

          self.Keys = []

if __name__ == "__main__":
  import BeautifulSoupHandler
  K = KeyHandler([], BeautifulSoupHandler.GetAllClasses())