import dataclasses
import enum
import datetime
import json

import numpy as np

import Args


class StatsType(enum.Enum):
    LANGUAGES = enum.auto()
    EDITORS = enum.auto()
    OPERATING_SYSTEMS = enum.auto()
    UNKNOWN = enum.auto()


@dataclasses.dataclass
class Stats:
    """Data class that can store statistics read from a WakaTime JSON file.

    :ivar type_: The type of the object.
    :ivar daily_stats: Container for daily stats.
    :ivar keys: Container for labels.
    :ivar total_times: Container for total times.
    """
    type_: StatsType = StatsType.UNKNOWN
    daily_stats: dict = dataclasses.field(default_factory=dict)
    keys: list = dataclasses.field(default_factory=list)
    total_times: list = dataclasses.field(default_factory=list)


dates: list = []
languages_stats: Stats = Stats(StatsType.LANGUAGES)
editors_stats: Stats = Stats(StatsType.EDITORS)
operating_systems_stats: Stats = Stats(StatsType.OPERATING_SYSTEMS)


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
    return datetime.date(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10]))


def fetch_keys(date: dict):
    """Get keys for stats.

    :param date: Date.
    """

    # Languages
    for language in date["languages"]:
        if "l" not in (Args.graphs + Args.totals).lower():
            break
        if len(Args.searched_stats) == 0:
            if language["name"] in Args.ignored_stats:
                continue
            languages_stats.daily_stats.setdefault(language["name"], [])
        else:
            if language["name"] not in Args.searched_stats:
                continue
            languages_stats.daily_stats.setdefault(language["name"], [])

    # Editors
    for editor in date["editors"]:
        if "e" not in (Args.graphs + Args.totals).lower():
            break
        if len(Args.searched_stats) == 0:
            if editor["name"] in Args.ignored_stats:
                continue
            editors_stats.daily_stats.setdefault(editor["name"], [])
        else:
            if editor["name"] not in Args.searched_stats:
                continue
            editors_stats.daily_stats.setdefault(editor["name"], [])

    # Operating systems
    for operating_system in date["operating_systems"]:
        if "o" not in (Args.graphs + Args.totals).lower():
            break
        if len(Args.searched_stats) == 0:
            if operating_system["name"] in Args.ignored_stats:
                continue
            operating_systems_stats.daily_stats.setdefault(operating_system["name"], [])
        else:
            if operating_system["name"] not in Args.searched_stats:
                continue
            operating_systems_stats.daily_stats.setdefault(operating_system["name"], [])


def read_stats(file_path: str) -> None:
    # Open file
    with open(file_path, "r") as file:
        stats = json.load(file)

        # Loop dates
        for date in stats["days"]:
            # Skip day if not in given range
            if date["date"] < str(Args.start_date) or date["date"] > str(Args.end_date):
                continue

            # Add date to list
            dates.append(string_to_date(date["date"]))

            # Fetch keys for stats
            fetch_keys(date)


def populate_stats(wakatime_json, stats):
    """Read daily stats in given file for operating systems.

    :param wakatime_json: Stats from WakaTime.
    :param stats: Object of type Stats.
    """

    # Loop through all days
    for day in wakatime_json["days"]:
        # Skip day depending on start and end dates
        if day["date"] < str(Args.start_date):
            continue
        elif day["date"] > str(Args.end_date):
            continue

        # Loop labels and append stats
        for label in stats.daily_stats.keys():
            # Stats for the type
            stats_of_the_day = day[stats.type_.name.lower()]

            # Add stats to label
            stats.daily_stats[label].append(seconds_to_hours(
                next((stat["total_seconds"] for stat in stats_of_the_day if stat["name"] == label), 0.0)
            ))


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


def sort_stats_and_populate_keys(stats):
    """Sort the stats from most common to least common.

    :param stats: Object of type Stats.
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
    if Args.minimum_labeling_percentage != 0.0:
        unify_stats(stats, Args.minimum_labeling_percentage)

    # Reorder from most used to least used
    stats.total_times, stats.keys = zip(*sorted(zip(stats.total_times, stats.keys), reverse=True))
