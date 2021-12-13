import click
from dtamg_py.full_extract import full_extract_cli

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
  pass

@cli.group()
def etl_make():
  pass

etl_make.add_command(full_extract_cli)
