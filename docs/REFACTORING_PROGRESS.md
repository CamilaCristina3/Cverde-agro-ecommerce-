# 🏗️ REFACTORING DJANGO APPS - ESTRUTURA REORGANIZADA

## ✅ FASE 1: Criação da Estrutura de Apps - COMPLETA

### Novo Mapa de Apps

```
apps/
├── users_auth/          # 🔐 User authentication & authorization
├── producers/           # 🌾 Producer profiles & management  
├── stores/              # 🏪 Producer storefronts
├── categories/          # 📁 Product categories
├── products/            # 📦 Product catalog
├── inventory/           # 📊 Inventory management
├── cart/                # 🛒 Shopping cart
├── orders_mgmt/         # 📋 Order management
├── payments/            # 💳 Payment processing
├── deliveries/          # 🚚 Delivery management
├── reviews/             # ⭐ Reviews & ratings
├── support/             # 💬 Support & ticketing
└── reports/             # 📈 Reports & analytics
```

### Status de Criação

| App | Models | Admin | Views | URLs | Status |
|---|---|---|---|---|---|
| users_auth | ✅ User, EmailToken, 2FA | ✅ | ✅ | ✅ | PRONTO |
| producers | ✅ Producer, Certification | ✅ | ✅ | ✅ | PRONTO |
| stores | ✅ Store | ✅ | ✅ | ✅ | PRONTO |
| categories | ✅ Category | ✅ | ✅ | ✅ | PRONTO |
| products | ✅ Product, ProductApproval | ✅ | ✅ | ✅ | PRONTO |
| inventory | ✅ InventoryLog, StockAlert | ✅ | ✅ | ✅ | PRONTO |
| cart | ✅ Cart, CartItem | ✅ | ✅ | ✅ | PRONTO |
| orders_mgmt | ✅ Order, OrderItem | ✅ | ✅ | ✅ | PRONTO |
| payments | ✅ Payment (existente) | ⚠️ | ✅ | ✅ | PRONTO |
| deliveries | ✅ Delivery | ✅ | ✅ | ✅ | PRONTO |
| reviews | ✅ Review (existente) | ✅ | ⚠️ | ✅ | PARCIAL |
| support | ✅ Ticket, Message | ✅ | ✅ | ✅ | PRONTO |
| reports | ✅ SalesReport, CommissionReport | ✅ | ✅ | ✅ | PRONTO |

## ⚠️ FASE 2: Migração de Imports - EM PROGRESSO

### Problemas Identificados

1. **Circular Dependencies**: Múltiplos arquivos importam de `apps.users.models` que não está mais em INSTALLED_APPS
   - apps/payments/views.py 
   - apps/reviews/views.py
   - cverde/views.py

2. **Modelos Legados**: `apps/users.models` e `apps/orders.models` ainda existem mas não devem ser usados

3. **URLs Conflitantes**: Namespace "orders" pode estar duplicado

### Solução

Preciso fazer find & replace em todos os arquivos:

```python
# OLD
from apps.users.models import Product, Producer, Category, Order

# NEW
from apps.products.models import Product
from apps.producers.models import Producer
from apps.categories.models import Category
from apps.orders_mgmt.models import Order
```

### Arquivos que Precisam Update

- [ ] apps/payments/views.py - Importa Order de apps.users
- [ ] apps/reviews/views.py - Importa Product, Producer, Order, OrderItem de apps.users
- [ ] cverde/views.py - ✅ CORRIGIDO
- [ ] Qualquer outro arquivo com imports legados

## 📋 PRÓXIMAS ETAPAS

### Fase 3: Limpeza de Imports (Próximo)
1. Find all references to old apps (apps.users, apps.orders)
2. Replace com imports novos
3. Test cada módulo

### Fase 4: Migrations
1. Deletar db.sqlite3
2. Deletar todas as migrations antigas
3. `python manage.py makemigrations` para cada novo app
4. `python manage.py migrate`
5. `python manage.py createsuperuser`

### Fase 5: Testes
1. Verificar se sistema sobe
2. Testar admin
3. Testar views
4. Testar models

### Fase 6: Remoção de Legacy Apps
1. Depois de verificar que tudo funciona em novo setup
2. Remover apps.users, apps.orders, apps.notifications, apps.pages, apps.chat, apps.logistics
3. Limpar imports e dependências

## 📊 SETTINGS.PY UPDATE

### INSTALLED_APPS ✅ ATUALIZADO

```python
INSTALLED_APPS = [
    # Django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Third-party
    'channels',
    
    # NEW REFACTORED APPS (13 apps)
    'apps.users_auth',
    'apps.producers',
    'apps.stores',
    'apps.categories',
    'apps.products',
    'apps.inventory',
    'apps.cart',
    'apps.orders_mgmt',
    'apps.payments',
    'apps.deliveries',
    'apps.reviews',
    'apps.support',
    'apps.reports',
    
    # Legacy (to be removed)
    'apps.notifications',
    'apps.pages',
    'apps.chat',
]
```

### AUTH_USER_MODEL ✅ ATUALIZADO

```python
AUTH_USER_MODEL = 'users_auth.User'
```

## 🔗 URLS.PY UPDATE

### cverde/urls.py ✅ ATUALIZADO

```python
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("admin/", admin.site.urls),
    
    # New refactored apps
    path("auth/", include("apps.users_auth.urls")),
    path("producers/", include("apps.producers.urls")),
    path("stores/", include("apps.stores.urls")),
    path("categories/", include("apps.categories.urls")),
    path("products/", include("apps.products.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("cart/", include("apps.cart.urls")),
    path("orders/", include("apps.orders_mgmt.urls")),
    path("payments/", include("apps.payments.urls")),
    path("deliveries/", include("apps.deliveries.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("support/", include("apps.support.urls")),
    path("reports/", include("apps.reports.urls")),
    
    # Legacy apps (temporary)
    path("notifications/", include("apps.notifications.urls")),
    path("chat/", include("apps.chat.urls")),
    path("", include("apps.pages.urls")),
]
```

## 📝 DETALHES DOS APPS

### apps/users_auth
- **Purpose**: User authentication and authorization
- **Models**: User (custom), EmailVerificationToken, TwoFactorCode
- **Key Features**: RGPD compliance, security lockout, 2FA support

### apps/producers
- **Purpose**: Farmer/producer profiles
- **Models**: Producer, ProducerCertification
- **Features**: Verification workflow, certification tracking, rating system

### apps/stores
- **Purpose**: Producer storefronts
- **Models**: Store
- **Features**: Custom shop branding, delivery methods, operating hours

### apps/categories
- **Purpose**: Product taxonomy
- **Models**: Category (hierarchical)
- **Features**: Nested categories, custom ordering

### apps/products
- **Purpose**: Product catalog
- **Models**: Product, ProductImage, ProductApproval
- **Features**: Multi-image gallery, approval workflow, certifications

### apps/inventory
- **Purpose**: Stock management
- **Models**: InventoryLog, StockAlert
- **Features**: Movement tracking, low-stock alerts

### apps/cart
- **Purpose**: Shopping cart
- **Models**: Cart, CartItem
- **Features**: Session-based or persistent cart

### apps/orders_mgmt
- **Purpose**: Order lifecycle
- **Models**: Order, OrderItem
- **Features**: Status workflow, shipping tracking

### apps/payments
- **Purpose**: Payment processing
- **Models**: Payment
- **Features**: Test mode, multiple payment methods, transaction tracking

### apps/deliveries
- **Purpose**: Shipment tracking
- **Models**: Delivery
- **Features**: Carrier integration, status updates, rastreio

### apps/reviews
- **Purpose**: Customer ratings and feedback
- **Models**: Review
- **Features**: Verified purchases, moderation, aggregated ratings

### apps/support
- **Purpose**: Customer support
- **Models**: SupportTicket, TicketMessage
- **Features**: Ticketing system, priority levels, assignment

### apps/reports
- **Purpose**: Analytics and reporting
- **Models**: SalesReport, CommissionReport
- **Features**: Period aggregation, commission calculations

## 🚀 PRÓXIMOS COMMANDS

```bash
# 1. Fix remaining imports
# (Will be done manually)

# 2. Delete old database
rm db.sqlite3

# 3. Delete old migrations
find apps -name migrations -type d -exec rm -rf {} +

# 4. Create new migrations
python manage.py makemigrations

# 5. Apply migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Check system
python manage.py check

# 8. Run server
python manage.py runserver
```

## 📚 REFERENCES

- Original Inventory: docs/PROJECT_INVENTORY.md
- Admin Guide: docs/ADMIN_GUIDE.md
- Client Guide: docs/CLIENT_GUIDE.md

---

**Status**: Phase 2 (In Progress)
**Last Updated**: 2026-06-25
**Next Task**: Fix all import statements
