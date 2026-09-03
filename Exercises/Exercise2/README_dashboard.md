# Pokemon Happiness Dashboard

This dashboard shows the happiness level of the Pokemon in the latest observation file.

## How to run the dashboard

1. Make sure Docker Desktop is installed and running.

2. Open a terminal in the `Exercise2` folder.

3. Run the dashboard container with the following command:

```bash
docker run --rm -p 8050:8050 \
-v "$PWD":/exercise2 \
-w /exercise2 \
pokemon-dashboard \
python scripts/poke_dashboard.py
```

4. Open a web browser and go to:

```text
http://localhost:8050
```

5. The Pokemon Happiness Dashboard will now be visible in the browser. This dashboard shows the happiness of Pokemon from different observation files. Use the dropdown menu to choose which observatin to display.

6. To stop the dashboard, return to the terminal and press:

```text
Ctrl + C
```

## Requirements

Docker Desktop must be installed and running.

No manual installation of Python, Dash, pandas or Plotly is required.
