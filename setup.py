from setuptools import setup, find_packages
import codecs
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# PREPARE

INSTALL_REQUIRES = [
  "click>=8.0.1",
  "python-dotenv>=0.19.1",
  "frictionless>=4.16.6",
  "frictionless-ckan-mapper>=1.0.6",
  "ckanapi>=4.0.0",
  "dpckan>=0.1.11",
  "jsonpatch>=1.32",
  "psycopg2>=2.9.1",
  "PyMySQL>=1.0.2",
  "ruamel.yaml==0.17.17",
  "pandas==1.4.1",
  "xlrd>=1.0.0",
  "openpyxl==3.0.9",
]

# Variáveis author, copyright e licence utilizadas para criação/atualização do arquivo LICENCE.txt (rotina Make durante processo de atualização do pacote "make update-package")
name = 'dtamg-py'
version = '0.1.6'
author = 'CONTROLADORIA GERAL DO ESTADO DE MINAS GERAIS - CGE/MG'
email_author = 'dadosabertos@cge.mg.gov.br'
description = 'Gestão do processos internos da Diretoria Central de Transparência Ativa'
copyright = f'Copyright 2021 {author}'
licence = """\n
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n
"""

def licence_production():
  """
  Rotina para cria/atualiza arquivo LICENCE.txt sempre que a versão do pacote é atualizada
  Chamada durante processo Make de atualização do pacote
  Parameters
  ----------
  Não recebe nenhum parêmetro
  Returns
  -------
  Arquivo LICENCE.txt criado/atualizado
  """
  with open('LICENCE.txt', 'w') as writer:
    for line in range(2):
      if line == 0:
        writer.writelines(copyright)
      else:
        writer.writelines(licence)


if __name__ == '__main__':
  licence_production()
  # Setting up
  setup(
      name=name,
      version=version,
      author=author,
      author_email=email_author,
      description=description,
      long_description_content_type="text/markdown",
      long_description=open('README.md', encoding='utf-8').read() + '\n\n' + open('CHANGELOG.md', encoding='utf-8').read(),
      url="https://github.com/gabrielbdornas/meu-contracheque",
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      keywords=['python', 'Minas Gerais', 'Contracheque'],
      classifiers=[
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3",
          "Operating System :: Unix",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
      ],
      entry_points="""
        [console_scripts]
        dtamg-py=dtamg_py.cli:cli
      """
  )
