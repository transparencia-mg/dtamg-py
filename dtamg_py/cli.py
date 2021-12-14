import click
from dtamg_py.full_extract import full_extract_cli
from dtamg_py.validate import validate_cli
from dtamg_py.build_datapackage import build_datapackage_cli
from dtamg_py.build_datapackages import build_datapackages_cli
from dtamg_py.create import dpckan_create_cli
from dtamg_py.update import dpckan_update_cli
from dtamg_py.build_documentation_folder import build_documentation_folder_cli

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
  pass

@cli.group()
def etl_make():
  pass

etl_make.add_command(full_extract_cli)
etl_make.add_command(validate_cli)
etl_make.add_command(build_datapackage_cli)
etl_make.add_command(build_datapackages_cli)
etl_make.add_command(dpckan_create_cli)
etl_make.add_command(dpckan_update_cli)
etl_make.add_command(build_documentation_folder_cli)
