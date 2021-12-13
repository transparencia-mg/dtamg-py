from frictionless import Package
from dtamg_py.utils import extract_resource

def full_extract():
  dp = Package('datapackage.yaml')
  for resource in dp.resources:
    extract_resource(resource.name)


@click.command(name='full-extract')
def full_extract_cli():
  full_extract()
