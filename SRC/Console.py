from Handlers import BeautifulSoupHandler

if __name__ == "__main__":

    print("\n\n\n Loading Modules... Please Wait \n\n\n")

    LoadedClasses = BeautifulSoupHandler.GetAllClasses()

    print("\n\n\n Unreal Class Modules Loaded \n\n\n")

    while 1:

        Query = input("Search For... (type \"exit\" to terminate)\n").replace(" ", "").lower()

        if Query == "exit":
            break

        try:
            URL = LoadedClasses[Query]
            print(f"\n\nPath Found!\n>>>{BeautifulSoupHandler.GetClassInclude(URL)}<<<\n\n")
        except:
            print(f"Keyword {Query} Not Found!")