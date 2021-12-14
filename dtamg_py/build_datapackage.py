import click
from dtamg_py.utils import build_datapackage

@click.command(name='build-datapackage')
def build_datapackage_cli():
  build_datapackage()
