import argparse
import json
import datetime

import GUI
import Data
import Plotting


parser: argparse.ArgumentParser
args: argparse.Namespace

file_name: str
graphs: str
totals: str
ignored_stats: list
searched_stats: list
minimum_labeling_percentage: float
start_date: datetime.date
end_date: datetime.date
gui: bool


def initialize_parser() -> None:
    """Initialize argparse parser."""
    global parser

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


def parse() -> None:
    """Parse arguments."""
    global args
    global file_name
    global graphs
    global totals
    global ignored_stats
    global searched_stats
    global minimum_labeling_percentage
    global start_date
    global end_date
    global gui

    initialize_parser()
    args = parser.parse_args()

    # Argument values
    file_name = args.file if args.file else ""
    graphs = args.graphs if args.graphs else ""
    totals = args.totals if args.totals else ""
    ignored_stats = args.ignore.split(",") if args.ignore else []
    searched_stats = args.search.split(",") if args.search else []
    minimum_labeling_percentage = float(args.minimum_labeling_percentage) if args.minimum_labeling_percentage else 0.0
    start_date = datetime.date(int(args.start_date[0:4]), int(args.start_date[5:7]), int(args.start_date[8:10]))\
        if args.start_date else datetime.date(1, 1, 1)
    end_date = datetime.date(int(args.end_date[0:4]), int(args.end_date[5:7]), int(args.end_date[8:10]))\
        if args.end_date else datetime.date(9999, 12, 31)
    gui = True if args.gui else False

    # Read values with GUI if user wants to
    if gui:
        GUI.show()

    execute_command()


def execute_command() -> None:
    """Execute command specified by arguments."""

    # User specified a file
    if file_name != "":
        with open(file_name, "r") as file:
            user_data = json.load(file)

            # Read dates and labels
            Data.fetch_dates_and_labels(user_data)

            # Convert strings to dates
            for index, date in enumerate(Data.dates):
                Data.dates[index] = Data.string_to_date(date)

            # Read and sort data
            if "l" in (graphs + totals).lower():
                Data.populate_stats(user_data, Data.languages_stats)
                Data.sort_stats_and_populate_keys(Data.languages_stats)
            if "e" in (graphs + totals).lower():
                Data.populate_stats(user_data, Data.editors_stats)
                Data.sort_stats_and_populate_keys(Data.editors_stats)
            if "o" in (graphs + totals).lower():
                Data.populate_stats(user_data, Data.operating_systems_stats)
                Data.sort_stats_and_populate_keys(Data.operating_systems_stats)

            # Daily stats
            if graphs != "" or (graphs == "" and totals == ""):
                # Languages
                if "l" in graphs.lower():
                    Plotting.draw_graphs(Data.dates, Data.languages_stats)
                # Editors
                if "e" in graphs.lower():
                    Plotting.draw_graphs(Data.dates, Data.editors_stats)
                # Operating systems
                if "o" in graphs.lower():
                    Plotting.draw_graphs(Data.dates, Data.operating_systems_stats)

            # Total times
            if totals != "" or (graphs == "" and totals == ""):
                # Languages
                if "l" in totals.lower():
                    Plotting.draw_pie_chart(Data.languages_stats)
                # Editors
                if "e" in totals.lower():
                    Plotting.draw_pie_chart(Data.editors_stats)
                # Operating systems
                if "o" in totals.lower():
                    Plotting.draw_pie_chart(Data.operating_systems_stats)

    # User did not give a file or an optional argument
    else:
        if not gui:
            print("\n"
                  "You did not specify what you would like to do."
                  " To get help, try using either of the following commands:\n\n"
                  "python WakaFree.py -h\n"
                  "python WakaFree.py --help")
