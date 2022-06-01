#Written to add a feature to all current bites

import os

from Handlers.SettingsHandler import YamlParser

def RecurFindAdd(Path, Directory, Value):
    for Dir in os.listdir(Path):
        if Dir.startswith("_"):
            continue
        Full = Path + "/" + Dir
        if os.path.isfile(Full):
            if Full.endswith("Details.yaml"):
                Write = YamlParser(Full)
                Write.Write(Directory, Value)
        else:
            RecurFindAdd(Full, Directory, Value)

RecurFindAdd(os.path.dirname(os.path.realpath(__file__)) + "/Bites", "ApplyLocation", "NONE")