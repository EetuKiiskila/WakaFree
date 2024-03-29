import os.path
import datetime

import yaml
import plotly.graph_objects as go
import plotly.express as px

import Args
import Data


project_directory: str = os.path.dirname(__file__)
colors_file_path_languages: str = os.path.join(project_directory, "Colors/languages_colors.yaml")
colors_file_path_editors: str = os.path.join(project_directory, "Colors/editors_colors.yaml")
colors_file_path_operating_systems: str = os.path.join(project_directory, "Colors/operating_systems_colors.yaml")


def draw_graphs(dates: list[datetime.date], stats: Data.Stats) -> None:
    """Draw graphs for daily stats.

    :param dates: Dates.
    :param stats: Stats.
    """
    match stats.type_:
        case Data.StatsType.LANGUAGES:
            colors_file_path = colors_file_path_languages
        case Data.StatsType.EDITORS:
            colors_file_path = colors_file_path_editors
        case Data.StatsType.OPERATING_SYSTEMS:
            colors_file_path = colors_file_path_operating_systems
        case _:
            colors_file_path = None

    with open(colors_file_path, "r") as colors_file:
        colors_data = yaml.safe_load(colors_file)

        fig = go.Figure()

        for key in stats.daily_stats.keys():
            try:
                color = colors_data[key]["color"]
            except KeyError:
                color = colors_data["Other"]["color"]

            fig.add_trace(go.Scatter(x=dates,
                                     y=stats.daily_stats[key],
                                     mode="lines",
                                     name=key,
                                     marker=dict(color=color)))

    fig.update_layout(yaxis_title="t (h)", plot_bgcolor="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    fig.show()


def draw_pie_chart(stats: Data.Stats) -> None:
    """Draw chart showing total times.

    :param stats: Stats.
    """
    match stats.type_:
        case Data.StatsType.LANGUAGES:
            colors_file_path = colors_file_path_languages
        case Data.StatsType.EDITORS:
            colors_file_path = colors_file_path_editors
        case Data.StatsType.OPERATING_SYSTEMS:
            colors_file_path = colors_file_path_operating_systems
        case _:
            colors_file_path = None

    labels = []
    colors = []

    total_hours = 0.0

    with open(colors_file_path, "r") as colors_file:
        colors_data = yaml.safe_load(colors_file)

        # Loop keys
        for key in stats.daily_stats.keys():
            # Get total time for current key
            hours = sum(stats.daily_stats[key])

            # Add time to total time of all keys
            total_hours += hours

            # Add label to list
            labels.append(key + " - {0} h {1} min".format(int(hours), int((hours - int(hours)) * 60)))
            try:
                colors.append(colors_data[key]["color"])
            except KeyError:
                colors.append(colors_data["Other"]["color"])

    # Add percent sign to legends
    for index, key in enumerate(stats.daily_stats.keys()):
        hours = sum(stats.daily_stats[key])
        labels[index] += " ({0:.2f} %)".format(hours / total_hours * 100)

    fig = px.pie(names=labels,
                 values=[sum(hours) for hours in stats.daily_stats.values()],
                 color_discrete_sequence=colors)
    fig.update_traces(marker=dict(line=dict(color="black", width=0.5)), textinfo="none", hovertemplate=labels)

    fig.show()


def plot() -> None:
    """Plot data."""

    # Daily stats
    if Args.graphs != "" or (Args.graphs == "" and Args.totals == ""):
        # Languages
        if "l" in Args.graphs.lower():
            draw_graphs(Data.dates, Data.languages_stats)
        # Editors
        if "e" in Args.graphs.lower():
            draw_graphs(Data.dates, Data.editors_stats)
        # Operating systems
        if "o" in Args.graphs.lower():
            draw_graphs(Data.dates, Data.operating_systems_stats)

    # Total times
    if Args.totals != "" or (Args.graphs == "" and Args.totals == ""):
        # Languages
        if "l" in Args.totals.lower():
            draw_pie_chart(Data.languages_stats)
        # Editors
        if "e" in Args.totals.lower():
            draw_pie_chart(Data.editors_stats)
        # Operating systems
        if "o" in Args.totals.lower():
            draw_pie_chart(Data.operating_systems_stats)
