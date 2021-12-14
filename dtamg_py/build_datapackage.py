import click
from dtamg_py.utils import buil_datapackage_json

@click.command(name='build-datapackage-json')
def buil_datapackage_json_cli():
  buil_datapackage_json()
