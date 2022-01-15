import os.path
import argparse
import json
import yaml
from datetime import datetime
import numpy as np
import plotly.express as px
import GraphicalUserInterface
import Plotting


def string_to_date(date_string):
    """Convert a string to a datetime date.

    :param date_string: Date string in format YYYY-MM-DD.
    :return: Date as a datetime date.
    """
    return datetime(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10])).date()


def initialize_argument_parser():
    """Initialize and return an argparse parser with description, usage help and arguments to parse.

    :return: Parser of type argparse.ArgumentParser.
    """
    parser = argparse.ArgumentParser(description="You can use this program to show your statistics from WakaTime.",
                                     usage=("python WakaFree.py {-h | -G | [-g GRAPHS] [-t TOTALS]"
                                            " [{-i IGNORE | -s SEARCH}] [-m MINIMUM_LABELING_PERCENTAGE]"
                                            " [--start-date START_DATE] [--end-date END_DATE] FILE}"))

    parser.add_argument("file", metavar="FILE", nargs="?", default="", help="path to file with statistics")
    parser.add_argument("-G", "--gui", action="store_true", help="use graphical user interface")
    parser.add_argument("-g", "--graphs",
                        help="show daily statistics: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-t", "--totals",
                        help="show total times: string with l, e, o for languages, editors, operating systems")
    parser.add_argument("-i", "--ignore", help="ignored stats: string with labels separated by commas (without spaces)")
    parser.add_argument("-s", "--search",
                        help="stats to search for: string with labels separated by commas (without spaces)")
    parser.add_argument("-m", "--minimum-labeling-percentage",
                        help="add together (under label Other) stats with lesser percentage than the given value")
    parser.add_argument("--start-date", help="start date in format YYYY-MM-DD (inclusive)")
    parser.add_argument("--end-date", help="end date in format YYYY-MM-DD (inclusive)")

    return parser


def fetch_dates_and_labels(wakatime_json,
                           start_date,
                           end_date, dates,
                           languages=None,
                           editors=None,
                           operating_systems=None,
                           ignored_stats=[],
                           searched_stats=[]):
    """Read dates in given file.

    :param wakatime_json: Stats from WakaTime.
    :param start_date: Start date to ignore dates before.
    :param end_date: End date to ignore dates after.
    :param dates: List to store dates in.
    :param languages: List to store labels of languages in.
    :param editors: List to store labels of editors in.
    :param operating_systems: List to store labels of operating systems in.
    """
    for day in wakatime_json["days"]:
        # Skip day if not in given range
        if day["date"] < str(start_date) or day["date"] > str(end_date):
            continue
        else:
            # Add date to the list of dates
            dates.append(day["date"])

            # Add language labels to the list of languages
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

            # Add editor labels to the list of editors
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

            # Add operating system labels to the list of operating systems
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


class Stats:
    """Class that contains stats and methods for modifying them."""
    days = []

    @classmethod
    def convert_dates(cls, days=days):
        '''Muuntaa merkkijonoina olevat päivämäärät oikean tyyppisiksi.'''
        for index, day in enumerate(days):
            days[index] = string_to_date(day)

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


def main():
    # Initialize argument parser
    parser = initialize_argument_parser()

    # Read arguments
    args = parser.parse_args()
    file_name = args.file if args.file else ""
    graphs = args.graphs if args.graphs else ""
    totals = args.totals if args.totals else ""
    ignored_stats = args.ignore.split(",") if args.ignore else []
    searched_stats = args.search.split(",") if args.search else []
    minimum_labeling_percentage = float(args.minimum_labeling_percentage) if args.minimum_labeling_percentage else 0.0
    start_date = datetime(int(args.start_date[0:4]),
                          int(args.start_date[5:7]),
                          int(args.start_date[8:10])).date() if args.start_date else datetime(1, 1, 1).date()
    end_date = datetime(int(args.end_date[0:4]),
                        int(args.end_date[5:7]),
                        int(args.end_date[8:10])).date() if args.end_date else datetime(9999, 12, 31).date()

    # Read values with GUI if user wants to
    if args.gui:
        file_name, graphs, totals, ignored_stats, searched_stats, minimum_labeling_percentage, start_date, end_date\
            = GraphicalUserInterface.initialize_gui()

    days = []


#Varsinainen ohjelma
if __name__ == "__main__":

    #Valmistellaan argumenttien lukeminen
    parser = initialize_argument_parser()

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
        file_name, graphs, totals, ignored_stats, searched_stats, minimum_labeling_percentage, start_date, end_date\
            = GraphicalUserInterface.initialize_gui()

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
                    Plotting.draw_graphs(Stats.days, languages.keys, languages.languages, "languages")

                #Editorien kuvaajat
                if "e" in graphs.lower():
                    Plotting.draw_graphs(Stats.days, editors.keys, editors.editors, "editors")

                #Käyttöjärjestelmien kuvaajat
                if "o" in graphs.lower():
                    Plotting.draw_graphs(Stats.days, operating_systems.keys, operating_systems.operating_systems, "operating_systems")

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

    #Jos käyttäjä ei antanut tiedostoa tai mitään vaihtoehtoista argumenttia
    else:
        if not args.gui:
            print("\nYou did not specify what you would like to do. To get help, try using either of the following commands:\n\npython WakaFree.py -h\npython WakaFree.py --help")
