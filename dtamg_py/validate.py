import click
import sys
from dtamg_py.utils import validate

@click.command(name='validate')
@click.option('--resource', '-r', required=True,
              help="Recursos a serem validados")
def validate_cli(resource):
  validate(sys.argv[-1])

