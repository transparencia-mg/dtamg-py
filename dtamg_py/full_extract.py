import click
from frictionless import Package
from dtamg_py.utils import full_extract

@click.command(name='full-extract')
def full_extract_cli():
  full_extract()
