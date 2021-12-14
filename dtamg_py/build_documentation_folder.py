import click
from dtamg_py.utils import build_documentation_folder

@click.command(name='build-documentation-folder')
def build_documentation_folder_cli():
  build_documentation_folder()
