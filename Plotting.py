import os.path
import datetime

import yaml
import plotly.graph_objects as go
import plotly.express as px

import Data


project_directory: str = os.path.dirname(__file__)
colors_file_path_languages: str = os.path.join(project_directory, "Colors/languages_colors.yml")
colors_file_path_editors: str = os.path.join(project_directory, "Colors/editors_colors.yml")
colors_file_path_operating_systems: str = os.path.join(project_directory, "Colors/operating_systems_colors.yml")


def draw_graphs(dates: list[datetime.date], stats: Data.Stats) -> None:
    """Draw graphs for daily stats.

    :param dates: Dates.
    :param stats: Stats.
    """
    match stats.type_:
        case "languages":
            colors_file_path = colors_file_path_languages
        case "editors":
            colors_file_path = colors_file_path_editors
        case "operating_systems":
            colors_file_path = colors_file_path_operating_systems
        case _:
            colors_file_path = None

    with open(colors_file_path, "r") as colors_file:
        colors_data = yaml.safe_load(colors_file)

        fig = go.Figure()

        for key in stats.keys:
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
        case "languages":
            colors_file_path = colors_file_path_languages
        case "editors":
            colors_file_path = colors_file_path_editors
        case "operating_systems":
            colors_file_path = colors_file_path_operating_systems
        case _:
            colors_file_path = None

    labels = []
    colors = []

    total_hours = 0.0

    with open(colors_file_path, "r") as colors_file:
        colors_data = yaml.safe_load(colors_file)

        # Loop keys
        for index, key in enumerate(stats.keys):

            hours = stats.total_times[index]

            # Add time to total time
            total_hours += hours

            # Add label to list
            labels.append(key + " - {0} h {1} min".format(int(hours), int((hours - int(hours)) * 60)))
            try:
                colors.append(colors_data[key]["color"])
            except KeyError:
                colors.append(colors_data["Other"]["color"])

    # Add percent sign to legends
    for index, time in enumerate(stats.total_times):
        labels[index] += " ({0:.2f} %)".format(stats.total_times[index] / total_hours * 100)

    fig = px.pie(names=labels, values=stats.total_times, color_discrete_sequence=colors)
    fig.update_traces(marker=dict(line=dict(color="black", width=0.5)), textinfo="none", hovertemplate=labels)

    fig.show()
