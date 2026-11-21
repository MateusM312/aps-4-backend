================================================================
GERENCIAMENTO DE EVENTOS ACADEMICOS
API REST com FastAPI, SQLite, SQLAlchemy e autenticacao JWT
Autores: Santana & Mendes
================================================================

1. DESCRICAO DO PROJETO

---

API para gerenciar eventos academicos, participantes e inscricoes.
Os dados ficam em um banco SQLite acessado com SQLAlchemy.

Funcionalidades:

- Cadastro, consulta, atualizacao e exclusao de eventos e participantes.
- Inscricao de participantes em eventos, com controle de vagas
  (capacidade do evento) e bloqueio de inscricao duplicada.
- Tres relatorios consolidados (ocupacao por evento, por categoria
  e por curso).
- Cadastro de usuarios e login com token JWT.
- Controle de acesso por perfil: "usuario" e "administrador".

2. INSTALACAO

---

Requisitos: Python 3.10 ou superior.

1. Baixe o projeto e entre na pasta:

   git clone <URL-DO-REPOSITORIO>
   cd aps-4-backend

2. Crie o ambiente virtual:

   py -m venv venv

3. Ative o ambiente virtual.

   PowerShell (Windows):
   Set-ExecutionPolicy -Scope Process Bypass
   venv\Scripts\activate

   Prompt de Comando (cmd):
   venv\Scripts\activate.bat

   Linux / Mac:
   source venv/bin/activate

4. Instale as dependencias:

   pip install -r requirements.txt

3) CONFIGURACAO (VARIAVEIS DE AMBIENTE)

---

A chave do JWT NAO fica escrita no codigo. Ela e lida de uma
variavel de ambiente. As variaveis devem ser definidas no MESMO
terminal em que a API for iniciada, antes do comando uvicorn.

SECRET_KEY Obrigatoria. Chave usada para assinar os tokens.
Sem ela a API nao inicia.
ADMIN_EMAIL Opcional. E-mail do administrador inicial.
ADMIN_SENHA Opcional. Senha do administrador inicial.
ADMIN_NOME Opcional. Nome do administrador inicial
(padrao: "Administrador").

PowerShell (Windows):

$env:SECRET_KEY="uma-chave-longa-e-aleatoria"
$env:ADMIN_EMAIL="admin@exemplo.com"
$env:ADMIN_SENHA="senha-do-admin"

Prompt de Comando (cmd):

set SECRET_KEY=uma-chave-longa-e-aleatoria
set ADMIN_EMAIL=admin@exemplo.com
set ADMIN_SENHA=senha-do-admin

Linux / Mac:

export SECRET_KEY="uma-chave-longa-e-aleatoria"
export ADMIN_EMAIL="admin@exemplo.com"
export ADMIN_SENHA="senha-do-admin"

Administrador inicial:
Na inicializacao, se ADMIN_EMAIL e ADMIN_SENHA estiverem definidas
e esse e-mail ainda nao existir no banco, o administrador e criado
automaticamente com o perfil "administrador". Este e o UNICO
caminho para criar um administrador: o cadastro publico
(POST /usuarios) sempre cria o perfil "usuario", mesmo que o JSON
enviado contenha o campo "perfil".

Perfis antigos:
Se o banco tiver usuarios com perfil "ADMIN" ou "CLIENTE" (versao
anterior do projeto), eles sao convertidos para "administrador" e
"usuario" na inicializacao.

4. EXECUCAO

---

Com o ambiente virtual ativo e as variaveis definidas:

uvicorn main:app --reload

- API: http://127.0.0.1:8000
- Documentacao (Swagger): http://127.0.0.1:8000/docs

Dica: o terminal onde a API roda apenas mostra o log. Para rodar
outros comandos (curl, Invoke-RestMethod), abra um segundo terminal.

5. ESTRUTURA DO PROJETO

---

main.py Cria o app, as tabelas e o administrador inicial
database.py Conexao com o SQLite e sessao do banco
auth.py Hash de senha, JWT e controle de acesso
models/ Tabelas do banco (SQLAlchemy)
schema/ Validacao de entrada e saida (Pydantic)
routers/ Rotas HTTP
services/ Regras de negocio
repositories/ Consultas ao banco
requirements.txt Dependencias do projeto

Fluxo de uma requisicao: router -> service -> repository -> banco.

6. BANCO DE DADOS

---

- Tipo: SQLite.
- Arquivo: eventos-academicos.db, criado automaticamente na pasta
  de onde o uvicorn for iniciado (normalmente a raiz do projeto),
  conforme DATABASE_URL em database.py.
- O arquivo .db esta no .gitignore e nao vai para o repositorio.
  Para recriar o banco do zero, basta apagar o arquivo e iniciar a
  API de novo.
- As tabelas sao criadas automaticamente na primeira execucao.

Tabelas:
usuarios id, nome, email (unico), senha_hash, perfil
participantes id, nome, email (unico), curso
eventos id, titulo, descricao, data, horario, local,
capacidade, categoria
inscricoes id, evento_id, participante_id, data_inscricao
(par evento_id + participante_id e unico)

Observacoes:

- A restricao unica em inscricoes impede inscricao duplicada.
- Ao excluir um evento, as inscricoes dele sao removidas junto.
- As senhas sao guardadas apenas como hash (bcrypt).

7. PERFIS E AUTENTICACAO

---

Perfis:
usuario Obtido no cadastro (POST /usuarios).
Consulta e opera participantes e inscricoes.
administrador Criado na inicializacao (variaveis ADMIN\_\*).
Tudo que o usuario faz, mais gerenciar eventos
e consultar relatorios.

Como autenticar:

1. Cadastre-se em POST /usuarios (ou use o administrador inicial).
2. Faca login em POST /auth/login e copie o "access_token".
3. Envie o token no cabecalho de cada requisicao protegida:

   Authorization: Bearer <access_token>

No Swagger (/docs): clique em "Authorize", cole apenas o token
(sem a palavra Bearer e sem aspas) e confirme.

O token expira em 60 minutos e guarda o id do usuario no campo
"sub". Token ausente, invalido ou expirado retorna 401 com a
mensagem "Nao foi possivel validar as credenciais.".

8. PRINCIPAIS ROTAS

---

PUBLICAS (sem token)

GET / Teste da API
POST /usuarios Cadastrar usuario
POST /auth/login Login (retorna o token)
GET /eventos Listar eventos
GET /eventos/{id} Consultar evento

EXIGEM LOGIN (qualquer perfil)

GET /auth/me Dados do usuario logado
POST /participantes Cadastrar participante
GET /participantes Listar participantes
GET /participantes/{id} Consultar participante
PUT /participantes/{id} Atualizar participante
DELETE /participantes/{id} Excluir participante
POST /eventos/{evento_id}/inscricoes/{participante_id}
Inscrever participante
GET /eventos/{evento_id}/inscricoes
Listar inscritos do evento

SOMENTE ADMINISTRADOR

POST /eventos Cadastrar evento
PUT /eventos/{id} Atualizar evento
DELETE /eventos/{id} Excluir evento
GET /relatorios/eventos/ocupacao Relatorio de ocupacao
GET /relatorios/eventos/categorias Relatorio por categoria
GET /relatorios/participantes/cursos
Relatorio por curso

Codigos de resposta principais:
200 Sucesso
201 Criado com sucesso
401 Token ausente/invalido/expirado ou login incorreto
403 Usuario logado sem permissao de administrador
404 Evento ou participante nao encontrado
409 E-mail ja cadastrado, participante ja inscrito no evento
ou evento sem vagas
422 Dados invalidos (ex.: e-mail mal formado, capacidade <= 0)

9. RELATORIOS E INFORMACOES CONSOLIDADAS

---

Todos os relatorios sao exclusivos do administrador e sao
calculados no banco com consultas agrupadas (GROUP BY).

1. Ocupacao por evento
   GET /relatorios/eventos/ocupacao
   Para cada evento retorna: evento_id, titulo, capacidade,
   total_inscritos, vagas_disponiveis e percentual_ocupacao.
   Eventos sem inscritos aparecem com total zero.

2. Por categoria
   GET /relatorios/eventos/categorias
   Para cada categoria retorna: categoria, total_eventos,
   capacidade_total e total_inscricoes.

3. Por curso
   GET /relatorios/participantes/cursos
   Para cada curso retorna: curso, total_participantes e
   total_inscricoes.

10) EXEMPLOS DE UTILIZACAO DA API

---

Os exemplos usam curl. No PowerShell do Windows, prefira
"curl.exe" (o "curl" puro e um apelido de outro comando), ou use
o Swagger em /docs.

1. Cadastrar usuario

   curl -X POST http://127.0.0.1:8000/usuarios \
    -H "Content-Type: application/json" \
    -d '{"nome": "Maria", "email": "maria@exemplo.com", "senha": "123456"}'

   Resposta (201):
   {"id": 2, "nome": "Maria", "email": "maria@exemplo.com",
   "perfil": "usuario"}

2. Login

   curl -X POST http://127.0.0.1:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "admin@exemplo.com", "senha": "senha-do-admin"}'

   Resposta (200):
   {"access_token": "<token>", "token_type": "bearer"}

3. Criar evento (administrador)

   curl -X POST http://127.0.0.1:8000/eventos/ \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"titulo": "Semana de Tecnologia", "descricao": "Palestras e oficinas", "data": "2026-12-10", "horario": "19:00:00", "local": "Auditorio", "capacidade": 2, "categoria": "Tecnologia"}'

4. Cadastrar participante

   curl -X POST http://127.0.0.1:8000/participantes/ \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"nome": "Joao", "email": "joao@exemplo.com", "curso": "Engenharia de Software"}'

5. Inscrever participante 1 no evento 1

   curl -X POST http://127.0.0.1:8000/eventos/1/inscricoes/1 \
    -H "Authorization: Bearer <token>"

6. Consultar relatorio de ocupacao (administrador)

   curl http://127.0.0.1:8000/relatorios/eventos/ocupacao \
    -H "Authorization: Bearer <token>"

11) COMO REPRODUZIR OS TESTES

---

Os testes sao manuais, feitos pelo Swagger (http://127.0.0.1:8000/docs)
ou por curl.

Preparacao:

1. Apague o arquivo eventos-academicos.db para comecar de um banco
   limpo.
2. Defina SECRET_KEY, ADMIN_EMAIL e ADMIN_SENHA e inicie a API
   (secoes 3 e 4).

Cenarios e resultados esperados:

Cenario Esperado

---

Listar participantes sem token 401
Login do administrador com credenciais corretas 200
Login com senha incorreta 401
Cadastro de usuario enviando "perfil": "ADMIN" 201,
perfil "usuario"
Cadastro repetindo o mesmo e-mail 409
Login do usuario comum 200
Relatorios com token de usuario comum 403
Criar evento com token de usuario comum 403
Relatorios com token de administrador 200
Criar evento com token de administrador 201
Cadastrar participante (com token) 201
Cadastrar participante com e-mail repetido 409
Inscrever participante em evento 201
Repetir a mesma inscricao 409
Inscrever alem da capacidade do evento 409
Consultar evento inexistente 404

Evidencias:
Para cada cenario, registre a requisicao enviada, o codigo HTTP e
o corpo da resposta (por exemplo, capturas de tela do Swagger).
Local das evidencias: <informar pasta ou documento da entrega>.

Cuidado ao testar no Swagger: ao trocar de usuario, clique em
"Authorize" > "Logout" antes de colar o novo token, e copie o
"access_token" sem as aspas.
