from Handlers import PopUpHandler
from Handlers import KeyStrokeHandler

import threading

class KeyStrokeWrapper():

    def __init__(self, AllClasses):
        self.Running = False
        self.KeyHandler = threading.Thread(target = lambda: [KeyStrokeHandler.KeyHandler([KeyStrokeWrapper.PopUpAssistant], AllClasses)]) 

    def PopUpAssistant(Keyword, URL, Include):
        def MakePopUp():
            PopUpHandler.PopUp(Keyword, URL, Include)

        NewWindow = threading.Thread(target=MakePopUp)
        NewWindow.start()

    def Start(self):
        self.KeyHandler.start()
        self.Running = True

    def Stop(self):
        self.KeyHandler.join()
        self.Running = False