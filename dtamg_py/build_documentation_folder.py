import click
from dtamg_py.utils import build_documentation_folder

@click.command(name='build-documentation-folder')
def build_documentation_folder_cli():
  """
  Função responsável pela construção da pasta de documentação datasets.
  """
  build_documentation_folder()
