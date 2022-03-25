dtamg-py :bookmark_tabs:
===

## Sobre este repositório :open_book:

## Orientações gerais

- Instalação de [Python 3](https://www.python.org/downloads/).

## Setup da máquina

#### Pasta para execução dos comandos e ativação de ambiente python

- Necessário instalação de [Python 3](https://www.python.org/downloads/) antes da execução os comandos abaixo para ambos os sistemas operacionais.

- Sistema operacional Linux:

```Terminal
# Criação ambiente python
$ python3 -m venv venv

# Ativação ambiente python
$ source venv/bin/activate
```

- Sistema operacional Windows:
  - Recomendo a utilização de Git Bash disponível com instalação de [Git para Windows](https://gitforwindows.org/).

```Terminal
# Criação ambiente python
$ python -m venv venv

# Ativação ambiente python
$ source venv/Scripts/activate
```

## Instalação

O `dtamg-py` está disponível no Python Package Index - [PyPI](https://pypi.org/project/dtamg-py/) e pode ser instalado utilizando-se o comando abaixo:

```bash
# Antes de executar o comando abaixo lembre-se que ambiente Python deverá estar ativo
$ pip install dtamg-py
```

## Atualizar versão

Conforme relatado no [issue 6](https://github.com/dados-mg/dpkgckanmg/issues/6), atualização de versões no [Pypi](https://pypi.org/) deve seguir [estes os passos](https://github.com/dados-mg/dpckan/issues/6#issuecomment-851678297)
