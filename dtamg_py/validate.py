import click
import sys
import json
from frictionless import Package
from frictionless import validate_resource
from dtamg_py.utils import validate

@click.command(name='validate')
def validate_cli():
  validate(sys.argv[1])
