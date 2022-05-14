import json

import numpy as np

import Args
import Data
import Plotting


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
    # Parse arguments
    Args.parse()

    # User specified a file
    if Args.file_name != "":
        with open(Args.file_name, "r") as file:
            data = json.load(file)

            # Read dates and labels
            Data.fetch_dates_and_labels(data,
                                   Args.start_date,
                                   Args.end_date,
                                   Data.dates,
                                   Data.languages_stats if "l" in (Args.graphs + Args.totals).lower() else None,
                                   Data.editors_stats if "e" in (Args.graphs + Args.totals).lower() else None,
                                   Data.operating_systems_stats if "o" in (Args.graphs + Args.totals).lower() else None,
                                   searched_stats=Args.searched_stats,
                                   ignored_stats=Args.ignored_stats)

            # Covert strings to dates
            for index, date in enumerate(Data.dates):
                Data.dates[index] = Data.string_to_date(date)

            # Read and sort data
            if "l" in (Args.graphs + Args.totals).lower():
                Data.populate_stats(data, Args.start_date, Args.end_date, Data.languages_stats, Args.searched_stats, Args.ignored_stats)
                sort_stats_and_populate_keys(Data.languages_stats, Args.minimum_labeling_percentage)
            if "e" in (Args.graphs + Args.totals).lower():
                Data.populate_stats(data, Args.start_date, Args.end_date, Data.editors_stats, Args.searched_stats, Args.ignored_stats)
                sort_stats_and_populate_keys(Data.editors_stats, Args.minimum_labeling_percentage)
            if "o" in (Args.graphs + Args.totals).lower():
                Data.populate_stats(data, Args.start_date, Args.end_date, Data.operating_systems_stats, Args.searched_stats, Args.ignored_stats)
                sort_stats_and_populate_keys(Data.operating_systems_stats, Args.minimum_labeling_percentage)

            # User wants to show daily stats
            if Args.graphs != "" or (Args.graphs == "" and Args.totals == ""):
                # Languages graphs
                if "l" in Args.graphs.lower():
                    Plotting.draw_graphs(Data.dates, Data.languages_stats.keys, Data.languages_stats.daily_stats, "languages")

                # Editors graphs
                if "e" in Args.graphs.lower():
                    Plotting.draw_graphs(Data.dates, Data.editors_stats.keys, Data.editors_stats.daily_stats, "editors")

                # Operating systems graphs
                if "o" in Args.graphs.lower():
                    Plotting.draw_graphs(Data.dates,
                                         Data.operating_systems_stats.keys,
                                         Data.operating_systems_stats.daily_stats,
                                         "operating_systems")

            # User wants to show total times
            if Args.totals != "" or (Args.graphs == "" and Args.totals == ""):
                # Languages total times
                if "l" in Args.totals.lower():
                    Plotting.draw_pie_chart(Data.languages_stats.keys, Data.languages_stats.total_times, "languages")

                # Editors total times
                if "e" in Args.totals.lower():
                    Plotting.draw_pie_chart(Data.editors_stats.keys, Data.editors_stats.total_times, "editors")

                # Operating systems total times
                if "o" in Args.totals.lower():
                    Plotting.draw_pie_chart(Data.operating_systems_stats.keys,
                                            Data.operating_systems_stats.total_times,
                                            "operating_systems")

    # User did not specify a file or an optional argument
    else:
        if not Args.gui:
            print("\n"
                  "You did not specify what you would like to do."
                  " To get help, try using either of the following commands:\n\n"
                  "python WakaFree.py -h\n"
                  "python WakaFree.py --help")


# Start main program
if __name__ == "__main__":
    main()
