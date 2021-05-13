import json
import yaml
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import argparse

class Stats:
    '''Yliluokka, joka sisältää päivämäärät sekä metodin näiden muuttamiseksi oikeaan muotoon ja metodin sekuntien muuttamiseksi tunneiksi.'''

    days = []

    @classmethod
    def convert_dates(cls, days=days):
        '''Muuntaa merkkijonoina olevat päivämäärät oikean tyyppisiksi.'''
        for index, day in enumerate(days):
            days[index] = datetime(int(day[0:4]), int(day[5:7]), int(day[8:10])).date()

    @staticmethod
    def seconds_to_hours(seconds):
        '''Muuntaa parametrina annetut sekunnit tunneiksi.'''
        hours = seconds / 3600
        return hours

    @staticmethod
    def fetch_days_and_labels(data, days=days, languages=None, editors=None, operating_systems=None, ignored_stats=[]):
        '''Lisää päivät listaan ja avaimet haluttuihin hakurakenteisiin.'''
        #Käydään läpi kaikki päivät
        for day in data["days"]:

            #Ohitetaan päivä käyttäjän antamista argumenteista riippuen
            if day["date"] < str(start_date):
                continue
            elif day["date"] > str(end_date):
                continue
            
            #Päivämäärät
            days.append(day["date"])

            #Kielet
            if languages is not None:
                for language in day["languages"]:
                    if language["name"] in ignored_stats:
                        continue
                    elif language["name"] not in languages:
                        languages[language["name"]] = []
        
            #Editorit
            if editors is not None:
                for editor in day["editors"]:
                    if editor["name"] in ignored_stats:
                        continue
                    elif editor["name"] not in editors:
                        editors[editor["name"]] = []

            #Käyttöjärjestelmät
            if operating_systems is not None:
                for operating_system in day["operating_systems"]:
                    if operating_system["name"] in ignored_stats:
                        continue
                    elif operating_system["name"] not in operating_systems:
                        operating_systems[operating_system["name"]] = []

class LanguagesStats(Stats):
    '''Aliluokka, joka sisältää tiedot eri ohjelmointikielistä.'''
    def __init__(self):
        self.languages = {}
        self.keys = []
        self.total_times = []

    def populate_stats(self, data):
        '''Lisää kielten tiedot hakurakenteeseen.

        Parametrit:

            data -- JSON-tiedostosta luetut tiedot.
        '''
        #Käydään läpi kaikki päivät
        for day in data["days"]:

            #Ohitetaan päivä käyttäjän antamista argumenteista riippuen
            if day["date"] < str(start_date):
                continue
            elif day["date"] > str(end_date):
                continue

            #Kuinka monen päivän tiedot on lisätty kieliin
            number_of_days = 0

            #Jos päivälle ei löydy tietoja kielistä
            if len(day["languages"]) == 0:

                #Lisätään kaikkiin ohjelmointikieliin nolla tuntia kyseiselle päivälle
                for language in self.languages:
                    self.languages[language].append(0.0)

            #Jos päivälle löytyy tietoja kielistä
            else:

                #Käydään läpi kaikki kielet
                for language in day["languages"]:

                    #Ohitetaan kieli käyttäjän halutessa
                    if language["name"] in ignored_stats:
                        continue

                    #Lisätään kieleen kyseisen päivän tiedot tunneiksi muutettuna
                    self.languages[language["name"]].append(Stats.seconds_to_hours(language["total_seconds"]))

                    #Tarkistetaan, monenko päivän tiedot on lisätty kieliin
                    if len(self.languages[language["name"]]) > number_of_days:
                        number_of_days = len(self.languages[language["name"]])

            #Käydään läpi kaikki kielet
            for language in self.languages:

                #Jos kielen tiedoista puuttuu päivä, lisätään nolla tuntia kyseiselle päivälle
                if len(self.languages[language]) < number_of_days:
                    self.languages[language].append(0.0)

    def sort_stats_and_populate_keys(self):
        '''Järjestää tiedot eniten käytetystä vähiten käytettyyn ja täyttää avaimet oikeassa järjestyksessä.'''
        total_hours = 0

        #Käydään läpi kielet
        for language in self.languages:

            #Lasketaan kielen päivittäiset ajat yhteen
            hours = sum(self.languages[language])

            #Lisätään aika kokonaisaikaan
            total_hours += hours

            #Lisätään kokonaisaika ja avain listoihin
            self.total_times.append(hours)
            self.keys.append(language)

        #Muutetaan järjestys eniten käytetystä vähiten käytettyyn, muuttuvat tupleiksi
        self.total_times, self.keys = zip(*sorted(zip(self.total_times, self.keys), reverse=True))

class EditorsStats(Stats):
    '''Aliluokka, joka sisältää tiedot eri editoreille.'''
    def __init__(self):
        self.editors = {}
        self.keys = []
        self.total_times = []

    def populate_stats(self, data):
        '''Lisää editorien tiedot hakurakenteeseen.

        Parametrit:

            data -- JSON-tiedostosta luetut tiedot.
        '''
        #Käydään läpi kaikki päivät
        for day in data["days"]:

            #Ohitetaan päivä käyttäjän antamista argumenteista riippuen
            if day["date"] < str(start_date):
                continue
            elif day["date"] > str(end_date):
                continue

            #Kuinka monen päivän tiedot on lisätty editoreihin
            number_of_days = 0

            #Jos päivälle ei löydy tietoja editoreista
            if len(day["editors"]) == 0:

                #Lisätään kaikkiin editoreihin nolla tuntia kyseiselle päivälle
                for editor in self.editors:
                    self.editors[editor].append(0.0)

            #Jos päivälle löytyy tietoja editoreista
            else:

                #Käydään läpi kaikki editorit
                for editor in day["editors"]:

                    #Ohitetaan editori käyttäjän halutessa
                    if editor["name"] in ignored_stats:
                        continue

                    #Lisätään editoriin kyseisen päivän tiedot tunneiksi muutettuna
                    self.editors[editor["name"]].append(Stats.seconds_to_hours(editor["total_seconds"]))

                    #Tarkistetaan, monenko päivän tiedot on lisätty editoreihin
                    if len(self.editors[editor["name"]]) > number_of_days:
                        number_of_days = len(self.editors[editor["name"]])

            #Käydään läpi kaikki editorit
            for editor in self.editors:

                #Jos editorin tiedoista puuttuu päivä, lisätään nolla tuntia kyseiselle päivälle
                if len(self.editors[editor]) < number_of_days:
                    self.editors[editor].append(0.0)

    def sort_stats_and_populate_keys(self):
        '''Järjestää tiedot eniten käytetystä vähiten käytettyyn ja täyttää avaimet oikeassa järjestyksessä.'''
        total_hours = 0

        #Käydään läpi editorit
        for editor in self.editors:

            #Lasketaan editorin päivittäiset ajat yhteen
            hours = sum(self.editors[editor])

            #Lisätään aika kokonaisaikaan
            total_hours += hours

            #Lisätään kokonaisaika ja avain listoihin
            self.total_times.append(hours)
            self.keys.append(editor)

        #Muutetaan järjestys eniten käytetystä vähiten käytettyyn, muuttuvat tupleiksi
        self.total_times, self.keys = zip(*sorted(zip(self.total_times, self.keys), reverse=True))

class OperatingSystemsStats(Stats):
    '''Aliluokka, joka sisältää tiedot eri käyttöjärjestelmille.'''
    def __init__(self):
        self.operating_systems = {}
        self.keys = []
        self.total_times = []

    def populate_stats(self, data):
        '''Lisää käyttöjärjestelmien tiedot hakurakenteeseen.

        Parametrit:

            data -- JSON-tiedostosta luetut tiedot.
        '''
        #Käydään läpi kaikki päivät
        for day in data["days"]:

            #Ohitetaan päivä käyttäjän antamista argumenteista riippuen
            if day["date"] < str(start_date):
                continue
            elif day["date"] > str(end_date):
                continue

            #Kuinka monen päivän tiedot on lisätty käyttöjärjestelmiin
            number_of_days = 0

            #Jos päivälle ei löydy tietoja käyttöjärjestelmistä
            if len(day["operating_systems"]) == 0:

                #Lisätään kaikkiin käyttöjärjestelmiin nolla tuntia kyseiselle päivälle 
                for operating_system in self.operating_systems:
                    self.operating_systems[operating_system].append(0.0)

            #Jos päivälle löytyy tietoja käyttöjärjestelmistä
            else:

                #Käydään läpi kaikki käyttöjärjestelmät
                for operating_system in day["operating_systems"]:

                    #Ohitetaan käyttöjärjestelmä käyttäjän halutessa
                    if operating_system["name"] in ignored_stats:
                        continue

                    #Lisätään käyttöjärjestelmään kyseisen päivän tiedot tunneiksi muutettuna
                    self.operating_systems[operating_system["name"]].append(Stats.seconds_to_hours(operating_system["total_seconds"]))

                    #Tarkistetaan, monenko päivän tiedot on lisätty käyttöjärjestelmiin
                    if len(self.operating_systems[operating_system["name"]]) > number_of_days:
                        number_of_days = len(self.operating_systems[operating_system["name"]])

            #Käydään läpi kaikki käyttöjärjestelmät
            for operating_system in self.operating_systems:

                #Jos käyttöjärjestelmän tiedoista puuttuu päivä, lisätään nolla tuntia kyseiselle päivälle
                if len(self.operating_systems[operating_system]) < number_of_days:
                    self.operating_systems[operating_system].append(0.0)

    def sort_stats_and_populate_keys(self):
        '''Järjestää tiedot eniten käytetystä vähiten käytettyyn ja täyttää avaimet oikeassa järjestyksessä.'''
        total_hours = 0

        #Käydään läpi käyttöjärjestelmät
        for operating_system in self.operating_systems:

            #Lasketaan käyttöjärjestelmän päivittäiset ajat yhteen
            hours = sum(self.operating_systems[operating_system])

            #Lisätään aika kokonaisaikaan
            total_hours += hours

            #Lisätään kokonaisaika ja avain listoihin
            self.total_times.append(hours)
            self.keys.append(operating_system)

        #Muutetaan järjestys eniten käytetystä vähiten käytettyyn, muuttuvat tupleiksi
        self.total_times, self.keys = zip(*sorted(zip(self.total_times, self.keys), reverse=True))

#Piirretään kuvaajat
def draw_graph(days, keys, datasets, colors_file_path):

    with open(colors_file_path, "r") as colors_file:

        colors_data = yaml.safe_load(colors_file)

        fig = go.Figure()

        #Käydään läpi kaikki tiedot
        for key in keys:
            try:
                fig.add_trace(go.Scatter(x=days, y=datasets[key], mode="lines", name=key, marker=dict(color=colors_data[key]["color"])))
            except Exception:
                fig.add_trace(go.Scatter(x=days, y=datasets[key], mode="lines", name=key, marker=dict(color=colors_data["Other"]["color"])))

    fig.update_layout(yaxis_title="t (h)", plot_bgcolor="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.show()

#Piirretään ympyrädiagrammi
def draw_pie_chart(keys, total_times, colors_file_path):

    labels = []
    colors = []

    total_hours = 0

    with open(colors_file_path, "r") as colors_file:

        colors_data = yaml.safe_load(colors_file)

        #Käydään läpi kaikki tiedot
        for index, key in enumerate(keys):

            hours = total_times[index]

            #Lisätään aika kokonaisaikaan
            total_hours += hours

            #Lisätään otsikko listoihin
            labels.append(key + " - {0} h {1} min".format(int(hours), int((hours - int(hours)) * 60)))
            try:
                colors.append(colors_data[key]["color"])
            except Exception:
                colors.append(colors_data["Other"]["color"])

    #Lisätään prosenttiosuudet selitteeseen
    for index, time in  enumerate(total_times):
        labels[index] += " ({0:.2f} %)".format(total_times[index] / total_hours * 100)

    #Piirretään ympyrädiagrammi
    fig = px.pie(names=labels, values=total_times, color_discrete_sequence=colors)
    fig.update_traces(marker=dict(line=dict(color="black", width=0.5)), textinfo="none", hovertemplate=labels)
    fig.show()

#Varsinainen ohjelma
if __name__ == "__main__":

    #Valmistellaan argumenttien lukeminen
    parser = argparse.ArgumentParser(
        description="You can use this program to show your statistics from WakaTime.",
        usage="python WakaFree.py {-h | [-g GRAPHS] [-t TOTALS] [-i IGNORE] [--start-date START_DATE] [--end-date END_DATE] FILE}")
    parser.add_argument("file", metavar="FILE", help="path to file with statistics")
    parser.add_argument("-g", "--graphs", help="show daily statistics: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-t", "--totals", help="show total times: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-i", "--ignore", help="ignored stats: string with labels separated by commas (without spaces)")
    parser.add_argument("--start-date", help="start date in format YYYY-MM-DD (inclusive)")
    parser.add_argument("--end-date", help="end date in format YYYY-MM-DD (inclusive)")

    #Luetaan argumentit
    args = parser.parse_args()
    graphs = args.graphs if args.graphs else ""
    totals = args.totals if args.totals else ""
    ignored_stats = args.ignore.split(",") if args.ignore else []
    start_date = datetime(int(args.start_date[0:4]), int(args.start_date[5:7]), int(args.start_date[8:10])).date() if args.start_date else datetime(1, 1, 1).date()
    end_date = datetime(int(args.end_date[0:4]), int(args.end_date[5:7]), int(args.end_date[8:10])).date() if args.end_date else datetime(9999, 12, 31).date()

    #Jos käyttäjä ei antanut kumpaakaan valinnaista argumenttia piirtämiseen
    if graphs == "" and totals == "":
        graphs = "leo"
        totals = "leo"

    #Jos käyttäjä antaa tiedoston
    if args.file:

        #Avataan tiedosto
        with open(args.file, "r") as file:

            #Luodaan oliot tietoja varten
            languages = LanguagesStats()
            editors = EditorsStats()
            operating_systems = OperatingSystemsStats()

            #Luetaan tiedot
            data = json.load(file)

            #Valmistellaan tietojen lukeminen
            Stats.fetch_days_and_labels(
                data,
                languages=languages.languages if "l" in (graphs + totals).lower() else None,
                editors=editors.editors if "e" in (graphs + totals).lower() else None,
                operating_systems=operating_systems.operating_systems if "o" in (graphs + totals).lower() else None,
                ignored_stats=ignored_stats)

            #Muunnetaan päivämäärät oikeaan muotoon
            Stats.convert_dates()

            #Haetaan halutut tiedot
            if "l" in (graphs + totals).lower():
                languages.populate_stats(data)
                languages.sort_stats_and_populate_keys()
            if "e" in (graphs + totals).lower():
                editors.populate_stats(data)
                editors.sort_stats_and_populate_keys()
            if "o" in (graphs + totals).lower():
                operating_systems.populate_stats(data)
                operating_systems.sort_stats_and_populate_keys()

            #Jos käyttäjä haluaa piirtää kuvaajat
            if args.graphs or (not args.graphs and not args.totals):

                #Kielten kuvaajat
                if "l" in graphs.lower():
                    draw_graph(Stats.days, languages.keys, languages.languages, "Colors/languages_colors.yml")

                #Editorien kuvaajat
                if "e" in graphs.lower():
                    draw_graph(Stats.days, editors.keys, editors.editors, "Colors/editors_colors.yml")

                #Käyttöjärjestelmien kuvaajat
                if "o" in graphs.lower():
                    draw_graph(Stats.days, operating_systems.keys, operating_systems.operating_systems, "Colors/operating_systems_colors.yml")

            #Jos käyttäjä haluaa näyttää kokonaisajat
            if args.totals or (not args.graphs and not args.totals):

                #Kielten kokonaisajat
                if "l" in totals.lower():
                    draw_pie_chart(languages.keys, languages.total_times, "Colors/languages_colors.yml")

                #Editorien kokonaisajat
                if "e" in totals.lower():
                    draw_pie_chart(editors.keys, editors.total_times, "Colors/editors_colors.yml")

                #Käyttöjärjestelmien kokonaisajat
                if "o" in totals.lower():
                    draw_pie_chart(operating_systems.keys, operating_systems.total_times, "Colors/operating_systems_colors.yml")