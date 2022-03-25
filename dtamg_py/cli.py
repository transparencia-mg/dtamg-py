import click
import logging
from dtamg_py.full_extract import full_extract_cli
from dtamg_py.extract import extract_cli
from dtamg_py.validate import validate_cli
from dtamg_py.build_datapackage import build_datapackage_cli
from dtamg_py.build_datapackages import build_datapackages_cli
from dtamg_py.create import dpckan_create_cli
from dtamg_py.update import dpckan_update_cli
from dtamg_py.build_documentation_folder import build_documentation_folder_cli
from dtamg_py.validate_tableschemas import validate_tableschemas_cli
from dtamg_py.remove_sqs import remove_sqs_cli
from dtamg_py.convert_to_csv import convert_csv_cli
from dtamg_py.compare_resource_paths import compare_data_resource_paths_cli

LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option('--verbose', '-v', default=False, is_flag=True, help='Produce detailed output for diagnostic purposes.')
def cli(verbose):
  if verbose:
        logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.DEBUG)
  else:
        logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)

@cli.group()
def etl_make():
  pass

etl_make.add_command(full_extract_cli)
etl_make.add_command(extract_cli)
etl_make.add_command(validate_cli)
etl_make.add_command(build_datapackage_cli)
etl_make.add_command(build_datapackages_cli)
etl_make.add_command(dpckan_create_cli)
etl_make.add_command(dpckan_update_cli)
etl_make.add_command(build_documentation_folder_cli)
etl_make.add_command(validate_tableschemas_cli)
etl_make.add_command(remove_sqs_cli)

@cli.group()
def template():
  pass

template.add_command(convert_csv_cli)
template.add_command(compare_data_resource_paths_cli)
