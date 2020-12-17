import json

#Tiedosto, johon käyttäjän tiedot on tallennettu 
file_path = "wakatime.json"

#Listat tietojen keräämistä varten 
days = []
languages = []
editors = []
operating_systems = []

if __name__ == "__main__":
    
    with open(file_path, "r") as file:

        data = json.load(file)

        #Listataan päivät, kielet, editorit ja käyttöjärjestelmät 
        for day in data["days"]:
            
            #Päivät 
            days.append(day["date"])

            #Kielet 
            for language in day["languages"]:
                if language["name"] not in languages:
                    languages.append(language["name"])

            #Editorit
            for editor in day["editors"]:
                if editor["name"] not in editors:
                    editors.append(editor["name"])

            #Käyttöjärjestelmät
            for operating_system in day["operating_systems"]:
                if operating_system["name"] not in operating_systems:
                    operating_systems.append(operating_system["name"])

