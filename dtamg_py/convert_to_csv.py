import click
from dtamg_py.utils import convert_csv

@click.command(name='convert')
@click.argument('xlsx_file_path', required=True)
@click.argument('csv_file_path', required=True)
def convert_csv_cli(xlsx_file_path, csv_file_path):
  """
  Função responsável por converter arquivos xls e xlsx da pasta data/raw in csv na raiz da pasta data
  """
  convert_csv(xlsx_file_path, csv_file_path)
