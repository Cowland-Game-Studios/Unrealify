from Handlers import PopUpHandler
from Handlers import KeyStrokeHandler

import threading

class KeyStrokeWrapper():

    Settings = None
    OnPopupFuncRef = None

    def __init__(self, AllClasses, Settings, OnPopupFuncRef = None):
        self.Running = False
        KeyStrokeWrapper.Settings = Settings
        KeyStrokeWrapper.OnPopupFuncRef = OnPopupFuncRef
        self.KeyHandler = KeyStrokeHandler.KeyHandler([KeyStrokeWrapper.PopUpAssistant], AllClasses, float(Settings.GetAllData()["C++"]["Type"]["DelayBetweenCharacters"])) 

    def PopUpAssistant(Keyword, URL, Include):
        def MakePopUp():
            if (KeyStrokeWrapper.OnPopupFuncRef):
                KeyStrokeWrapper.OnPopupFuncRef(f"{Keyword.capitalize()}: \n\n{Include} \n\nURL: {URL}\n ---- \n")
            
            if (KeyStrokeWrapper.Settings and KeyStrokeWrapper.Settings.GetAllData()["C++"]["PopUps"]["Enabled"]):
                PopUpHandler.PopUp(Keyword, URL, Include, AutoCloseIn=float(KeyStrokeWrapper.Settings.GetAllData()["C++"]["PopUps"]["AutoCloseAfter"]))

        NewWindow = threading.Thread(target=MakePopUp)
        NewWindow.start()

    def Start(self):
        self.KeyHandler.Start()
        self.Running = True

    def Stop(self):
        self.KeyHandler.Stop()
        self.Running = False