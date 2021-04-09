import json
import yaml
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import argparse

class Stats:
    '''Yliluokka, joka sisältää päivämäärät sekä metodin näiden muuttamiseksi oikeaan muotoon ja metodin sekuntien muuttamiseksi tunneiksi.'''

    days = []

    @classmethod
    def convert_dates(cls, days):
        '''Muuntaa merkkijonoina olevat päivämäärät oikean tyyppisiksi.'''
        for index, day in enumerate(days):
            days[index] = datetime(int(day[0:4]), int(day[5:7]), int(day[8:10])).date()

    @staticmethod
    def seconds_to_hours(seconds):
        '''Muuntaa parametrina annetut sekunnit tunneiksi.'''
        hours = seconds / 3600
        return hours

class LanguagesStats(Stats):
    '''Aliluokka, joka sisältää tiedot eri ohjelmointikielistä.'''
    def __init__(self):
        self.languages = {}

class EditorsStats(Stats):
    '''Aliluokka, joka sisältää tiedot eri editoreille.'''
    def __init__(self):
        self.editors = {}

class OperatingSystemsStats(Stats):
    '''Aliluokka, joka sisältää tiedot eri käyttöjärjestelmille.'''
    def __init__(self):
        self.operating_systems = {}

#Listataan päivät, kielet, editorit ja käyttöjärjestelmät
def initialize_lists(data, languages, editors, operating_systems):

    #Käydään läpi kaikki päivät
    for day in data["days"]:
            
        #Päivämäärät
        Stats.days.append(day["date"])

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
def fill_languages(data, languages):

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
def fill_editors(data, editors):

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
def fill_operating_systems(data, operating_systems):

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

#Piirretään kuvaajat
def draw_graph(days, datasets, colors_file_path):

    with open(colors_file_path, "r") as colors_file:

        colors_data = yaml.safe_load(colors_file)

        #Käydään läpi kaikki tiedot
        for dataset in datasets:

            #Muutetaan ajat sekunneista tunneiksi
            datasets[dataset] = [Stats.seconds_to_hours(total_seconds) for total_seconds in datasets[dataset]]

            try:
                plt.plot(days, datasets[dataset], linestyle="solid", marker="", label=dataset, color=colors_data[dataset]["color"])
            except Exception:
                plt.plot(days, datasets[dataset], linestyle="solid", marker="", label=dataset)

    plt.ylabel("t (h)")

    plt.legend()
    plt.show()

#Piirretään ympyrädiagrammi
def draw_pie_chart(datasets, colors_file_path):

    total_times = []
    labels = []
    colors = []

    total_hours = 0

    with open(colors_file_path, "r") as colors_file:

        colors_data = yaml.safe_load(colors_file)

        #Käydään läpi kaikki tiedot
        for dataset in datasets:

            #Lasketaan ajat yhteen ja muutetaan ne sekunneista tunneiksi
            hours = Stats.seconds_to_hours(sum(datasets[dataset]))

            #Lisätään aika kokonaisaikaan
            total_hours += hours

            #Lisätään aika ja otsikko listoihin
            total_times.append(hours)
            labels.append(dataset + " - {0} h {1} min".format(int(hours), int((hours - int(hours)) * 60)))
            try:
                colors.append(colors_data[dataset]["color"])
            except Exception:
                colors.append(colors_data["Other"]["color"])

    #Lisätään prosenttiosuudet selitteeseen
    for index, time in  enumerate(total_times):
        labels[index] += " ({0:.2f} %)".format(total_times[index] / total_hours * 100)

    #Muutetaan järjestys eniten käytetystä vähiten käytettyyn, muuttuvat tupleiksi
    total_times, labels, colors = zip(*sorted(zip(total_times, labels, colors), reverse=True))

    #Piirretään ympyrädiagrammi
    fig = px.pie(names=labels, values=total_times, color_discrete_sequence=colors)
    fig.update_traces(marker=dict(line=dict(color="black", width=0.5)), textinfo="none", hovertemplate=labels)
    fig.show()

#Varsinainen ohjelma
if __name__ == "__main__":

    #Valmistellaan argumenttien lukeminen
    parser = argparse.ArgumentParser(description="You can use this program to show your statistics from WakaTime.")
    parser.add_argument("file", metavar="FILE", help="path to file with statistics")
    parser.add_argument("-g", "--graphs", help="show daily statistics: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-t", "--totals", help="show total times: string with l, e, o for languages, editors, operating systems")

    #Luetaan argumentit
    args = parser.parse_args()

    #Jos käyttäjä antaa tiedoston
    if args.file:

        #Avataan tiedosto
        with open(args.file, "r") as file:

            #Luodaan oliot tietoja varten
            languages = LanguagesStats()
            editors = EditorsStats()
            operating_systems = OperatingSystemsStats()

            #Kopioidaan tiedot muuttujaan
            data = json.load(file)

            #Valmistellaan tietojen lukeminen
            initialize_lists(data, languages.languages, editors.editors, operating_systems.operating_systems)

            #Muunnetaan päivämäärät oikeaan muotoon
            Stats.convert_dates(Stats.days)

            #Jos käyttäjä antaa argumentin kuvaajien piirtämiseen
            if args.graphs:

                #Kielten kuvaajat
                if "l" in args.graphs  or "L" in args.graphs:

                    fill_languages(data, languages.languages)
                    draw_graph(Stats.days, languages.languages, "Colors/languages_colors.yml")

                #Editorien kuvaajat
                if "e" in args.graphs or "E" in args.graphs:

                    fill_editors(data, editors.editors)
                    draw_graph(Stats.days, editors.editors, "Colors/editors_colors.yml")

                #Käyttöjärjestelmien kuvaajat
                if "o" in args.graphs or "O" in args.graphs:

                    fill_operating_systems(data, operating_systems.operating_systems)
                    draw_graph(Stats.days, operating_systems.operating_systems, "Colors/operating_systems_colors.yml")

            #Jos käyttäjä antaa argumentin kokonaisaikojen näyttämiseen
            if args.totals:

                #Kielten kokonaisajat
                if "l" in args.totals or "L" in args.totals:

                    fill_languages(data, languages.languages)
                    draw_pie_chart(languages.languages, "Colors/languages_colors.yml")

                #Editorien kokonaisajat
                if "e" in args.totals or "E" in args.totals:

                    fill_editors(data, editors.editors)
                    draw_pie_chart(editors.editors, "Colors/editors_colors.yml")

                #Käyttöjärjestelmien kokonaisajat
                if "o" in args.totals or "O" in args.totals:

                    fill_operating_systems(data, operating_systems.operating_systems)
                    draw_pie_chart(operating_systems.operating_systems, "Colors/operating_systems_colors.yml")