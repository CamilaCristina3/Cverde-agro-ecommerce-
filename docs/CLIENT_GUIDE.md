# 🛒 GUIA DO CLIENTE - COVERDE ECOMMERCE

## ✅ O Cliente Pode Agora:

### 1. **Criar Conta** 👤

**Localização:** Botão "Registar" na navbar ou `/users/register/`

**Tipos de Conta:**
- 👥 **Consumidor** - Para comprar produtos
- 🌾 **Produtor** - Para vender produtos

**Como registar:**
1. Clicar em "Registar como Consumidor"
2. Preencher:
   - Email (vai receber confirmação)
   - Password (mínimo 8 caracteres)
   - Primeiro e último nome
   - Telemóvel (opcional)
3. Aceitar termos e política de privacidade
4. Clicar "Registar"

---

### 2. **Confirmar Conta por Email/Token** ✅

**Como confirmar:**
1. Após registar, receberá email com link de confirmação
2. Clicar no link ou copiar token
3. Link levará para página de confirmação automática
4. Ou inserir manualmente o token se solicitado
5. Conta confirmada! ✓

**Validade:** Token válido por 7 dias

---

### 3. **Ver Produtos** 📦

**Localização:** Menu → "Produtos" ou `/products/`

**Funcionalidades:**
- 📸 Imagem do produto
- 📝 Nome e descrição
- 💰 Preço
- 📊 Stock disponível
- 🌾 Produtor/Quinta
- 🏷️ Categoria
- ✅ Certificação (Biológico, DOP, etc)

**Filtros Disponíveis:**
- 🔍 Buscar por nome ou produtor
- 📁 Filtrar por categoria
- ✅ Filtrar por certificação
- 👥 Filtrar por produtor
- 📊 Ordenar por (novo, preço, avaliação)
- 📦 Em stock vs Todos

---

### 4. **Filtrar por Categoria** 📁

**Como filtrar:**
1. Na página de produtos, ver filtro "Categoria"
2. Seleccionar categoria desejada (ex: Frutas, Hortaliças)
3. Produtos filtrados aparecem automaticamente

**Categorias Disponíveis:**
- 🍎 Frutas
- 🥗 Hortaliças
- 🥛 Lacticínios
- 🍞 Pão e Cereais
- 🍯 Mel e Doces
- (... outras)

---

### 5. **Adicionar Produtos ao Carrinho** 🛒

**Como adicionar:**
1. Ver produto desejado
2. Clicar em "Adicionar ao Carrinho"
3. Seleccionar quantidade (ou padrão 1)
4. Mensagem "✓ Adicionado ao carrinho"

**Limitações:**
- Máximo = stock disponível
- Não pode adicionar produto esgotado

**Ver Carrinho:**
- Clicar ícone 🛒 no topo direito
- Ou ir a `/orders/cart/`

---

### 6. **Fazer Encomendas** 🛍️

**Fluxo de Compra:**

#### Passo 1: Ver Carrinho
1. Clicar 🛒 Carrinho
2. Ver produtos adicionados
3. Ver subtotal, IVA (23%), portes
4. Total = Subtotal + IVA + Portes

**Dados do Carrinho:**
- 📦 Produto + Quantidade
- 💰 Preço unitário
- 🔄 Botão para atualizar quantidade
- 🗑️ Botão para remover item

#### Passo 2: Checkout
1. Clicar "Proceder para Checkout"
2. Ser redireccionado para `/orders/checkout/`
3. Preencher dados de entrega

#### Passo 3: Confirmar Encomenda
1. Ver resumo de produtos
2. Ver total final
3. Clicar "Finalizar Encomenda"

---

### 7. **Escolher Endereço de Entrega** 📍

**Durante o Checkout:**

1. Preencher "Morada de Entrega"
   - Rua, número, andar (se aplicável)
   - Código postal + Localidade
   - Exemplo: "Rua da Paz, nº 123, 3º dto, 3000-000 Covilhã"

2. Preencher "Contacto para Entrega"
   - Telemóvel (ex: 912345678)
   - Usado pela transportadora para contactar

3. Confirmar e prosseguir para pagamento

---

### 8. **Fazer Pagamento em Modo Teste** 💳

**Acesso ao Pagamento:**
1. Após confirmar encomenda
2. Ser redireccionado para `/payments/checkout/<order_id>/`
3. Ver dados da encomenda e total

**Credenciais de Teste:**

Escolher UMA das opções:

**Opção 1: Senha de Teste**
- Campo: "Senha de Teste"
- Valor: `1234`
- Clicar "Processar Pagamento"

**Opção 2: Assinatura de Teste**
- Campo: "Assinatura"
- Valor: `COVERDE-TEST`
- Clicar "Processar Pagamento"

**Resultado:**
- ✅ Pagamento aprovado
- 📧 Email de confirmação
- 🟢 Encomenda marcada como "Confirmada"

**Nota:** Em produção, isto será integrado com gateway real (Stripe, MBway, etc)

---

### 9. **Acompanhar Estado da Encomenda** 📦

**Ver Minhas Encomendas:**
1. Login na conta
2. Menu → "Minhas Encomendas"
3. Ver lista de todas as suas encomendas

**Estados da Encomenda:**
- 🟡 **Pendente** - Acabada de criar
- 🔵 **Confirmada** - Pagamento recebido
- 💳 **Paga** - Processada
- 📦 **Em Preparação** - Sendo embalada
- 🚚 **Enviada** - Em trânsito para você
- 🟢 **Entregue** - Chegou!
- 🔴 **Cancelada** - Cancelada pelo cliente ou loja

**Detalhes da Encomenda:**
- 📌 ID (#123456)
- 📅 Data de criação
- 💰 Total pago
- 📍 Morada de entrega
- 📮 Código de rastreio (quando em trânsito)
- 🏪 Produtos encomendados
- 📊 Estado actual

**Rastreio:**
- Ver "Código de Rastreio" com transportadora
- Integração futura com CTT, DHL, etc

---

### 10. **Avaliar Produtos e Lojas** ⭐

**Criar Avaliação de Produto:**
1. Ir para produto que comprou
2. Clicar "Deixar Avaliação" ou "Avaliar este Produto"
3. Preencher formulário:
   - ⭐ **Classificação** (1-5 estrelas)
   - **Título** (ex: "Produto excelente!")
   - **Comentário** (detalhes da avaliação, máx 1000 caracteres)
4. Clicar "Guardar Avaliação"

**Criar Avaliação de Produtor/Quinta:**
1. Ir para página do produtor
2. Clicar "Avaliar este Produtor"
3. Preencher formulário igual:
   - ⭐ **Classificação** (1-5 estrelas)
   - **Título** (ex: "Produtor muito fiável")
   - **Comentário** (feedback sobre o serviço)
4. Clicar "Guardar Avaliação"

**Validação:**
- ✅ Apenas se comprou o produto/produtor
- 📌 "Compra Verificada" aparece na avaliação
- 🟢 Auto-aprovada (visível imediatamente)
- ❌ Apenas uma avaliação por produto/produtor por utilizador

**Ver Minhas Avaliações:**
1. Menu → "Minhas Avaliações"
2. Ver todas as suas avaliações
3. Opção para editar ou deletar (futuro)

**Ver Avaliações Públicas:**
- Cada produto mostra:
  - ⭐ Classificação média
  - 📊 Contagem total de avaliações
  - 💬 Últimas avaliações (truncadas)
- Cada produtor mostra:
  - ⭐ Classificação média
  - 📊 Histórico de avaliações
  - 👤 Rating público

**Escala de Classificação:**
- ⭐ 1 - Muito Mau
- ⭐⭐ 2 - Mau
- ⭐⭐⭐ 3 - Aceitável
- ⭐⭐⭐⭐ 4 - Bom
- ⭐⭐⭐⭐⭐ 5 - Excelente

---

## 📝 Resumo de Funcionalidades

| Funcionalidade | Status | Notas |
|---|---|---|
| Criar Conta | ✅ | Consumidor ou Produtor |
| Confirmar Email | ✅ | Token válido 7 dias |
| Ver Produtos | ✅ | Todos activos |
| Filtrar por Categoria | ✅ | 6+ categorias |
| Adicionar ao Carrinho | ✅ | Validação de stock |
| Fazer Encomendas | ✅ | Carrinho → Checkout |
| Escolher Endereço | ✅ | Morada + Contacto |
| Pagamento em Teste | ✅ | Senha 1234 ou COVERDE-TEST |
| Acompanhar Encomenda | ✅ | 7 estados |
| Avaliar Produtos | ✅ | 1-5 estrelas + comentário |
| Avaliar Produtores | ✅ | 1-5 estrelas + comentário |

---

## 🚀 Próximos Passos (Futuro)

- 🔐 Login com redes sociais (Google, Facebook)
- 📱 App mobile
- 💳 Integração com Stripe / MBway
- 📊 Wishlists / Favoritos
- 🔄 Devolução de produtos
- 📧 Notificações por email
- 🛍️ Compras recorrentes
- 👤 Perfil de cliente aprimorado

---

## ❓ FAQ

**P: Quanto tempo leva a confirmar o email?**
A: Instantaneamente após clicar no link. O link está válido por 7 dias.

**P: Qual é a taxa de IVA?**
A: 23% por padrão. Varia se existem certificações especiais.

**P: Como funciona o pagamento de teste?**
A: Use senha "1234" ou assinatura "COVERDE-TEST" para simular aprovação.

**P: Posso editar minha avaliação?**
A: Futuro - por agora, contacte suporte para editar/deletar.

**P: Quanto tempo leva a entrega?**
A: Depende do produtor. Ver prazo estimado na página do produtor (futuro).

---

**Versão:** 1.0
**Data:** 25/06/2026
**Sistema:** Coverde Ecommerce
