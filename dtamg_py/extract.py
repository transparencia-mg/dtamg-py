import click
from dtamg_py.utils import extract

@click.command(name='extract')
@click.option('--resource', '-r', required=True,
              help="Recurso a ser extraído")
def extract_cli(resource):
  """
  Função responsável pela extração dos dados de tabela específica no banco Mysql.
  """
  extract(resource)
