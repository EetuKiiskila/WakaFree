import json

import Args
import Data
import Plotting


def main():
    # Parse arguments
    Args.parse()

    # User specified a file
    if Args.file_name != "":
        with open(Args.file_name, "r") as file:
            data = json.load(file)

            # Read dates and labels
            Data.fetch_dates_and_labels(data)

            # Covert strings to dates
            for index, date in enumerate(Data.dates):
                Data.dates[index] = Data.string_to_date(date)

            # Read and sort data
            if "l" in (Args.graphs + Args.totals).lower():
                Data.populate_stats(data, Data.languages_stats)
                Data.sort_stats_and_populate_keys(Data.languages_stats)
            if "e" in (Args.graphs + Args.totals).lower():
                Data.populate_stats(data, Data.editors_stats)
                Data.sort_stats_and_populate_keys(Data.editors_stats)
            if "o" in (Args.graphs + Args.totals).lower():
                Data.populate_stats(data, Data.operating_systems_stats)
                Data.sort_stats_and_populate_keys(Data.operating_systems_stats)

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


# Start main program
if __name__ == "__main__":
    main()
