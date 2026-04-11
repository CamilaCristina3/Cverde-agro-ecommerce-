# Cverde Agro E-commerce

Plataforma de e-commerce agrícola de impacto social que conecta produtores rurais a consumidores, empresas e logística local.

## Missão
Promover desenvolvimento económico sustentável e inclusivo digitalizando o comércio local e aproximando produtor e consumidor final.

## Stack
- Backend: Python + Django
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Base de dados: PostgreSQL (desenvolvimento padrão em SQLite)

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

## Estrutura
- apps/: apps de domínio (produtores, produtos, encomendas, logística, pagamentos, notificações)
- cverde/: configuração do projeto Django (settings, urls, wsgi)
- templates/ e static/: assets frontend
- docs/: documentação
- tests/: testes automatizados
