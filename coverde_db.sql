-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.40 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping data for table coverde_db.auth_group: ~0 rows (approximately)
DELETE FROM `auth_group`;

-- Dumping data for table coverde_db.auth_group_permissions: ~0 rows (approximately)
DELETE FROM `auth_group_permissions`;

-- Dumping data for table coverde_db.auth_permission: ~92 rows (approximately)
DELETE FROM `auth_permission`;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add content type', 4, 'add_contenttype'),
	(14, 'Can change content type', 4, 'change_contenttype'),
	(15, 'Can delete content type', 4, 'delete_contenttype'),
	(16, 'Can view content type', 4, 'view_contenttype'),
	(17, 'Can add session', 5, 'add_session'),
	(18, 'Can change session', 5, 'change_session'),
	(19, 'Can delete session', 5, 'delete_session'),
	(20, 'Can view session', 5, 'view_session'),
	(21, 'Can add user', 6, 'add_user'),
	(22, 'Can change user', 6, 'change_user'),
	(23, 'Can delete user', 6, 'delete_user'),
	(24, 'Can view user', 6, 'view_user'),
	(25, 'Can add producer', 7, 'add_producer'),
	(26, 'Can change producer', 7, 'change_producer'),
	(27, 'Can delete producer', 7, 'delete_producer'),
	(28, 'Can view producer', 7, 'view_producer'),
	(29, 'Can add product', 8, 'add_product'),
	(30, 'Can change product', 8, 'change_product'),
	(31, 'Can delete product', 8, 'delete_product'),
	(32, 'Can view product', 8, 'view_product'),
	(33, 'Can add order', 9, 'add_order'),
	(34, 'Can change order', 9, 'change_order'),
	(35, 'Can delete order', 9, 'delete_order'),
	(36, 'Can view order', 9, 'view_order'),
	(37, 'Can add order item', 10, 'add_orderitem'),
	(38, 'Can change order item', 10, 'change_orderitem'),
	(39, 'Can delete order item', 10, 'delete_orderitem'),
	(40, 'Can view order item', 10, 'view_orderitem'),
	(41, 'Can add payment', 11, 'add_payment'),
	(42, 'Can change payment', 11, 'change_payment'),
	(43, 'Can delete payment', 11, 'delete_payment'),
	(44, 'Can view payment', 11, 'view_payment'),
	(45, 'Can add notification', 12, 'add_notification'),
	(46, 'Can change notification', 12, 'change_notification'),
	(47, 'Can delete notification', 12, 'delete_notification'),
	(48, 'Can view notification', 12, 'view_notification'),
	(49, 'Can add Carrinho', 13, 'add_cart'),
	(50, 'Can change Carrinho', 13, 'change_cart'),
	(51, 'Can delete Carrinho', 13, 'delete_cart'),
	(52, 'Can view Carrinho', 13, 'view_cart'),
	(53, 'Can add Categoria', 14, 'add_category'),
	(54, 'Can change Categoria', 14, 'change_category'),
	(55, 'Can delete Categoria', 14, 'delete_category'),
	(56, 'Can view Categoria', 14, 'view_category'),
	(57, 'Can add Encomenda', 15, 'add_order'),
	(58, 'Can change Encomenda', 15, 'change_order'),
	(59, 'Can delete Encomenda', 15, 'delete_order'),
	(60, 'Can view Encomenda', 15, 'view_order'),
	(61, 'Can add Produtor', 16, 'add_producer'),
	(62, 'Can change Produtor', 16, 'change_producer'),
	(63, 'Can delete Produtor', 16, 'delete_producer'),
	(64, 'Can view Produtor', 16, 'view_producer'),
	(65, 'Can add Produto', 17, 'add_product'),
	(66, 'Can change Produto', 17, 'change_product'),
	(67, 'Can delete Produto', 17, 'delete_product'),
	(68, 'Can view Produto', 17, 'view_product'),
	(69, 'Can add Pagamento', 18, 'add_payment'),
	(70, 'Can change Pagamento', 18, 'change_payment'),
	(71, 'Can delete Pagamento', 18, 'delete_payment'),
	(72, 'Can view Pagamento', 18, 'view_payment'),
	(73, 'Can add Item da encomenda', 19, 'add_orderitem'),
	(74, 'Can change Item da encomenda', 19, 'change_orderitem'),
	(75, 'Can delete Item da encomenda', 19, 'delete_orderitem'),
	(76, 'Can view Item da encomenda', 19, 'view_orderitem'),
	(77, 'Can add Preferência de notificação', 20, 'add_notificationpreference'),
	(78, 'Can change Preferência de notificação', 20, 'change_notificationpreference'),
	(79, 'Can delete Preferência de notificação', 20, 'delete_notificationpreference'),
	(80, 'Can view Preferência de notificação', 20, 'view_notificationpreference'),
	(81, 'Can add Notificação', 21, 'add_notification'),
	(82, 'Can change Notificação', 21, 'change_notification'),
	(83, 'Can delete Notificação', 21, 'delete_notification'),
	(84, 'Can view Notificação', 21, 'view_notification'),
	(85, 'Can add Registo de consentimento', 22, 'add_consentlog'),
	(86, 'Can change Registo de consentimento', 22, 'change_consentlog'),
	(87, 'Can delete Registo de consentimento', 22, 'delete_consentlog'),
	(88, 'Can view Registo de consentimento', 22, 'view_consentlog'),
	(89, 'Can add Avaliação', 23, 'add_review'),
	(90, 'Can change Avaliação', 23, 'change_review'),
	(91, 'Can delete Avaliação', 23, 'delete_review'),
	(92, 'Can view Avaliação', 23, 'view_review');

-- Dumping data for table coverde_db.django_admin_log: ~1 rows (approximately)
DELETE FROM `django_admin_log`;
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2026-04-11 19:26:23.600851', '1', 'Quinta do Sol', 1, '[{"added": {}}]', 7, 2);

-- Dumping data for table coverde_db.django_content_type: ~23 rows (approximately)
DELETE FROM `django_content_type`;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'contenttypes', 'contenttype'),
	(12, 'notifications', 'notification'),
	(9, 'orders', 'order'),
	(10, 'orders', 'orderitem'),
	(11, 'payments', 'payment'),
	(7, 'producers', 'producer'),
	(8, 'products', 'product'),
	(5, 'sessions', 'session'),
	(13, 'users', 'cart'),
	(14, 'users', 'category'),
	(22, 'users', 'consentlog'),
	(21, 'users', 'notification'),
	(20, 'users', 'notificationpreference'),
	(15, 'users', 'order'),
	(19, 'users', 'orderitem'),
	(18, 'users', 'payment'),
	(16, 'users', 'producer'),
	(17, 'users', 'product'),
	(23, 'users', 'review'),
	(6, 'users', 'user');

-- Dumping data for table coverde_db.django_migrations: ~29 rows (approximately)
DELETE FROM `django_migrations`;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-04-11 05:43:44.792622'),
	(2, 'contenttypes', '0002_remove_content_type_name', '2026-04-11 05:43:44.885692'),
	(3, 'auth', '0001_initial', '2026-04-11 05:43:45.549006'),
	(4, 'auth', '0002_alter_permission_name_max_length', '2026-04-11 05:43:45.660562'),
	(5, 'auth', '0003_alter_user_email_max_length', '2026-04-11 05:43:45.669411'),
	(6, 'auth', '0004_alter_user_username_opts', '2026-04-11 05:43:45.678510'),
	(7, 'auth', '0005_alter_user_last_login_null', '2026-04-11 05:43:45.686096'),
	(8, 'auth', '0006_require_contenttypes_0002', '2026-04-11 05:43:45.691095'),
	(9, 'auth', '0007_alter_validators_add_error_messages', '2026-04-11 05:43:45.699904'),
	(10, 'auth', '0008_alter_user_username_max_length', '2026-04-11 05:43:45.707144'),
	(11, 'auth', '0009_alter_user_last_name_max_length', '2026-04-11 05:43:45.713832'),
	(12, 'auth', '0010_alter_group_name_max_length', '2026-04-11 05:43:45.732262'),
	(13, 'auth', '0011_update_proxy_permissions', '2026-04-11 05:43:45.737064'),
	(14, 'auth', '0012_alter_user_first_name_max_length', '2026-04-11 05:43:45.747580'),
	(15, 'users', '0001_initial', '2026-04-11 05:43:46.234641'),
	(16, 'admin', '0001_initial', '2026-04-11 05:43:46.397442'),
	(17, 'admin', '0002_logentry_remove_auto_add', '2026-04-11 05:43:46.413592'),
	(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-04-11 05:43:46.437022'),
	(19, 'notifications', '0001_initial', '2026-04-11 05:43:46.459100'),
	(20, 'notifications', '0002_initial', '2026-04-11 05:43:46.536085'),
	(21, 'products', '0001_initial', '2026-04-11 05:43:46.575849'),
	(22, 'orders', '0001_initial', '2026-04-11 05:43:46.792361'),
	(23, 'orders', '0002_initial', '2026-04-11 05:43:46.885266'),
	(24, 'payments', '0001_initial', '2026-04-11 05:43:47.014090'),
	(25, 'producers', '0001_initial', '2026-04-11 05:43:47.135538'),
	(26, 'products', '0002_alter_product_options_product_available_and_more', '2026-04-11 05:43:47.472183'),
	(27, 'sessions', '0001_initial', '2026-04-11 05:43:47.529427'),
	(28, 'users', '0002_user_consents', '2026-04-11 19:20:37.679333'),
	(29, 'users', '0003_cart_category_order_producer_product_and_more', '2026-04-11 19:40:56.706809');

-- Dumping data for table coverde_db.django_session: ~0 rows (approximately)
DELETE FROM `django_session`;

-- Dumping data for table coverde_db.notifications_notification: ~0 rows (approximately)
DELETE FROM `notifications_notification`;

-- Dumping data for table coverde_db.orders_order: ~0 rows (approximately)
DELETE FROM `orders_order`;

-- Dumping data for table coverde_db.orders_orderitem: ~0 rows (approximately)
DELETE FROM `orders_orderitem`;

-- Dumping data for table coverde_db.payments_payment: ~0 rows (approximately)
DELETE FROM `payments_payment`;

-- Dumping data for table coverde_db.producers_producer: ~7 rows (approximately)
DELETE FROM `producers_producer`;
INSERT INTO `producers_producer` (`id`, `name`, `description`, `location`, `rating`, `active`, `created_at`, `user_id`) VALUES
	(1, 'Quinta do Sol', 'Agricultura familiar sustentável há 30 anos.', 'Sintra', 0.08, 1, '2026-04-11 19:26:23.597335', 2),
	(2, 'Quinta do Sol', 'Agricultura familiar sustentável há mais de 30 anos. Produzimos frutas e legumes frescos com métodos tradicionais.', 'Sintra, Portugal', 4.80, 1, '2026-04-11 19:42:59.909230', 3),
	(3, 'Horta da Vila', 'Produtos frescos colhidos diariamente. Compromisso com a qualidade e o sabor autêntico.', 'Cascais, Portugal', 4.60, 1, '2026-04-11 19:43:00.158907', 4),
	(4, 'Fazenda Verde', 'Certificação biológica desde 2010. Produtos 100% orgânicos e sustentáveis.', 'Óbidos, Portugal', 4.90, 1, '2026-04-11 19:43:00.448460', 5),
	(5, 'Pomar do Oeste', 'Especialistas em frutas de qualidade. Maçãs, peras e morangos cultivados com paixão.', 'Alcobaça, Portugal', 5.00, 1, '2026-04-11 19:43:00.747344', 6),
	(6, 'Quinta Bio Coimbra', 'Produtos biológicos certificados. Agricultura regenerativa e respeito pelo meio ambiente.', 'Coimbra, Portugal', 4.70, 1, '2026-04-11 19:43:01.047285', 7),
	(7, 'Hortas do Ave', 'Legumes e verduras frescas. Tradição familiar e qualidade garantida.', 'Vila Nova de Famalicão, Portugal', 4.50, 1, '2026-04-11 19:43:01.322273', 8);

-- Dumping data for table coverde_db.products_product: ~0 rows (approximately)
DELETE FROM `products_product`;

-- Dumping data for table coverde_db.users_cart: ~0 rows (approximately)
DELETE FROM `users_cart`;

-- Dumping data for table coverde_db.users_category: ~0 rows (approximately)
DELETE FROM `users_category`;

-- Dumping data for table coverde_db.users_consentlog: ~0 rows (approximately)
DELETE FROM `users_consentlog`;

-- Dumping data for table coverde_db.users_notification: ~0 rows (approximately)
DELETE FROM `users_notification`;

-- Dumping data for table coverde_db.users_notificationpreference: ~0 rows (approximately)
DELETE FROM `users_notificationpreference`;

-- Dumping data for table coverde_db.users_order: ~0 rows (approximately)
DELETE FROM `users_order`;

-- Dumping data for table coverde_db.users_orderitem: ~0 rows (approximately)
DELETE FROM `users_orderitem`;

-- Dumping data for table coverde_db.users_payment: ~0 rows (approximately)
DELETE FROM `users_payment`;

-- Dumping data for table coverde_db.users_producer: ~0 rows (approximately)
DELETE FROM `users_producer`;

-- Dumping data for table coverde_db.users_product: ~0 rows (approximately)
DELETE FROM `users_product`;

-- Dumping data for table coverde_db.users_review: ~0 rows (approximately)
DELETE FROM `users_review`;

-- Dumping data for table coverde_db.users_user: ~8 rows (approximately)
DELETE FROM `users_user`;
INSERT INTO `users_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `accepted_privacy_policy_at`, `accepted_terms_at`, `marketing_opt_in`, `marketing_opt_in_at`, `producer_public_profile_consent_at`, `county`, `data_deleted_at`, `data_exported_at`, `deletion_requested_at`, `district`, `is_verified`, `last_login_ip`, `locked_until`, `login_attempts`, `parish`, `phone`, `profile_image`, `user_type`) VALUES
	(1, 'pbkdf2_sha256$600000$HGBUe8S4WwehwbVWt3Oma1$gfz4x8dqrwDv6mPCuVlESfDFtpZzvnF7Pb2AZdb+DJo=', NULL, 1, 'Admin', '', '', 'a2023110951@alumni.iscac.pt', 1, 1, '2026-04-11 05:51:55.934491', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', NULL, 'consumer'),
	(2, 'pbkdf2_sha256$600000$Z4Px2WeC5A9pgPNRkQS9hK$RXJb7U9iG4UV1TPqxZ6ztThye23g0nRNYw+v0xih3EE=', '2026-04-11 19:22:19.124939', 1, 'PDI', '', '', 'a2023110951@alumni.iscac.pt', 1, 1, '2026-04-11 09:21:35.606357', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', NULL, 'consumer'),
	(3, 'pbkdf2_sha256$600000$0c7qOOnCMWyXyCfDC3xBaU$E3xrVNPVrQyxzQSb7CmzrBfpelupMpvJLdqBnFhMihE=', NULL, 0, 'quinta_do_sol', 'João', 'Silva', 'contato@quintadosol.pt', 0, 1, '2026-04-11 19:42:59.645368', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', '', 'consumer'),
	(4, 'pbkdf2_sha256$600000$aMZXxXTWmMWggOCcHUIdkE$Md2AKInLnwlV98EdpuAFu2McFtUyDCfrBVl+qlYfByg=', NULL, 0, 'horta_da_vila', 'Maria', 'Santos', 'contato@hortadavila.pt', 0, 1, '2026-04-11 19:42:59.913197', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', '', 'consumer'),
	(5, 'pbkdf2_sha256$600000$Ght0xP1YwdLgPi8YDa8Jsz$FixIVYWEad07UwuroXBhDlaTU9foNvJl7JCKUasXGzg=', NULL, 0, 'fazenda_verde', 'António', 'Ferreira', 'contato@fazendaverde.pt', 0, 1, '2026-04-11 19:43:00.158907', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', '', 'consumer'),
	(6, 'pbkdf2_sha256$600000$WXjkZc2xGk5wXVlA0zmk6Y$ZwkiL1xjAwzL5OiDZ206b48bmRPtjmDWduQXtbXG8VM=', NULL, 0, 'pomar_do_oeste', 'Ricardo', 'Almeida', 'contato@pomardoeste.pt', 0, 1, '2026-04-11 19:43:00.448460', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', '', 'consumer'),
	(7, 'pbkdf2_sha256$600000$HRpz58n27BkEjIAdFR2T42$tV8ZyX2lh9rknf8T5EmH2aegjPhZgnKDmqjFvz3FeTU=', NULL, 0, 'quinta_bio_coimbra', 'Teresa', 'Costa', 'contato@quintabio.pt', 0, 1, '2026-04-11 19:43:00.747344', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', '', 'consumer'),
	(8, 'pbkdf2_sha256$600000$COzdZxNiW2RIO0iUdZ7kKF$+9WsUgJXdaKGNrGOeY8Gz6mOqscPjzDKskUmlVE8/5Q=', NULL, 0, 'hortas_do_ave', 'Manuel', 'Rodrigues', 'contato@hortasdoave.pt', 0, 1, '2026-04-11 19:43:01.047285', NULL, NULL, 0, NULL, NULL, '', NULL, NULL, NULL, '', 0, NULL, NULL, 0, '', '', '', 'consumer');

-- Dumping data for table coverde_db.users_user_groups: ~0 rows (approximately)
DELETE FROM `users_user_groups`;

-- Dumping data for table coverde_db.users_user_user_permissions: ~0 rows (approximately)
DELETE FROM `users_user_user_permissions`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
