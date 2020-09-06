# Open Financial Management Gate - OpenFMG

OpenFMG - Portal de Gestão Financeira

Temos como objetivo ajudar a investir melhor. Sendo o mais completo portal de gestão financeira OpenSource, voltado para o mercado Brasileiro.
Atualmente o sistema consegue receber uma tabela de Excel com Headers: ATIVO, DATA, QUANTIDADE, VALOR. Que são as movimentações. Com isso o sistema já calcula a posição atual de cada ativo, bem como qual seria o benchmark atrelado a SELIC para essas mesmas movimentações, já levando em conta eventuais desdobramentos e agrupamentos. O processo de proventos para cada ativo está em processo de desenvolvimento, e em breve estará disponível.

O objetivo é que o sistema mostre a Gestão de Fluxo de Caixa (Receitas e Despesas) e gestão de Balanço Financeiro (Ativos e Passivos).  Com Gráficos, Tabelas e afins. Para qualquer tipo de *ativos* (Renda Variável, Renda Fixa, Imóveis, Lojas, Sites, etc. Qualquer coisa que gere renda)
Por hora, o sistema está sendo desenvolvido em torno de carteiras de ativos de Renda Variável.

Em um único lugar, cadastrar e gerenciar seus ativos, bem como os proventos, rendimento de suas carteiras.
Ainda não implementado, mas sendo um interesse, aqui poderá ser gerenciado seus gastos, e receitas.

Estudar seus ativos, com dados fundamentalistas, ajudando ao investidor a escolher boas empresas e negócios para ser sócio. Comprando bons ATIVOS:
Ativos -> Geram renda.
Passivos -> Geram despesas.


O Sistema está dividido entre o FrontEnd e o BackEnd.

FrontEnd - Desenvolvido em Angular
BackEnd  - Desenvolvido em Django (Python)



## Instalação

Na pasta BackEnd: 
```bash
pip install -r requirements.txt
```

Na pasta do FrontEnd:

```bash
npm install
```

## Uso

Na pasta BackEnd:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Na pasta FronEnd (Ver README.md na pasta frontend):
```bash
ng serve
```


## Contribuição


Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Licença
[MIT](https://choosealicense.com/licenses/mit/)


## Autores

Felipe Maion

José Alison Aguiar

<< YOUR NAME GOES HERE >>
