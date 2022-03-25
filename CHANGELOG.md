## Controle de alterações

Documentação das principais alterações sofridas por este repositório. Baseado na filosofia [Mantenha um Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

### [0.1.6] - 2022-03-25
  - Melhora função para converter arquivos. Conversão apenas de arquivos xlsx da pasta "upload" para pasta data
  - Cria função para comparação entre paths dos recursos presentes no datapackage.json e na pasta data

### [0.1.5] - 2022-03-22
  - Inclui função para converter arquivos xls ou xlsx da pasta data/raw em arquivos .csv na raiz da pasta data

### [0.1.4] - 2022-03-07

- Insere lógica de _retry_ para conexões perdidas com o banco de dados ([#16](https://github.com/transparencia-mg/dtamg-py/pull/16))
- Geração de mensanges de log com pacote logging ([#15](https://github.com/transparencia-mg/dtamg-py/pull/15))

### [0.1.3] - 2022-01-31

- Inclui função extract

### [0.1.2] - 2021-12-21

- Especifica versões de dependências com >=
- Merge branch dev

### [0.1.1] - 2021-12-21

- Acrescenta função de validação e remoção colunas sqa e sqe

### [0.1.0] - 2021-12-15

- Otimiza função extract_resource

### [0.0.900] - 2021-12-13

- Criação do pacote
- Migração projeto etl-make - https://github.com/dados-mg/etl-make
