import json

#Polku tiedostoon, johon käyttäjän tiedot on tallennettu 
file_path = "wakatime.json"

#Listat tietojen keräämistä varten 
days = []
languages = {}
editors = {}
operating_systems = {}

#Listataan päivät, kielet, editorit ja käyttöjärjestelmät 
def initialize_lists(data):

    #Käydään läpi kaikki päivät 
    for day in data["days"]:
            
        #Päivämäärät 
        days.append(day["date"])

        #Kielet 
        for language in day["languages"]:
                if language["name"] not in languages:
                    languages[language["name"]] = []

        #Editorit 
        for editor in day["editors"]:
            if editor["name"] not in editors:
                editors[editor["name"]] = []

        #Käyttöjärjestelmät 
        for operating_system in day["operating_systems"]:
            if operating_system["name"] not in operating_systems:
                operating_systems[operating_system["name"]] = []

#Lisätään tiedot listoihin 
def fill_lists(data):

    #Käydään läpi kaikki päivät 
    for day in data["days"]:

        #Kuinka monen päivän tiedot on lisätty kieliin 
        number_of_days = 0

        #Jos päivälle ei löydy tietoja kielistä 
        if len(day["languages"]) == 0:

            #Lisätään kaikkiin ohjelmointikieliin nolla sekuntia kyseiselle päivälle  
            for language in languages:
                languages[language].append(0.0)

        #Jos päivälle löytyy tietoja kielistä 
        else:

            #Käydään läpi kaikki kielet 
            for language in day["languages"]:

                #Lisätään kieleen kyseisen päivän tiedot 
                languages[language["name"]].append(language["total_seconds"])

                #Tarkistetaan, monenko päivän tiedot on lisätty kieliin 
                if len(languages[language["name"]]) > number_of_days:
                    number_of_days = len(languages[language["name"]])

        #Käydään läpi kaikki kielet 
        for language in languages:

            #Jos kielen tiedoista puuttuu päivä, lisätään nolla sekuntia kyseiselle päivälle 
            if len(languages[language]) < number_of_days:
                languages[language].append(0.0)

#Varsinainen ohjelma 
if __name__ == "__main__":
    
    #Avataan tiedosto 
    with open(file_path, "r") as file:

        #Kopioidaan tiedot muuttujaan 
        data = json.load(file)

        #Valmistellaan tietojen lukeminen 
        initialize_lists(data)

        #Käydään läpi tiedot ja lisätään ne listoihin 
        fill_lists(data)