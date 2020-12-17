import json

#Tiedosto, johon käyttäjän tiedot on tallennettu
file_path = "wakatime.json"

#Listat tietojen keräämistä varten
days = []
languages = []
editors = []

if __name__ == "__main__":
    
    with open(file_path, "r") as file:

        data = json.load(file)

        #Lisätään 
        for day in data["days"]:
            days.append(day["date"])

