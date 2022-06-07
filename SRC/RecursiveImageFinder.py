import os

from Handlers.UIComponents.Usefuls import Usefuls

BlacklistedEndings = [
    "py",
    ".md",
    ".spec"
]

BlacklistedDirectories = [
    "__pycache__",
    ".DS_Store",
    ".git/",
    "build",
    "dist",
]

def FindData(Dir) -> list:
    Ttl = []
    print(Dir)
    for Item in os.listdir(f"{Usefuls.DirectoryAbove}{Dir}"):
        if Item.startswith("."):
            continue
        if os.path.isfile(f"{Usefuls.DirectoryAbove}{Dir}/{Item}") and Item.split(".")[-1] not in BlacklistedEndings:
            Ttl.append((f"{Usefuls.DirectoryAbove}{Dir}/{Item}", f"""{Dir}/{".".join(Item.split(".")[:-1])}"""))
        elif os.path.isdir(f"{Usefuls.DirectoryAbove}{Dir}/{Item}") and Item not in BlacklistedDirectories:
            Ttl += FindData(f"{Dir}/{Item}")
    return Ttl

print(FindData(""))