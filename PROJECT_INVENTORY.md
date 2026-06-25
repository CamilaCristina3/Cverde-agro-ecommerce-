# CVerde Agro-Ecommerce - Complete Project Inventory

**Generated:** 2026-06-25  
**Project:** Coverde (Agro-Ecommerce Platform)  
**Framework:** Django + Channels + MySQL

---

## 📋 TABLE OF CONTENTS

1. [MODELS](#models)
2. [VIEWS](#views)
3. [FORMS](#forms)
4. [ADMIN CLASSES](#admin-classes)
5. [URL PATTERNS](#url-patterns)
6. [INSTALLED_APPS](#installed_apps)

---

## MODELS

### 1. **apps/users/models.py** - All models centralized

#### User (AbstractUser) ⭐ CUSTOM AUTH USER
- **Fields:**
  - `user_type` (CharField: consumer|producer|admin, default: consumer)
  - `phone` (CharField, regex validated)
  - `district`, `county`, `parish` (CharField - location in Portugal)
  - `is_verified` (BooleanField, default: False)
  - `email_verified_at` (DateTimeField, nullable)
  - `profile_image` (ImageField, upload to 'profiles/')
  - **RGPD Consent Fields:**
    - `accepted_terms_at` (DateTimeField)
    - `accepted_privacy_policy_at` (DateTimeField)
    - `marketing_opt_in` (BooleanField, default: False)
    - `marketing_opt_in_at` (DateTimeField)
    - `producer_public_profile_consent_at` (DateTimeField)
  - **Right to Erasure:**
    - `data_exported_at` (DateTimeField)
    - `data_deleted_at` (DateTimeField)
    - `deletion_requested_at` (DateTimeField)
  - **Security:**
    - `login_attempts` (IntegerField, default: 0)
    - `locked_until` (DateTimeField, nullable)
    - `last_login_ip` (GenericIPAddressField)
    - `two_factor_enabled` (BooleanField, default: False)
- **Methods:**
  - `is_producer()` - Returns True if user_type == 'producer'
  - `is_consumer()` - Returns True if user_type == 'consumer'
  - `is_admin_user()` - Returns True if user_type == 'admin' or is_superuser
  - `delete_account()` - RGPD right to erasure (anonymizes data)
  - `export_personal_data()` - RGPD data portability (returns JSON)
- **Related Models:**
  - `email_verification_tokens` (ForeignKey: EmailVerificationToken)
  - `two_factor_codes` (ForeignKey: TwoFactorCode)
  - `orders` (ForeignKey: Order)
  - `consents` (ForeignKey: ConsentLog)
  - `producer` (OneToOneField: Producer)
  - `reviews` (ForeignKey: Review)
  - `chat_messages` (ForeignKey: ChatMessage)
  - `verified_producers` (ForeignKey: Producer - verified_by)
  - `product_reviews` (ForeignKey: ProductApproval - reviewed_by)

#### EmailVerificationToken
- **Fields:**
  - `user` (ForeignKey: User, CASCADE, related_name: email_verification_tokens)
  - `token` (UUIDField, unique, indexed)
  - `created_at` (DateTimeField, auto_now_add)
  - `used_at` (DateTimeField, nullable)
- **Methods:**
  - `__str__()` - Returns email, date, and status

#### TwoFactorCode
- **Fields:**
  - `user` (ForeignKey: User, CASCADE, related_name: two_factor_codes)
  - `code_hash` (CharField, max 128 - hashed)
  - `created_at` (DateTimeField, auto_now_add)
  - `expires_at` (DateTimeField)
  - `used_at` (DateTimeField, nullable)
- **Methods:**
  - `issue(user, code, ttl_seconds=600)` - Class method to issue and hash new codes
  - `verify(code)` - Verify code against hash

#### Cart
- **Fields:**
  - `session_key` (CharField, unique, max 40)
  - `items` (JSONField - list of {product_id, quantity})
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Methods:**
  - `add_item(product_id, quantity=1)` - Add or increment item
  - `remove_item(product_id)` - Remove item
  - `clear()` - Clear all items

#### ConsentLog - RGPD Auditing
- **Fields:**
  - `user` (ForeignKey: User, SET_NULL, nullable, related_name: consents)
  - `consent_type` (CharField: cookies|terms|privacy|marketing|profile_public)
  - `status` (CharField: accepted|rejected|withdrawn, default: accepted)
  - `ip_address` (GenericIPAddressField)
  - `user_agent` (TextField)
  - `document_version` (CharField, blank)
  - `created_at` (DateTimeField, auto_now_add)

#### Producer - Agricultural Producer Profile
- **Fields:**
  - `user` (OneToOneField: User, CASCADE, related_name: producer)
  - `name` (CharField, max 200 - farm/company name)
  - `description` (TextField)
  - `location` (CharField, max 200)
  - `nif` (CharField, max 20 - tax ID)
  - `verification_document` (FileField, upload to 'producers/verification/')
  - `status` (CharField: pending|approved|rejected|suspended, default: pending)
  - `is_verified` (BooleanField, default: False)
  - `verified_at` (DateTimeField, nullable)
  - `verified_by` (ForeignKey: User, SET_NULL, nullable, related_name: verified_producers)
  - `rejection_reason` (TextField)
  - `rating` (DecimalField, max_digits: 3, decimal_places: 2, default: 0)
  - `total_ratings` (IntegerField, default: 0)
  - `is_active` (BooleanField, default: True)
  - `created_at` (DateTimeField, auto_now_add)
- **Related Models:**
  - `products` (ForeignKey: Product)
  - `reviews` (ForeignKey: Review)
- **DB Table:** users_producer

#### Category - Product Categories
- **Fields:**
  - `name` (CharField, max 100)
  - `slug` (SlugField, unique)
  - `parent` (ForeignKey: self, SET_NULL, nullable, related_name: subcategories)
  - `icon` (CharField, max 50)
  - `image` (ImageField, upload to 'categories/', nullable)
  - `is_active` (BooleanField, default: True)
  - `order` (IntegerField, default: 0)
- **Related Models:**
  - `subcategories` (ForeignKey: self)
  - `products` (ForeignKey: Product)
  - `commission` (OneToOneField: PlatformCommission)
- **DB Table:** users_category

#### Product - Agricultural Products
- **Fields:**
  - `producer` (ForeignKey: Producer, CASCADE, related_name: products)
  - `category` (ForeignKey: Category, SET_NULL, nullable, related_name: products)
  - `name` (CharField, max 200)
  - `slug` (SlugField, unique)
  - `description` (TextField)
  - `price` (DecimalField, max_digits: 10, decimal_places: 2)
  - `stock` (PositiveIntegerField, default: 0)
  - `unit` (CharField: kg|un|l|pct|maco|caixa|dúzia, default: kg)
  - `certification` (CharField: biologico|dop|igp|integrada|tradicional, blank)
  - `main_image` (ImageField, upload to 'products/')
  - `is_active` (BooleanField, default: True)
  - `is_featured` (BooleanField, default: False)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Related Models:**
  - `reviews` (ForeignKey: Review)
  - `order_items` (ForeignKey: OrderItem)
  - `approval` (OneToOneField: ProductApproval)
- **Methods:**
  - Auto-generates slug from name
- **DB Table:** users_product

#### Order - Customer Orders
- **Fields:**
  - `user` (ForeignKey: User, CASCADE, related_name: orders)
  - `subtotal` (DecimalField, max_digits: 10, decimal_places: 2)
  - `shipping_cost` (DecimalField, max_digits: 10, decimal_places: 2)
  - `vat` (DecimalField, max_digits: 10, decimal_places: 2)
  - `total` (DecimalField, max_digits: 10, decimal_places: 2)
  - `status` (CharField: pending|confirmed|paid|preparing|shipped|delivered|cancelled)
  - `shipping_address` (TextField)
  - `shipping_contact` (CharField, max 15)
  - `tracking_code` (CharField, max 100)
  - `invoice_number` (CharField, max 50)
  - `invoice_pdf` (FileField, upload to 'invoices/', nullable)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
  - `paid_at` (DateTimeField, nullable)
  - `delivered_at` (DateTimeField, nullable)
- **Related Models:**
  - `items` (ForeignKey: OrderItem)
  - `payments` (ForeignKey: Payment)
  - `delivery` (OneToOneField: Delivery)
- **Methods:**
  - `generate_invoice_number()` - Generates COV-YYYY-NNNNNN format
- **DB Table:** users_order

#### OrderItem - Order Line Items
- **Fields:**
  - `order` (ForeignKey: Order, CASCADE, related_name: items)
  - `product` (ForeignKey: Product, SET_NULL, nullable, related_name: order_items)
  - `quantity` (PositiveIntegerField, default: 1)
  - `price` (DecimalField, max_digits: 10, decimal_places: 2 - unit price)
  - `product_name` (CharField, max 200 - snapshot)
  - `producer_name` (CharField, max 200 - snapshot)
- **Properties:**
  - `total` - quantity × price
- **DB Table:** users_orderitem

#### PlatformCommission - Platform Fees Configuration
- **Fields:**
  - `category` (OneToOneField: Category, CASCADE, nullable, related_name: commission)
  - `commission_percentage` (DecimalField, max_digits: 5, decimal_places: 2)
  - `is_active` (BooleanField, default: True)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
  - `notes` (TextField)
- **Logic:** If category is null, it's the global commission

#### Delivery - Delivery Tracking
- **Fields:**
  - `order` (OneToOneField: Order, CASCADE, related_name: delivery)
  - `tracking_number` (CharField, unique, max 100)
  - `carrier` (CharField, max 100 - CTT, DHL, Fedex, etc.)
  - `status` (CharField: pending|in_transit|delivered|failed|returned)
  - `scheduled_date` (DateTimeField, nullable)
  - `delivered_date` (DateTimeField, nullable)
  - `delivery_address` (TextField)
  - `delivery_notes` (TextField)
  - `signature_required` (BooleanField, default: False)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)

#### ProductApproval - Product Moderation
- **Fields:**
  - `product` (OneToOneField: Product, CASCADE, related_name: approval)
  - `status` (CharField: pending|approved|rejected, default: pending)
  - `reviewed_by` (ForeignKey: User, SET_NULL, nullable, related_name: product_reviews)
  - `rejection_reason` (TextField)
  - `reviewed_at` (DateTimeField, nullable)
  - `created_at` (DateTimeField, auto_now_add)

#### Review - Product & Producer Reviews
- **Fields:**
  - `product` (ForeignKey: Product, CASCADE, nullable, related_name: reviews)
  - `producer` (ForeignKey: Producer, CASCADE, nullable, related_name: reviews)
  - `user` (ForeignKey: User, CASCADE, related_name: reviews)
  - `rating` (IntegerField: 1-5, choices with stars emoji)
  - `title` (CharField, max 200)
  - `comment` (TextField, max 1000)
  - `verified_purchase` (BooleanField, default: False)
  - `is_approved` (BooleanField, default: True - moderation)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Constraints:**
  - unique_together: (user, product), (user, producer)
  - Either product OR producer must be filled, not both
- **Methods:**
  - `clean()` - Validates only one of product/producer

---

### 2. **apps/orders/models.py**

#### Order (DUPLICATE - see users/models.py)
#### OrderItem (DUPLICATE - see users/models.py)

---

### 3. **apps/payments/models.py**

#### Payment - Payment Processing with Test Mode
- **Fields:**
  - `order` (ForeignKey: Order, CASCADE, related_name: payments)
  - `provider` (CharField, max 100, blank)
  - `amount` (DecimalField, max_digits: 10, decimal_places: 2)
  - `currency` (CharField, max 3, default: EUR)
  - `status` (CharField: pending|processing|paid|failed|cancelled|refunded|test_approved)
  - `payment_method` (CharField: card_test|bank_transfer_test|cash_on_delivery|mbay_test|stripe|paypal|other)
  - **Test Mode:**
    - `is_test_payment` (BooleanField, default: False)
    - `test_signature` (CharField, max 50)
    - `test_password_hash` (CharField, max 128)
  - **Tracking:**
    - `transaction_id` (CharField, max 100)
    - `reference` (CharField, max 100 - tracking reference)
  - **Security:**
    - `retry_count` (IntegerField, default: 0)
    - `error_message` (TextField)
  - **Timestamps:**
    - `created_at` (DateTimeField, auto_now_add)
    - `paid_at` (DateTimeField, nullable)
    - `updated_at` (DateTimeField, auto_now)
- **Methods:**
  - `set_test_password(password)` - Hash test password
  - `verify_test_password(password)` - Verify against hash
  - `approve_test_payment()` - Mark as test_approved
  - `mark_as_failed(error_msg)` - Mark failed & increment retry

---

### 4. **apps/notifications/models.py**

#### Notification
- **Fields:**
  - `user` (ForeignKey: User, CASCADE)
  - `message` (TextField)
  - `created_at` (DateTimeField, auto_now_add)
  - `read` (BooleanField, default: False)

---

### 5. **apps/chat/models.py**

#### ChatRoom
- **Fields:**
  - `name` (SlugField, unique, max 64)
  - `title` (CharField, max 120)
  - `created_at` (DateTimeField, auto_now_add)
- **Related Models:**
  - `messages` (ForeignKey: ChatMessage)

#### ChatMessage
- **Fields:**
  - `room` (ForeignKey: ChatRoom, CASCADE, related_name: messages)
  - `user` (ForeignKey: User, CASCADE, related_name: chat_messages)
  - `content` (TextField, max 2000)
  - `created_at` (DateTimeField, auto_now_add)

---

## VIEWS

### **apps/users/views.py** - Authentication & User Management

#### Class-Based Views (CBV)
- `CustomLoginView(LoginView)` - Custom login with email support & 2FA
- `CustomLogoutView(LogoutView)` - Logout redirects to home
- `CustomPasswordResetView(PasswordResetView)` - Password reset
- `CustomPasswordResetDoneView(PasswordResetDoneView)` - Reset sent confirmation
- `CustomPasswordResetConfirmView(PasswordResetConfirmView)` - Confirm reset link
- `CustomPasswordResetCompleteView(PasswordResetCompleteView)` - Reset success page

#### Function-Based Views (FBV)
- **`dashboard(request)`** - Routes to appropriate dashboard (admin|producer|consumer)
- **`register(request)`** - Unified registration (consumer/producer selection)
- **`register_consumer(request)`** - Redirect to consumer registration
- **`register_producer(request)`** - Redirect to producer registration
- **`verify_email(request, token)`** - Email verification with 48h token expiry
- **`two_factor_verify(request)`** - 2FA code verification (session-based)
- **`profile(request)`** - Consumer profile view
- **`edit_profile(request)`** - Profile edit form
- **`delete_account(request)`** - Account deletion (RGPD anonymization)
- **`producer_panel(request)`** - Producer dashboard with sales analytics
  - Calculates: daily sales, daily sales change %, active orders, recent items
  - Shows: products, stock status, order analytics

---

### **apps/products/views.py** - Product Management

- **`product_list(request)`** - Product listing with filters
  - Filters: q (search), category, certification, producer, in_stock
  - Sorting: newest, price_asc, price_desc, rating_desc, name_asc
  - Pagination: 12 items per page
- **`product_detail(request, product_id)`** - Product detail with related products
- **`create_product(request)`** - Create product (producer only)
- **`edit_product(request, product_id)`** - Edit product (producer only, owner check)
- **`delete_product(request, product_id)`** - Delete product (producer only)
- **`producer_products(request)`** - List producer's own products

---

### **apps/orders/views.py** - Shopping Cart & Checkout

- **`cart(request)`** - View cart with calculated totals
  - Calculates: subtotal, shipping, VAT, total
- **`add_to_cart(request, product_id)`** - Add product to cart (POST)
  - Stock validation, quantity limits
- **`update_cart_item(request, product_id)`** - Update item quantity (POST)
- **`remove_from_cart(request, product_id)`** - Remove item (POST)
- **`clear_cart(request)`** - Clear entire cart (POST)
- **`checkout(request)`** - Checkout form & order creation
  - Stock locking with select_for_update()
  - Order & OrderItem creation
- **`order_detail(request, order_id)`** - View order details (owner only)

---

### **apps/payments/views.py** - Payment Processing

- **`payment_checkout(request, order_id)`** - Simulated payment form
  - Test mode: accepts password "1234" or signature "COVERDE-TEST"
  - Creates Payment record, updates order status to 'confirmed'
  - Sends confirmation emails
- **`payment_success(request, order_id)`** - Success page after payment
- **`payment_status(request)`** - Payment status placeholder

---

### **apps/reviews/views.py** - Reviews Management

- **`create_product_review(request, product_id)`** - Create product review
  - Validates verified purchase (from OrderItem)
  - Prevents duplicate reviews per user/product
- **`create_producer_review(request, producer_id)`** - Create producer review
  - Validates purchase from producer (from Order)
  - Prevents duplicate reviews per user/producer
- **`product_reviews(request, product_id)`** - List product reviews
- **`producer_reviews(request, producer_id)`** - List producer reviews
- **`my_reviews(request)`** - List user's own reviews (with edit/delete)
- **`_update_product_rating(product)`** - Helper to recalculate product rating

---

### **apps/notifications/views.py**

- **`inbox(request)`** - Notification inbox placeholder

---

## FORMS

### **forms.py** - All forms centralized

#### Authentication & Registration
- **`LoginForm`** - Custom login with email & remember-me checkbox
- **`TwoFactorVerifyForm`** - 6-digit code input
- **`ProfileUpdateForm`** - Update user profile fields
  - Fields: first_name, last_name, phone, district, county, parish, profile_image, 2FA, marketing_opt_in

#### Registration (Multi-type)
- **`BaseRegisterForm`** - Common registration fields
  - Includes password validation, RGPD checkboxes (privacy, terms, marketing)
  - Fields: username, first_name, last_name, email, phone, location (district/county/parish)

- **`ConsumerRegisterForm`** - Consumer registration (inherits BaseRegisterForm)
  - Sets user_type = "consumer", is_verified = False

- **`RegistrationForm`** - Unified registration with type selection
  - Account type: consumer|producer (RadioSelect)
  - Conditional producer fields: name, description, location, NIF, verification_document, public_profile_consent

- **`ProducerRegisterForm`** - Producer-specific registration
  - All producer fields required
  - Enforces public_profile_consent checkbox
  - Creates Producer object on save

#### Product Management
- **`ProducerVerificationRequestForm`** - Producer verification request
  - Fields: NIF, verification_document

- **`ProductForm`** - Product creation/editing
  - Fields: name, category, description, price, stock, unit, certification, main_image

#### Checkout
- **`CheckoutForm`** - Order checkout
  - Fields: shipping_address, shipping_contact

#### Reviews
- **`ReviewForm`** - Product/Producer review
  - Fields: rating (IntegerField 1-5), title, comment

---

## ADMIN CLASSES

### **apps/users/admin.py**

#### UserAdmin
- **List Display:** id, username, email, first_name, last_name, user_type, is_verified, is_active, is_staff, date_joined
- **List Filters:** user_type, is_verified, is_active, is_staff, is_superuser, two_factor_enabled, marketing_opt_in
- **Search:** username, email, first_name, last_name, phone
- **Editable:** user_type, is_verified, is_active
- **Actions:** mark_as_verified, mark_as_unverified, activate_users, deactivate_users
- **Fieldsets:** 
  - Access Info, Personal Info, Location, Permissions, Security, RGPD Consents, Right to Erasure

#### EmailVerificationTokenAdmin
- **List Display:** user, token, created_at, used_at, is_used_display
- **Readonly:** user, token, created_at, used_at
- **Searchable:** user__username, user__email, token
- **Filters:** used_at, created_at

#### TwoFactorCodeAdmin
- **List Display:** user, created_at, expires_at, used_at
- **Readonly:** user, code_hash, created_at, expires_at, used_at
- **Searchable:** user__username, user__email

#### ProducerAdmin
- **List Display:** id, name, status, user, is_verified, is_active, rating, total_ratings, created_at
- **List Filters:** status, is_verified, is_active, created_at
- **Editable:** status, is_active
- **Actions:** approve_producers, reject_producers, suspend_producers, activate_producers, deactivate_producers
- **Fieldsets:** Basic Info, Verification, Rating, Status

#### ConsentLogAdmin
- **List Display:** user, consent_type, status, ip_address, created_at
- **Filters:** consent_type, status, created_at
- **Searchable:** user__username, user__email, ip_address

#### CartAdmin
- **List Display:** session_key, created_at, updated_at
- **Readonly:** session_key, created_at, updated_at, items

#### CategoryAdmin
- **List Display:** name, slug, parent, is_active, order, product_count
- **List Filters:** is_active
- **Editable:** is_active, order
- **Prepopulated Fields:** slug ← name
- **Fieldsets:** Basic Info, Configuration

#### ProductAdmin
- **List Display:** name, producer, category, price, stock, status_badge, is_featured, is_active, created_at
- **List Filters:** is_active, is_featured, category, certification, created_at, producer
- **Editable:** is_active, is_featured, price, stock
- **Readonly:** slug, created_at, updated_at
- **Actions:** activate_products, deactivate_products, mark_as_featured, remove_from_featured, suspend_products
- **Fieldsets:** Basic Info, Price & Stock, Image & Visibility, Timestamps

#### ProductApprovalAdmin
- **List Display:** product, status_badge, product_producer, reviewed_by, created_at
- **List Filters:** status, created_at
- **Readonly:** product, created_at, reviewed_at, reviewed_by
- **Actions:** approve_products, reject_products
- **Fieldsets:** Product, Approval, Review

#### PlatformCommissionAdmin
- **List Display:** category_or_global, commission_percentage, is_active, updated_at
- **List Filters:** is_active, updated_at
- **Editable:** commission_percentage, is_active
- **Readonly:** created_at, updated_at

#### DeliveryAdmin
- **List Display:** tracking_number, order, status_badge, carrier, scheduled_date, delivered_date
- **List Filters:** status, carrier, signature_required, delivered_date, created_at
- **Readonly:** order, created_at, updated_at
- **Actions:** mark_as_pending, mark_as_in_transit, mark_as_delivered, mark_as_failed
- **Fieldsets:** Encomenda & Rastreio, Delivery Address, Scheduling & Delivery, Notes, Timestamps

#### ReviewAdmin
- **List Display:** target, rating_stars, user, verified_purchase, is_approved, created_at
- **List Filters:** rating, is_approved, verified_purchase, created_at
- **Editable:** is_approved
- **Readonly:** user, created_at, updated_at
- **Actions:** approve_reviews, reject_reviews
- **Fieldsets:** Review, Content, Moderation, Timestamps

---

### **apps/orders/admin.py**

#### OrderAdmin
- **List Display:** id, user, created_at, items_count
- **List Filters:** created_at
- **Searchable:** id, user__email, user__username
- **Readonly:** created_at
- **Inlines:** OrderItemInline (readonly)
- **Fieldsets:** Order Info
- **Date Hierarchy:** created_at

---

### **apps/payments/admin.py**

#### PaymentAdmin
- **List Display:** id, order, amount, status, payment_method, is_test_badge, reference, created_at
- **List Filters:** status, payment_method, is_test_payment, created_at
- **Editable:** (none)
- **Readonly:** order, created_at, paid_at, reference, transaction_id
- **Searchable:** order__id, order__user__email, reference, transaction_id
- **Actions:** mark_as_paid, mark_as_failed
- **Fieldsets:** Encomenda, Payment, Test Mode, Security & Audit

---

### **apps/notifications/admin.py**

#### Simple Registration
- **Model:** Notification
- **Default Admin Display**

---

## URL PATTERNS

### **cverde/urls.py** - Main URL Configuration

```
/                                      → HomeView
/admin/                                → Django Admin
/users/                                → Include apps.users.urls
/products/                             → Include apps.products.urls
/orders/                               → Include apps.orders.urls
/payments/                             → Include apps.payments.urls
/reviews/                              → Include apps.reviews.urls
/notifications/                        → Include apps.notifications.urls
/chat/                                 → Include apps.chat.urls
/                                      → Include apps.pages.urls (static pages)
```

---

### **apps/users/urls.py** - Authentication & User Management

```
login/                                 → CustomLoginView
logout/                                → CustomLogoutView
register/                              → register view
register/consumer/                     → register_consumer (redirect)
register/producer/                     → register_producer (redirect)
dashboard/                             → dashboard (route to user type)
verify-email/<uuid:token>/             → verify_email
two-factor/                            → two_factor_verify
profile/                               → profile
profile/edit/                          → edit_profile
delete-account/                        → delete_account
producer/                              → producer_panel
producer/verification/                 → producer_verification_request

password-reset/                        → CustomPasswordResetView
password-reset/done/                   → CustomPasswordResetDoneView
password-reset/<uidb64>/<token>/       → CustomPasswordResetConfirmView
password-reset/complete/               → CustomPasswordResetCompleteView

PRODUCT ROUTES (lazy-loaded from products app):
products/                              → product_list
products/create/                       → create_product
products/my-products/                  → producer_products
products/<int:product_id>/             → product_detail
products/<int:product_id>/edit/        → edit_product
products/<int:product_id>/delete/      → delete_product
```

---

### **apps/products/urls.py** - Product Catalog

```
products/                              → product_list
products/create/                       → create_product
products/my-products/                  → producer_products
products/<int:product_id>/             → product_detail
products/<int:product_id>/edit/        → edit_product
products/<int:product_id>/delete/      → delete_product
```

---

### **apps/orders/urls.py** - Shopping & Checkout

```
orders/cart/                           → cart
orders/cart/add/<int:product_id>/      → add_to_cart (POST)
orders/cart/update/<int:product_id>/   → update_cart_item (POST)
orders/cart/remove/<int:product_id>/   → remove_from_cart (POST)
orders/cart/clear/                     → clear_cart (POST)
orders/checkout/                       → checkout
orders/orders/<int:order_id>/          → order_detail
```

---

### **apps/payments/urls.py** - Payment Processing

```
payments/checkout/<int:order_id>/      → payment_checkout
payments/success/<int:order_id>/       → payment_success
payments/status/                       → payment_status
```

---

### **apps/reviews/urls.py** - Reviews Management

```
reviews/product/<int:product_id>/create/       → create_product_review
reviews/producer/<int:producer_id>/create/     → create_producer_review
reviews/product/<int:product_id>/              → product_reviews
reviews/producer/<int:producer_id>/            → producer_reviews
reviews/my-reviews/                            → my_reviews
```

---

### **apps/notifications/urls.py**

```
notifications/inbox/                   → inbox
```

---

### **apps/chat/urls.py**

(Not fully detailed in available code)

---

### **apps/pages/urls.py**

(Not detailed - static pages like terms, privacy, cookies)

---

## INSTALLED_APPS

Located in [cverde/settings.py](cverde/settings.py#L40-L56)

```python
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party
    'channels',                    # WebSockets for chat
    
    # Local apps (Coverde)
    'apps.users',                  # User auth, profiles, products, orders (main app)
    'apps.orders',                 # Orders & checkout
    'apps.payments',               # Payment processing
    'apps.notifications',          # Notifications
    'apps.pages',                  # Static pages
    'apps.chat',                   # Chat functionality
    'apps.reviews',                # Product/Producer reviews
    'apps.logistics',              # Logistics (minimal)
]
```

---

## KEY CONFIGURATION SETTINGS

### Authentication
- **Custom User Model:** `AUTH_USER_MODEL = 'users.User'`
- **Authentication Backends:**
  - `apps.users.backends.EmailAuthBackend` (custom - email login)
  - `django.contrib.auth.backends.ModelBackend` (standard)
- **Login URL:** `users:login`
- **Login Redirect:** `users:dashboard`
- **Logout Redirect:** `home`

### Email & Verification
- **Email Backend:** Console (configurable via .env)
- **Require Email Verification:** True (configurable)
- **Require Producer Verification:** False (configurable)

### Security
- **Max Login Attempts:** 5
- **Account Lock Duration:** 15 minutes
- **Session Cookie Age:** 2 weeks (1209600 seconds)
- **CSRF Protection:** Enabled (can be disabled for testing)

### Shipping & Pricing
- **Free Shipping Threshold:** €50
- **Default Shipping Cost:** €5
- **VAT Rate:** 6%

### Database
- **Engine:** MySQL (forced in settings)
- **Database:** coverde_db
- **Charset:** utf8mb4
- **Strict Mode:** STRICT_TRANS_TABLES

### Internationalization
- **Language:** pt-pt (Portuguese)
- **Timezone:** Europe/Lisbon
- **Use I18N:** True
- **Use TZ:** True

### File Storage
- **Media Root:** `BASE_DIR / 'media'`
- **Media URL:** `/media/`
- **Static Root:** `BASE_DIR / 'staticfiles'`
- **Static URL:** `/static/`

### Message Tags (for Bulma CSS)
```python
ERROR → 'danger'
WARNING → 'warning'
SUCCESS → 'success'
INFO → 'info'
```

---

## SUMMARY STATISTICS

| Category | Count |
|----------|-------|
| **Models** | 17 total |
| - User Models | 6 (User, EmailVerificationToken, TwoFactorCode, Cart, ConsentLog, Producer) |
| - Product Models | 4 (Category, Product, ProductApproval, Review) |
| - Order Models | 2 (Order, OrderItem) |
| - Payment Models | 1 (Payment) |
| - Delivery Models | 1 (Delivery) |
| - Commission Models | 1 (PlatformCommission) |
| - Notification Models | 1 (Notification) |
| - Chat Models | 2 (ChatRoom, ChatMessage) |
| **Views** | ~30+ functions across apps |
| **Forms** | 10+ classes |
| **Admin Classes** | 16 registered classes |
| **URL Patterns** | 40+ unique routes |
| **Installed Apps** | 13 apps |

---

## RELATIONSHIPS DIAGRAM (Text)

```
User (AbstractUser)
├── 1:1 ← Producer
│   ├── 1:M → Product
│   └── 1:M → Review
├── 1:M → Order
│   ├── 1:M → OrderItem
│   │   └── M:1 ← Product
│   ├── 1:M → Payment
│   └── 1:1 → Delivery
├── 1:M → EmailVerificationToken
├── 1:M → TwoFactorCode
├── 1:M → ConsentLog
├── 1:M → Review
├── 1:M → ChatMessage
│   └── M:1 ← ChatRoom
└── M:1 ← User (verified_producers via Producer.verified_by)

Category
├── M:1 → Category (parent)
└── 1:M → Product
    └── 1:1 → ProductApproval

Product
├── 1:M → Review
├── 1:M → OrderItem
└── 1:1 → ProductApproval

PlatformCommission
└── 1:1 → Category (optional - null for global)
```

---

**End of Inventory Report**
