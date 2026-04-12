# Cverde Agro E-commerce

Plataforma de e-commerce agrícola de impacto social que conecta produtores rurais a consumidores, empresas e logística local. Projeto académico desenvolvido em Django/Python.

## Missão
Promover desenvolvimento económico sustentável e inclusivo digitalizando o comércio local e aproximando produtor e consumidor final.

## Stack
- Backend: Python + Django
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Base de dados: SQLite (desenvolvimento), PostgreSQL (produção)
- ORM: Django ORM

## Como iniciar (dev)
1) Crie um virtualenv e instale dependências:
```
pip install -r requirements.txt
```
2) Execute migrações e servidor:
```
python manage.py migrate
python manage.py runserver
```

## Dados de demonstração

- Criar/atualizar 6 produtores de exemplo:
```
python manage.py seed_producers
```

## Requisitos SRS (utilizadores)

- Verificação de email: após registo é enviado link; login só após confirmar.
- 2FA opcional por email: pode ativar em `Minha Conta -> Editar perfil`.

## Estrutura
- apps/: apps de domínio (utilizadores, produtores, produtos, encomendas, pagamentos, notificações)
- cverde/: configuração do projeto Django (settings, urls, wsgi)
- templates/ e static/: assets frontend
- docs/: documentação
- tests/: testes automatizados

## Funcionalidades

### Página Inicial
- Hero com call-to-action
- Categorias de produtos
- Produtos em destaque
- Listagem de produtores locais

### Painel de Produtor
- Métricas de vendas, encomendas, produtos e avaliações
- Gestão de produtos disponíveis
- Acompanhamento de encomendas

### Listagem de Produtos
- Produtos agrupados por produtor
- Detalhes de categoria, unidade, stock e preço
- Filtragem por disponibilidade
