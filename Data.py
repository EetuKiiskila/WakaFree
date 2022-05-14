from dataclasses import dataclass
import datetime


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
