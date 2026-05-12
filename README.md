# 🌱 Coverde Agro E-commerce

Plataforma de e-commerce agrícola de impacto social que conecta produtores rurais a consumidores, empresas e logística local.  
**Projeto académico** desenvolvido em Django/Python.

## 🎯 Missão

Promover desenvolvimento económico sustentável e inclusivo, digitalizando o comércio local e aproximando produtor e consumidor final.

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| Backend | Python + Django |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Base de Dados | SQLite (desenvolvimento) / MySQL (produção) |
| ORM | Django ORM |

## 🚀 Como iniciar (desenvolvimento)

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar base de dados (SQLite para testes rápidos)
echo "DB_USE_SQLITE=true" > .env

# 4. Aplicar migrações
python manage.py migrate

# 5. Executar servidor
python manage.py runserver

Aceda em: http://127.0.0.1:8000

🗄️ Como restaurar a base de dados MySQL (para avaliação)
Pré-requisitos
MySQL instalado (versão 8.0+)

Acesso ao terminal

Passos
bash
# 1. Criar a base de dados
mysql -u root -p -e "CREATE DATABASE coverde_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

# 2. Restaurar o backup
mysql -u root -p coverde_db < coverde_db_backup.sql

# 3. Configurar o .env para usar MySQL
echo "DB_USE_SQLITE=false" > .env
echo "DB_NAME=coverde_db" >> .env
echo "DB_USER=root" >> .env
echo "DB_PASSWORD=" >> .env
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=3306" >> .env

# 4. Executar o servidor
python manage.py runserver
Credenciais de teste (após restauro)
Perfil	Email	Password
Consumidor	consumidor@teste.com	teste123
Produtor	produtor@teste.com	teste123
Administrador	admin@coverde.pt	admin123
📦 Dados de demonstração (alternativa com fixtures)
bash
# Carregar dados de exemplo (sem MySQL)
python manage.py loaddata fixtures/seed_data.json
👥 Requisitos SRS (utilizadores)
Verificação de email: após registo é enviado link de confirmação; login só após confirmar.

2FA opcional por email: pode ativar em Minha Conta → Editar perfil.

📁 Estrutura do Projeto
text
Cverde-agro-ecommerce/
├── apps/                    # Apps de domínio
│   ├── users/              # Autenticação e perfis
│   ├── products/           # Catálogo de produtos
│   ├── orders/             # Encomendas e carrinho
│   ├── payments/           # Pagamentos
│   └── notifications/      # Notificações
├── cverde/                 # Configuração do projeto
├── templates/              # Templates HTML
├── static/                 # Ficheiros estáticos
├── fixtures/               # Dados de exemplo (JSON)
├── docs/                   # Documentação
├── tests/                  # Testes automatizados
├── requirements.txt
├── manage.py
└── coverde_db_backup.sql   # Backup MySQL
✨ Funcionalidades
Página Inicial
Hero com call-to-action

Categorias de produtos

Produtos em destaque

Listagem de produtores locais

Painel do Produtor
Métricas de vendas, encomendas, produtos e avaliações

Gestão de produtos disponíveis

Acompanhamento de encomendas

Listagem de Produtos
Produtos agrupados por produtor

Detalhes de categoria, unidade, stock e preço

Filtragem por disponibilidade

💬 Chat em tempo real (WebSockets)
Pré-requisitos
pip install -r requirements.txt

Configuração
- Por defeito (sem Redis): usa InMemoryChannelLayer (bom para DEV).
- Com Redis: define REDIS_URL (ex.: redis://localhost:6379/0).

Rotas
- UI: /chat/
- WebSocket: /ws/chat/<room_name>/

## 🏷️ Release v1.0.0
- Integração da secretária virtual Coverde com widget flutuante em todas as páginas
- Adição de chat em tempo real com Django Channels e WebSockets
- Otimização de frontend: CSS/JS minificados e imagens otimizadas
- Correção de configuração do app `apps.producers` no `INSTALLED_APPS`
- Ajustes no admin Django para compatibilidade com o modelo `Producer`

Licença
MIT License

 Autora
Camila Esteves
Licenciatura em Informática de Gestão – ISCAC
a2023110951@alumni.iscac.pt
