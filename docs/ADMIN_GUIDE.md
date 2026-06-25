# 📋 GUIA DO ADMINISTRADOR - COVERDE ECOMMERCE

## ✅ O Administrador Pode Agora:

### 1. **Aprovar ou Rejeitar Produtores** 👥

**Localização:** Admin → Utilizadores → Produtores

**Ações Disponíveis:**
- 🟢 **Aprovar Produtores** - Status → Approved, Verificado → Sim
- 🔴 **Rejeitar Produtores** - Status → Rejected
- 🟡 **Suspender Produtores** - Status → Suspended, Ativo → Não
- ✅ **Ativar Produtores** - Ativo → Sim
- ❌ **Desativar Produtores** - Ativo → Não

**Como usar:**
1. Seleccionar um ou mais produtores na lista
2. Escolher ação no dropdown "Ação"
3. Clicar "Ir"

---

### 2. **Aprovar ou Rejeitar Produtos** 📦

**Localização:** Admin → Utilizadores → Aprovações de Produto

**Estados:**
- 🟡 **Pendente** - Novo produto aguardando revisão
- 🟢 **Aprovado** - Produto aprovado, pode ser vendido
- 🔴 **Rejeitado** - Rejeitado com motivo de rejeição

**Como usar:**
1. Ver lista de produtos pendentes
2. Clicar no produto para editar
3. Seleccionar status: Approved/Rejected
4. Se rejeitar: preencher "Motivo da Rejeição"
5. Guardar

**Ações Rápidas:**
- Seleccionar produtos, escolher "Aprovar produtos", clicar "Ir"
- Seleccionar produtos, escolher "Rejeitar produtos", clicar "Ir"

---

### 3. **Gerir Categorias** 📁

**Localização:** Admin → Utilizadores → Categorias

**Funcionalidades:**
- ✏️ Criar nova categoria
- 🗑️ Deletar categoria
- 🔄 Reordenar (campo "Ordem")
- 👁️ Ativar/Desativar
- 📸 Adicionar ícone e imagem

**Como usar:**
1. "Adicionar categoria" para nova
2. Preencher: Nome, Slug (auto), Imagem, Ordem
3. Guardar

---

### 4. **Gerir Encomendas** 🛒

**Localização:** Admin → Encomendas → Encomendas

**Informações Disponíveis:**
- 📌 ID, Consumidor, Items
- 📅 Data de criação
- 💰 Total (excepção: modelo simples não tem total)
- 📊 Filtros por data

**Como usar:**
1. Clicar em encomenda para ver detalhes
2. Ver itens na tabela inline
3. Buscar por email ou ID

---

### 5. **Gerir Pagamentos** 💳

**Localização:** Admin → Pagamentos → Pagamentos

**Informações Disponíveis:**
- 💳 Tipo: 🧪 **TESTE** ou 💳 **Real**
- 💰 Montante
- 📊 Estado: Pendente, A Processar, Pago, Falha, Cancelado
- 🔢 Referência e ID de transação
- ⏰ Data de pagamento

**Filtros:**
- Por estado (Pago, Falha, etc)
- Por método (Cartão, Transferência, etc)
- 🧪 Pagamentos de Teste vs Real

**Ações:**
- ✅ Marcar como pago
- ❌ Marcar como falha

**Como usar:**
1. Ver coluna "Tipo" para identificar Teste vs Real
2. Filtrar por "É Pagamento de Teste" = ✓ para ver apenas testes
3. Seleccionar pagamentos e marcar como Pago/Falha

---

### 6. **Gerir Entregas** 🚚

**Localização:** Admin → Utilizadores → Entregas

**Estados da Entrega:**
- 🟡 **Pendente** - Aguardando envio
- 📦 **Em Trânsito** - A caminho do cliente
- 🟢 **Entregue** - Entrega concluída
- 🔴 **Falha** - Falha na entrega
- 🔄 **Devolvida** - Devolvida pelo cliente

**Campos:**
- 📮 Número de Rastreio (único, obrigatório)
- 🚛 Transportadora (CTT, DHL, Fedex, etc)
- 📍 Morada de entrega
- 📝 Notas de entrega
- ✋ Assinatura obrigatória (Sim/Não)
- 📅 Data agendada e data de entrega

**Ações:**
- 🟡 Marcar como pendente
- 📦 Marcar como em trânsito
- 🟢 Marcar como entregue (auto data)
- 🔴 Marcar como falha

**Como usar:**
1. Criar nova entrega quando ordem é confirmada
2. Preencher rastreio e transportadora
3. Atualizar estado conforme progride
4. Clicar ação para mudar estado em bulk

---

### 7. **Definir Comissões** 💰

**Localização:** Admin → Utilizadores → Comissões da Plataforma

**Tipos de Comissões:**
- 🌍 **Global** - Padrão para todas as categorias
- 📁 **Por Categoria** - Específica por categoria

**Como usar:**
1. "Adicionar comissão" para nova taxa
2. Deixar "Categoria" vazio para comissão global
3. Ou seleccionar categoria específica
4. Preencher percentagem (ex: 5.00 para 5%)
5. Marcar como Ativa
6. Adicionar notas se necessário (para auditar)
7. Guardar

**Exemplo:**
- Comissão Global: 5%
- Categoria "Frutas": 3%
- Categoria "Hortaliças": 4%

---

### 8. **Suspender Produtores ou Produtos** 🛑

**Suspender Produtores:**
1. Admin → Utilizadores → Produtores
2. Seleccionar produtor(es)
3. Ação: "Suspender produtores"
4. Status fica "Suspenso" e Ativo = Não

**Suspender Produtos:**
1. Admin → Utilizadores → Produtos
2. Seleccionar produto(s)
3. Ação: "Suspender produtos (desativar)"
4. Ativo = Não (produto não aparece na loja)

---

### 9. **Aceder a Relatórios Gerais** 📊

**Relatórios Disponíveis via Filtros:**

**Pagamentos:**
- Ver total de pagamentos reais vs teste
- Filtrar por estado
- Filtrar por método

**Produtores:**
- Ver status de aprovação
- Ver rating
- Ver se verificado

**Produtos:**
- Ver por categoria
- Ver por certificação
- Ver ativos vs inativos
- Ver destaques

**Encomendas:**
- Filtrar por data
- Buscar por cliente

**Entregas:**
- Ver por estado
- Ver por transportadora
- Ver por data

---

### 10. **Ver Pagamentos Reais vs Teste** 🧪

**Localização:** Admin → Pagamentos → Pagamentos

**Coluna "Tipo":**
- 🧪 **TESTE** - Pagamento de teste (desenvolvimento)
- 💳 **Real** - Pagamento real do cliente

**Como filtrar:**
1. Ir a "Pagamentos"
2. No filtro "É Pagamento de Teste"
3. Marcar ✓ para ver apenas testes
4. Deixar vazio para ver apenas reais

**Como marcar um pagamento como teste:**
1. Criar/editar pagamento
2. Campo "É Pagamento de Teste" = ✓
3. Preencher "Assinatura de Teste" (ex: COVERDE-TEST)
4. Hash da Senha Teste (opcional, para validação)
5. Guardar

---

## 📝 Resumo de Permissões

| Funcionalidade | Acesso | Status |
|---|---|---|
| Aprovar/Rejeitar Produtores | ✅ | Completo |
| Aprovar/Rejeitar Produtos | ✅ | Completo |
| Gerir Categorias | ✅ | CRUD |
| Gerir Encomendas | ✅ | Visualização |
| Gerir Pagamentos | ✅ | Completo com Teste/Real |
| Gerir Entregas | ✅ | CRUD |
| Definir Comissões | ✅ | Editável |
| Suspender Produtores | ✅ | Actions |
| Suspender Produtos | ✅ | Actions |
| Aceder a Relatórios | ✅ | Via Filtros |
| Ver Teste vs Real | ✅ | Badges 🧪 💳 |

---

## 🔐 Notas de Segurança

✅ Todas as ações são auditadas (Django admin log)
✅ Apenas admin/superuser pode aceder
✅ Campos readonly protegidos contra edição acidental
✅ Confirmação de ações em massa
✅ Timestamps registados automaticamente

---

## 🚀 Próximos Passos (Futuro)

- 📊 Dashboard de vendas com gráficos
- 📈 Relatórios PDF exportáveis
- 📉 Analytics de categorias mais vendidas
- 💰 Relatório de comissões processadas
- 📧 Alertas por email (ex: baixo stock)

---

**Versão:** 1.0
**Data:** 25/06/2026
**Sistema:** Coverde Ecommerce Admin
