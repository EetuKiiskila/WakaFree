from dataclasses import dataclass
import datetime
import numpy as np


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


dates: list = []
languages_stats: Stats = Stats("languages", {}, [], [])
editors_stats: Stats = Stats("editors", {}, [], [])
operating_systems_stats: Stats = Stats("operating_systems", {}, [], [])


def seconds_to_hours(seconds):
    """Convert seconds to hours.

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
        del(stats.total_times[stats.keys.index("Other")])
        del(stats.daily_stats["Other"])
        stats.keys.remove("Other")
        return

    # Remove duplicate stats of labels moved to Other
    for index in reversed(removed_at_indexes):
        del(stats.daily_stats[stats.keys[index]])
        del(stats.keys[index])
        del(stats.total_times[index])
