# Gerenciamento de Eventos Academicos

API REST com FastAPI, SQLite, SQLAlchemy e autenticacao JWT.

Autores: Santana & Mendes

---

## 1. Descricao do projeto

API para gerenciar eventos academicos, participantes e inscricoes. Os dados ficam em um banco SQLite acessado com SQLAlchemy.

Funcionalidades:

- Cadastro, consulta, atualizacao e exclusao de eventos e participantes.
- Inscricao de participantes em eventos, com controle de vagas (capacidade do evento) e bloqueio de inscricao duplicada.
- Tres relatorios consolidados (ocupacao por evento, por categoria e por curso).
- Cadastro de usuarios e login com token JWT.
- Controle de acesso por perfil: `usuario` e `administrador`.

---

## 2. Instalacao

Requisitos: Python 3.10 ou superior.

1. Baixe o projeto e entre na pasta:

```
git clone <URL-DO-REPOSITORIO>
cd aps-4-backend
```

2. Crie o ambiente virtual:

```
py -m venv venv
```

3. Ative o ambiente virtual:

```
# PowerShell (Windows)
Set-ExecutionPolicy -Scope Process Bypass
venv\Scripts\activate

# Prompt de Comando (cmd)
venv\Scripts\activate.bat

# Linux / Mac
source venv/bin/activate
```

> **Erro no PowerShell?** Se aparecer a mensagem de que a execucao de scripts foi desabilitada, rode antes o comando `Set-ExecutionPolicy -Scope Process Bypass`. Ele libera a execucao de scripts **apenas na janela atual** do PowerShell (ao fechar o terminal, volta ao normal e nada no computador e alterado). Depois disso, o `venv\Scripts\activate` funciona. No Prompt de Comando (cmd) esse passo nao e necessario.

4. Instale as dependencias:

```
pip install -r requirements.txt
```

### Principais dependencias

| Biblioteca                 | Para que serve                                              |
| -------------------------- | ----------------------------------------------------------- |
| fastapi                    | Criacao da API e do Swagger (`/docs`)                       |
| uvicorn                    | Servidor que executa a API                                  |
| sqlalchemy                 | Acesso ao banco SQLite (ORM)                                |
| pydantic / email-validator | Validacao dos dados de entrada e saida, incluindo e-mail    |
| passlib + bcrypt           | Geracao e verificacao do hash das senhas (algoritmo bcrypt) |
| PyJWT                      | Geracao e validacao dos tokens JWT                          |

---

## 3. Configuracao (variaveis de ambiente)

A chave do JWT **nao fica escrita no codigo**. Ela e lida de uma variavel de ambiente. As variaveis devem ser definidas no **mesmo terminal** em que a API for iniciada, antes do comando `uvicorn`.

| Variavel      | Obrigatoria? | Descricao                                                     |
| ------------- | ------------ | ------------------------------------------------------------- |
| `SECRET_KEY`  | Sim          | Chave usada para assinar os tokens. Sem ela a API nao inicia. |
| `ADMIN_EMAIL` | Nao          | E-mail do administrador inicial.                              |
| `ADMIN_SENHA` | Nao          | Senha do administrador inicial.                               |
| `ADMIN_NOME`  | Nao          | Nome do administrador inicial (padrao: "Administrador").      |

Para gerar uma chave aleatoria:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

**PowerShell (Windows):**

```
$env:SECRET_KEY="uma-chave-longa-e-aleatoria"
$env:ADMIN_EMAIL="admin@exemplo.com"
$env:ADMIN_SENHA="senha-do-admin"
```

**Prompt de Comando (cmd):**

```
set SECRET_KEY=uma-chave-longa-e-aleatoria
set ADMIN_EMAIL=admin@exemplo.com
set ADMIN_SENHA=senha-do-admin
```

**Linux / Mac:**

```
export SECRET_KEY="uma-chave-longa-e-aleatoria"
export ADMIN_EMAIL="admin@exemplo.com"
export ADMIN_SENHA="senha-do-admin"
```

Essas variaveis valem apenas para o terminal em que foram definidas. Se abrir outro terminal, defina de novo.

### Administrador inicial

Na inicializacao, se `ADMIN_EMAIL` e `ADMIN_SENHA` estiverem definidas e esse e-mail ainda nao existir no banco, o administrador e criado automaticamente com o perfil `administrador`.

Este e o **unico caminho** para criar um administrador: o cadastro publico (`POST /usuarios`) sempre cria o perfil `usuario`, mesmo que o JSON enviado contenha o campo `perfil`.

### Perfis antigos

Se o banco tiver usuarios com perfil `ADMIN` ou `CLIENTE` (versao anterior do projeto), eles sao convertidos para `administrador` e `usuario` na inicializacao.

---

## 4. Execucao

Com o ambiente virtual ativo e as variaveis definidas:

```
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Documentacao (Swagger): http://127.0.0.1:8000/docs

Dica: o terminal onde a API roda apenas mostra o log. Para rodar outros comandos (curl, Invoke-RestMethod), abra um segundo terminal.

---

## 5. Estrutura do projeto

| Arquivo / pasta    | Funcao                                           |
| ------------------ | ------------------------------------------------ |
| `main.py`          | Cria o app, as tabelas e o administrador inicial |
| `database.py`      | Conexao com o SQLite e sessao do banco           |
| `auth.py`          | Hash de senha, JWT e controle de acesso          |
| `models/`          | Tabelas do banco (SQLAlchemy)                    |
| `schema/`          | Validacao de entrada e saida (Pydantic)          |
| `routers/`         | Rotas HTTP                                       |
| `services/`        | Regras de negocio                                |
| `repositories/`    | Consultas ao banco                               |
| `requirements.txt` | Dependencias do projeto                          |

Fluxo de uma requisicao: `router -> service -> repository -> banco`.

---

## 6. Banco de dados

- Tipo: SQLite.
- Arquivo: `eventos-academicos.db`, criado automaticamente na pasta de onde o uvicorn for iniciado (normalmente a raiz do projeto), conforme `DATABASE_URL` em `database.py`.
- O arquivo `.db` esta no `.gitignore` e nao vai para o repositorio. Para recriar o banco do zero, basta apagar o arquivo e iniciar a API de novo.
- As tabelas sao criadas automaticamente na primeira execucao.

Tabelas:

| Tabela        | Colunas                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------ |
| usuarios      | id, nome, email (unico), senha_hash, perfil                                                |
| participantes | id, nome, email (unico), curso                                                             |
| eventos       | id, titulo, descricao, data, horario, local, capacidade, categoria                         |
| inscricoes    | id, evento_id, participante_id, data_inscricao (o par evento_id + participante_id e unico) |

Observacoes:

- A restricao unica em `inscricoes` impede inscricao duplicada.
- Ao excluir um evento, as inscricoes dele sao removidas junto.
- As senhas sao guardadas apenas como hash (bcrypt).

---

## 7. Perfis e autenticacao

| Perfil          | Como se obtem                                 | Permissoes                                                                       |
| --------------- | --------------------------------------------- | -------------------------------------------------------------------------------- |
| `usuario`       | Cadastro em `POST /usuarios`                  | Consulta eventos, opera participantes e inscricoes, consulta seus proprios dados |
| `administrador` | Criado na inicializacao (variaveis `ADMIN_*`) | Tudo que o usuario faz, mais gerenciar eventos e consultar relatorios            |

A permissao e verificada no servidor, a partir do usuario identificado pelo token. O perfil nao e lido do corpo da requisicao.

Como autenticar:

1. Cadastre-se em `POST /usuarios` (ou use o administrador inicial).
2. Faca login em `POST /auth/login` e copie o `access_token`.
3. Envie o token no cabecalho de cada requisicao protegida:

```
Authorization: Bearer <access_token>
```

No Swagger (`/docs`): clique em **Authorize**, cole apenas o token (sem a palavra `Bearer` e sem aspas) e confirme.

O token expira em 60 minutos e guarda o id do usuario no campo `sub`. Token ausente, invalido ou expirado retorna 401 com a mensagem "Nao foi possivel validar as credenciais.".

---

## 8. Principais rotas

**Publicas (sem token)**

| Metodo e rota       | Descricao               |
| ------------------- | ----------------------- |
| `GET /`             | Teste da API            |
| `POST /usuarios`    | Cadastrar usuario       |
| `POST /auth/login`  | Login (retorna o token) |
| `GET /eventos`      | Listar eventos          |
| `GET /eventos/{id}` | Consultar evento        |

**Exigem login (qualquer perfil)**

| Metodo e rota                                            | Descricao                  |
| -------------------------------------------------------- | -------------------------- |
| `GET /auth/me`                                           | Dados do usuario logado    |
| `POST /participantes`                                    | Cadastrar participante     |
| `GET /participantes`                                     | Listar participantes       |
| `GET /participantes/{id}`                                | Consultar participante     |
| `PUT /participantes/{id}`                                | Atualizar participante     |
| `DELETE /participantes/{id}`                             | Excluir participante       |
| `POST /eventos/{evento_id}/inscricoes/{participante_id}` | Inscrever participante     |
| `GET /eventos/{evento_id}/inscricoes`                    | Listar inscritos do evento |

**Somente administrador**

| Metodo e rota                          | Descricao               |
| -------------------------------------- | ----------------------- |
| `POST /eventos`                        | Cadastrar evento        |
| `PUT /eventos/{id}`                    | Atualizar evento        |
| `DELETE /eventos/{id}`                 | Excluir evento          |
| `GET /relatorios/eventos/ocupacao`     | Relatorio de ocupacao   |
| `GET /relatorios/eventos/categorias`   | Relatorio por categoria |
| `GET /relatorios/participantes/cursos` | Relatorio por curso     |

Codigos de resposta principais:

| Codigo | Significado                                                                  |
| ------ | ---------------------------------------------------------------------------- |
| 200    | Sucesso                                                                      |
| 201    | Criado com sucesso                                                           |
| 401    | Token ausente, invalido ou expirado, ou login incorreto                      |
| 403    | Usuario logado sem permissao de administrador                                |
| 404    | Evento ou participante nao encontrado                                        |
| 409    | E-mail ja cadastrado, participante ja inscrito no evento ou evento sem vagas |
| 422    | Dados invalidos (ex.: e-mail mal formado, capacidade <= 0)                   |

---

## 9. Relatorios e informacoes consolidadas

Todos os relatorios sao exclusivos do administrador e sao calculados no banco com consultas agrupadas (`GROUP BY`).

1. **Ocupacao por evento** - `GET /relatorios/eventos/ocupacao`
   Para cada evento retorna: `evento_id`, `titulo`, `capacidade`, `total_inscritos`, `vagas_disponiveis` e `percentual_ocupacao`. Eventos sem inscritos aparecem com total zero.

2. **Por categoria** - `GET /relatorios/eventos/categorias`
   Para cada categoria retorna: `categoria`, `total_eventos`, `capacidade_total` e `total_inscricoes`.

3. **Por curso** - `GET /relatorios/participantes/cursos`
   Para cada curso retorna: `curso`, `total_participantes` e `total_inscricoes`.

---

## 10. Exemplos de utilizacao da API

Os exemplos usam curl. No PowerShell do Windows, prefira `curl.exe` (o `curl` puro e um apelido de outro comando), ou use o Swagger em `/docs`.

**1. Cadastrar usuario**

```
curl -X POST http://127.0.0.1:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria", "email": "maria@exemplo.com", "senha": "123456"}'
```

Resposta (201):

```
{"id": 2, "nome": "Maria", "email": "maria@exemplo.com", "perfil": "usuario"}
```

**2. Login**

```
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@exemplo.com", "senha": "senha-do-admin"}'
```

Resposta (200):

```
{"access_token": "<token>", "token_type": "bearer"}
```

**3. Consultar os proprios dados**

```
curl http://127.0.0.1:8000/auth/me \
  -H "Authorization: Bearer <token>"
```

**4. Criar evento (administrador)**

```
curl -X POST http://127.0.0.1:8000/eventos/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Semana de Tecnologia", "descricao": "Palestras e oficinas", "data": "2026-12-10", "horario": "19:00:00", "local": "Auditorio", "capacidade": 2, "categoria": "Tecnologia"}'
```

**5. Cadastrar participante**

```
curl -X POST http://127.0.0.1:8000/participantes/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Joao", "email": "joao@exemplo.com", "curso": "Engenharia de Software"}'
```

**6. Inscrever participante 1 no evento 1**

```
curl -X POST http://127.0.0.1:8000/eventos/1/inscricoes/1 \
  -H "Authorization: Bearer <token>"
```

**7. Consultar relatorio de ocupacao (administrador)**

```
curl http://127.0.0.1:8000/relatorios/eventos/ocupacao \
  -H "Authorization: Bearer <token>"
```

---

## 11. Como reproduzir os testes

Os testes sao manuais, feitos pelo Swagger (http://127.0.0.1:8000/docs) ou por curl.

**Preparacao**

1. Apague o arquivo `eventos-academicos.db` para comecar de um banco limpo.
2. Defina `SECRET_KEY`, `ADMIN_EMAIL` e `ADMIN_SENHA` e inicie a API (secoes 3 e 4).

**Cenarios e resultados esperados**

| #   | Cenario                                                        | Esperado                            |
| --- | -------------------------------------------------------------- | ----------------------------------- |
| 1   | Cadastro de usuario (`POST /usuarios`)                         | 201, resposta sem senha e sem hash  |
| 2   | Senha gravada como hash no banco (ver abaixo)                  | coluna `senha_hash` com hash bcrypt |
| 3   | Cadastro repetindo o mesmo e-mail                              | 409                                 |
| 4   | Cadastro de usuario enviando `"perfil": "ADMIN"`               | 201, perfil `usuario`               |
| 5   | Login do administrador com credenciais corretas                | 200                                 |
| 6   | Login do usuario comum                                         | 200                                 |
| 7   | Login com senha incorreta                                      | 401                                 |
| 8   | Login com e-mail inexistente                                   | 401                                 |
| 9   | Listar participantes sem token                                 | 401                                 |
| 10  | Acessar rota protegida com token invalido (texto qualquer)     | 401                                 |
| 11  | Acessar rota protegida com token adulterado (trocar uma letra) | 401                                 |
| 12  | Acessar rota protegida com token expirado (ver abaixo)         | 401                                 |
| 13  | Acessar rota protegida com token valido                        | 200                                 |
| 14  | `GET /auth/me` com token valido                                | 200, dados do proprio usuario       |
| 15  | `GET /auth/me` sem token                                       | 401                                 |
| 16  | Criar evento com token de usuario comum                        | 403                                 |
| 17  | Relatorios com token de usuario comum                          | 403                                 |
| 18  | Criar evento com token de administrador                        | 201                                 |
| 19  | Relatorios com token de administrador                          | 200                                 |
| 20  | Cadastrar participante (com token)                             | 201                                 |
| 21  | Cadastrar participante com e-mail repetido                     | 409                                 |
| 22  | Inscrever participante em evento                               | 201                                 |
| 23  | Repetir a mesma inscricao                                      | 409                                 |
| 24  | Inscrever alem da capacidade do evento                         | 409                                 |
| 25  | Consultar evento inexistente                                   | 404                                 |
| 26  | Listar eventos, participantes e inscritos com token            | 200                                 |
| 27  | Relatorio de ocupacao apos nova inscricao                      | `total_inscritos` aumenta           |
| 28  | Relatorio de ocupacao apos excluir evento                      | evento some do relatorio            |

**Como verificar que a senha foi gravada como hash (cenario 2)**

1. Cadastre um usuario com senha `123456` em `POST /usuarios`.
2. Abra o arquivo `eventos-academicos.db` com uma ferramenta como o DB Browser for SQLite ou a extensao SQLite Viewer do VS Code.
3. Na tabela `usuarios`, confira que a coluna `senha_hash` comeca com `$2b$` e nao contem `123456`.

**Como testar token expirado (cenario 12)**

1. No `auth.py`, troque `EXPIRACAO_TOKEN_MINUTOS = 60` por `1`.
2. Reinicie a API, faca login e copie o token.
3. Espere mais de 1 minuto e use o token em uma rota protegida: deve retornar 401.
4. Volte `EXPIRACAO_TOKEN_MINUTOS` para `60`.

**Como testar token invalido (cenarios 10 e 11)**

No Swagger, clique em **Authorize** e cole um texto qualquer (por exemplo, `abc123`) no lugar do token. Para o token adulterado, copie um token real e troque uma letra do meio.

**Evidencias**

Para cada cenario, registre a requisicao enviada, o codigo HTTP e o corpo da resposta (por exemplo, capturas de tela do Swagger).

Local das evidencias: `<informar pasta ou documento da entrega>`

Cuidado ao testar no Swagger: ao trocar de usuario, clique em **Authorize > Logout** antes de colar o novo token, e copie o `access_token` sem as aspas.
