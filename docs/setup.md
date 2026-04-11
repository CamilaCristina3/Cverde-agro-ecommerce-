# Setup de desenvolvimento

1. Criar virtualenv e instalar dependências: `pip install -r requirements.txt`.
2. Configurar `.env` com credenciais do PostgreSQL ou usar SQLite para dev.
3. Aplicar migrações: `python manage.py migrate`.
4. Rodar servidor: `python manage.py runserver`.
5. (Opcional) Via Docker: `docker-compose up`.
