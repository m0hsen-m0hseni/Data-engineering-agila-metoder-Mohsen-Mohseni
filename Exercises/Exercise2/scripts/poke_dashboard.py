from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dcc, html, no_update

BASE_DIR = Path(__file__).resolve().parent.parent
OBSERVATIONS_DIR = BASE_DIR / "pokedata" / "observations"
SAVED_DATA_DIR = BASE_DIR / "saved_data"

REQUIRED_COLUMNS = {"pokemon", "happiness"}
REFRESH_INTERVAL_MS = 30_000

app = Dash(__name__)
app.title = "Pokemon Happiness Dashboard"


def is_valid_csv(path: Path) -> bool:
    """Cheap, exception-safe validity check used for the dropdown list."""
    try:
        if path.stat().st_size == 0:
            return False
        df = pd.read_csv(path)
    except Exception:
        return False
    return (not df.empty) and REQUIRED_COLUMNS.issubset(df.columns)


def get_observation_files():
    """Newest-first list of currently-valid observation CSVs. Never raises."""
    if not OBSERVATIONS_DIR.exists():
        return []
    files = [p for p in OBSERVATIONS_DIR.glob("*.csv") if is_valid_csv(p)]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def build_options():
    return [{"label": p.name, "value": str(p)} for p in get_observation_files()]


def empty_figure(message: str):
    fig = px.bar(title=message)
    fig.update_layout(xaxis={"visible": False}, yaxis={"visible": False})
    return fig


def create_figure(file_path):
    """Read the selected CSV fresh from disk and build a figure.

    Deliberately never lets an exception escape: if it did, Dash would
    silently keep showing the *previous* figure instead of the one you
    just selected, which is exactly the bug this replaces.
    """
    if not file_path:
        return empty_figure("No observation selected")

    path = Path(file_path)
    if not path.exists():
        return empty_figure(f"File not found: {path.name}")

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        return empty_figure(f"Could not read {path.name}: {exc}")

    if df.empty or not REQUIRED_COLUMNS.issubset(df.columns):
        return empty_figure(f"{path.name} has no usable data")

    return px.bar(
        df,
        x="pokemon",
        y="happiness",
        title=f"Pokemon Happiness — {path.name}",
    )


def serve_layout():
    options = build_options()
    default_value = options[0]["value"] if options else None

    return html.Div(
        [
            html.H2("Pokemon Happiness Dashboard"),
            dcc.Dropdown(
                id="observation-dropdown",
                options=options,
                value=default_value,
                clearable=False,
            ),

            html.Button(
                "Save Experiment",
                id="save-button",
                n_clicks=0,
            ),

            html.Div(id="save-message"),
            dcc.Graph(id="happiness-graph"),
            dcc.Interval(
                id="refresh-interval",
                interval=REFRESH_INTERVAL_MS,
                n_intervals=0,
            ),
        ]
    )


app.layout = serve_layout


@app.callback(
    Output("observation-dropdown", "options"),
    Output("observation-dropdown", "value"),
    Input("refresh-interval", "n_intervals"),
    State("observation-dropdown", "value"),
)
def refresh_dropdown(_n_intervals, current_value):
    """Re-scan the observations folder on a timer, without disturbing a
    still-valid selection the user has made."""
    options = build_options()
    if not options:
        return [], None

    valid_values = {opt["value"] for opt in options}
    if current_value in valid_values:
        return options, no_update
    return options, options[0]["value"]


@app.callback(
    Output("happiness-graph", "figure"),
    Input("observation-dropdown", "value"),
)
def update_graph(selected_file):
    return create_figure(selected_file)


@app.callback(
    Output("save-message", "children"),
    Input("save-button", "n_clicks"),
    State("observation-dropdown", "value"),
    prevent_initial_call=True,
)
def save_experiment(n_clicks, selected_file):
    if not selected_file:
        return "No observation selected."

    SAVED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(selected_file)

    save_path = SAVED_DATA_DIR / f"experiment_{n_clicks}.csv"
    df.to_csv(save_path, index=False)

    return f"Experiment saved: {save_path.name}"


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8050, debug=True, use_reloader=False)
