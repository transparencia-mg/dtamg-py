import click
from dtamg_py.utils import run_dpckan_dataset

@click.command(name='dpckan-create')
def dpckan_create_cli():
  run_dpckan_dataset('create')
