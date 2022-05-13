from datetime import datetime
import ctypes
import PySimpleGUI as sg


def initialize_gui():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    help_string_file = "The file that contains your statistics."
    help_string_graphs = "Daily statistics."
    help_string_totals = "Total times."
    help_string_ignore = "Ignored stats. Labels separated by commas and nothing more."
    help_string_search = ("Stats to search for. Labels separated by commas and nothing more.\n"
                          "If nothing is entered then all the stats in the given file will be read.")
    help_string_minimum_labeling_percentage = ("Inclusive lover limit for labeling the stats.\n"
                                               "Everything under this percentage will be moved to the group Other.")
    help_string_start_date = ("Start date in format YYYY-MM-DD. Inclusive.\n"
                              "If no date is entered then the stats will be drawn from the very beginning.")
    help_string_end_date = ("End date in format YYYY-MM-DD. Inclusive.\n"
                            "If no date is entered then the stats will be drawn to the very end.")

    layout = [
        [sg.Text("Hover over a variable name to get help.")],
        [sg.HorizontalSeparator()],
        [sg.Text("File*", tooltip=help_string_file), sg.InputText(key="input_file"),
         sg.FileBrowse(file_types=(("JSON Files", "*.json"),))],
        [
            sg.Text("Graphs", tooltip=help_string_graphs),
            sg.Checkbox("Languages", default=True, key="input_graphs_l"),
            sg.Checkbox("Editors", default=True, key="input_graphs_e"),
            sg.Checkbox("Operating systems", default=True, key="input_graphs_o")
        ],
        [
            sg.Text("Totals", tooltip=help_string_totals),
            sg.Checkbox("Languages", default=True, key="input_totals_l"),
            sg.Checkbox("Editors", default=True, key="input_totals_e"),
            sg.Checkbox("Operating systems", default=True, key="input_totals_o")
        ],
        [sg.Text("Ignore**", tooltip=help_string_ignore), sg.InputText(key="input_ignore"), sg.Text("or"),
         sg.Text("Search**", tooltip=help_string_search), sg.InputText(key="input_search")],
        [sg.Text("Minimum labeling percentage", tooltip=help_string_minimum_labeling_percentage),
         sg.InputText("0.0", key="input_minimum_labeling_percentage"), sg.Text("%")],
        [sg.Text("Start date", tooltip=help_string_start_date), sg.InputText("YYYY-MM-DD", key="input_start_date"),
         sg.CalendarButton("Calendar", format="%Y-%m-%d")],
        [sg.Text("End date", tooltip=help_string_end_date), sg.InputText("YYYY-MM-DD", key="input_end_date"),
         sg.CalendarButton("Calendar", format="%Y-%m-%d")],
        [sg.OK()],
        [sg.HorizontalSeparator()],
        [sg.Text("* Required.")],
        [sg.Text("** Labels separated by commas only.")]
    ]

    window = sg.Window("WakaFree", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "OK":
            file_name = values["input_file"]

            graphs = ""
            graphs += "l" if values["input_graphs_l"] else ""
            graphs += "e" if values["input_graphs_e"] else ""
            graphs += "o" if values["input_graphs_o"] else ""

            totals = ""
            totals += "l" if values["input_totals_l"] else ""
            totals += "e" if values["input_totals_e"] else ""
            totals += "o" if values["input_totals_o"] else ""

            ignored_stats = values["input_ignore"].split(",") if values["input_ignore"] != "" else []
            searched_stats = values["input_search"].split(",") if values["input_search"] != "" else []

            minimum_labeling_percentage = float(values["input_minimum_labeling_percentage"])

            try:
                start_date = datetime(int(values["input_start_date"][0:4]), int(values["input_start_date"][5:7]),
                                      int(values["input_start_date"][8:10])).date()
            except:
                start_date = datetime(1, 1, 1).date()
            try:
                end_date = datetime(int(values["input_end_date"][0:4]), int(values["input_end_date"][5:7]),
                                    int(values["input_end_date"][8:10])).date()
            except:
                end_date = datetime(9999, 12, 31).date()

            break

    window.close()

    return file_name, graphs, totals, ignored_stats, searched_stats, minimum_labeling_percentage, start_date, end_date
