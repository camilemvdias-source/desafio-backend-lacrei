# Desafio Backend - Lacrei Saúde

API RESTful desenvolvida em Python com **Django** e **Django REST Framework (DRF)** para o desafio técnico de voluntariado da Lacrei Saúde. O sistema gerencia profissionais de saúde e consultas, com autenticação via JWT, testes automatizados e integração contínua (CI/CD).

## Tecnologias utilizadas

* **Python 3.13** & **Django / DRF**
* **Poetry** (gerenciamento de dependências)
* **PostgreSQL** (banco de dados relacional)
* **SimpleJWT** (autenticação via JSON Web Tokens)
* **Docker / Docker Compose** (containerização)
* **GitHub Actions** (pipeline de CI/CD: lint, testes, build e deploy)

## Rodando com Docker (recomendado)

```bash
git clone <url-do-repositorio>
cd desafio-backend-lacrei
cp .env.example .env   # ajuste os valores se quiser
docker-compose up --build
```

A API sobe em `http://localhost:8000`. Migrações rodam automaticamente ao subir o container `web`.

## Rodando localmente sem Docker

Pré-requisitos: Python 3.13, Poetry e um PostgreSQL rodando localmente.

```bash
git clone <url-do-repositorio>
cd desafio-backend-lacrei
cp .env.example .env   # aponte POSTGRES_HOST=localhost e ajuste as credenciais
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser   # opcional, para acessar o /admin
poetry run python manage.py runserver
```

## Rodando os testes

```bash
poetry run python manage.py test
```

Os testes usam `APITestCase` e cobrem: CRUD de profissionais, CRUD de consultas, casos de erro (dados ausentes, referência a profissional inexistente), busca de consultas por profissional (com e sem resultados), detalhe de consulta por ID (existente e inexistente), acesso sem autenticação (rotas públicas e bloqueadas), autenticação via JWT real (obtendo o token em `/api/token/`), validação de contato inválido e bloqueio de consulta para profissional inativo.

## Autenticação (JWT)

As rotas de listagem (`GET`) são públicas; criação, atualização e exclusão exigem autenticação (`IsAuthenticatedOrReadOnly`).

* **Obter token (login):** `POST /api/token/`
  * Payload: `{"username": "seu_usuario", "password": "sua_senha"}`
* **Atualizar token:** `POST /api/token/refresh/`
  * Payload: `{"refresh": "seu_token_refresh"}`

Rotas protegidas: envie `Authorization: Bearer <token_de_acesso>` no header.

## Endpoints principais

* `GET /api/profissionais/` — lista profissionais
* `POST /api/profissionais/` — cadastra profissional (requer autenticação)
* `GET /api/profissionais/{id}/` — detalha um profissional
* `PUT/PATCH /api/profissionais/{id}/` — edita (requer autenticação)
* `DELETE /api/profissionais/{id}/` — remove (requer autenticação)
* `GET /api/consultas/` — lista consultas
* `GET /api/consultas/?profissional=<id>` — busca consultas por profissional
* `POST /api/consultas/` — agenda consulta (requer autenticação)

## Documentação da API

Com o servidor rodando, a documentação interativa fica disponível em:

* **Swagger UI:** `/api/docs/`
* **Redoc:** `/api/redoc/`
* **Schema OpenAPI (JSON/YAML):** `/api/schema/`

Gerada automaticamente a partir dos serializers e views com `drf-spectacular`.

## CI/CD

O pipeline (`.github/workflows/ci-cd.yml`) roda em cada push/PR para `main`/`master` com 4 etapas: **lint** (flake8) → **testes** (contra um PostgreSQL de serviço) → **build** (imagem Docker) → **deploy** (apenas na branch `main`).

## Deploy e rollback

Ver [DEPLOY.md](./DEPLOY.md) para a estratégia de deploy em staging/produção e o plano de rollback.

## Decisões técnicas

* **PostgreSQL via variáveis de ambiente**: nenhuma credencial fica hardcoded; tudo vem de `.env` (local/Docker) ou de secrets do CI. `DJANGO_SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER` e `POSTGRES_PASSWORD` são obrigatórias — se alguma não estiver definida, a aplicação falha ao subir em vez de usar um valor padrão inseguro.
* **JWT (SimpleJWT)** como mecanismo de autenticação por ser stateless e adequado a uma API consumida por outros serviços da Lacrei Saúde.
* **CORS restrito por variável de ambiente** (`CORS_ALLOWED_ORIGINS`), nunca `*`.
* **Logging** configurado em `core/settings.py`: logs de acesso em `logs/access.log` e de erro em `logs/error.log`, além de saída no console (útil em containers).
* **Validações nos serializers**: nome social e endereço com tamanho mínimo, contato validado como telefone (DDD + número) ou e-mail, registro de conselho obrigatório, e bloqueio de agendamento de consulta para profissional inativo.
* **Documentação da API via drf-spectacular**, gerada a partir do código (serializers/views), evitando divergência entre documentação e implementação.

## Problemas encontrados e como foram resolvidos

* **Estrutura de pastas duplicada no repositório**: um `git init` feito na pasta errada deixou todo o projeto aninhado uma pasta abaixo da raiz do repositório, o que quebrava o `docker build` e o `poetry install` no CI (não encontravam `Dockerfile`/`pyproject.toml` na raiz esperada). Corrigido movendo todo o conteúdo para a raiz do repositório.
* **Health check falhando na AWS (`Target.FailedHealthChecks`)**: o Elastic Beanstalk (plataforma Docker) espera a aplicação respondendo na porta 80 da instância, mas o `docker-compose.yml` só expunha a porta 8000. Corrigido mapeando `"80:8000"` no serviço `web`.
* **Falhas de lint (Flake8)**: arquivos sem quebra de linha final (`W292`), import não utilizado (`F401`) e espaços em branco sobrando (`W291`)/linhas em branco em excesso (`E303`) foram corrigidos sem alterar lógica, nomes ou testes.
* **Valor padrão inseguro para `SECRET_KEY` e credenciais de banco**: identificado em revisão — removido; agora a ausência dessas variáveis derruba a aplicação com um erro claro em vez de rodar com um valor conhecido/inseguro.

## Melhorias futuras

* Integração real (ou proposta detalhada de arquitetura) com a Asaas para split de pagamento.
* Cobertura de testes adicional para os endpoints de token JWT (expiração, refresh inválido).
* Paginação e filtros adicionais na listagem de profissionais.
