import click
from dtamg_py.utils import build_datapackages

@click.command(name='build-datapackages')
def build_datapackages_cli():
  build_datapackages()
