import click
from dtamg_py.utils import convert_csv

@click.command(name='convert')
def convert_csv_cli():
  """
  Função responsável por converter arquivos xls e xlsx da pasta data/raw in csv na raiz da pasta data
  """
  convert_csv()
