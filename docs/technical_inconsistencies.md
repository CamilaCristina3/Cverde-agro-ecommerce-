# Technical inconsistencies — Coverde

Resumo conciso das inconsistências técnicas identificadas no repositório Coverde.

Objetivo: documentar duplicações de modelos e referências cruzadas para apoiar uma unificação futura sem alterar código, migrations ou base de dados neste passo.

1) Duplicações principais
- Orders / OrderItem
  - `apps/users/models.py` define `Order` e `OrderItem` (completo: subtotal, shipping_cost, vat, total, status, invoice_number, payment OneToOne, etc.).
  - `apps/orders/models.py` define `Order` e `OrderItem` simplificados (user, created_at; items com product+quantity).
  - Evidência: templates e views usam `order.items`, `order.total`, `order.get_status_display()` (ex.: `templates/orders/detail.html`, `apps/users/views.py`), enquanto `apps/payments/models.py` e `apps/payments` migrations referenciam `orders.Order`.

- Products
  - `apps/products/models.py` é o modelo autoritativo (usado em views/templates). Há sinais de um `Product` também presente em `apps/users.models` (duplicação histórica). Preferir `apps/products.Product`.

- Producers
  - `apps/producers.models.Producer` e `apps/users.models.Producer` coexistem. Código de runtime costuma usar `apps.producers.Producer`, mas migrations/dumps podem apontar para `users.producer` em versões antigas.

2) Referências cruzadas e riscos
- `apps/payments/models.py` importa `from apps.orders.models import Order` — payments migrations point to `orders.order` table. Contudo, várias views and templates use `users.Order` API. Risco: FK/migrations e runtime inconsistência.
- SQL dumps (`coverde_db.sql`, `coverde_db_backup.sql`) incluem tabelas `users_order` e `orders_order` ambos, o que mostra que ambientes diferentes podem ter estados divergentes.

3) Impacto e riscos
- Alterações estruturais (mover/renomear modelos, editar migrations) podem quebrar o ambiente do avaliador ou impedir execução do projecto — por isso não devem ser aplicadas antes da entrega académica.
- Problemas possíveis: referências a campos inexistentes, integrações de pagamentos falharem por FK para outra tabela, dificuldades em debug e manutenção.

4) Recomendações imediatas (ações seguras)
- Documentar esta inconsistência (este ficheiro).
- Incluir inventário por linha (já recolhido) e anexar aos docs para facilitar auditoria futura.
- Atualizar `README_submission.md` para clarificar criação de `demoadmin` via `create_demo_data` (evita confusão sobre senhas pré-existentes).
- Evitar alterações em modelos/migrations/DB até haver plano de unificação aprovado.

5) Plano de unificação (alto nível — não aplicar agora)
- Mapear campos entre `users.Order` e `orders.Order` e entre `users.OrderItem` e `orders.OrderItem`.
- Decidir modelo autoritativo (recomendado: `apps/users.models.Order` pela completude) e preparar script de migração de dados (export, transform, importar para tabela alvo).
- Criar migrations de transição e testes automatizados antes de alteração real.

6) Próximos passos propostos (aplicar um de cada vez)
- Criar documentação (feito). Executar `python manage.py check` (para validar que não há erros óbvios).  
- Atualizar `README_submission.md` com instrução clara sobre `create_demo_data` e `changepassword`.  
- Preparar documento de mapeamento detalhado (campo a campo) para `Order`/`OrderItem`.

---
Gerado automaticamente pela auditoria em workspace local — não altera código nem migrations.
