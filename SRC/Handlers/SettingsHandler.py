import yaml

class YamlParser():

    def __init__(self, Path):
        self.Path = Path

    def GetAllData(self) -> dict:
        try:
            with open(self.Path) as f:
                Data = yaml.safe_load(f)

            return Data

        except Exception as e:
            print(e)
            return None

    def Write(self, Directories, NewVal, DelimOverride="") -> bool:
        try:
            Data = self.GetAllData()
            Directories = "".join([f"[\"{x}\"]" for x in Directories.split(("/" if DelimOverride == "" else DelimOverride))])

            exec(f"""Data{Directories} = {NewVal if type(NewVal) != str else "'"+NewVal+"'" }""")

            with open(self.Path, "w") as f:
                Dumped = yaml.dump(Data, f)

            return True

        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    A = YamlParser(r"C:\Users\kingo\Documents\GitHub\UnrealCppImportHelper\SRC\Configuration.yaml")
    #print(A.GetAllData())
    A.Write("C++/Enabled", True)