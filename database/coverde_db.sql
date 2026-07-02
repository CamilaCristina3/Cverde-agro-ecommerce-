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
-- Current Database: `coverde_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `coverde_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `coverde_db`;

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
) ENGINE=InnoDB AUTO_INCREMENT=177 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add User',6,'add_user'),(22,'Can change User',6,'change_user'),(23,'Can delete User',6,'delete_user'),(24,'Can view User',6,'view_user'),(25,'Can add Two-Factor Code',7,'add_twofactorcode'),(26,'Can change Two-Factor Code',7,'change_twofactorcode'),(27,'Can delete Two-Factor Code',7,'delete_twofactorcode'),(28,'Can view Two-Factor Code',7,'view_twofactorcode'),(29,'Can add Email Verification Token',8,'add_emailverificationtoken'),(30,'Can change Email Verification Token',8,'change_emailverificationtoken'),(31,'Can delete Email Verification Token',8,'delete_emailverificationtoken'),(32,'Can view Email Verification Token',8,'view_emailverificationtoken'),(33,'Can add Producer',9,'add_producer'),(34,'Can change Producer',9,'change_producer'),(35,'Can delete Producer',9,'delete_producer'),(36,'Can view Producer',9,'view_producer'),(37,'Can add Producer Certification',10,'add_producercertification'),(38,'Can change Producer Certification',10,'change_producercertification'),(39,'Can delete Producer Certification',10,'delete_producercertification'),(40,'Can view Producer Certification',10,'view_producercertification'),(41,'Can add Store',11,'add_store'),(42,'Can change Store',11,'change_store'),(43,'Can delete Store',11,'delete_store'),(44,'Can view Store',11,'view_store'),(45,'Can add Category',12,'add_category'),(46,'Can change Category',12,'change_category'),(47,'Can delete Category',12,'delete_category'),(48,'Can view Category',12,'view_category'),(49,'Can add Product',13,'add_product'),(50,'Can change Product',13,'change_product'),(51,'Can delete Product',13,'delete_product'),(52,'Can view Product',13,'view_product'),(53,'Can add Product Image',14,'add_productimage'),(54,'Can change Product Image',14,'change_productimage'),(55,'Can delete Product Image',14,'delete_productimage'),(56,'Can view Product Image',14,'view_productimage'),(57,'Can add Product Approval',15,'add_productapproval'),(58,'Can change Product Approval',15,'change_productapproval'),(59,'Can delete Product Approval',15,'delete_productapproval'),(60,'Can view Product Approval',15,'view_productapproval'),(61,'Can add Inventory Log',16,'add_inventorylog'),(62,'Can change Inventory Log',16,'change_inventorylog'),(63,'Can delete Inventory Log',16,'delete_inventorylog'),(64,'Can view Inventory Log',16,'view_inventorylog'),(65,'Can add Stock Alert',17,'add_stockalert'),(66,'Can change Stock Alert',17,'change_stockalert'),(67,'Can delete Stock Alert',17,'delete_stockalert'),(68,'Can view Stock Alert',17,'view_stockalert'),(69,'Can add Cart',18,'add_cart'),(70,'Can change Cart',18,'change_cart'),(71,'Can delete Cart',18,'delete_cart'),(72,'Can view Cart',18,'view_cart'),(73,'Can add Cart Item',19,'add_cartitem'),(74,'Can change Cart Item',19,'change_cartitem'),(75,'Can delete Cart Item',19,'delete_cartitem'),(76,'Can view Cart Item',19,'view_cartitem'),(77,'Can add Order',20,'add_order'),(78,'Can change Order',20,'change_order'),(79,'Can delete Order',20,'delete_order'),(80,'Can view Order',20,'view_order'),(81,'Can add Order Item',21,'add_orderitem'),(82,'Can change Order Item',21,'change_orderitem'),(83,'Can delete Order Item',21,'delete_orderitem'),(84,'Can view Order Item',21,'view_orderitem'),(85,'Can add Pagamento',22,'add_payment'),(86,'Can change Pagamento',22,'change_payment'),(87,'Can delete Pagamento',22,'delete_payment'),(88,'Can view Pagamento',22,'view_payment'),(89,'Can add Delivery',23,'add_delivery'),(90,'Can change Delivery',23,'change_delivery'),(91,'Can delete Delivery',23,'delete_delivery'),(92,'Can view Delivery',23,'view_delivery'),(93,'Can add Avaliação',24,'add_review'),(94,'Can change Avaliação',24,'change_review'),(95,'Can delete Avaliação',24,'delete_review'),(96,'Can view Avaliação',24,'view_review'),(97,'Can add Support Ticket',25,'add_supportticket'),(98,'Can change Support Ticket',25,'change_supportticket'),(99,'Can delete Support Ticket',25,'delete_supportticket'),(100,'Can view Support Ticket',25,'view_supportticket'),(101,'Can add Ticket Message',26,'add_ticketmessage'),(102,'Can change Ticket Message',26,'change_ticketmessage'),(103,'Can delete Ticket Message',26,'delete_ticketmessage'),(104,'Can view Ticket Message',26,'view_ticketmessage'),(105,'Can add Commission Report',27,'add_commissionreport'),(106,'Can change Commission Report',27,'change_commissionreport'),(107,'Can delete Commission Report',27,'delete_commissionreport'),(108,'Can view Commission Report',27,'view_commissionreport'),(109,'Can add Sales Report',28,'add_salesreport'),(110,'Can change Sales Report',28,'change_salesreport'),(111,'Can delete Sales Report',28,'delete_salesreport'),(112,'Can view Sales Report',28,'view_salesreport'),(113,'Can add Perfil de Cliente',29,'add_customerprofile'),(114,'Can change Perfil de Cliente',29,'change_customerprofile'),(115,'Can delete Perfil de Cliente',29,'delete_customerprofile'),(116,'Can view Perfil de Cliente',29,'view_customerprofile'),(117,'Can add Morada',30,'add_address'),(118,'Can change Morada',30,'change_address'),(119,'Can delete Morada',30,'delete_address'),(120,'Can view Morada',30,'view_address'),(121,'Can add Categoria',31,'add_category'),(122,'Can change Categoria',31,'change_category'),(123,'Can delete Categoria',31,'delete_category'),(124,'Can view Categoria',31,'view_category'),(125,'Can add Perfil de Produtor',32,'add_supplierprofile'),(126,'Can change Perfil de Produtor',32,'change_supplierprofile'),(127,'Can delete Perfil de Produtor',32,'delete_supplierprofile'),(128,'Can view Perfil de Produtor',32,'view_supplierprofile'),(129,'Can add Token de Ativação',33,'add_accountactivationtoken'),(130,'Can change Token de Ativação',33,'change_accountactivationtoken'),(131,'Can delete Token de Ativação',33,'delete_accountactivationtoken'),(132,'Can view Token de Ativação',33,'view_accountactivationtoken'),(133,'Can add Notificação',34,'add_notification'),(134,'Can change Notificação',34,'change_notification'),(135,'Can delete Notificação',34,'delete_notification'),(136,'Can view Notificação',34,'view_notification'),(137,'Can add Produto',35,'add_product'),(138,'Can change Produto',35,'change_product'),(139,'Can delete Produto',35,'delete_product'),(140,'Can view Produto',35,'view_product'),(141,'Can add Produtor',36,'add_producer'),(142,'Can change Produtor',36,'change_producer'),(143,'Can delete Produtor',36,'delete_producer'),(144,'Can view Produtor',36,'view_producer'),(145,'Can add chat room',37,'add_chatroom'),(146,'Can change chat room',37,'change_chatroom'),(147,'Can delete chat room',37,'delete_chatroom'),(148,'Can view chat room',37,'view_chatroom'),(149,'Can add chat message',38,'add_chatmessage'),(150,'Can change chat message',38,'change_chatmessage'),(151,'Can delete chat message',38,'delete_chatmessage'),(152,'Can view chat message',38,'view_chatmessage'),(153,'Can add Perfil de Produtor',39,'add_producerprofile'),(154,'Can change Perfil de Produtor',39,'change_producerprofile'),(155,'Can delete Perfil de Produtor',39,'delete_producerprofile'),(156,'Can view Perfil de Produtor',39,'view_producerprofile'),(157,'Can add Encomenda',40,'add_order'),(158,'Can change Encomenda',40,'change_order'),(159,'Can delete Encomenda',40,'delete_order'),(160,'Can view Encomenda',40,'view_order'),(161,'Can add Sub-Encomenda do Produtor',41,'add_sellerorder'),(162,'Can change Sub-Encomenda do Produtor',41,'change_sellerorder'),(163,'Can delete Sub-Encomenda do Produtor',41,'delete_sellerorder'),(164,'Can view Sub-Encomenda do Produtor',41,'view_sellerorder'),(165,'Can add Item de Encomenda',42,'add_orderitem'),(166,'Can change Item de Encomenda',42,'change_orderitem'),(167,'Can delete Item de Encomenda',42,'delete_orderitem'),(168,'Can view Item de Encomenda',42,'view_orderitem'),(169,'Can add notification',43,'add_notification'),(170,'Can change notification',43,'change_notification'),(171,'Can delete notification',43,'delete_notification'),(172,'Can view notification',43,'view_notification'),(173,'Can add Pagamento ao Produtor',44,'add_producerpayout'),(174,'Can change Pagamento ao Produtor',44,'change_producerpayout'),(175,'Can delete Pagamento ao Produtor',44,'delete_producerpayout'),(176,'Can view Pagamento ao Produtor',44,'view_producerpayout');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_cart`
--

LOCK TABLES `cart_cart` WRITE;
/*!40000 ALTER TABLE `cart_cart` DISABLE KEYS */;
INSERT INTO `cart_cart` VALUES (1,'la4vrf8x1agkvrfldtyvu1aysno1a9f9','[]','2026-06-27 15:39:45.710098','2026-06-27 15:39:45.710098'),(2,'bfipi3mvbb92jkoerzqu881pdjpm4k0k','[]','2026-06-29 12:36:20.101232','2026-06-29 12:36:20.101232'),(3,'r3jg42xa1nwi7i0jf2u2wsw7hhtazlyd','[{\"quantity\": 1, \"product_id\": \"b5050d40-3728-4319-96bc-6343d798e536\"}]','2026-06-29 17:21:48.636280','2026-06-29 17:21:48.643158'),(4,'nr8wm1ccfj6s6rqrwlwf2oja5y6v49rz','[{\"quantity\": 2, \"product_id\": \"b5050d40-3728-4319-96bc-6343d798e536\"}]','2026-06-29 17:22:49.799401','2026-06-29 17:23:51.730044'),(5,'8vunu6b1yg2x8he3n6mcvrb84y98tsmd','[{\"quantity\": 1, \"product_id\": \"b5050d40-3728-4319-96bc-6343d798e536\"}]','2026-06-29 17:45:54.722462','2026-06-29 17:45:54.733670'),(6,'xfi6sksqdqpnyu3q5r1u8kyjrqxjvn6x','[]','2026-06-29 17:49:24.522539','2026-06-29 17:51:45.224364');
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
  `product_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cart_cartitem_cart_id_product_id_53cce7c3_uniq` (`cart_id`,`product_id`),
  KEY `cart_cartitem_product_id_b24e265a_fk_users_product_id` (`product_id`),
  CONSTRAINT `cart_cartitem_cart_id_370ad265_fk_cart_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `cart_cart` (`id`),
  CONSTRAINT `cart_cartitem_product_id_b24e265a_fk_users_product_id` FOREIGN KEY (`product_id`) REFERENCES `users_product` (`id`),
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories_category`
--

LOCK TABLES `categories_category` WRITE;
/*!40000 ALTER TABLE `categories_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_chatmessage`
--

DROP TABLE IF EXISTS `chat_chatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_chatmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chat_chatmessage_room_id_5d04fb68_fk_chat_chatroom_id` (`room_id`),
  KEY `chat_chatmessage_user_id_fa615e65_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `chat_chatmessage_room_id_5d04fb68_fk_chat_chatroom_id` FOREIGN KEY (`room_id`) REFERENCES `chat_chatroom` (`id`),
  CONSTRAINT `chat_chatmessage_user_id_fa615e65_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_chatmessage`
--

LOCK TABLES `chat_chatmessage` WRITE;
/*!40000 ALTER TABLE `chat_chatmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_chatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_chatroom`
--

DROP TABLE IF EXISTS `chat_chatroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_chatroom` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_chatroom`
--

LOCK TABLES `chat_chatroom` WRITE;
/*!40000 ALTER TABLE `chat_chatroom` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_chatroom` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-06-29 17:03:29.745939','38288389-9454-4c80-b67d-19bd83739c09','QUINTA P1 - produtor1 AAAAAAAAA',2,'[{\"changed\": {\"fields\": [\"Estado\", \"Verificado\", \"Verificado por\"]}}]',36,11),(2,'2026-06-29 17:07:54.083012','9ad2f136-dd57-4c7c-8c36-3113f323ce07','FRUTAS',1,'[{\"added\": {}}]',31,11),(3,'2026-06-29 17:18:16.032056','1','QUINTA P1 (produtor1@coverde.pt)',2,'[{\"changed\": {\"fields\": [\"Estado\", \"Aprovado por\"]}}]',32,11),(4,'2026-07-02 17:43:49.824801','1','Smoke Category',1,'[{\"added\": {}}]',12,14),(5,'2026-07-02 17:43:49.984385','1','Smoke Category Updated',2,'[{\"changed\": {\"fields\": [\"Name\", \"Description\", \"Icon\", \"Order\"]}}]',12,14),(6,'2026-07-02 17:43:50.026151','1','Smoke Category Updated',3,'',12,14);
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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(18,'cart','cart'),(19,'cart','cartitem'),(12,'categories','category'),(38,'chat','chatmessage'),(37,'chat','chatroom'),(4,'contenttypes','contenttype'),(23,'deliveries','delivery'),(16,'inventory','inventorylog'),(17,'inventory','stockalert'),(43,'notifications','notification'),(40,'orders','order'),(42,'orders','orderitem'),(41,'orders','sellerorder'),(20,'orders_mgmt','order'),(21,'orders_mgmt','orderitem'),(22,'payments','payment'),(44,'payments','producerpayout'),(9,'producers','producer'),(10,'producers','producercertification'),(39,'products','producerprofile'),(13,'products','product'),(15,'products','productapproval'),(14,'products','productimage'),(27,'reports','commissionreport'),(28,'reports','salesreport'),(24,'reviews','review'),(5,'sessions','session'),(11,'stores','store'),(25,'support','supportticket'),(26,'support','ticketmessage'),(33,'users','accountactivationtoken'),(30,'users','address'),(31,'users','category'),(29,'users','customerprofile'),(34,'users','notification'),(36,'users','producer'),(35,'users','product'),(32,'users','supplierprofile'),(8,'users_auth','emailverificationtoken'),(7,'users_auth','twofactorcode'),(6,'users_auth','user');
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-06-25 18:37:18.151650'),(2,'contenttypes','0002_remove_content_type_name','2026-06-25 18:37:18.241829'),(3,'auth','0001_initial','2026-06-25 18:37:18.630503'),(4,'auth','0002_alter_permission_name_max_length','2026-06-25 18:37:18.720741'),(5,'auth','0003_alter_user_email_max_length','2026-06-25 18:37:18.727743'),(6,'auth','0004_alter_user_username_opts','2026-06-25 18:37:18.734809'),(7,'auth','0005_alter_user_last_login_null','2026-06-25 18:37:18.741645'),(8,'auth','0006_require_contenttypes_0002','2026-06-25 18:37:18.752009'),(9,'auth','0007_alter_validators_add_error_messages','2026-06-25 18:37:18.758801'),(10,'auth','0008_alter_user_username_max_length','2026-06-25 18:37:18.765025'),(11,'auth','0009_alter_user_last_name_max_length','2026-06-25 18:37:18.769372'),(12,'auth','0010_alter_group_name_max_length','2026-06-25 18:37:18.790584'),(13,'auth','0011_update_proxy_permissions','2026-06-25 18:37:18.797314'),(14,'auth','0012_alter_user_first_name_max_length','2026-06-25 18:37:18.806197'),(15,'users_auth','0001_initial','2026-06-25 18:37:19.790030'),(16,'admin','0001_initial','2026-06-25 18:37:20.021503'),(17,'admin','0002_logentry_remove_auto_add','2026-06-25 18:37:20.033205'),(18,'admin','0003_logentry_add_action_flag_choices','2026-06-25 18:37:20.049260'),(19,'products','0001_initial','2026-06-25 18:37:20.345833'),(20,'cart','0001_initial','2026-06-25 18:37:20.498255'),(21,'cart','0002_initial','2026-06-25 18:37:20.637096'),(22,'categories','0001_initial','2026-06-25 18:37:20.775063'),(23,'orders_mgmt','0001_initial','2026-06-25 18:37:20.914911'),(26,'inventory','0001_initial','2026-06-25 18:37:21.101977'),(27,'inventory','0002_initial','2026-06-25 18:37:21.188003'),(28,'inventory','0003_initial','2026-06-25 18:37:21.366268'),(29,'orders_mgmt','0002_initial','2026-06-25 18:37:21.484127'),(30,'orders_mgmt','0003_initial','2026-06-25 18:37:21.574970'),(32,'producers','0001_initial','2026-06-25 18:37:21.824148'),(33,'producers','0002_initial','2026-06-25 18:37:22.018746'),(34,'products','0002_initial','2026-06-25 18:37:22.344639'),(35,'reports','0001_initial','2026-06-25 18:37:22.608488'),(36,'sessions','0001_initial','2026-06-25 18:37:22.657035'),(37,'stores','0001_initial','2026-06-25 18:37:22.799442'),(38,'support','0001_initial','2026-06-25 18:37:22.941968'),(39,'support','0002_initial','2026-06-25 18:37:23.308950'),(41,'users','0001_initial','2026-06-27 11:43:18.730888'),(47,'users','0002_remove_product_image_remove_product_is_organic_and_more','2026-06-27 11:54:58.115209'),(48,'cart','0003_alter_cartitem_product','2026-06-27 14:21:28.055571'),(49,'chat','0001_initial','2026-06-27 14:21:28.236619'),(50,'chat','0002_initial','2026-06-27 14:21:28.368034'),(51,'inventory','0004_alter_inventorylog_product_alter_stockalert_product','2026-06-27 14:21:28.902780'),(52,'products','0003_producerprofile_remove_productapproval_product_and_more','2026-06-27 17:51:11.725863'),(53,'products','0004_delete_producerprofile_producerprofile','2026-06-27 17:51:26.631665'),(54,'stores','0002_alter_store_options_remove_store_delivery_fee_and_more','2026-06-27 17:52:07.342650'),(55,'orders','0001_initial','2026-06-27 17:52:08.176824'),(56,'deliveries','0001_initial','2026-06-27 17:56:05.816163'),(57,'deliveries','0002_initial','2026-06-27 17:56:20.775972'),(58,'notifications','0001_initial','2026-06-27 17:56:27.399185'),(59,'notifications','0002_initial','2026-06-27 17:56:27.511029'),(60,'payments','0001_initial','2026-06-27 17:56:33.858831'),(61,'payments','0002_remove_payment_currency_remove_payment_error_message_and_more','2026-06-27 17:56:41.449758'),(63,'reports','0002_alter_commissionreport_producer_and_more','2026-06-27 17:58:47.499761'),(64,'producers','0003_alter_producercertification_options_and_more','2026-06-27 17:59:04.926918'),(65,'reviews','0001_initial','2026-06-29 16:45:00.614800'),(66,'reviews','0002_alter_review_options_review_is_approved_and_more','2026-06-29 16:45:00.883003');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
INSERT INTO `django_session` VALUES ('iea3f9sbq7jmgirrtv0jkfnycr1lfmfc','.eJxVi0sKwjAQQO-StQRnUpOJOwXPEWaSCSl-KMauxLvbQhe6fZ-3STy_Wpq7PtNYzNHAYHa_UDhf9bEanqZuV9btBru93Hm8nZb4vGV_b-PeltFlrJ5iOZDjXIYAwkEQgyeEjFkBPagg-bg4B2EftRZyhKLVOxHz-QLBxDXW:1wfLS1:n-KpZ-8aDOy4hGMMuy6y1rxyUP6JfC1ipVzeiQ_f01w','2026-07-16 17:43:49.743256'),('la4vrf8x1agkvrfldtyvu1aysno1a9f9','e30:1wdV8D:ofy5WehHBb_TxXjGkbEc0BX9Pl2wPk15saeYWFVv9io','2026-07-11 15:39:45.718255'),('ssc7f12zwrjaugv3jnvxgd1y3wlgc2nj','.eJxVjM0KwjAQhN8lZylt89f2puBzhM1mQ4JaQ9eCIr67KfSgx_nmm3kLB-sjuZVpcTmISRhx-GUe8ELzVkAp3GyMmx1yc75Bvh6rfNq1v20CTnXYmzgE71UEQqVbrRVYlNKgsoQDjl0gaTUEOcbaht5j2-lxMMZEr2raTpmY83129Cx5eYmp_XwBUSE9pA:1weBE4:rksQjEQq8MoasJuUmh_5fO1xtEMmDnA1Rw2w-lg-m7g','2026-07-13 12:36:36.134422'),('xfi6sksqdqpnyu3q5r1u8kyjrqxjvn6x','.eJxVjEEOgjAQRe_StSGlQ2vLThLP0Uw7Q2hUJIwkGuPdhYSFbt9_779VxOUxxEV4joVUq2pQh1-YMF943BacJqk2JtUOpTrfsFxPq9zt2l87oAxrqHtvLEGtXXYJMJMP2oV09M7WhliDS85Qsg145mwpNV5DQENge82h306FRcp9jPycyvxSrf58AUI7PT8:1weG6W:6hZW-EYs8sxJt_cr8BlqbH5HZfiponRDElOAbpmKDpU','2026-07-13 17:49:08.878941');
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
  `product_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_inventoryl_created_by_id_8d5d00f5_fk_users_aut` (`created_by_id`),
  KEY `inventory_inventorylog_product_id_eba27e8c_fk_users_product_id` (`product_id`),
  CONSTRAINT `inventory_inventoryl_created_by_id_8d5d00f5_fk_users_aut` FOREIGN KEY (`created_by_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `inventory_inventorylog_product_id_eba27e8c_fk_users_product_id` FOREIGN KEY (`product_id`) REFERENCES `users_product` (`id`)
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
  `product_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_stockalert_product_id_11f4588d_fk_users_product_id` (`product_id`),
  CONSTRAINT `inventory_stockalert_product_id_11f4588d_fk_users_product_id` FOREIGN KEY (`product_id`) REFERENCES `users_product` (`id`),
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
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `read` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_notifi_user_id_b5e8c0ff_fk_users_aut` (`user_id`),
  CONSTRAINT `notifications_notifi_user_id_b5e8c0ff_fk_users_aut` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_notification`
--

LOCK TABLES `notifications_notification` WRITE;
/*!40000 ALTER TABLE `notifications_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications_notification` ENABLE KEYS */;
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
-- Table structure for table `orders_order`
--

DROP TABLE IF EXISTS `orders_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_order` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_street` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_district` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `delivery_fee` decimal(8,2) NOT NULL,
  `discount` decimal(8,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `confirmed_at` datetime(6) DEFAULT NULL,
  `shipped_at` datetime(6) DEFAULT NULL,
  `delivered_at` datetime(6) DEFAULT NULL,
  `cancelled_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `customer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference` (`reference`),
  KEY `orders_order_customer_id_0b76f6a4_fk_users_auth_user_id` (`customer_id`),
  CONSTRAINT `orders_order_customer_id_0b76f6a4_fk_users_auth_user_id` FOREIGN KEY (`customer_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order`
--

LOCK TABLES `orders_order` WRITE;
/*!40000 ALTER TABLE `orders_order` DISABLE KEYS */;
INSERT INTO `orders_order` VALUES ('ae2f31ab367f4883bb6f41f6708a5594','COVAT573R4','Karla Blanco','56756465','ddddddddddddd','N/D','N/D','Portugal',1.00,5.00,0.00,6.06,'pending','','',NULL,NULL,NULL,NULL,'2026-06-29 17:51:43.920026','2026-06-29 17:51:43.920026',13);
/*!40000 ALTER TABLE `orders_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderitem`
--

DROP TABLE IF EXISTS `orders_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_unit` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `quantity` decimal(8,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `order_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `store_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` (`order_id`),
  KEY `orders_orderitem_product_id_afe4254a_fk_users_product_id` (`product_id`),
  KEY `orders_orderitem_store_id_060d1281_fk_stores_store_id` (`store_id`),
  CONSTRAINT `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_orderitem_product_id_afe4254a_fk_users_product_id` FOREIGN KEY (`product_id`) REFERENCES `users_product` (`id`),
  CONSTRAINT `orders_orderitem_store_id_060d1281_fk_stores_store_id` FOREIGN KEY (`store_id`) REFERENCES `stores_store` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderitem`
--

LOCK TABLES `orders_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_orderitem` DISABLE KEYS */;
INSERT INTO `orders_orderitem` VALUES (1,'Abacate','caixa',1.00,1.00,1.00,'ae2f31ab367f4883bb6f41f6708a5594','b5050d403728431996bc6343d798e536','02c43850cc2f42e4a93dd66f67a915a3');
/*!40000 ALTER TABLE `orders_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_sellerorder`
--

DROP TABLE IF EXISTS `orders_sellerorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_sellerorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `commission_rate` decimal(5,2) NOT NULL,
  `commission_amount` decimal(10,2) NOT NULL,
  `payout_amount` decimal(12,2) NOT NULL,
  `rejection_reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `accepted_at` datetime(6) DEFAULT NULL,
  `rejected_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `store_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_sellerorder_order_id_993ac2f3_fk_orders_order_id` (`order_id`),
  KEY `orders_sellerorder_store_id_100744ad_fk_stores_store_id` (`store_id`),
  CONSTRAINT `orders_sellerorder_order_id_993ac2f3_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_sellerorder_store_id_100744ad_fk_stores_store_id` FOREIGN KEY (`store_id`) REFERENCES `stores_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_sellerorder`
--

LOCK TABLES `orders_sellerorder` WRITE;
/*!40000 ALTER TABLE `orders_sellerorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_sellerorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_payment`
--

DROP TABLE IF EXISTS `payments_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_payment` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_test_payment` tinyint(1) NOT NULL,
  `reference` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `paid_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  `cancelled_at` datetime(6) DEFAULT NULL,
  `customer_id` bigint DEFAULT NULL,
  `failed_at` datetime(6) DEFAULT NULL,
  `failure_reason` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `method` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb4''),
  `refunded_at` datetime(6) DEFAULT NULL,
  `test_approved_at` datetime(6) DEFAULT NULL,
  `test_password_used` tinyint(1) NOT NULL,
  `test_signature_used` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payments_payment_reference_1d502039_uniq` (`reference`),
  KEY `payments_payment_order_id_22c479b7_fk_orders_mgmt_order_id` (`order_id`),
  KEY `payments_payment_customer_id_8b4d6141_fk_users_auth_user_id` (`customer_id`),
  CONSTRAINT `payments_payment_customer_id_8b4d6141_fk_users_auth_user_id` FOREIGN KEY (`customer_id`) REFERENCES `users_auth_user` (`id`),
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
-- Table structure for table `payments_producerpayout`
--

DROP TABLE IF EXISTS `payments_producerpayout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_producerpayout` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `commission_deducted` decimal(10,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_test` tinyint(1) NOT NULL,
  `paid_at` datetime(6) DEFAULT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `seller_order_id` bigint NOT NULL,
  `store_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_producerpay_seller_order_id_5de1b8e2_fk_orders_se` (`seller_order_id`),
  KEY `payments_producerpayout_store_id_474f5b8f_fk_stores_store_id` (`store_id`),
  CONSTRAINT `payments_producerpay_seller_order_id_5de1b8e2_fk_orders_se` FOREIGN KEY (`seller_order_id`) REFERENCES `orders_sellerorder` (`id`),
  CONSTRAINT `payments_producerpayout_store_id_474f5b8f_fk_stores_store_id` FOREIGN KEY (`store_id`) REFERENCES `stores_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_producerpayout`
--

LOCK TABLES `payments_producerpayout` WRITE;
/*!40000 ALTER TABLE `payments_producerpayout` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_producerpayout` ENABLE KEYS */;
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
  `producer_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `producers_producerce_producer_id_6fd18ee6_fk_users_pro` (`producer_id`),
  CONSTRAINT `producers_producerce_producer_id_6fd18ee6_fk_users_pro` FOREIGN KEY (`producer_id`) REFERENCES `users_producer` (`id`)
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
-- Table structure for table `products_producerprofile`
--

DROP TABLE IF EXISTS `products_producerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_producerprofile` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `producer_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nif` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `banner` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `farm_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `farm_address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `district` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `county` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parish` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `postal_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `website` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bank_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bank_account` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bank_owner` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `rejection_reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `rejected_at` datetime(6) DEFAULT NULL,
  `custom_commission` decimal(5,2) DEFAULT NULL,
  `total_sales` decimal(12,2) NOT NULL,
  `total_orders` int unsigned NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `total_reviews` int unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `rejected_by_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `products_producerprofile_chk_1` CHECK ((`total_orders` >= 0)),
  CONSTRAINT `products_producerprofile_chk_2` CHECK ((`total_reviews` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_producerprofile`
--

LOCK TABLES `products_producerprofile` WRITE;
/*!40000 ALTER TABLE `products_producerprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_producerprofile` ENABLE KEYS */;
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
  PRIMARY KEY (`id`)
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
  PRIMARY KEY (`id`)
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
-- Table structure for table `reviews_review`
--

DROP TABLE IF EXISTS `reviews_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `producer_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reviews_review_producer_id_aa06f3e6_fk_users_producer_id` (`producer_id`),
  KEY `reviews_review_product_id_ce2fa4c6_fk_users_product_id` (`product_id`),
  KEY `reviews_review_user_id_875caff2_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `reviews_review_producer_id_aa06f3e6_fk_users_producer_id` FOREIGN KEY (`producer_id`) REFERENCES `users_producer` (`id`),
  CONSTRAINT `reviews_review_product_id_ce2fa4c6_fk_users_product_id` FOREIGN KEY (`product_id`) REFERENCES `users_product` (`id`),
  CONSTRAINT `reviews_review_user_id_875caff2_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `review_product_or_producer_only` CHECK ((((`producer_id` is null) and (`product_id` is not null)) or ((`producer_id` is not null) and (`product_id` is null))))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_review`
--

LOCK TABLES `reviews_review` WRITE;
/*!40000 ALTER TABLE `reviews_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stores_store`
--

DROP TABLE IF EXISTS `stores_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stores_store` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(220) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `banner` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `min_order_value` decimal(10,2) NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `producer_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `accepts_returns` tinyint(1) NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb4''),
  `approved_at` datetime(6) DEFAULT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `commission_rate` decimal(5,2) NOT NULL,
  `county` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `delivery_time_days` smallint unsigned NOT NULL,
  `district` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `owner_id` bigint DEFAULT NULL,
  `parish` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `return_policy` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb4''),
  `review_count` int unsigned NOT NULL,
  `tagline` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_orders` int unsigned NOT NULL,
  `total_products` int unsigned NOT NULL,
  `total_sales` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `stores_store_approved_by_id_c0b58b41_fk_users_auth_user_id` (`approved_by_id`),
  KEY `stores_store_owner_id_2ba58adb_fk_users_auth_user_id` (`owner_id`),
  KEY `stores_store_producer_id_f9d755b1` (`producer_id`),
  CONSTRAINT `stores_store_approved_by_id_c0b58b41_fk_users_auth_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `stores_store_owner_id_2ba58adb_fk_users_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `stores_store_producer_id_f9d755b1_fk_users_producer_id` FOREIGN KEY (`producer_id`) REFERENCES `users_producer` (`id`),
  CONSTRAINT `stores_store_chk_1` CHECK ((`delivery_time_days` >= 0)),
  CONSTRAINT `stores_store_chk_2` CHECK ((`review_count` >= 0)),
  CONSTRAINT `stores_store_chk_3` CHECK ((`total_orders` >= 0)),
  CONSTRAINT `stores_store_chk_4` CHECK ((`total_products` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stores_store`
--

LOCK TABLES `stores_store` WRITE;
/*!40000 ALTER TABLE `stores_store` DISABLE KEYS */;
INSERT INTO `stores_store` VALUES ('02c43850cc2f42e4a93dd66f67a915a3','QUINTA P1','quinta-p1','LOJA','','','pending',0.00,0.00,'2026-06-29 17:02:08.273938','2026-06-29 17:02:08.273938','3828838994544c80b67d19bd83739c09',1,'',NULL,NULL,8.00,'',NULL,3,'','produtor1@coverde.pt',1,0,12,'','453654345','',0,'',0,0,0.00);
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
-- Table structure for table `users_accountactivationtoken`
--

DROP TABLE IF EXISTS `users_accountactivationtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_accountactivationtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `users_accountactivat_user_id_44dee096_fk_users_aut` (`user_id`),
  CONSTRAINT `users_accountactivat_user_id_44dee096_fk_users_aut` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_accountactivationtoken`
--

LOCK TABLES `users_accountactivationtoken` WRITE;
/*!40000 ALTER TABLE `users_accountactivationtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_accountactivationtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_address`
--

DROP TABLE IF EXISTS `users_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_address` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `label` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `street` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `district` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `postal_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_address_user_id_4c106ba4_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `users_address_user_id_4c106ba4_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_address`
--

LOCK TABLES `users_address` WRITE;
/*!40000 ALTER TABLE `users_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_address` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_auth_user`
--

LOCK TABLES `users_auth_user` WRITE;
/*!40000 ALTER TABLE `users_auth_user` DISABLE KEYS */;
INSERT INTO `users_auth_user` VALUES (1,'pbkdf2_sha256$600000$0FFb9jEVO3x2DWyTFfOvca$gmyQcYgG6nooXDP4BDTauf2myN8CI+56OvXF8EuH6M0=',NULL,1,'admin@teste.com','','','admin@teste.com',1,1,'2026-06-25 18:37:32.250844','admin',NULL,'',1,'2026-06-27 18:40:58.952003',NULL,NULL,0,NULL,NULL,NULL,4,NULL,NULL,0),(2,'pbkdf2_sha256$600000$7dkRj8vDKV7dAFAJPNMLSK$OncRmR5pm+LtLUBzuiT+UKxCw9JN0kxRPV5AxGF4uGE=',NULL,1,'admin@test.pt','','','admin@test.pt',1,1,'2026-06-27 18:01:20.872006','admin',NULL,'',1,'2026-06-27 18:40:58.952482',NULL,NULL,0,NULL,NULL,NULL,0,NULL,NULL,0),(6,'pbkdf2_sha256$600000$OUnX0nsgKPKbyV78g4zRKb$Hc3DFXaXF/loaUnoYhd55R27LKE3QEV++xen5g1ZQ30=','2026-06-29 12:36:36.132061',0,'joao.silva.produtor@teste.com','João','Silva','joao.silva.produtor@teste.com',0,1,'2026-06-27 20:04:56.483690','producer','+351912346001','',1,'2026-06-27 20:04:56.483690','2026-06-27 20:04:56.483690','2026-06-27 20:04:56.483690',0,NULL,NULL,NULL,0,NULL,'127.0.0.1',0),(7,'pbkdf2_sha256$600000$46AtNMrwlf5gviRByPE3lE$t/ZGV/FPYGXny0Kjl4Eenagdbe53AUcg3WEx/Yn3Qoo=',NULL,0,'maria.santos.produtora@teste.com','Maria','Santos','maria.santos.produtora@teste.com',0,1,'2026-06-27 20:04:56.735807','producer','+351912346002','',1,'2026-06-27 20:04:56.740197','2026-06-27 20:04:56.740197','2026-06-27 20:04:56.740197',0,NULL,NULL,NULL,0,NULL,NULL,0),(8,'pbkdf2_sha256$600000$tlzZI7ierZ00vLH9xFpwxt$FztyP3LcqSpNHFtIcLibRmx8oJnx3cA5Td/X6GaxJ+4=',NULL,0,'antonio.costa.produtor@teste.com','António','Costa','antonio.costa.produtor@teste.com',0,1,'2026-06-27 20:04:57.027092','producer','+351912346003','',1,'2026-06-27 20:04:57.032099','2026-06-27 20:04:57.032099','2026-06-27 20:04:57.032099',0,NULL,NULL,NULL,0,NULL,NULL,0),(9,'pbkdf2_sha256$600000$rnkxFqh2m4uI3FVpauFYsv$AAllShjWTzysQIIwOBxkjlzxknYmD2EM8wobcD8whe0=',NULL,0,'ana.ferreira.produtora@teste.com','Ana','Ferreira','ana.ferreira.produtora@teste.com',0,1,'2026-06-27 20:04:57.309549','producer','+351912346004','',1,'2026-06-27 20:04:57.315596','2026-06-27 20:04:57.315596','2026-06-27 20:04:57.315596',0,NULL,NULL,NULL,0,NULL,NULL,0),(10,'pbkdf2_sha256$600000$2koizFDVt8IpsKQS7PBUBY$VpRR+T7LEmsS0mvg3C8PE2pqm4g8WcmVxh2e01QN7mo=',NULL,0,'miguel.pereira.produtor@teste.com','Miguel','Pereira','miguel.pereira.produtor@teste.com',0,1,'2026-06-27 20:04:57.620269','producer','+351912346005','',1,'2026-06-27 20:04:57.627166','2026-06-27 20:04:57.627166','2026-06-27 20:04:57.627166',0,NULL,NULL,NULL,0,NULL,NULL,0),(11,'pbkdf2_sha256$600000$wCLbogBxV8oTkWHLJ9Dpwg$W4m8ZNgEad+s4nzO8ZxDq2RrEXn8bpiUX3fhNx4s9x4=','2026-06-29 17:48:21.033864',1,'aadmin','','','aadmin@coverde.pt',1,1,'2026-06-29 16:55:25.258766','consumer',NULL,'',0,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,'127.0.0.1',0),(12,'pbkdf2_sha256$600000$mtiEOBFx1sMnPdgrOuYfGl$vHAZjXV+s8WwuunSfPPU6bqPDZQTKxJwqpp+BDh4jeU=','2026-06-29 17:46:38.865455',0,'produtor1@coverde.pt','produtor1','AAAAAAAAA','produtor1@coverde.pt',0,1,'2026-06-29 17:02:07.508336','producer','453654345','',1,'2026-06-29 17:02:08.253010','2026-06-29 17:02:08.225674','2026-06-29 17:02:08.225674',0,NULL,NULL,NULL,0,NULL,'127.0.0.1',0),(13,'pbkdf2_sha256$600000$5Nd4dnstHnxoaPNKzkYtyH$S23fikhUmLLU6Jon3uVzecesHFr9boa+dTOm7QGm1y8=','2026-06-29 17:49:08.872832',0,'kayo@blanco.pt','Karla','Blanco','kayo@blanco.pt',0,1,'2026-06-29 17:22:49.223381','consumer','56756465','',1,'2026-06-29 17:22:49.739039','2026-06-29 17:22:49.726627','2026-06-29 17:22:49.726627',0,NULL,NULL,NULL,0,NULL,'127.0.0.1',0),(14,'pbkdf2_sha256$600000$HrtsWDWZdIpsOPYkuY4g66$L1vLUoyeaNTXHnVmztbb3MX1r9AKalhJpgbSdS5jCfg=','2026-07-02 17:43:49.735110',1,'admin_smoke','','','admin.smoke@example.com',1,1,'2026-07-02 17:43:49.185926','consumer',NULL,'',0,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,NULL,0);
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

--
-- Table structure for table `users_category`
--

DROP TABLE IF EXISTS `users_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_category` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `ordering` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `users_category_parent_id_7ed3fb68_fk_users_category_id` (`parent_id`),
  CONSTRAINT `users_category_parent_id_7ed3fb68_fk_users_category_id` FOREIGN KEY (`parent_id`) REFERENCES `users_category` (`id`),
  CONSTRAINT `users_category_chk_1` CHECK ((`ordering` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_category`
--

LOCK TABLES `users_category` WRITE;
/*!40000 ALTER TABLE `users_category` DISABLE KEYS */;
INSERT INTO `users_category` VALUES ('9ad2f136dd574c7c8c363113f323ce07','FRUTAS','frutas','','','',1,0,'2026-06-29 17:07:54.083012','2026-06-29 17:07:54.083012',NULL);
/*!40000 ALTER TABLE `users_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customerprofile`
--

DROP TABLE IF EXISTS `users_customerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_customerprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `newsletter_subscribed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `users_customerprofile_user_id_c320f1e5_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customerprofile`
--

LOCK TABLES `users_customerprofile` WRITE;
/*!40000 ALTER TABLE `users_customerprofile` DISABLE KEYS */;
INSERT INTO `users_customerprofile` VALUES (1,NULL,'',1,'2026-06-29 17:22:49.740942','2026-06-29 17:22:49.740942',13);
/*!40000 ALTER TABLE `users_customerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_notification`
--

DROP TABLE IF EXISTS `users_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notif_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_notification_user_id_fed360c8_fk_users_auth_user_id` (`user_id`),
  CONSTRAINT `users_notification_user_id_fed360c8_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_notification`
--

LOCK TABLES `users_notification` WRITE;
/*!40000 ALTER TABLE `users_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_producer`
--

DROP TABLE IF EXISTS `users_producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_producer` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
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
  `total_ratings` int unsigned NOT NULL,
  `total_products` int unsigned NOT NULL,
  `total_sales` decimal(12,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `verified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `users_producer_verified_by_id_1deba7d4_fk_users_auth_user_id` (`verified_by_id`),
  CONSTRAINT `users_producer_user_id_4ac9d565_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `users_producer_verified_by_id_1deba7d4_fk_users_auth_user_id` FOREIGN KEY (`verified_by_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `users_producer_chk_1` CHECK ((`total_ratings` >= 0)),
  CONSTRAINT `users_producer_chk_2` CHECK ((`total_products` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_producer`
--

LOCK TABLES `users_producer` WRITE;
/*!40000 ALTER TABLE `users_producer` DISABLE KEYS */;
INSERT INTO `users_producer` VALUES ('3828838994544c80b67d19bd83739c09','QUINTA P1','LOJA','COIMBRA','564764532','producers/verification/atividade-4_1.pdf','approved',1,NULL,'',0.00,0,0,0.00,1,'2026-06-29 17:02:08.260456','2026-06-29 17:03:29.743935',NULL,12,11);
/*!40000 ALTER TABLE `users_producer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_product`
--

DROP TABLE IF EXISTS `users_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_product` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int unsigned NOT NULL,
  `unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `certification` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `total_reviews` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `producer_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `extra_images` json NOT NULL DEFAULT (_utf8mb4'[]'),
  `main_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_sold` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `users_produ_status_4fcfe3_idx` (`status`),
  KEY `users_produ_produce_30430c_idx` (`producer_id`),
  KEY `users_produ_categor_fdd57d_idx` (`category_id`),
  CONSTRAINT `users_product_category_id_e6940bc9_fk_users_category_id` FOREIGN KEY (`category_id`) REFERENCES `users_category` (`id`),
  CONSTRAINT `users_product_producer_id_6e10d53c_fk_users_producer_id` FOREIGN KEY (`producer_id`) REFERENCES `users_producer` (`id`),
  CONSTRAINT `users_product_chk_1` CHECK ((`stock` >= 0)),
  CONSTRAINT `users_product_chk_2` CHECK ((`total_reviews` >= 0)),
  CONSTRAINT `users_product_chk_3` CHECK ((`total_sold` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_product`
--

LOCK TABLES `users_product` WRITE;
/*!40000 ALTER TABLE `users_product` DISABLE KEYS */;
INSERT INTO `users_product` VALUES ('1c8bf30ad686463db5f8b5fadb5ef3fd','ccccccc','ccccccc','cccccccccccc',4.00,6,'kg','integrada','active',0,1,0.00,0,'2026-06-29 17:47:59.381759','2026-06-29 17:47:59.383812','9ad2f136dd574c7c8c363113f323ce07','3828838994544c80b67d19bd83739c09','[]','products/Ananás_nywNIQ6.webp',0),('b5050d403728431996bc6343d798e536','Abacate','abacate','frutassss',1.00,3,'caixa','','active',0,1,0.00,0,'2026-06-29 17:20:19.867093','2026-06-29 17:20:19.867093','9ad2f136dd574c7c8c363113f323ce07','3828838994544c80b67d19bd83739c09','[]','products/Abacate_Xw26rVO.webp',0);
/*!40000 ALTER TABLE `users_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_supplierprofile`
--

DROP TABLE IF EXISTS `users_supplierprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_supplierprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nif` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `users_supplierprofil_approved_by_id_c332bf8d_fk_users_aut` (`approved_by_id`),
  CONSTRAINT `users_supplierprofil_approved_by_id_c332bf8d_fk_users_aut` FOREIGN KEY (`approved_by_id`) REFERENCES `users_auth_user` (`id`),
  CONSTRAINT `users_supplierprofile_user_id_5a230cd1_fk_users_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_supplierprofile`
--

LOCK TABLES `users_supplierprofile` WRITE;
/*!40000 ALTER TABLE `users_supplierprofile` DISABLE KEYS */;
INSERT INTO `users_supplierprofile` VALUES (1,'QUINTA P1','564764532','LOJA','','453654345','produtor1@coverde.pt','','approved',NULL,'2026-06-29 17:02:08.261435','2026-06-29 17:18:16.030049',11,12);
/*!40000 ALTER TABLE `users_supplierprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'coverde_db'
--

--
-- Dumping routines for database 'coverde_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-02 21:05:40
