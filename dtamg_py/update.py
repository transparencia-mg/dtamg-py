import click
from dtamg_py.utils import run_dpckan_dataset

@click.command(name='dpckan-update')
def dpckan_update_cli():
  run_dpckan_dataset('update')
