import os.path

import yaml
import plotly.graph_objects as go
import plotly.express as px


def draw_graphs(days, keys, datasets, data_type):

    project_directory = os.path.dirname(__file__)

    colors_file_path_languages = os.path.join(project_directory, "Colors/languages_colors.yml")
    colors_file_path_editors = os.path.join(project_directory, "Colors/editors_colors.yml")
    colors_file_path_operating_systems = os.path.join(project_directory, "Colors/operating_systems_colors.yml")

    colors_file_path = None

    match data_type:
        case "languages":
            colors_file_path = colors_file_path_languages
        case "editors":
            colors_file_path = colors_file_path_editors
        case "operating_systems":
            colors_file_path = colors_file_path_operating_systems

    with open(colors_file_path, "r") as colors_file:
        colors_data = yaml.safe_load(colors_file)

        fig = go.Figure()

        for key in keys:
            try:
                fig.add_trace(go.Scatter(x=days,
                                         y=datasets[key],
                                         mode="lines",
                                         name=key,
                                         marker=dict(color=colors_data[key]["color"])))
            except Exception:
                fig.add_trace(go.Scatter(x=days,
                                         y=datasets[key],
                                         mode="lines",
                                         name=key,
                                         marker=dict(color=colors_data["Other"]["color"])))

    fig.update_layout(yaxis_title="t (h)", plot_bgcolor="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    fig.show()
