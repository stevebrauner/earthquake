"""
Commandline Interface for retrieving, parsing, and displaying recent
earthquake data.

The earthquake data is retrieved from the USGA website and parsed into
plots with the UPDATE command.

The earthquake data is displayed via the system default browser with the
DISPLAY command.
"""

import click

from earthquake.model import Model

model = Model()


@click.group()
def cli():
    pass


@cli.command()
def update():
    """Update data (from USGA website) and create plots."""
    model.get_all_earthquake_data()
    model.create_all_earthquake_plots()
    click.echo("Updated data and plots.")


@cli.command()
@click.option(
    "--timeframe",
    type=click.Choice(["DAY", "WEEK", "MONTH", "q"], case_sensitive=False),
    prompt="Enter timeframe or 'q' to quit",
)
def display(timeframe):
    """Display an earthquake plot by timeframe ['DAY', 'WEEK', 'MONTH'] or 'q' to quit."""
    if timeframe != "q":
        click.launch(model.get_plot_filename(timeframe))
