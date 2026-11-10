# Cidade Alerta (nome do projeto e foi utilizado a ODS 11) (foi utilizado IA pra formalizar o texto e outros fins)


Protótipo acadêmico de zeladoria colaborativa. Moradores registram problemas de iluminação, lixo, buracos e calçadas e acompanham o status. ODS 11, cidades e comunidades sustentáveis.

## O que foi usado

Python e Flask para API, MySQL no FreeDB para dados, HTML/CSS/JavaScript para a página, requests para ViaCEP, sockets TCP para avisos locais e logs em arquivo. Não usa ORM.

## Como executar usando o VS Code

1. Primeiro tem que extrair o ZIP e abrir a pasta `Cidade_Alerta_Simples` no VS Code.
2. Depois abre o terminal e execute `python -m pip install -r requirements.txt`.
3. Crie o banco MySQL no FreeDB (ou use MySQL local, mas pra não ter que instalar eu usei o FreeDB).
4. Abra o painel SQL do banco e execute o conteúdo de `bd.sql`.
5. Abra o `.env` e preencha DB_HOST, DB_PORT, DB_USER, DB_PASSWORD e DB_NAME.
6. No primeiro terminal, execute `python servidor_tcp.py` (pra verificar a conexão entre o usuário e o servidor).
7. Em outro terminal, execute `python app.py`.
8. Abra `http://127.0.0.1:5000` ou `localhost:5000` no navegador.

Para rodar os testes de funcionamento: `python -m unittest discover -s tests -v` (pra ver se tá tudo certo com as funções).

## Endpoints

| Método | Endereço | Uso |
| --- | --- | --- |
| GET | /api/ocorrencias | Listar |
| GET | /api/ocorrencias/1 | Consultar uma |
| POST | /api/ocorrencias | Criar |
| PUT | /api/ocorrencias/1 | Atualizar status |
| DELETE | /api/ocorrencias/1 | Excluir |
| GET | /api/cep/01001000 | Consultar ViaCEP |

POST recebe JSON com titulo, descricao, categoria, cep, rua, bairro, cidade e uf. PUT recebe `{"status":"resolvida"}`. Status aceitos: aberta, em_andamento, resolvida.

## Organização

- `app.py`: rotas Flask, erros e logs.
- `database.py`: comandos SQL com parâmetros `%s`.
- `validacao.py`: checagem dos dados recebidos.
- `config.py`: leitura das configurações do banco.
- `notificacoes.py` e `servidor_tcp.py`: aviso TCP local de novo cadastro.
- `templates/index.html`: conteúdo da página.
- `static/estilo.css`: cores, espaçamento e versão para celular.
- `static/app.js`: ações dos botões e chamadas à API.
- `schema.sql`: tabela MySQL.
- `tests/`: testes de validação.

## Segurança e limites

O sistema valida entradas, usa SQL parametrizado, não pede nome ou CPF, mantém senha no `.env` e grava logs em `logs/acoes.log`. No JavaScript, `textContent` evita interpretar como HTML o texto enviado pelo usuário. O limite de requisição é 16 KB.

