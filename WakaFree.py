import argparse
import json
import datetime
from dataclasses import dataclass

import numpy as np

import GraphicalUserInterface
import Plotting


@dataclass
class Stats:
    """Data class that can store statistics read from a WakaTime JSON file.

    :ivar type_: The type of the object. Possible values: "languages", "editors", "operating_systems".
    :ivar daily_stats: Container for daily stats. Should be initialized as an empty dict.
    :ivar keys: Container for labels. Should be initialized as an empty list.
    :ivar total_times: Container for total times. Should be initialized as an empty list.
    """
    type_: str
    daily_stats: dict
    keys: list
    total_times: list


def seconds_to_hours(seconds):
    """Convert seconds to hours

    :param seconds: Time in seconds.
    :return: Time in hours.
    """
    return seconds / 3600


def string_to_date(date_string):
    """Convert a string to a datetime date.

    :param date_string: Date string in format YYYY-MM-DD.
    :return: Date as a datetime date.
    """
    return datetime.datetime(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10])).date()


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


def fetch_labels_of_a_day(day, stats, searched_stats, ignored_stats):
    if stats is not None:
        for label in day[stats.type_]:
            if label["name"] in stats.daily_stats:
                continue
            if len(searched_stats) == 0:
                if label["name"] in ignored_stats:
                    continue
                stats.daily_stats[label["name"]] = []
            else:
                if label["name"] not in searched_stats:
                    continue
                stats.daily_stats[label["name"]] = []


def fetch_dates_and_labels(wakatime_json,
                           start_date,
                           end_date,
                           dates,
                           languages_stats,
                           editors_stats,
                           operating_systems_stats,
                           searched_stats,
                           ignored_stats):
    """Read dates in given file.

    :param wakatime_json: Stats from WakaTime.
    :param start_date: Start date to ignore dates before.
    :param end_date: End date to ignore dates after.
    :param dates: List to store dates in.
    :param languages_stats: Dict to create lists for stats in with languages as keys.
    :param editors_stats: Dict to create lists for stats in with editors as keys.
    :param operating_systems_stats: Dict to create lists for stats in with operating systems as keys.
    :param searched_stats: List of labels to search for.
    :param ignored_stats: List of labels to ignore.
    """
    for day in wakatime_json["days"]:
        # Skip day if not in given range
        if day["date"] < str(start_date) or day["date"] > str(end_date):
            continue
        else:
            # Add date to the list of dates
            dates.append(day["date"])

            # Add language labels to the list of languages
            if languages_stats is not None:
                fetch_labels_of_a_day(day, languages_stats, searched_stats, ignored_stats)

            # Add editor labels to the list of editors
            if editors_stats is not None:
                fetch_labels_of_a_day(day, editors_stats, searched_stats, ignored_stats)

            # Add operating system labels to the list of operating systems
            if operating_systems_stats is not None:
                fetch_labels_of_a_day(day, operating_systems_stats, searched_stats, ignored_stats)


def populate_stats(wakatime_json, start_date, end_date, stats, searched_stats, ignored_stats):
    """Read daily stats in given file for operating systems.

    :param wakatime_json: Stats from WakaTime.
    :param start_date: Start date to ignore dates before.
    :param end_date: End date to ignore dates after.
    :param stats: Object of type Stats.
    :param searched_stats: List of labels to search for.
    :param ignored_stats: List of labels to ignore.
    """

    # How many days have been processed
    number_of_days = 0

    # Loop through all days
    for day in wakatime_json["days"]:
        # Skip day depending on start and end dates
        if day["date"] < str(start_date):
            continue
        elif day["date"] > str(end_date):
            continue

        # Increment how many days have been processed
        number_of_days += 1

        # No stats of specified type for the day
        if len(day[stats.type_]) == 0:
            # Add 0 hours to all labels for the day
            for label in stats.daily_stats:
                stats.daily_stats[label].append(0.0)

        # Stats of specified type exist for the day
        else:
            # Loop through labels
            for label in day[stats.type_]:
                # Skip the label depending on user input
                if len(searched_stats) == 0:
                    if label["name"] in ignored_stats:
                        continue
                else:
                    if label["name"] not in searched_stats:
                        continue

                # Add label's stats for the day converted to hours
                stats.daily_stats[label["name"]]\
                    .append(seconds_to_hours(label["total_seconds"]))

        # Loop through labels
        for label in stats.daily_stats:
            # If the label has no stats for the day add 0 hours
            if len(stats.daily_stats[label]) < number_of_days:
                stats.daily_stats[label].append(0.0)


def unify_stats(stats, minimum_labeling_percentage):
    """Group stats under the label Other.

    :param stats: Object of type stats.
    :param minimum_labeling_percentage: Anything less than this percentage will be moved under the label Other.
    """
    removed_at_indexes = []

    # Add label other if not already present
    if "Other" not in stats.keys:
        stats.keys.append("Other")
        stats.total_times.append(0.0)
        stats.daily_stats["Other"] = [0.0 for value in stats.daily_stats[stats.keys[0]]]

    # Move stats with low percentage under the label Other
    for index, total_time in enumerate(stats.total_times):
        if stats.keys[index] == "Other":
            continue
        elif total_time / sum(stats.total_times) * 100.0 < minimum_labeling_percentage:
            stats.daily_stats["Other"] = np.add(stats.daily_stats["Other"], stats.daily_stats[stats.keys[index]]).tolist()
            stats.total_times[stats.keys.index("Other")] += stats.total_times[index]
            removed_at_indexes.append(index)

    # Remove the label Other if it is not used
    if len(removed_at_indexes) == 0:
        del (stats.total_times[stats.keys.index("Other")])
        del (stats.total_times["Other"])
        stats.keys.remove("Other")
        return

    # Remove duplicate stats of labels moved to Other
    for index in reversed(removed_at_indexes):
        del(stats.daily_stats[stats.keys[index]])
        del(stats.keys[index])
        del(stats.total_times[index])


def sort_stats_and_populate_keys(stats, minimum_labeling_percentage):
    """Sort the stats from most common to least common.

    :param stats: Object of type Stats.
    :param minimum_labeling_percentage: Stats are moved under the label Other according to this percentage.
    """
    total_hours = 0

    # Loop through labels
    for label in stats.daily_stats:
        # Total times for each label
        hours = sum(stats.daily_stats[label])

        # Add to total time of all labels
        total_hours += hours

        # Add to total times and keys of the label
        stats.total_times.append(hours)
        stats.keys.append(label)

    # Unify stats according to user input
    if minimum_labeling_percentage != 0.0:
        unify_stats(stats, minimum_labeling_percentage)

    # Reorder from most used to least used
    stats.total_times, stats.keys = zip(*sorted(zip(stats.total_times, stats.keys), reverse=True))


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
    start_date = datetime.datetime(int(args.start_date[0:4]),
                          int(args.start_date[5:7]),
                          int(args.start_date[8:10])).date() if args.start_date else datetime.datetime(1, 1, 1).date()
    end_date = datetime.datetime(int(args.end_date[0:4]),
                        int(args.end_date[5:7]),
                        int(args.end_date[8:10])).date() if args.end_date else datetime.datetime(9999, 12, 31).date()

    # Read values with GUI if user wants to
    if args.gui:
        file_name, graphs, totals, ignored_stats, searched_stats, minimum_labeling_percentage, start_date, end_date\
            = GraphicalUserInterface.initialize_gui()

    dates = []

    languages_stats = Stats("languages", {}, [], [])
    editors_stats = Stats("editors", {}, [], [])
    operating_systems_stats = Stats("operating_systems", {}, [], [])

    # User specified a file
    if file_name != "":
        with open(file_name, "r") as file:
            data = json.load(file)

            # Read dates and labels
            fetch_dates_and_labels(data,
                                   start_date,
                                   end_date,
                                   dates,
                                   languages_stats if "l" in (graphs + totals).lower() else None,
                                   editors_stats if "e" in (graphs + totals).lower() else None,
                                   operating_systems_stats if "o" in (graphs + totals).lower() else None,
                                   searched_stats=searched_stats,
                                   ignored_stats=ignored_stats)

            # Covert strings to dates
            for index, date in enumerate(dates):
                dates[index] = string_to_date(date)

            # Read and sort data
            if "o" in (graphs + totals).lower():
                # Languages
                populate_stats(data, start_date, end_date, languages_stats, searched_stats, ignored_stats)
                sort_stats_and_populate_keys(languages_stats, minimum_labeling_percentage)

                # Editors
                populate_stats(data, start_date, end_date, editors_stats, searched_stats, ignored_stats)
                sort_stats_and_populate_keys(editors_stats, minimum_labeling_percentage)

                # Operating systems
                populate_stats(data, start_date, end_date, operating_systems_stats, searched_stats, ignored_stats)
                sort_stats_and_populate_keys(operating_systems_stats, minimum_labeling_percentage)

            # User wants to show daily stats
            if graphs != "" or (graphs == "" and totals == ""):
                # Languages graphs
                if "l" in graphs.lower():
                    Plotting.draw_graphs(dates, languages_stats.keys, languages_stats.daily_stats, "languages")

                # Editors graphs
                if "e" in graphs.lower():
                    Plotting.draw_graphs(dates, editors_stats.keys, editors_stats.daily_stats, "editors")

                # Operating systems graphs
                if "o" in graphs.lower():
                    Plotting.draw_graphs(dates,
                                         operating_systems_stats.keys,
                                         operating_systems_stats.daily_stats,
                                         "operating_systems")

            # User wants to show total times
            if totals != "" or (graphs == "" and totals == ""):
                # Languages total times
                if "l" in totals.lower():
                    Plotting.draw_pie_chart(languages_stats.keys, languages_stats.total_times, "languages")

                # Editors total times
                if "e" in totals.lower():
                    Plotting.draw_pie_chart(editors_stats.keys, editors_stats.total_times, "editors")

                # Operating systems total times
                if "o" in totals.lower():
                    Plotting.draw_pie_chart(operating_systems_stats.keys,
                                            operating_systems_stats.total_times,
                                            "operating_systems")

    # User did not specify a file or an optional argument
    else:
        if not args.gui:
            print("\n"
                  "You did not specify what you would like to do."
                  " To get help, try using either of the following commands:\n\n"
                  "python WakaFree.py -h\n"
                  "python WakaFree.py --help")


# Start main program
if __name__ == "__main__":
    main()
