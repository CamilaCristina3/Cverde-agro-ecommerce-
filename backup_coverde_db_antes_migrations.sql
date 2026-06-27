-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: coverde_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add User',6,'add_user'),(22,'Can change User',6,'change_user'),(23,'Can delete User',6,'delete_user'),(24,'Can view User',6,'view_user'),(25,'Can add Two-Factor Code',7,'add_twofactorcode'),(26,'Can change Two-Factor Code',7,'change_twofactorcode'),(27,'Can delete Two-Factor Code',7,'delete_twofactorcode'),(28,'Can view Two-Factor Code',7,'view_twofactorcode'),(29,'Can add Email Verification Token',8,'add_emailverificationtoken'),(30,'Can change Email Verification Token',8,'change_emailverificationtoken'),(31,'Can delete Email Verification Token',8,'delete_emailverificationtoken'),(32,'Can view Email Verification Token',8,'view_emailverificationtoken'),(33,'Can add Producer',9,'add_producer'),(34,'Can change Producer',9,'change_producer'),(35,'Can delete Producer',9,'delete_producer'),(36,'Can view Producer',9,'view_producer'),(37,'Can add Producer Certification',10,'add_producercertification'),(38,'Can change Producer Certification',10,'change_producercertification'),(39,'Can delete Producer Certification',10,'delete_producercertification'),(40,'Can view Producer Certification',10,'view_producercertification'),(41,'Can add Store',11,'add_store'),(42,'Can change Store',11,'change_store'),(43,'Can delete Store',11,'delete_store'),(44,'Can view Store',11,'view_store'),(45,'Can add Category',12,'add_category'),(46,'Can change Category',12,'change_category'),(47,'Can delete Category',12,'delete_category'),(48,'Can view Category',12,'view_category'),(49,'Can add Product',13,'add_product'),(50,'Can change Product',13,'change_product'),(51,'Can delete Product',13,'delete_product'),(52,'Can view Product',13,'view_product'),(53,'Can add Product Image',14,'add_productimage'),(54,'Can change Product Image',14,'change_productimage'),(55,'Can delete Product Image',14,'delete_productimage'),(56,'Can view Product Image',14,'view_productimage'),(57,'Can add Product Approval',15,'add_productapproval'),(58,'Can change Product Approval',15,'change_productapproval'),(59,'Can delete Product Approval',15,'delete_productapproval'),(60,'Can view Product Approval',15,'view_productapproval'),(61,'Can add Inventory Log',16,'add_inventorylog'),(62,'Can change Inventory Log',16,'change_inventorylog'),(63,'Can delete Inventory Log',16,'delete_inventorylog'),(64,'Can view Inventory Log',16,'view_inventorylog'),(65,'Can add Stock Alert',17,'add_stockalert'),(66,'Can change Stock Alert',17,'change_stockalert'),(67,'Can delete Stock Alert',17,'delete_stockalert'),(68,'Can view Stock Alert',17,'view_stockalert'),(69,'Can add Cart',18,'add_cart'),(70,'Can change Cart',18,'change_cart'),(71,'Can delete Cart',18,'delete_cart'),(72,'Can view Cart',18,'view_cart'),(73,'Can add Cart Item',19,'add_cartitem'),(74,'Can change Cart Item',19,'change_cartitem'),(75,'Can delete Cart Item',19,'delete_cartitem'),(76,'Can view Cart Item',19,'view_cartitem'),(77,'Can add Order',20,'add_order'),(78,'Can change Order',20,'change_order'),(79,'Can delete Order',20,'delete_order'),(80,'Can view Order',20,'view_order'),(81,'Can add Order Item',21,'add_orderitem'),(82,'Can change Order Item',21,'change_orderitem'),(83,'Can delete Order Item',21,'delete_orderitem'),(84,'Can view Order Item',21,'view_orderitem'),(85,'Can add Pagamento',22,'add_payment'),(86,'Can change Pagamento',22,'change_payment'),(87,'Can delete Pagamento',22,'delete_payment'),(88,'Can view Pagamento',22,'view_payment'),(89,'Can add Delivery',23,'add_delivery'),(90,'Can change Delivery',23,'change_delivery'),(91,'Can delete Delivery',23,'delete_delivery'),(92,'Can view Delivery',23,'view_delivery'),(93,'Can add Avaliação',24,'add_review'),(94,'Can change Avaliação',24,'change_review'),(95,'Can delete Avaliação',24,'delete_review'),(96,'Can view Avaliação',24,'view_review'),(97,'Can add Support Ticket',25,'add_supportticket'),(98,'Can change Support Ticket',25,'change_supportticket'),(99,'Can delete Support Ticket',25,'delete_supportticket'),(100,'Can view Support Ticket',25,'view_supportticket'),(101,'Can add Ticket Message',26,'add_ticketmessage'),(102,'Can change Ticket Message',26,'change_ticketmessage'),(103,'Can delete Ticket Message',26,'delete_ticketmessage'),(104,'Can view Ticket Message',26,'view_ticketmessage'),(105,'Can add Commission Report',27,'add_commissionreport'),(106,'Can change Commission Report',27,'change_commissionreport'),(107,'Can delete Commission Report',27,'delete_commissionreport'),(108,'Can view Commission Report',27,'view_commissionreport'),(109,'Can add Sales Report',28,'add_salesreport'),(110,'Can change Sales Report',28,'change_salesreport'),(111,'Can delete Sales Report',28,'delete_salesreport'),(112,'Can view Sales Report',28,'view_salesreport');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_cart`
--

DROP TABLE IF EXISTS `cart_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `items` json NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_key` (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_cart`
--

LOCK TABLES `cart_cart` WRITE;
/*!40000 ALTER TABLE `cart_cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_cartitem`
--

DROP TABLE IF EXISTS `cart_cartitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_cartitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `cart_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cart_cartitem_cart_id_product_id_53cce7c3_uniq` (`cart_id`,`product_id`),
  KEY `cart_cartitem_product_id_b24e265a_fk_products_product_id` (`product_id`),
  CONSTRAINT `cart_cartitem_cart_id_370ad265_fk_cart_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `cart_cart` (`id`),
  CONSTRAINT `cart_cartitem_product_id_b24e265a_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `cart_cartitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_cartitem`
--

LOCK TABLES `cart_cartitem` WRITE;
/*!40000 ALTER TABLE `cart_cartitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories_category`
--

DROP TABLE IF EXISTS `categories_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `categories_category_parent_id_f141de59_fk_categories_category_id` (`parent_id`),
  CONSTRAINT `categories_category_parent_id_f141de59_fk_categories_category_id` FOREIGN KEY (`parent_id`) REFERENCES `categories_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories_category`
--

LOCK TABLES `categories_category` WRITE;
/*!40000 ALTER TABLE `categories_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliveries_delivery`
--

DROP TABLE IF EXISTS `deliveries_delivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveries_delivery` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tracking_number` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `carrier` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `scheduled_date` date DEFAULT NULL,
  `delivered_date` date DEFAULT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  CONSTRAINT `deliveries_delivery_order_id_ed63b6ba_fk_orders_mgmt_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_mgmt_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliveries_delivery`
--

LOCK TABLES `deliveries_delivery` WRITE;
/*!40000 ALTER TABLE `deliveries_delivery` DISABLE KEYS */;
/*!40000 ALTER TABLE `deliveries_delivery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(18,'cart','cart'),(19,'cart','cartitem'),(12,'categories','category'),(4,'contenttypes','contenttype'),(23,'deliveries','delivery'),(16,'inventory','inventorylog'),(17,'inventory','stockalert'),(20,'orders_mgmt','order'),(21,'orders_mgmt','orderitem'),(22,'payments','payment'),(9,'producers','producer'),(10,'producers','producercertification'),(13,'products','product'),(15,'products','productapproval'),(14,'products','productimage'),(27,'reports','commissionreport'),(28,'reports','salesreport'),(24,'reviews','review'),(5,'sessions','session'),(11,'stores','store'),(25,'support','supportticket'),(26,'support','ticketmessage'),(8,'users_auth','emailverificationtoken'),(7,'users_auth','twofactorcode'),(6,'users_auth','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-06-25 18:37:18.151650'),(2,'contenttypes','0002_remove_content_type_name','2026-06-25 18:37:18.241829'),(3,'auth','0001_initial','2026-06-25 18:37:18.630503'),(4,'auth','0002_alter_permission_name_max_length','2026-06-25 18:37:18.720741'),(5,'auth','0003_alter_user_email_max_length','2026-06-25 18:37:18.727743'),(6,'auth','0004_alter_user_username_opts','2026-06-25 18:37:18.734809'),(7,'auth','0005_alter_user_last_login_null','2026-06-25 18:37:18.741645'),(8,'auth','0006_require_contenttypes_0002','2026-06-25 18:37:18.752009'),(9,'auth','0007_alter_validators_add_error_messages','2026-06-25 18:37:18.758801'),(10,'auth','0008_alter_user_username_max_length','2026-06-25 18:37:18.765025'),(11,'auth','0009_alter_user_last_name_max_length','2026-06-25 18:37:18.769372'),(12,'auth','0010_alter_group_name_max_length','2026-06-25 18:37:18.790584'),(13,'auth','0011_update_proxy_permissions','2026-06-25 18:37:18.797314'),(14,'auth','0012_alter_user_first_name_max_length','2026-06-25 18:37:18.806197'),(15,'users_auth','0001_initial','2026-06-25 18:37:19.790030'),(16,'admin','0001_initial','2026-06-25 18:37:20.021503'),(17,'admin','0002_logentry_remove_auto_add','2026-06-25 18:37:20.033205'),(18,'admin','0003_logentry_add_action_flag_choices','2026-06-25 18:37:20.049260'),(19,'products','0001_initial','2026-06-25 18:37:20.345833'),(20,'cart','0001_initial','2026-06-25 18:37:20.498255'),(21,'cart','0002_initial','2026-06-25 18:37:20.637096'),(22,'categories','0001_initial','2026-06-25 18:37:20.775063'),(23,'orders_mgmt','0001_initial','2026-06-25 18:37:20.914911'),(26,'inventory','0001_initial','2026-06-25 18:37:21.101977'),(27,'inventory','0002_initial','2026-06-25 18:37:21.188003'),(28,'inventory','0003_initial','2026-06-25 18:37:21.366268'),(29,'orders_mgmt','0002_initial','2026-06-25 18:37:21.484127'),(30,'orders_mgmt','0003_initial','2026-06-25 18:37:21.574970'),(31,'payments','0001_initial','2026-06-25 18:37:21.680131'),(32,'producers','0001_initial','2026-06-25 18:37:21.824148'),(33,'producers','0002_initial','2026-06-25 18:37:22.018746'),(34,'products','0002_initial','2026-06-25 18:37:22.344639'),(35,'reports','0001_initial','2026-06-25 18:37:22.608488'),(36,'sessions','0001_initial','2026-06-25 18:37:22.657035'),(37,'stores','0001_initial','2026-06-25 18:37:22.799442'),(38,'support','0001_initial','2026-06-25 18:37:22.941968'),(39,'support','0002_initial','2026-06-25 18:37:23.308950');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations_backup_20260626`
--

DROP TABLE IF EXISTS `django_migrations_backup_20260626`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations_backup_20260626` (
  `id` bigint NOT NULL DEFAULT '0',
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations_backup_20260626`
--

LOCK TABLES `django_migrations_backup_20260626` WRITE;
/*!40000 ALTER TABLE `django_migrations_backup_20260626` DISABLE KEYS */;
INSERT INTO `django_migrations_backup_20260626` VALUES (1,'contenttypes','0001_initial','2026-06-25 18:37:18.151650'),(2,'contenttypes','0002_remove_content_type_name','2026-06-25 18:37:18.241829'),(3,'auth','0001_initial','2026-06-25 18:37:18.630503'),(4,'auth','0002_alter_permission_name_max_length','2026-06-25 18:37:18.720741'),(5,'auth','0003_alter_user_email_max_length','2026-06-25 18:37:18.727743'),(6,'auth','0004_alter_user_username_opts','2026-06-25 18:37:18.734809'),(7,'auth','0005_alter_user_last_login_null','2026-06-25 18:37:18.741645'),(8,'auth','0006_require_contenttypes_0002','2026-06-25 18:37:18.752009'),(9,'auth','0007_alter_validators_add_error_messages','2026-06-25 18:37:18.758801'),(10,'auth','0008_alter_user_username_max_length','2026-06-25 18:37:18.765025'),(11,'auth','0009_alter_user_last_name_max_length','2026-06-25 18:37:18.769372'),(12,'auth','0010_alter_group_name_max_length','2026-06-25 18:37:18.790584'),(13,'auth','0011_update_proxy_permissions','2026-06-25 18:37:18.797314'),(14,'auth','0012_alter_user_first_name_max_length','2026-06-25 18:37:18.806197'),(15,'users_auth','0001_initial','2026-06-25 18:37:19.790030'),(16,'admin','0001_initial','2026-06-25 18:37:20.021503'),(17,'admin','0002_logentry_remove_auto_add','2026-06-25 18:37:20.033205'),(18,'admin','0003_logentry_add_action_flag_choices','2026-06-25 18:37:20.049260'),(19,'products','0001_initial','2026-06-25 18:37:20.345833'),(20,'cart','0001_initial','2026-06-25 18:37:20.498255'),(21,'cart','0002_initial','2026-06-25 18:37:20.637096'),(22,'categories','0001_initial','2026-06-25 18:37:20.775063'),(23,'orders_mgmt','0001_initial','2026-06-25 18:37:20.914911'),(24,'deliveries','0001_initial','2026-06-25 18:37:20.949240'),(25,'deliveries','0002_initial','2026-06-25 18:37:21.046922'),(26,'inventory','0001_initial','2026-06-25 18:37:21.101977'),(27,'inventory','0002_initial','2026-06-25 18:37:21.188003'),(28,'inventory','0003_initial','2026-06-25 18:37:21.366268'),(29,'orders_mgmt','0002_initial','2026-06-25 18:37:21.484127'),(30,'orders_mgmt','0003_initial','2026-06-25 18:37:21.574970'),(31,'payments','0001_initial','2026-06-25 18:37:21.680131'),(32,'producers','0001_initial','2026-06-25 18:37:21.824148'),(33,'producers','0002_initial','2026-06-25 18:37:22.018746'),(34,'products','0002_initial','2026-06-25 18:37:22.344639'),(35,'reports','0001_initial','2026-06-25 18:37:22.608488'),(36,'sessions','0001_initial','2026-06-25 18:37:22.657035'),(37,'stores','0001_initial','2026-06-25 18:37:22.799442'),(38,'support','0001_initial','2026-06-25 18:37:22.941968'),(39,'support','0002_initial','2026-06-25 18:37:23.308950'),(40,'orders','0001_initial','2026-06-26 23:40:51.000000');
/*!40000 ALTER TABLE `django_migrations_backup_20260626` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_inventorylog`
--

DROP TABLE IF EXISTS `inventory_inventorylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_inventorylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `movement_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` int NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_inventoryl_created_by_id_8d5d00f5_fk_users_aut` (`created_by_id`),
  KEY `inventory_inventoryl_product_id_eba27e8c_fk_products_` (`product_id`),
  CONSTRAINT `inventory_inventoryl_created_by_id_8d5d00f5_fk_users_aut` FOREIGN KEY (`created_by_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `inventory_inventoryl_product_id_eba27e8c_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_inventorylog`
--

LOCK TABLES `inventory_inventorylog` WRITE;
/*!40000 ALTER TABLE `inventory_inventorylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_inventorylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_stockalert`
--

DROP TABLE IF EXISTS `inventory_stockalert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_stockalert` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `threshold` int unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `notified_at` datetime(6) DEFAULT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_stockalert_product_id_11f4588d_fk_products_product_id` (`product_id`),
  CONSTRAINT `inventory_stockalert_product_id_11f4588d_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `inventory_stockalert_chk_1` CHECK ((`threshold` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_stockalert`
--

LOCK TABLES `inventory_stockalert` WRITE;
/*!40000 ALTER TABLE `inventory_stockalert` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_stockalert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_mgmt_order`
--

DROP TABLE IF EXISTS `orders_mgmt_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_mgmt_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `vat_amount` decimal(10,2) NOT NULL,
  `shipping_cost` decimal(10,2) NOT NULL,
  `shipping_address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipping_contact` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_number` (`order_number`),
  KEY `orders_mgmt_order_user_id_66d8d27f_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `orders_mgmt_order_user_id_66d8d27f_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_mgmt_order`
--

LOCK TABLES `orders_mgmt_order` WRITE;
/*!40000 ALTER TABLE `orders_mgmt_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_mgmt_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_mgmt_orderitem`
--

DROP TABLE IF EXISTS `orders_mgmt_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_mgmt_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_mgmt_orderitem_order_id_0c0184c8_fk_orders_mgmt_order_id` (`order_id`),
  KEY `orders_mgmt_orderitem_product_id_6c89e427_fk_products_product_id` (`product_id`),
  CONSTRAINT `orders_mgmt_orderitem_order_id_0c0184c8_fk_orders_mgmt_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_mgmt_order` (`id`),
  CONSTRAINT `orders_mgmt_orderitem_product_id_6c89e427_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `orders_mgmt_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_mgmt_orderitem`
--

LOCK TABLES `orders_mgmt_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_mgmt_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_mgmt_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_payment`
--

DROP TABLE IF EXISTS `payments_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `provider` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_method` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_test_payment` tinyint(1) NOT NULL,
  `test_signature` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `test_password_hash` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `transaction_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `retry_count` int NOT NULL,
  `error_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `paid_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_payment_order_id_22c479b7_fk_orders_mgmt_order_id` (`order_id`),
  CONSTRAINT `payments_payment_order_id_22c479b7_fk_orders_mgmt_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_mgmt_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_payment`
--

LOCK TABLES `payments_payment` WRITE;
/*!40000 ALTER TABLE `payments_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producers_producer`
--

DROP TABLE IF EXISTS `producers_producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producers_producer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nif` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `verification_document` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `verified_at` datetime(6) DEFAULT NULL,
  `rejection_reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `total_ratings` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `verified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `producers_producer_verified_by_id_7f1fcf32_fk_users_auth_user_id` (`verified_by_id`),
  CONSTRAINT `producers_producer_user_id_64341d4f_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `producers_producer_verified_by_id_7f1fcf32_fk_users_auth_user_id` FOREIGN KEY (`verified_by_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producers_producer`
--

LOCK TABLES `producers_producer` WRITE;
/*!40000 ALTER TABLE `producers_producer` DISABLE KEYS */;
/*!40000 ALTER TABLE `producers_producer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producers_producercertification`
--

DROP TABLE IF EXISTS `producers_producercertification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producers_producercertification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cert_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `issue_date` date NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `certificate_number` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `document` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `producer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `producers_producerce_producer_id_6fd18ee6_fk_producers` (`producer_id`),
  CONSTRAINT `producers_producerce_producer_id_6fd18ee6_fk_producers` FOREIGN KEY (`producer_id`) REFERENCES `producers_producer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producers_producercertification`
--

LOCK TABLES `producers_producercertification` WRITE;
/*!40000 ALTER TABLE `producers_producercertification` DISABLE KEYS */;
/*!40000 ALTER TABLE `producers_producercertification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product`
--

DROP TABLE IF EXISTS `products_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int unsigned NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `certification` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `total_reviews` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint DEFAULT NULL,
  `producer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `products_product_category_id_9b594869_fk_categories_category_id` (`category_id`),
  KEY `products_product_producer_id_be45bf24_fk_producers_producer_id` (`producer_id`),
  CONSTRAINT `products_product_category_id_9b594869_fk_categories_category_id` FOREIGN KEY (`category_id`) REFERENCES `categories_category` (`id`),
  CONSTRAINT `products_product_producer_id_be45bf24_fk_producers_producer_id` FOREIGN KEY (`producer_id`) REFERENCES `producers_producer` (`id`),
  CONSTRAINT `products_product_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product`
--

LOCK TABLES `products_product` WRITE;
/*!40000 ALTER TABLE `products_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_productapproval`
--

DROP TABLE IF EXISTS `products_productapproval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_productapproval` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `rejection_reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `reviewed_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`),
  KEY `products_productappr_reviewed_by_id_bef35484_fk_users_aut` (`reviewed_by_id`),
  CONSTRAINT `products_productappr_product_id_65adecbc_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `products_productappr_reviewed_by_id_bef35484_fk_users_aut` FOREIGN KEY (`reviewed_by_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productapproval`
--

LOCK TABLES `products_productapproval` WRITE;
/*!40000 ALTER TABLE `products_productapproval` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_productapproval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_productimage`
--

DROP TABLE IF EXISTS `products_productimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_productimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alt_text` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_productimage_product_id_e747596a_fk_products_product_id` (`product_id`),
  CONSTRAINT `products_productimage_product_id_e747596a_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productimage`
--

LOCK TABLES `products_productimage` WRITE;
/*!40000 ALTER TABLE `products_productimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_productimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_commissionreport`
--

DROP TABLE IF EXISTS `reports_commissionreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports_commissionreport` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `period_start` date NOT NULL,
  `period_end` date NOT NULL,
  `gross_revenue` decimal(12,2) NOT NULL,
  `commission_percentage` decimal(5,2) NOT NULL,
  `commission_amount` decimal(12,2) NOT NULL,
  `net_revenue` decimal(12,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `producer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reports_commissionre_producer_id_4be24f51_fk_producers` (`producer_id`),
  CONSTRAINT `reports_commissionre_producer_id_4be24f51_fk_producers` FOREIGN KEY (`producer_id`) REFERENCES `producers_producer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_commissionreport`
--

LOCK TABLES `reports_commissionreport` WRITE;
/*!40000 ALTER TABLE `reports_commissionreport` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_commissionreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_salesreport`
--

DROP TABLE IF EXISTS `reports_salesreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports_salesreport` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `period` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `total_orders` int NOT NULL,
  `total_revenue` decimal(12,2) NOT NULL,
  `total_items_sold` int NOT NULL,
  `average_order_value` decimal(10,2) NOT NULL,
  `generated_at` datetime(6) NOT NULL,
  `producer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reports_salesreport_producer_id_period_start_abb8a880_uniq` (`producer_id`,`period`,`start_date`,`end_date`),
  CONSTRAINT `reports_salesreport_producer_id_b4c71798_fk_producers` FOREIGN KEY (`producer_id`) REFERENCES `producers_producer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_salesreport`
--

LOCK TABLES `reports_salesreport` WRITE;
/*!40000 ALTER TABLE `reports_salesreport` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_salesreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stores_store`
--

DROP TABLE IF EXISTS `stores_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stores_store` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `banner` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_methods` json NOT NULL,
  `delivery_fee` decimal(10,2) NOT NULL,
  `min_order_value` decimal(10,2) NOT NULL,
  `operating_hours` json NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `total_reviews` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `producer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  UNIQUE KEY `producer_id` (`producer_id`),
  CONSTRAINT `stores_store_producer_id_f9d755b1_fk_producers_producer_id` FOREIGN KEY (`producer_id`) REFERENCES `producers_producer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stores_store`
--

LOCK TABLES `stores_store` WRITE;
/*!40000 ALTER TABLE `stores_store` DISABLE KEYS */;
/*!40000 ALTER TABLE `stores_store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support_supportticket`
--

DROP TABLE IF EXISTS `support_supportticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `support_supportticket` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ticket_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `priority` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `resolved_at` datetime(6) DEFAULT NULL,
  `assigned_to_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ticket_number` (`ticket_number`),
  KEY `support_supportticke_assigned_to_id_1b1ae160_fk_users_aut` (`assigned_to_id`),
  KEY `support_supportticket_user_id_afde63b2_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `support_supportticke_assigned_to_id_1b1ae160_fk_users_aut` FOREIGN KEY (`assigned_to_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `support_supportticket_user_id_afde63b2_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support_supportticket`
--

LOCK TABLES `support_supportticket` WRITE;
/*!40000 ALTER TABLE `support_supportticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `support_supportticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support_ticketmessage`
--

DROP TABLE IF EXISTS `support_ticketmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `support_ticketmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `attachment` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `ticket_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `support_ticketmessag_ticket_id_70fe8f82_fk_support_s` (`ticket_id`),
  KEY `support_ticketmessage_user_id_7463032e_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `support_ticketmessag_ticket_id_70fe8f82_fk_support_s` FOREIGN KEY (`ticket_id`) REFERENCES `support_supportticket` (`id`),
  CONSTRAINT `support_ticketmessage_user_id_7463032e_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support_ticketmessage`
--

LOCK TABLES `support_ticketmessage` WRITE;
/*!40000 ALTER TABLE `support_ticketmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `support_ticketmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_auth_emailverificationtoken`
--

DROP TABLE IF EXISTS `users_auth_emailverificationtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_auth_emailverificationtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `used_at` datetime(6) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `users_auth_emailveri_user_id_a4387a68_fk_users_aut` (`user_id`),
  CONSTRAINT `users_auth_emailveri_user_id_a4387a68_fk_users_aut` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_auth_emailverificationtoken`
--

LOCK TABLES `users_auth_emailverificationtoken` WRITE;
/*!40000 ALTER TABLE `users_auth_emailverificationtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_auth_emailverificationtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_auth_twofactorcode`
--

DROP TABLE IF EXISTS `users_auth_twofactorcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_auth_twofactorcode` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code_hash` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `used_at` datetime(6) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_auth_twofactorcode_user_id_827f2fd2_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `users_auth_twofactorcode_user_id_827f2fd2_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_auth_twofactorcode`
--

LOCK TABLES `users_auth_twofactorcode` WRITE;
/*!40000 ALTER TABLE `users_auth_twofactorcode` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_auth_twofactorcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_auth_user`
--

DROP TABLE IF EXISTS `users_auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_auth_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profile_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `email_verified_at` datetime(6) DEFAULT NULL,
  `accepted_terms_at` datetime(6) DEFAULT NULL,
  `accepted_privacy_policy_at` datetime(6) DEFAULT NULL,
  `marketing_opt_in` tinyint(1) NOT NULL,
  `marketing_opt_in_at` datetime(6) DEFAULT NULL,
  `data_deleted_at` datetime(6) DEFAULT NULL,
  `deletion_requested_at` datetime(6) DEFAULT NULL,
  `login_attempts` int NOT NULL,
  `locked_until` datetime(6) DEFAULT NULL,
  `last_login_ip` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `two_factor_enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_auth_user`
--

LOCK TABLES `users_auth_user` WRITE;
/*!40000 ALTER TABLE `users_auth_user` DISABLE KEYS */;
INSERT INTO `users_auth_user` VALUES (1,'pbkdf2_sha256$600000$s2oOJ8cGteRwcA6bWlIqZi$yebxzLa7I+/Nah8V1Y033/enPk0yQP40y9BmCcqLSec=',NULL,1,'admin','','','admin@coverde.pt',1,1,'2026-06-25 18:37:32.250844','consumer',NULL,'',0,NULL,NULL,NULL,0,NULL,NULL,NULL,4,NULL,NULL,0);
/*!40000 ALTER TABLE `users_auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_auth_user_groups`
--

DROP TABLE IF EXISTS `users_auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_auth_user_groups_user_id_group_id_a0811253_uniq` (`user_id`,`group_id`),
  KEY `users_auth_user_groups_group_id_c71e3cd1_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_auth_user_groups_group_id_c71e3cd1_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_auth_user_groups_user_id_b88383ed_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_auth_user_groups`
--

LOCK TABLES `users_auth_user_groups` WRITE;
/*!40000 ALTER TABLE `users_auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_auth_user_user_permissions`
--

DROP TABLE IF EXISTS `users_auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_auth_user_user_per_user_id_permission_id_9e8689c4_uniq` (`user_id`,`permission_id`),
  KEY `users_auth_user_user_permission_id_80bb93d0_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_auth_user_user_permission_id_80bb93d0_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_auth_user_user_user_id_2268a911_fk_users_aut` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_auth_user_user_permissions`
--

LOCK TABLES `users_auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-27 12:31:04
