import click
from dtamg_py.utils import build_datapackages

@click.command(name='build-datapackages')
def build_datapackages_cli():
  """
  Função responsável pela construção dos conjuntos derivados de todo conjunto AGE7. Constroi pasta build_datasets.
  """
  build_datapackages()
