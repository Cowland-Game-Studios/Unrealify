from Handlers import BeautifulSoupHandler

if __name__ == "__main__":

    print("\n\n\n Loading Modules... Please Wait \n\n\n")

    LoadedClasses = BeautifulSoupHandler.GetAllClasses()

    print("\n\n\n Unreal Class Modules Loaded \n\n\n")

    while 1:

        Query = input("Search For...\n")

        try:
            URL = LoadedClasses[Query]
            print(BeautifulSoupHandler.GetClassInclude(URL))
        except:
            print(f"Keyword {Query} Not Found!")

        if input("Exit? (Y/N)\n").lower() == "y":
            break