# sspdata

## Como instalar
```
pip install sspdata
```
## Documentação dos dados e features de cada dataset
Todos os dados são removídos do portal da transparência da SSP do estado de São Paulo:
http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx

Futuramente pretendo adicionar aqui ao projeto os dicionários de dados para facilitar ainda mais a utilização do projeto.

## Como usar
```python
from sspdata.datasets.feminicidio import extrair_feminicidios

df = extrair_feminicidios(2021, 6)
```
![example of how to use](img/example.png)

## Como contrubuir?

Instale as dependências do projeto (prod e dev)
```
$ poetry install
```
Code...
Code...
Code...

Para checar se o código está dentro dos padrões:
```
$ poetry run fmt
$ poetry run isort-fmt
$ poetry run linter
$ poetry run tests
```
Agora é só abrir o PR e aproveitar a review :)