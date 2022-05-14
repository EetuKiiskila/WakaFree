import ctypes
import datetime

import PySimpleGUI as sg

import Args


def show() -> None:
    """Show GUI."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except AttributeError:
        pass

    help_file = "The file that contains your statistics."
    help_graphs = "Daily statistics."
    help_totals = "Total times."
    help_ignore = "Ignored stats. Labels separated by commas and nothing more."
    help_search = ("Stats to search for. Labels separated by commas and nothing more.\n"
                   "If nothing is entered then all the stats in the given file will be read.")
    help_minimum_labeling_percentage = ("Inclusive lover limit for labeling the stats.\n"
                                        "Everything under this percentage will be moved to the group Other.")
    help_start_date = ("Start date in format YYYY-MM-DD. Inclusive.\n"
                       "If no date is entered then the stats will be drawn from the very beginning.")
    help_end_date = ("End date in format YYYY-MM-DD. Inclusive.\n"
                     "If no date is entered then the stats will be drawn to the very end.")

    # Window layout
    layout_row_0 = [sg.Text("Hover over a variable name to get help.")]
    layout_row_1 = [sg.HorizontalSeparator()]
    layout_row_2 = [sg.Text("File*", tooltip=help_file),
                    sg.InputText(key="input_file"),
                    sg.FileBrowse(file_types=(("JSON Files", "*.json"),))]
    layout_row_3 = [sg.Text("Graphs", tooltip=help_graphs),
                    sg.Checkbox("Languages", default=True, key="input_graphs_l"),
                    sg.Checkbox("Editors", default=True, key="input_graphs_e"),
                    sg.Checkbox("Operating systems", default=True, key="input_graphs_o")]
    layout_row_4 = [sg.Text("Totals", tooltip=help_totals),
                    sg.Checkbox("Languages", default=True, key="input_totals_l"),
                    sg.Checkbox("Editors", default=True, key="input_totals_e"),
                    sg.Checkbox("Operating systems", default=True, key="input_totals_o")]
    layout_row_5 = [sg.Text("Ignore**", tooltip=help_ignore),
                    sg.InputText(key="input_ignore"),
                    sg.Text("or"),
                    sg.Text("Search**", tooltip=help_search),
                    sg.InputText(key="input_search")]
    layout_row_6 = [sg.Text("Minimum labeling percentage", tooltip=help_minimum_labeling_percentage),
                    sg.InputText("0.0", key="input_minimum_labeling_percentage"),
                    sg.Text("%")]
    layout_row_7 = [sg.Text("Start date", tooltip=help_start_date),
                    sg.InputText("YYYY-MM-DD", key="input_start_date"),
                    sg.CalendarButton("Calendar", format="%Y-%m-%d")]
    layout_row_8 = [sg.Text("End date", tooltip=help_end_date),
                    sg.InputText("YYYY-MM-DD", key="input_end_date"),
                    sg.CalendarButton("Calendar", format="%Y-%m-%d")]
    layout_row_9 = [sg.OK()]
    layout_row_10 = [sg.HorizontalSeparator()]
    layout_row_11 = [sg.Text("* Required.")]
    layout_row_12 = [sg.Text("** Labels separated by commas only.")]
    layout = [layout_row_0,
              layout_row_1,
              layout_row_2,
              layout_row_3,
              layout_row_4,
              layout_row_5,
              layout_row_6,
              layout_row_7,
              layout_row_8,
              layout_row_9,
              layout_row_10,
              layout_row_11,
              layout_row_12]

    # Create window
    window = sg.Window("WakaFree", layout)

    # Window event loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "OK":
            Args.file_name = values["input_file"]

            Args.graphs = ""
            Args.graphs += "l" if values["input_graphs_l"] else ""
            Args.graphs += "e" if values["input_graphs_e"] else ""
            Args.graphs += "o" if values["input_graphs_o"] else ""

            Args.totals = ""
            Args.totals += "l" if values["input_totals_l"] else ""
            Args.totals += "e" if values["input_totals_e"] else ""
            Args.totals += "o" if values["input_totals_o"] else ""

            Args.ignored_stats = values["input_ignore"].split(",") if values["input_ignore"] != "" else []

            Args.searched_stats = values["input_search"].split(",") if values["input_search"] != "" else []

            Args.minimum_labeling_percentage = float(values["input_minimum_labeling_percentage"])

            try:
                Args.start_date = datetime.date(int(values["input_start_date"][0:4]),
                                                int(values["input_start_date"][5:7]),
                                                int(values["input_start_date"][8:10]))
            except ValueError:
                Args.start_date = datetime.date(1, 1, 1)

            try:
                Args.end_date = datetime.date(int(values["input_end_date"][0:4]),
                                              int(values["input_end_date"][5:7]),
                                              int(values["input_end_date"][8:10]))
            except ValueError:
                Args.end_date = datetime.date(9999, 12, 31)

            break

    window.close()
