# Earthquake -- an earthquake plotting CLI app

This project provides a simple CLI interface to download, parse, and display
plots of earthquake data for the last day, week, or month from USGA website.

## Installation

1. Clone this project.
2. Create the virtual environment via poetry or through requirements.txt file.
3. Run from within the poetry shell use earthquake.
4. From with a virtual environment us earthquake_CLI.py

## Use

Use earthquake (or earthquake_CLI.py) help option (--help) for
more information.

The two commands are:
1. update -- downloads, parses, and creates plots from data.
2. display -- user inputs "DAY", "WEEK", or "MONTH" to display
   the chosen plot via the default browser, input "q" to exit.

## License

This project is under MIT license (see LICENSE file).
