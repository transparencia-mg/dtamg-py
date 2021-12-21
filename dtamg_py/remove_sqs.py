import click
import sys
from dtamg_py.utils import remove_sqs

@click.command(name='remove-sqs')
def remove_sqs_cli():
  """
  Função responsável pela remoção de campos sqs (sqa e sqe).
  """
  remove_sqs()