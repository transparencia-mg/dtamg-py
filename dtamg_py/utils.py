import time
import os
import sys
import json
import csv
import shutil
import hashlib
from pymysql import OperationalError
import yaml
import ruamel.yaml
from frictionless import Package
from frictionless import validate_resource
from frictionless import validate_schema
from dpckan import update_resource
import pymysql
import json
import click
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def connect():
  result = pymysql.connect(host=os.environ.get('DB_HOST'),
                         user=os.environ.get('DB_USER'),
                         password=os.environ.get('DB_PASSWORD'),
                         database=os.environ.get('DB_DATABASE'),
                         cursorclass=pymysql.cursors.DictCursor,
                         read_timeout=30)
  return result

def extract_resources(resources):
  
  MAX_RETRIES = 10
  WAIT_IN_SECONDS_BETWEEN_RETRIES = 10
  retry = 1
  while(bool(resources)):
    try:
      connection = connect()
      with connection:
          for resource in resources:
            extract_csv(connection, resource)
            resources.remove(resource)
    except OperationalError as e:
      logger.error(e)
      while retry < MAX_RETRIES:
        retry += 1
        time.sleep(WAIT_IN_SECONDS_BETWEEN_RETRIES)
        try:
          logger.info(f'{retry} retry attempt.')
          connection = connect()
          break
        except OperationalError as e:
          logger.error(e)
          continue

def extract_csv(connection, resource):
    with connection.cursor() as cursor:
      if cursor.execute(f"show tables where Tables_in_age7 = '{resource.sources[0]['table']}';") == 1:
        logger.info(f"Extraindo recurso {resource.name}...")
        sql_file = open(f'scripts/sql/{resource.name}.sql', encoding='utf-8')
        sql_query = sql_file.read()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        if len(rows) == 0:
          logger.warning(f"Recurso {resource.name} sem nenhum registro.")
        colnames = [desc[0] for desc in cursor.description]
        with open(f'data/raw/{resource.name}.csv', "w", encoding='utf-8-sig', newline='') as fp:
          myFile = csv.DictWriter(fp, colnames, delimiter=';')
          myFile.writeheader()
          myFile.writerows(rows)
      else:
        logger.error(f"echo Tabela {resource.name} não existente no banco de dados")

def full_extract():
  dp = Package('datapackage.yaml')
  extract_resources(dp.resources)

def extract(resource_name):
  dp = Package('datapackage.yaml')
  resources = []
  resources.append(dp.get_resource(resource_name))
  extract_resources(resources)

def update_resource_hash(resource_name):
    dp = Package('datapackage.json')
    resource = dp.get_resource(resource_name)
    md5_hash = hashlib.md5()
    file = open(resource.path, "rb")
    content = file.read()
    md5_hash.update(content)
    resource.stats.update({'hash': md5_hash.hexdigest()})
    dp.to_json('datapackage.json')

def build_documentation_folder():
  from_to_file_path = 'age7.yaml'
  from_to_file = load_yaml_file(from_to_file_path)
  for dataset in from_to_file['consultas'].keys():
    if not os.path.exists(f'datasets/{dataset}'):
      shutil.copytree('templates/', f'datasets/{dataset}/')

def build_datapackages():
  if os.path.exists('build_datasets/'):
    shutil.rmtree('build_datasets/')
  from_to_file_path = 'age7.yaml'
  from_to_file = load_yaml_file(from_to_file_path)
  for dataset in from_to_file['consultas'].keys():
    shutil.copytree(f'datasets/{dataset}/', f'build_datasets/{dataset}/', ignore=shutil.ignore_patterns("*.yaml"))
    os.makedirs(f'build_datasets/{dataset}/data')
    # os.system(f'cp datasets/{dataset}/*.md build_datasets/{dataset}')
    # Lê o arquivo datapackage.json para, entre outros, extrair os recursos daquele conjunto
    base_dp = Package('datapackage.json')
    # Lê o arquivo datasets/conjunto/datapakcage.yaml para extrair os metadados personalizados do conjunto
    target_dp = Package(f'datasets/{dataset}/datapackage.yaml')
    # Inclui no base_dp os metadados extraídos do arquivo datapackage.yaml
    for k in target_dp.keys():
      base_dp[k] = target_dp[k]
    base_dp['name'] = dataset
    base_dp['title'] = from_to_file['consultas'][dataset]['title']
    base_dp['homepage'] = from_to_file['consultas'][dataset]['url']
    fact_tables = from_to_file['consultas'][dataset]['fact_tables']
    target_resources = find_target_resources(from_to_file, fact_tables)
    resources_diff = find_resource_diff(base_dp.resource_names, target_resources)
    base_dp = remove_resources(base_dp, resources_diff)
    base_dp = update_resource_properties(base_dp)
    base_dp.to_json(f'build_datasets/{dataset}/datapackage.json')

def find_resource_diff(original_resources, target_resources):
  resources_diff = [i for i in original_resources if not i in target_resources]
  return resources_diff

def remove_resources(base_dp, resources_diff):
  for resource in resources_diff:
    base_dp.remove_resource(resource)
  return base_dp

def update_resource_properties(base_dp):
  for resource in base_dp.resource_names:
    path = base_dp.get_resource(resource).path
    base_dp.get_resource(resource).schema.expand()
    base_dp.get_resource(resource).dialect.expand()
    if not os.path.exists(path):
      # Excluir recurso se arquivo de dados não existir
      logger.warning(f'Arquivo de dados do recurso "{resource}" do dataset "{base_dp.name}" ausente.')
      base_dp.remove_resource(resource)
    else:
      new_path = f'build_datasets/{base_dp.name}/{path}'
      # base_dp.get_resource(resource).path = new_path
      os.system(f'cp {path} {new_path}')
  return base_dp

def load_yaml_file(file_path):
  yaml_dict_content = file_path
  yaml_dict_content = open(yaml_dict_content, encoding='utf-8').read()
  yaml_dict_content = yaml.load(yaml_dict_content, Loader=yaml.FullLoader)
  return yaml_dict_content

def find_target_resources(from_to_file, fact_tables):
  target_resources = []
  for fact_table in fact_tables:
    target_resources.append(fact_table)
    if fact_table in from_to_file['fact_tables'].keys():
      for dim_table in from_to_file['fact_tables'][fact_table]:
        if dim_table not in target_resources:
          target_resources.append(dim_table)
    else:
      logger.warning(f"{fact_table} não existente em data['fact_tables']")
  return target_resources

def run_dpckan_dataset(action):
  path = 'build_datasets'
  folder = os.fsencode(path)
  for sub_folder in os.listdir(folder):
    folder_name = str(sub_folder).split('\'')[1]
    datapackage_path = f'build_datasets/{folder_name}/datapackage.json'
    new_datapackage_ckan_hosts = ''
    # os.system(f'dpckan dataset create -dp {datapackage_path}')
    # ipdb.set_trace(context=10)
    if action == 'create':
      os.system(f'dpckan dataset create -dp {datapackage_path}')
      new_datapackage_ckan_hosts = Package(datapackage_path)["ckan_hosts"]
    if action == 'update':
      os.system(f'dpckan dataset update -dp {datapackage_path}')
      new_datapackage_ckan_hosts = Package(datapackage_path)["ckan_hosts"]
    datapackage_yaml_path = f'datasets/{folder_name}/datapackage.yaml'
    datapackage_yaml = load_yaml_file(datapackage_yaml_path)
    with open(datapackage_yaml_path, 'w', encoding='utf-8') as f:
      datapackage_yaml['ckan_hosts'] = new_datapackage_ckan_hosts
      yaml.dump(datapackage_yaml, f)

def validate(resource_name):
  package = Package('datapackage.yaml')
  resource = package.get_resource(resource_name)
  report = validate_resource(resource)
  json.dump(report, sys.stdout, indent=2, ensure_ascii=False)

def build_datapackage():
  dp = Package('./datapackage.yaml')
  readme = os.path.join(dp.basepath, 'README.md')
  contributing = os.path.join(dp.basepath, 'CONTRIBUTING.md')
  changelog = os.path.join(dp.basepath, 'CHANGELOG.md')
  if os.path.isfile(readme):
      dp.update({'description': f"{dp.get('description')}\n{open(readme, encoding='utf-8').read()}"})
  if os.path.isfile(contributing):
      dp.update({'description': f"{dp.get('description')}\n{open(contributing, encoding='utf-8').read()}"})
  if os.path.isfile(changelog):
      dp.update({'description': f"{dp.get('description')}\n{open(changelog, encoding='utf-8').read()}"})
  for resource in dp.resources:
    logger.info(f"Processando recurso {resource.name}...")
    resource.schema.expand()
    with open(f"logs/validate/{resource.name}.json", encoding='utf-8') as json_file:
        validation_log = json.load(json_file)
    resource.update({'validation': validation_log})
  dp.to_json('datapackage.json')

def validate_tableschema():
  path = 'schemas'
  folder = os.fsencode(path)
  for file in os.listdir(folder):
    file_name = str(file).split('\'')[1]
    if file_name.split('.')[-1] == 'yaml':
      file_path = f'{path}/{file_name}'
      report = validate_schema(file_path)
      if report.valid == False:
        logger.warning(f'Metadado do recurso {file} inválido')

def remove_sqs():
  path = 'schemas'
  folder = os.fsencode(path)
  for file in os.listdir(folder):
    file_name = str(file).split('\'')[1]
    if file_name.split('.')[-1] == 'yaml':
      file_path = f'{path}/{file_name}'
      yaml = ruamel.yaml.YAML()
      yaml.allow_duplicate_keys = True
      yaml.preserve_quotes = True
      yaml.indent(mapping=2, sequence=4, offset=2)
      file_content = open(file_path, encoding='utf-8').read()
      file_content = yaml.load(file_content)
      with open(file_path, 'w', encoding='utf-8') as f:
        for resource in file_content['fields']:
          test = resource['name'][0:4]
          if test == 'sqa_' or test == 'sqe_':
            index = file_content['fields'].index(resource)
            logger.info(f"Retirando campo {resource['name']} do recurso {file_name}")
            file_content['fields'].pop(index)
        logger.info(f"Salvando alterações no recurso {file_name}")
        yaml.dump(file_content, f)

def convert_csv(xlsx_file_path, csv_file_path):
  # referências: https://towardsdatascience.com/how-to-export-pandas-dataframe-to-csv-2038e43d9c03
  # referências: https://colab.research.google.com/drive/1R6SHFugbCEuy5ppjDFymquj3jjbgY7Sx?authuser=1
  read_file = pd.read_excel (xlsx_file_path, )
  read_file.to_csv (csv_file_path, index = None, header=True, sep = ';', decimal = ',', encoding = 'utf-8-sig', na_rep = "")

def compare_data_resource_paths():
  data_resources_names = os.listdir('data')
  data_resources_paths = [os.path.join('data', i) for i in data_resources_names]
  local_package = Package('datapackage.json')
  datapackage_resouces_paths = [i["path"] for i in local_package.resources]
  if data_resources_paths != datapackage_resouces_paths:
    click.echo(f"Resources presentes no arquivo datapackage.json diferente dos listados da pasta data.")
    sys.exit(1)
