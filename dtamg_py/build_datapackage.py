import click
from dtamg_py.utils import build_datapackage

@click.command(name='build-datapackage')
def build_datapackage_cli():
  """
  Função responsável pela construção do arquivo datapackage.json de todo conjunto AGE7.
  """
  build_datapackage()
