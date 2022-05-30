#!/usr/bin/env python3
from datetime import datetime
import sys
import click

import pandas as pd
import rich.console
from rich.traceback import install

install(show_locals=True)
console = rich.console.Console()


def column_validator(ctx, param: click.Option, value):
    if param.name == "column" and value < 1:
        raise click.BadParameter("column must be a positive integer.")
    else:
        return value


def custom_date_parser(ds):
    ret_val = datetime.strptime(ds, "%d.%m.%Y %H.%M")
    return ret_val


@click.command(no_args_is_help=True)
@click.option(
    "--ascending",
    "-a",
    "direction",
    required=False,
    help="Sort CSV in ascending order",
    default=True,
    show_default=True,
    flag_value=True,
)
@click.option(
    "--descending",
    "-d",
    "direction",
    required=False,
    help="Sort CSV in descending order",
    show_default=True,
    flag_value=False,
)
@click.option("--output-file", "-o", required=False, help="Specify the output file")
@click.argument("filename", required=True)
def sort(direction, filename, output_file):
    date_column = "Päivämäärä"
    df = pd.read_csv(
        filename,
        sep=None,
        on_bad_lines="warn",
        skip_blank_lines=True,
        header=0,
        engine="python",
        encoding="utf-8-sig",
        date_parser=custom_date_parser,
        parse_dates=[date_column],
    )
    df.sort_values(by=date_column, axis=0, ascending=direction, inplace=True)
    if output_file is None:
        output_file = sys.stdout
    df.to_csv(output_file, sep=";", doublequote=True, index=False)


if __name__ == "__main__":
    sort()
