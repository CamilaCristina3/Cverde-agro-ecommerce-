# COVERDE Agro E-commerce

Plataforma de e-commerce agricola com foco em aproximar produtores e consumidores, suportando catalogo, carrinho, encomendas, pagamentos e areas de perfil.

Projeto academico desenvolvido com Django.

## Visao Geral

O COVERDE organiza o fluxo principal de um marketplace:

1. Navegacao por produtos e categorias.
2. Carrinho e checkout.
3. Registo/login para consumidor e produtor.
4. Painel do produtor para gestao de produtos.
5. Avaliacoes e area de apoio/FAQ.

## Stack Tecnologica

| Camada | Tecnologia |
|---|---|
| Backend | Python + Django 4.2 |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Base de dados | SQLite (dev) / MySQL (principal) |
| ORM | Django ORM |
| Imagens | Pillow |

Dependencias em [requirements.txt](requirements.txt).

## Requisitos

1. Python 3.11+
2. pip
3. MySQL 8+ (opcional em desenvolvimento se usar SQLite)

## Configuracao Rapida (Desenvolvimento)

### 1) Criar ambiente virtual e instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configurar variaveis de ambiente

Crie um ficheiro `.env` na raiz do projeto.

Exemplo para usar SQLite (mais rapido para desenvolvimento):

```env
DEBUG=true
SECRET_KEY=change-me-dev-coverde
DB_USE_SQLITE=true
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
```

Exemplo para usar MySQL:

```env
DEBUG=true
SECRET_KEY=change-me-dev-coverde
DB_USE_SQLITE=false
DB_NAME=coverde_db
DB_USER=root
DB_PASSWORD=0000
DB_HOST=localhost
DB_PORT=3306
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
```

### 3) Aplicar migracoes e arrancar servidor

```bash
python manage.py migrate
python manage.py runserver
```

Aplicacao disponivel em:

`http://127.0.0.1:8000`

## Comandos Uteis

### Validacao basica do projeto

```bash
python manage.py check
```

### Criar superutilizador

```bash
python manage.py createsuperuser
```

### Carregar fixtures (se necessario)

```bash
python manage.py loaddata fixtures/seed_data.json
```

## Rotas Principais

1. Homepage: `/`
2. Admin: `/admin/`
3. Utilizadores: `/utilizadores/` (compatibilidade tambem em `/users/`)
4. Produtos: `/produtos/`
5. Carrinho: `/encomendas/cart/` e endpoints de carrinho em `/encomendas/cart/...`
6. Encomendas: `/encomendas/`
7. Pagamentos: `/pagamentos/`
8. Avaliacoes: `/avaliacoes/`

## Estrutura do Projeto

```text
Cverde-agro-ecommerce/
├── apps/
│   ├── users_auth/
│   ├── users/
│   ├── products/
│   ├── orders/
│   ├── payments/
│   ├── reviews/
│   ├── stores/
│   ├── cart/
│   └── ...
├── cverde/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/
├── static/
├── media/
├── fixtures/
├── docs/
├── requirements.txt
└── manage.py
```

## Notas de Desenvolvimento

1. O modelo de utilizador ativo e [apps.users_auth.User](apps/users_auth/models.py).
2. O backend de autenticacao por email esta configurado em [cverde/settings.py](cverde/settings.py).
3. A homepage usa dados reais de produtos ativos e fallback visual com imagens estaticas.
4. O projeto inclui melhorias recentes de UI para homepage, catalogo e detalhe de produto.

## Licenca

MIT

## Autoria

Camila Esteves  
Licenciatura em Informatica de Gestao - ISCAC  
a2023110951@alumni.iscac.pt
