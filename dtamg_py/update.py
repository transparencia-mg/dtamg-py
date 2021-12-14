import click
from dtamg_py.utils import run_dpckan_dataset

@click.command(name='dpckan-update')
def dpckan_update_cli():
  """
  Função responsável pela atualização dos conjuntos no CKAN.
  """
  run_dpckan_dataset('update')
