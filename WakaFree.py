import os.path
import json
import yaml
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import argparse
import ctypes
import PySimpleGUI as sg

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
    def fetch_days_and_labels(data, days=days, languages=None, editors=None, operating_systems=None, ignored_stats=[], searched_stats=[]):
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
                    if len(searched_stats) == 0:
                        if language["name"] in ignored_stats:
                            continue
                        elif language["name"] not in languages:
                            languages[language["name"]] = []
                    else:
                        if language["name"] not in searched_stats:
                            continue
                        elif language["name"] not in languages:
                            languages[language["name"]] = []
        
            #Editorit
            if editors is not None:
                for editor in day["editors"]:
                    if len(searched_stats) == 0:
                        if editor["name"] in ignored_stats:
                            continue
                        elif editor["name"] not in editors:
                            editors[editor["name"]] = []
                    else:
                        if editor["name"] not in searched_stats:
                            continue
                        elif editor["name"] not in editors:
                            editors[editor["name"]] = []

            #Käyttöjärjestelmät
            if operating_systems is not None:
                for operating_system in day["operating_systems"]:
                    if len(searched_stats) == 0:
                        if operating_system["name"] in ignored_stats:
                            continue
                        elif operating_system["name"] not in operating_systems:
                            operating_systems[operating_system["name"]] = []
                    else:
                        if operating_system["name"] not in searched_stats:
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
        #Kuinka monen päivän tiedot on lisätty kieliin
        number_of_days = 0

        #Käydään läpi kaikki päivät
        for day in data["days"]:

            #Ohitetaan päivä käyttäjän antamista argumenteista riippuen
            if day["date"] < str(start_date):
                continue
            elif day["date"] > str(end_date):
                continue

            number_of_days += 1

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
                    if len(searched_stats) == 0:
                        if language["name"] in ignored_stats:
                            continue
                    else:
                        if language["name"] not in searched_stats:
                            continue

                    #Lisätään kieleen kyseisen päivän tiedot tunneiksi muutettuna
                    self.languages[language["name"]].append(Stats.seconds_to_hours(language["total_seconds"]))

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

        if minimum_labeling_percentage != 0.0:
            self.unify_stats()

        #Muutetaan järjestys eniten käytetystä vähiten käytettyyn, muuttuvat tupleiksi
        self.total_times, self.keys = zip(*sorted(zip(self.total_times, self.keys), reverse=True))

    def unify_stats(self):
        '''Yhdistää tiedot otsikon Other alle tietyn raja-arvon mukaisesti.'''
        removed_at_indexes = []

        #Lisätään tarvittaessa otsikko Other
        if "Other" not in self.keys:
            self.keys.append("Other")
            self.total_times.append(0.0)
            self.languages["Other"] = [0.0 for value in self.languages[self.keys[0]]]

        #Lisätään raja-arvon alittavat osuudet Otheriin
        for index, total_time in enumerate(self.total_times):
            if self.keys[index] == "Other":
                continue
            elif total_time / sum(self.total_times) * 100.0 < minimum_labeling_percentage:
                self.languages["Other"] = np.add(self.languages["Other"], self.languages[self.keys[index]]).tolist()
                self.total_times[self.keys.index("Other")] += self.total_times[index]
                removed_at_indexes.append(index)

        #Poistetaan Other-otsikko ja sen tiedot, jos se on turha, ja poistutaan metodista
        if len(removed_at_indexes) == 0:
            del(self.total_times[self.keys.index("Other")])
            del(self.languages["Other"])
            self.keys.remove("Other")
            return

        #Poistetaan Otheriin yhdistettyjen tietojen päivittäiset tiedot, otsikot ja kokonaisajat
        for index in reversed(removed_at_indexes):
            del(self.languages[self.keys[index]])
            del(self.keys[index])
            del(self.total_times[index])

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
        #Kuinka monen päivän tiedot on lisätty editoreihin
        number_of_days = 0

        #Käydään läpi kaikki päivät
        for day in data["days"]:

            #Ohitetaan päivä käyttäjän antamista argumenteista riippuen
            if day["date"] < str(start_date):
                continue
            elif day["date"] > str(end_date):
                continue

            number_of_days += 1

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
                    if len(searched_stats) == 0:
                        if editor["name"] in ignored_stats:
                            continue
                    else:
                        if editor["name"] not in searched_stats:
                            continue

                    #Lisätään editoriin kyseisen päivän tiedot tunneiksi muutettuna
                    self.editors[editor["name"]].append(Stats.seconds_to_hours(editor["total_seconds"]))

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

        if minimum_labeling_percentage != 0.0:
            self.unify_stats()

        #Muutetaan järjestys eniten käytetystä vähiten käytettyyn, muuttuvat tupleiksi
        self.total_times, self.keys = zip(*sorted(zip(self.total_times, self.keys), reverse=True))

    def unify_stats(self):
        '''Yhdistää tiedot otsikon Other alle tietyn raja-arvon mukaisesti.'''
        removed_at_indexes = []

        #Lisätään tarvittaessa otsikko Other
        if "Other" not in self.keys:
            self.keys.append("Other")
            self.total_times.append(0.0)
            self.editors["Other"] = [0.0 for value in self.editors[self.keys[0]]]

        #Lisätään raja-arvon alittavat osuudet Otheriin
        for index, total_time in enumerate(self.total_times):
            if self.keys[index] == "Other":
                continue
            elif total_time / sum(self.total_times) * 100.0 < minimum_labeling_percentage:
                self.editors["Other"] = np.add(self.editors["Other"], self.editors[self.keys[index]]).tolist()
                self.total_times[self.keys.index("Other")] += self.total_times[index]
                removed_at_indexes.append(index)

        #Poistetaan Other-otsikko ja sen tiedot, jos se on turha, ja poistutaan metodista
        if len(removed_at_indexes) == 0:
            del(self.total_times[self.keys.index("Other")])
            del(self.editors["Other"])
            self.keys.remove("Other")
            return

        #Poistetaan Otheriin yhdistettyjen tietojen päivittäiset tiedot, otsikot ja kokonaisajat
        for index in reversed(removed_at_indexes):
            del(self.editors[self.keys[index]])
            del(self.keys[index])
            del(self.total_times[index])

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
        #Kuinka monen päivän tiedot on lisätty käyttöjärjestelmiin
        number_of_days = 0

        #Käydään läpi kaikki päivät
        for day in data["days"]:

            #Ohitetaan päivä käyttäjän antamista argumenteista riippuen
            if day["date"] < str(start_date):
                continue
            elif day["date"] > str(end_date):
                continue

            number_of_days += 1

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
                    if len(searched_stats) == 0:
                        if operating_system["name"] in ignored_stats:
                            continue
                    else:
                        if operating_system["name"] not in searched_stats:
                            continue

                    #Lisätään käyttöjärjestelmään kyseisen päivän tiedot tunneiksi muutettuna
                    self.operating_systems[operating_system["name"]].append(Stats.seconds_to_hours(operating_system["total_seconds"]))

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

        if minimum_labeling_percentage != 0.0:
            self.unify_stats()

        #Muutetaan järjestys eniten käytetystä vähiten käytettyyn, muuttuvat tupleiksi
        self.total_times, self.keys = zip(*sorted(zip(self.total_times, self.keys), reverse=True))

    def unify_stats(self):
        '''Yhdistää tiedot otsikon Other alle tietyn raja-arvon mukaisesti.'''
        removed_at_indexes = []

        #Lisätään tarvittaessa otsikko Other
        if "Other" not in self.keys:
            self.keys.append("Other")
            self.total_times.append(0.0)
            self.operating_systems["Other"] = [0.0 for value in self.operating_systems[self.keys[0]]]

        #Lisätään raja-arvon alittavat osuudet Otheriin
        for index, total_time in enumerate(self.total_times):
            if self.keys[index] == "Other":
                continue
            elif total_time / sum(self.total_times) * 100.0 < minimum_labeling_percentage:
                self.operating_systems["Other"] = np.add(self.operating_systems["Other"], self.operating_systems[self.keys[index]]).tolist()
                self.total_times[self.keys.index("Other")] += self.total_times[index]
                removed_at_indexes.append(index)

        #Poistetaan Other-otsikko ja sen tiedot, jos se on turha, ja poistutaan metodista
        if len(removed_at_indexes) == 0:
            del(self.total_times[self.keys.index("Other")])
            del(self.operating_systems["Other"])
            self.keys.remove("Other")
            return

        #Poistetaan Otheriin yhdistettyjen tietojen päivittäiset tiedot, otsikot ja kokonaisajat
        for index in reversed(removed_at_indexes):
            del(self.operating_systems[self.keys[index]])
            del(self.keys[index])
            del(self.total_times[index])

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
        usage="python WakaFree.py {-h | -G | [-g GRAPHS] [-t TOTALS] [{-i IGNORE | -s SEARCH}] [-m MINIMUM_LABELING_PERCENTAGE] [--start-date START_DATE] [--end-date END_DATE] FILE}")
    parser.add_argument("file", metavar="FILE", nargs="?", default="", help="path to file with statistics")
    parser.add_argument("-G", "--gui", action="store_true", help="use graphical user interface")
    parser.add_argument("-g", "--graphs", help="show daily statistics: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-t", "--totals", help="show total times: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-i", "--ignore", help="ignored stats: string with labels separated by commas (without spaces)")
    parser.add_argument("-s", "--search", help="stats to search for: string with labels separated by commas (without spaces)")
    parser.add_argument("-m", "--minimum-labeling-percentage", help="add together (under label Other) stats with lesser percentage than the given value")
    parser.add_argument("--start-date", help="start date in format YYYY-MM-DD (inclusive)")
    parser.add_argument("--end-date", help="end date in format YYYY-MM-DD (inclusive)")

    #Luetaan argumentit
    args = parser.parse_args()
    file_name = args.file if args.file else ""
    graphs = args.graphs if args.graphs else ""
    totals = args.totals if args.totals else ""
    ignored_stats = args.ignore.split(",") if args.ignore else []
    searched_stats = args.search.split(",") if args.search else []
    minimum_labeling_percentage = float(args.minimum_labeling_percentage) if args.minimum_labeling_percentage else 0.0
    start_date = datetime(int(args.start_date[0:4]), int(args.start_date[5:7]), int(args.start_date[8:10])).date() if args.start_date else datetime(1, 1, 1).date()
    end_date = datetime(int(args.end_date[0:4]), int(args.end_date[5:7]), int(args.end_date[8:10])).date() if args.end_date else datetime(9999, 12, 31).date()

    #Jos käyttäjä haluaa graafisen käyttöliittymän
    if args.gui:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
        except:
            pass

        help_file = "The file that contains your statistics."
        help_graphs = "Daily statistics."
        help_totals = "Total times."
        help_ignore = "Ignored stats. Labels separated by commas and nothing more."
        help_search = "Stats to search for. Labels separated by commas and nothing more.\nIf nothing is entered then all the stats in the given file will be read."
        help_minimum_labeling_percentage = "Inclusive lover limit for labeling the stats.\nEverything under this percentage will be moved to the group Other."
        help_start_date = "Start date in format YYYY-MM-DD. Inclusive.\nIf no date is entered then the stats will be drawn from the very beginning."
        help_end_date = "End date in format YYYY-MM-DD. Inclusive.\nIf no date is entered then the stats will be drawn to the very end."

        layout = [
            [sg.Text("Hover over a variable name to get help.")],
            [sg.HorizontalSeparator()],
            [sg.Text("File*", tooltip=help_file), sg.InputText(key="input_file"), sg.FileBrowse(file_types=(("JSON Files", "*.json"),))],
            [
                sg.Text("Graphs", tooltip=help_graphs),
                sg.Checkbox("Languages", default=True, key="input_graphs_l"),
                sg.Checkbox("Editors", default=True, key="input_graphs_e"),
                sg.Checkbox("Operating systems", default=True, key="input_graphs_o")
            ],
            [
                sg.Text("Totals", tooltip=help_totals),
                sg.Checkbox("Languages", default=True, key="input_totals_l"),
                sg.Checkbox("Editors", default=True, key="input_totals_e"),
                sg.Checkbox("Operating systems", default=True, key="input_totals_o")
            ],
            [sg.Text("Ignore**", tooltip=help_ignore), sg.InputText(key="input_ignore"), sg.Text("or"), sg.Text("Search**", tooltip=help_search), sg.InputText(key="input_search")],
            [sg.Text("Minimum labeling percentage", tooltip=help_minimum_labeling_percentage), sg.InputText("0.0", key="input_minimum_labeling_percentage"), sg.Text("%")],
            [sg.Text("Start date", tooltip=help_start_date), sg.InputText("YYYY-MM-DD", key="input_start_date"), sg.CalendarButton("Calendar", format="%Y-%m-%d")],
            [sg.Text("End date", tooltip=help_end_date), sg.InputText("YYYY-MM-DD", key="input_end_date"), sg.CalendarButton("Calendar", format="%Y-%m-%d")],
            [sg.OK()],
            [sg.HorizontalSeparator()],
            [sg.Text("* Required.")],
            [sg.Text("** Labels separated by commas only.")]
        ]

        window = sg.Window("WakaFree", layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            elif event == "OK":
                file_name = values["input_file"]

                graphs += "l" if values["input_graphs_l"] else ""
                graphs += "e" if values["input_graphs_e"] else ""
                graphs += "o" if values["input_graphs_o"] else ""

                totals += "l" if values["input_totals_l"] else ""
                totals += "e" if values["input_totals_e"] else ""
                totals += "o" if values["input_totals_o"] else ""

                ignored_stats = values["input_ignore"].split(",") if values["input_ignore"] != "" else []
                searched_stats = values["input_search"].split(",") if values["input_search"] != "" else []

                minimum_labeling_percentage = float(values["input_minimum_labeling_percentage"])

                try:
                    start_date = datetime(int(values["input_start_date"][0:4]), int(values["input_start_date"][5:7]), int(values["input_start_date"][8:10])).date()
                except:
                    start_date = datetime(1, 1, 1).date()
                try:
                    end_date = datetime(int(values["input_end_date"][0:4]), int(values["input_end_date"][5:7]), int(values["input_end_date"][8:10])).date()
                except:
                    end_date = datetime(9999, 12, 31).date()

                break

        window.close()

    #Jos käyttäjä ei antanut kumpaakaan valinnaista argumenttia piirtämiseen
    if graphs == "" and totals == "":
        graphs = "leo"
        totals = "leo"

    #Jos käyttäjä antaa tiedoston
    if file_name != "":

        #Avataan tiedosto
        with open(file_name, "r") as file:

            #Projektin hakemisto
            project_directory = os.path.dirname(__file__)

            #Luodaan oliot tietoja varten
            languages = LanguagesStats()
            editors = EditorsStats()
            operating_systems = OperatingSystemsStats()

            #Haetaan tiedot
            data = json.load(file)

            #Valmistellaan tietojen lukeminen
            Stats.fetch_days_and_labels(
                data,
                languages=languages.languages if "l" in (graphs + totals).lower() else None,
                editors=editors.editors if "e" in (graphs + totals).lower() else None,
                operating_systems=operating_systems.operating_systems if "o" in (graphs + totals).lower() else None,
                ignored_stats=ignored_stats, searched_stats=searched_stats)

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
            if graphs != "" or (graphs == "" and totals == ""):

                #Kielten kuvaajat
                if "l" in graphs.lower():
                    draw_graph(Stats.days, languages.keys, languages.languages, os.path.join(project_directory, "Colors/languages_colors.yml"))

                #Editorien kuvaajat
                if "e" in graphs.lower():
                    draw_graph(Stats.days, editors.keys, editors.editors, os.path.join(project_directory, "Colors/editors_colors.yml"))

                #Käyttöjärjestelmien kuvaajat
                if "o" in graphs.lower():
                    draw_graph(Stats.days, operating_systems.keys, operating_systems.operating_systems, os.path.join(project_directory, "Colors/operating_systems_colors.yml"))

            #Jos käyttäjä haluaa näyttää kokonaisajat
            if totals != "" or (graphs == "" and totals == ""):

                #Kielten kokonaisajat
                if "l" in totals.lower():
                    draw_pie_chart(languages.keys, languages.total_times, os.path.join(project_directory, "Colors/languages_colors.yml"))

                #Editorien kokonaisajat
                if "e" in totals.lower():
                    draw_pie_chart(editors.keys, editors.total_times, os.path.join(project_directory, "Colors/editors_colors.yml"))

                #Käyttöjärjestelmien kokonaisajat
                if "o" in totals.lower():
                    draw_pie_chart(operating_systems.keys, operating_systems.total_times, os.path.join(project_directory, "Colors/operating_systems_colors.yml"))