import click
import sys
from dtamg_py.utils import validate_tableschema

@click.command(name='validate-tableschemas')
def validate_tableschemas_cli():
  """
  Função responsável pela validação frictionless de todos os conjuntos e seus recursos.
  """
  validate_tableschema()
