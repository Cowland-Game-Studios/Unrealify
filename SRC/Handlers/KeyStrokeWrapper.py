from Handlers import PopUpHandler
from Handlers import KeyStrokeHandler

import threading

class KeyStrokeWrapper():

    EnablePopup = True
    OnPopupFuncRef = None

    def __init__(self, AllClasses, EnablePopup = True, OnPopupFuncRef = None):
        self.Running = False
        KeyStrokeWrapper.EnablePopup = EnablePopup
        KeyStrokeWrapper.OnPopupFuncRef = OnPopupFuncRef
        self.KeyHandler = KeyStrokeHandler.KeyHandler([KeyStrokeWrapper.PopUpAssistant], AllClasses) 

    def PopUpAssistant(Keyword, URL, Include):
        def MakePopUp():
            if (KeyStrokeWrapper.OnPopupFuncRef):
                KeyStrokeWrapper.OnPopupFuncRef(f"{Keyword.capitalize()}: \n\n{Include} \n\nURL: {URL}\n ---- \n")
            
            if (KeyStrokeWrapper.EnablePopup):
                PopUpHandler.PopUp(Keyword, URL, Include)

        NewWindow = threading.Thread(target=MakePopUp)
        NewWindow.start()

    def Start(self):
        self.KeyHandler.Start()
        self.Running = True

    def Stop(self):
        self.KeyHandler.Stop()
        self.Running = False