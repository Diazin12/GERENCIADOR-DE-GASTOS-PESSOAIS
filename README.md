# Gerenciador de Gastos Pessoais

Aplicação web para registrar e acompanhar gastos pessoais. Cada usuário cria uma conta e acessa seus próprios lançamentos, com filtros por mês e categoria, resumo dos valores e gráfico por categoria.

## Funcionalidades

- Cadastro de usuário e login/logout.
- Senhas armazenadas com hash.
- Cadastro, consulta, edição e exclusão de gastos.
- Gastos associados ao usuário que os cadastrou.
- Filtros por mês e categoria.
- Soma dos gastos exibidos no período filtrado.
- Gráfico de barras com os totais por categoria.
- Interface responsiva para celular e computador.

## Capturas de tela

### Cadastro

![Tela de cadastro](docs/images/cadastro.png)

### Login

![Tela de login](docs/images/login.png)

### Dashboard sem gastos

![Dashboard sem gastos cadastrados](docs/images/dashboard-vazio.png)

### Dashboard com gasto

![Dashboard com um gasto cadastrado](docs/images/dashboard-com-gastos.png)

### Edição de gasto

![Formulário de edição de gasto](docs/images/editar-gasto.png)

## Tecnologias

- Python, Flask e Flask-Login
- SQLite
- HTML, CSS, Bootstrap e Jinja2
- JavaScript e Chart.js

## Como executar localmente

Tenha Python 3 instalado. No terminal, dentro da pasta do projeto, crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Inicie a aplicação a partir da pasta principal do projeto:

```bash
export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
python app/app.py
```

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000) no navegador. Crie uma conta para começar a usar o sistema.

Ao iniciar, a aplicação cria as tabelas no banco SQLite `data/gastos.db`. A pasta `data/` também é criada automaticamente caso ainda não exista.

## Como executar com Docker

O projeto também pode ser iniciado com Docker Compose. Antes da primeira execução, crie o arquivo `.env` na pasta principal e coloque nele uma chave secreta gerada por você:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copie o valor exibido e salve no `.env` neste formato, sem espaços ao redor do `=`:

```env
SECRET_KEY=cole_a_chave_gerada_aqui
```

O `.env` está no `.dockerignore` e no `.gitignore`; não publique nem compartilhe esse arquivo.

Construa a imagem e inicie a aplicação:

```bash
docker compose up --build
```

Abra [http://127.0.0.1:5001](http://127.0.0.1:5001). O Compose publica a porta `5001` do computador na porta `5000` do contêiner. Para parar a aplicação, pressione `Ctrl+C` ou execute `docker compose down` em outro terminal. Para iniciá-la em segundo plano, use `docker compose up -d`.

O Compose monta `./data` em `/app/data`, onde o app grava `gastos.db`. Assim, o arquivo SQLite permanece na pasta `data/` do projeto mesmo quando o contêiner é recriado. Ele também monta `./app` no contêiner para disponibilizar os arquivos da aplicação.

## Estrutura do projeto

```text
gerenciador-de-gastos/
├── app/
│   ├── app.py
│   ├── models.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── cadastro.js
│   │       ├── dashboard-filters.js
│   │       └── dashboard.js
│   └── templates/
│       ├── base.html
│       ├── cadastro.html
│       ├── dashboard.html
│       ├── form_gasto.html
│       ├── gastos.html
│       └── login.html
├── data/
│   └── gastos.db  (criado ao iniciar a aplicação)
├── docs/
│   └── images/
│       ├── cadastro.png
│       ├── login.png
│       ├── dashboard-vazio.png
│       ├── dashboard-com-gastos.png
│       └── editar-gasto.png
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── README.md
└── .gitignore
```

## Uso de inteligência artificial

Usei uma ferramenta de inteligência artificial como apoio na criação e estilização do front-end com Bootstrap e JavaScript, incluindo o gráfico. As funcionalidades em Python foram desenvolvidas completamente por mim.
