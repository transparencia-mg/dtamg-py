import click
from dtamg_py.utils import compare_data_resource_paths

@click.command(name='compare')
def compare_data_resource_paths_cli():
  """
  Função responsável pela comparação dos paths de recursos listados na pasta data e no datapackage.json.
  """
  compare_data_resource_paths()
