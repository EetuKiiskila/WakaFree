import json
from datetime import datetime
import matplotlib.pyplot as plt

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

#Lisätään kielten tiedot hakurakenteeseen 
def fill_languages(data):

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

#Lisätään editorien tiedot hakurakenteeseen 
def fill_editors(data):

    #Käydään läpi kaikki päivät 
    for day in data["days"]:

        #Kuinka monen päivän tiedot on lisätty editoreihin 
        number_of_days = 0

        #Jos päivälle ei löydy tietoja editoreista 
        if len(day["editors"]) == 0:

            #Lisätään kaikkiin editoreihin nolla sekuntia kyseiselle päivälle  
            for editor in editors:
                editors[editor].append(0.0)

        #Jos päivälle löytyy tietoja editoreista 
        else:

            #Käydään läpi kaikki editorit 
            for editor in day["editors"]:

                #Lisätään editoriin kyseisen päivän tiedot 
                editors[editor["name"]].append(editor["total_seconds"])

                #Tarkistetaan, monenko päivän tiedot on lisätty editoreihin 
                if len(editors[editor["name"]]) > number_of_days:
                    number_of_days = len(editors[editor["name"]])

        #Käydään läpi kaikki editorit 
        for editor in editors:

            #Jos editorin tiedoista puuttuu päivä, lisätään nolla sekuntia kyseiselle päivälle 
            if len(editors[editor]) < number_of_days:
                editors[editor].append(0.0)

#Lisätään käyttöjärjestelmien tiedot hakurakenteeseen 
def fill_operating_systems(data):

    #Käydään läpi kaikki päivät 
    for day in data["days"]:

        #Kuinka monen päivän tiedot on lisätty käyttöjärjestelmiin 
        number_of_days = 0

        #Jos päivälle ei löydy tietoja käyttöjärjestelmistä 
        if len(day["operating_systems"]) == 0:

            #Lisätään kaikkiin käyttöjärjestelmiin nolla sekuntia kyseiselle päivälle  
            for operating_system in operating_systems:
                operating_systems[operating_system].append(0.0)

        #Jos päivälle löytyy tietoja käyttöjärjestelmistä 
        else:

            #Käydään läpi kaikki käyttöjärjestelmät 
            for operating_system in day["operating_systems"]:

                #Lisätään käyttöjärjestelmään kyseisen päivän tiedot 
                operating_systems[operating_system["name"]].append(operating_system["total_seconds"])

                #Tarkistetaan, monenko päivän tiedot on lisätty käyttöjärjestelmiin 
                if len(operating_systems[operating_system["name"]]) > number_of_days:
                    number_of_days = len(operating_systems[operating_system["name"]])

        #Käydään läpi kaikki käyttöjärjestelmät 
        for operating_system in operating_systems:

            #Jos käyttöjärjestelmän tiedoista puuttuu päivä, lisätään nolla sekuntia kyseiselle päivälle 
            if len(operating_systems[operating_system]) < number_of_days:
                operating_systems[operating_system].append(0.0)

#Muunnetaan päivämäärät oikeaan muotoon kuvaajien piirtämistä varten 
def convert_dates(days):

    for index, day in enumerate(days):

        days[index] = datetime(int(day[0:4]), int(day[5:7]), int(day[8:10])).date()

#Muunnetaan sekunnit tunneiksi 
def seconds_to_hours(seconds):

    hours = seconds / 3600
    return hours

#Piirretään kielten kuvaajat 
def draw_languages_graph(days, languages):

    #Käydään läpi kaikki kielet 
    for language in languages:

        #Muutetaan kielten ajat sekunneista tunneiksi 
        languages[language] = [seconds_to_hours(total_seconds) for total_seconds in languages[language]]

        plt.plot(days, languages[language], linestyle="solid", marker="", label=language)

    plt.legend()
    plt.show()

#Varsinainen ohjelma 
if __name__ == "__main__":
    
    #Avataan tiedosto 
    with open(file_path, "r") as file:

        #Kopioidaan tiedot muuttujaan 
        data = json.load(file)

        #Valmistellaan tietojen lukeminen 
        initialize_lists(data)

        #Käydään läpi kielet, editorit ja käyttöjärjestelmät 
        fill_languages(data)
        fill_editors(data)
        fill_operating_systems(data)

        #Muunnetaan päivämäärät oikeaan muotoon 
        convert_dates(days)

        draw_languages_graph(days, languages)