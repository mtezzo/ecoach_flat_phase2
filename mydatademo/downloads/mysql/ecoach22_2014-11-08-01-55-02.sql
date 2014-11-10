-- MySQL dump 10.13  Distrib 5.6.21, for osx10.9 (x86_64)
--
-- Host: localhost    Database: ecoach22
-- ------------------------------------------------------
-- Server version	5.6.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add migration history',9,'add_migrationhistory'),(26,'Can change migration history',9,'change_migrationhistory'),(27,'Can delete migration history',9,'delete_migrationhistory'),(28,'Can add source1',10,'add_source1'),(29,'Can change source1',10,'change_source1'),(30,'Can delete source1',10,'delete_source1'),(31,'Can add empty source',11,'add_emptysource'),(32,'Can change empty source',11,'change_emptysource'),(33,'Can delete empty source',11,'delete_emptysource'),(34,'Can add user profile',12,'add_userprofile'),(35,'Can change user profile',12,'change_userprofile'),(36,'Can delete user profile',12,'delete_userprofile'),(37,'Can add copycat',13,'add_copycat'),(38,'Can change copycat',13,'change_copycat'),(39,'Can delete copycat',13,'delete_copycat'),(40,'Can add copycat_ column',14,'add_copycat_column'),(41,'Can change copycat_ column',14,'change_copycat_column'),(42,'Can delete copycat_ column',14,'delete_copycat_column'),(43,'Can add bc c_ query',15,'add_bcc_query'),(44,'Can change bc c_ query',15,'change_bcc_query'),(45,'Can delete bc c_ query',15,'delete_bcc_query'),(46,'Can add message',16,'add_message'),(47,'Can change message',16,'change_message'),(48,'Can delete message',16,'delete_message'),(49,'Can add csv data file',17,'add_csvdatafile'),(50,'Can change csv data file',17,'change_csvdatafile'),(51,'Can delete csv data file',17,'delete_csvdatafile'),(52,'Can add csv map file',18,'add_csvmapfile'),(53,'Can change csv map file',18,'change_csvmapfile'),(54,'Can delete csv map file',18,'delete_csvmapfile'),(55,'Can add digestion',19,'add_digestion'),(56,'Can change digestion',19,'change_digestion'),(57,'Can delete digestion',19,'delete_digestion'),(58,'Can add digestion_ column',20,'add_digestion_column'),(59,'Can change digestion_ column',20,'change_digestion_column'),(60,'Can delete digestion_ column',20,'delete_digestion_column'),(61,'Can add download',21,'add_download'),(62,'Can change download',21,'change_download'),(63,'Can delete download',21,'delete_download'),(64,'Can add download_ column',22,'add_download_column'),(65,'Can change download_ column',22,'change_download_column'),(66,'Can delete download_ column',22,'delete_download_column'),(67,'Can add e log',23,'add_elog'),(68,'Can change e log',23,'change_elog'),(69,'Can delete e log',23,'delete_elog'),(70,'Can add serialized subject data',24,'add_serializedsubjectdata'),(71,'Can change serialized subject data',24,'change_serializedsubjectdata'),(72,'Can delete serialized subject data',24,'delete_serializedsubjectdata'),(73,'Can add survey state',25,'add_surveystate'),(74,'Can change survey state',25,'change_surveystate'),(75,'Can delete survey state',25,'delete_surveystate'),(76,'Can add event',26,'add_event'),(77,'Can change event',26,'change_event'),(78,'Can delete event',26,'delete_event');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'ezzomich','Michael','Ezzo','ezzomich@msu.edu','sha1$ad4be$cf1c141372fc6725ec91e30d8a0d1637da5259d7',1,1,1,'2014-11-08 01:50:49','2014-11-07 21:37:45');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'log entry','admin','logentry'),(9,'migration history','south','migrationhistory'),(10,'source1','mydata22','source1'),(11,'empty source','mydata22','emptysource'),(12,'user profile','mytailoring','userprofile'),(13,'copycat','mypublisher','copycat'),(14,'copycat_ column','mypublisher','copycat_column'),(15,'bc c_ query','myemailer','bcc_query'),(16,'message','myemailer','message'),(17,'csv data file','myloader','csvdatafile'),(18,'csv map file','myloader','csvmapfile'),(19,'digestion','myloader','digestion'),(20,'digestion_ column','myloader','digestion_column'),(21,'download','myexporter','download'),(22,'download_ column','myexporter','download_column'),(23,'e log','mylogger','elog'),(24,'serialized subject data','djangotailoring','serializedsubjectdata'),(25,'survey state','surveys','surveystate'),(26,'event','tracking','event');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('48c145a02f2aa7a8afa9aa29045cc269','YmI1ODI1ODQ0ZDYwODAxNTk2NTFiODAzNWJmNDU5ZjViMmE1ODM0YjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSRteXRhaWxvcmluZy5iYWNrZW5kcy5TZXR0aW5nc0JhY2tlbmRxA1UNX2F1\ndGhfdXNlcl9pZHEEigEBdS4=\n','2014-11-22 01:50:49'),('7b2939e36cfd954585053f2c90cea53e','YmI1ODI1ODQ0ZDYwODAxNTk2NTFiODAzNWJmNDU5ZjViMmE1ODM0YjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSRteXRhaWxvcmluZy5iYWNrZW5kcy5TZXR0aW5nc0JhY2tlbmRxA1UNX2F1\ndGhfdXNlcl9pZHEEigEBdS4=\n','2014-11-21 21:38:43'),('91cddce12fad174e14b869d9ab4c979f','YmI1ODI1ODQ0ZDYwODAxNTk2NTFiODAzNWJmNDU5ZjViMmE1ODM0YjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSRteXRhaWxvcmluZy5iYWNrZW5kcy5TZXR0aW5nc0JhY2tlbmRxA1UNX2F1\ndGhfdXNlcl9pZHEEigEBdS4=\n','2014-11-22 01:09:25');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djangotailoring_serializedsubjectdata`
--

DROP TABLE IF EXISTS `djangotailoring_serializedsubjectdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djangotailoring_serializedsubjectdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) NOT NULL,
  `primary_data` longtext NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djangotailoring_serializedsubjectdata`
--

LOCK TABLES `djangotailoring_serializedsubjectdata` WRITE;
/*!40000 ALTER TABLE `djangotailoring_serializedsubjectdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `djangotailoring_serializedsubjectdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mydata22_emptysource`
--

DROP TABLE IF EXISTS `mydata22_emptysource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mydata22_emptysource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) DEFAULT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mydata22_emptysource_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_username_c4a6eb2d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mydata22_emptysource`
--

LOCK TABLES `mydata22_emptysource` WRITE;
/*!40000 ALTER TABLE `mydata22_emptysource` DISABLE KEYS */;
/*!40000 ALTER TABLE `mydata22_emptysource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mydata_source1`
--

DROP TABLE IF EXISTS `mydata_source1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mydata_source1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) DEFAULT NULL,
  `updated` datetime NOT NULL,
  `SLCENROLLED` varchar(3) DEFAULT NULL,
  `First_Name` varchar(20) DEFAULT NULL,
  `NetID` varchar(20) DEFAULT NULL,
  `Gender` varchar(1) DEFAULT NULL,
  `Last_Name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mydata_source1_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_username_f8bf72d1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mydata_source1`
--

LOCK TABLES `mydata_source1` WRITE;
/*!40000 ALTER TABLE `mydata_source1` DISABLE KEYS */;
INSERT INTO `mydata_source1` VALUES (1,'ezzomich','2014-11-08 01:51:27','Yes','Mike','ezzomich','M','Ezzo');
/*!40000 ALTER TABLE `mydata_source1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myemailer_bcc_query`
--

DROP TABLE IF EXISTS `myemailer_bcc_query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myemailer_bcc_query` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `sql` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myemailer_bcc_query`
--

LOCK TABLES `myemailer_bcc_query` WRITE;
/*!40000 ALTER TABLE `myemailer_bcc_query` DISABLE KEYS */;
/*!40000 ALTER TABLE `myemailer_bcc_query` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myemailer_message`
--

DROP TABLE IF EXISTS `myemailer_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myemailer_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) NOT NULL,
  `created` datetime DEFAULT NULL,
  `sender` varchar(200) NOT NULL,
  `to` varchar(200) NOT NULL,
  `bcc_query_id` int(11) NOT NULL,
  `bcc` longtext,
  `subject` varchar(200) NOT NULL,
  `body` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myemailer_message_fbfc09f1` (`user_id`),
  KEY `myemailer_message_d0b9de74` (`bcc_query_id`),
  CONSTRAINT `bcc_query_id_refs_id_66b8d1f7` FOREIGN KEY (`bcc_query_id`) REFERENCES `myemailer_bcc_query` (`id`),
  CONSTRAINT `user_id_refs_username_e74a24f2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myemailer_message`
--

LOCK TABLES `myemailer_message` WRITE;
/*!40000 ALTER TABLE `myemailer_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `myemailer_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myexporter_download`
--

DROP TABLE IF EXISTS `myexporter_download`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myexporter_download` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) NOT NULL,
  `table` varchar(30) DEFAULT NULL,
  `seperator` varchar(10) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `downloaded` tinyint(1) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `myexporter_download_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_username_1348d5dd` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myexporter_download`
--

LOCK TABLES `myexporter_download` WRITE;
/*!40000 ALTER TABLE `myexporter_download` DISABLE KEYS */;
INSERT INTO `myexporter_download` VALUES (1,'ezzomich','Source1',',','','1_.csv',1,'2014-11-08 01:54:40'),(2,'ezzomich',NULL,',','','',0,NULL);
/*!40000 ALTER TABLE `myexporter_download` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myexporter_download_column`
--

DROP TABLE IF EXISTS `myexporter_download_column`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myexporter_download_column` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `column_name` varchar(100) NOT NULL,
  `download_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myexporter_download_column_30b991ec` (`download_id`),
  CONSTRAINT `download_id_refs_id_79b91239` FOREIGN KEY (`download_id`) REFERENCES `myexporter_download` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myexporter_download_column`
--

LOCK TABLES `myexporter_download_column` WRITE;
/*!40000 ALTER TABLE `myexporter_download_column` DISABLE KEYS */;
INSERT INTO `myexporter_download_column` VALUES (1,'id',1),(2,'user_id',1),(3,'updated',1),(4,'SLCENROLLED',1),(5,'First_Name',1),(6,'NetID',1),(7,'Gender',1),(8,'Last_Name',1);
/*!40000 ALTER TABLE `myexporter_download_column` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myloader_csvdatafile`
--

DROP TABLE IF EXISTS `myloader_csvdatafile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myloader_csvdatafile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(260) NOT NULL,
  `name` varchar(260) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myloader_csvdatafile`
--

LOCK TABLES `myloader_csvdatafile` WRITE;
/*!40000 ALTER TABLE `myloader_csvdatafile` DISABLE KEYS */;
/*!40000 ALTER TABLE `myloader_csvdatafile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myloader_csvmapfile`
--

DROP TABLE IF EXISTS `myloader_csvmapfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myloader_csvmapfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(260) NOT NULL,
  `name` varchar(260) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myloader_csvmapfile`
--

LOCK TABLES `myloader_csvmapfile` WRITE;
/*!40000 ALTER TABLE `myloader_csvmapfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `myloader_csvmapfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myloader_digestion`
--

DROP TABLE IF EXISTS `myloader_digestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myloader_digestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) NOT NULL,
  `created` datetime DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `map_file_id` int(11) DEFAULT NULL,
  `data_file_id` int(11) DEFAULT NULL,
  `data_file_id_column` int(11) DEFAULT NULL,
  `function` int(11) DEFAULT NULL,
  `inserts` int(11) DEFAULT NULL,
  `overwrites` int(11) DEFAULT NULL,
  `mts_characteristic` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myloader_digestion_fbfc09f1` (`user_id`),
  KEY `myloader_digestion_cfbb1221` (`map_file_id`),
  KEY `myloader_digestion_231d4f10` (`data_file_id`),
  CONSTRAINT `data_file_id_refs_id_d7291975` FOREIGN KEY (`data_file_id`) REFERENCES `myloader_csvdatafile` (`id`),
  CONSTRAINT `map_file_id_refs_id_908688ba` FOREIGN KEY (`map_file_id`) REFERENCES `myloader_csvmapfile` (`id`),
  CONSTRAINT `user_id_refs_username_905bd2f6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myloader_digestion`
--

LOCK TABLES `myloader_digestion` WRITE;
/*!40000 ALTER TABLE `myloader_digestion` DISABLE KEYS */;
INSERT INTO `myloader_digestion` VALUES (1,'ezzomich',NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'');
/*!40000 ALTER TABLE `myloader_digestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myloader_digestion_column`
--

DROP TABLE IF EXISTS `myloader_digestion_column`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myloader_digestion_column` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `column_number` int(11) NOT NULL,
  `digestion_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myloader_digestion_column_8fc8b705` (`digestion_id`),
  CONSTRAINT `digestion_id_refs_id_c21aa651` FOREIGN KEY (`digestion_id`) REFERENCES `myloader_digestion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myloader_digestion_column`
--

LOCK TABLES `myloader_digestion_column` WRITE;
/*!40000 ALTER TABLE `myloader_digestion_column` DISABLE KEYS */;
/*!40000 ALTER TABLE `myloader_digestion_column` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mylogger_elog`
--

DROP TABLE IF EXISTS `mylogger_elog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mylogger_elog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `who` varchar(30) NOT NULL,
  `mwhen` datetime DEFAULT NULL,
  `url` longtext,
  `category` longtext,
  `action` longtext,
  `label` longtext,
  `value` int(11) DEFAULT NULL,
  `json` longtext,
  PRIMARY KEY (`id`),
  KEY `mylogger_elog_3419672c` (`who`),
  CONSTRAINT `who_refs_username_14876439` FOREIGN KEY (`who`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=178 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mylogger_elog`
--

LOCK TABLES `mylogger_elog` WRITE;
/*!40000 ALTER TABLE `mylogger_elog` DISABLE KEYS */;
INSERT INTO `mylogger_elog` VALUES (1,'ezzomich','2014-11-07 21:38:44','/coaches/','null','null','null',0,'{}'),(2,'ezzomich','2014-11-07 21:38:52','/coach22/message/home/','null','null','null',0,'{}'),(3,'ezzomich','2014-11-07 21:38:55','/coach22/message/Welcome/','null','null','null',0,'{}'),(4,'ezzomich','2014-11-07 21:38:57','/coach22/message/home/','null','null','null',0,'{}'),(5,'ezzomich','2014-11-07 21:38:58','/coach22/staff/','null','null','null',0,'{}'),(6,'ezzomich','2014-11-07 21:39:00','/coach22/publisher/copycat/','null','null','null',0,'{}'),(7,'ezzomich','2014-11-07 21:46:59','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(8,'ezzomich','2014-11-07 21:47:00','/coach22/messageframe/home/','null','null','null',0,'{}'),(9,'ezzomich','2014-11-07 21:47:03','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(10,'ezzomich','2014-11-07 21:47:03','/coach22/messageframe/home/','null','null','null',0,'{}'),(11,'ezzomich','2014-11-07 21:47:04','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(12,'ezzomich','2014-11-07 21:47:04','/coach22/messageframe/home/','null','null','null',0,'{}'),(13,'ezzomich','2014-11-07 21:47:05','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(14,'ezzomich','2014-11-07 21:47:06','/coach22/messageframe/home/','null','null','null',0,'{}'),(15,'ezzomich','2014-11-07 21:47:07','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(16,'ezzomich','2014-11-07 21:47:07','/coach22/messageframe/home/','null','null','null',0,'{}'),(17,'ezzomich','2014-11-07 21:47:08','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(18,'ezzomich','2014-11-07 21:47:08','/coach22/messageframe/home/','null','null','null',0,'{}'),(19,'ezzomich','2014-11-07 21:47:11','/coach22/publisher/copycat/','null','null','null',0,'{}'),(20,'ezzomich','2014-11-07 21:47:12','/coach22/publisher/run_checkout/','null','null','null',0,'{}'),(21,'ezzomich','2014-11-07 21:47:13','/coach22/publisher/copycat/','null','null','null',0,'{}'),(22,'ezzomich','2014-11-07 21:47:14','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(23,'ezzomich','2014-11-07 21:47:14','/coach22/messageframe/home/','null','null','null',0,'{}'),(24,'ezzomich','2014-11-07 21:47:15','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(25,'ezzomich','2014-11-07 21:47:15','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(26,'ezzomich','2014-11-07 21:47:16','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(27,'ezzomich','2014-11-07 21:47:16','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(28,'ezzomich','2014-11-07 21:47:18','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(29,'ezzomich','2014-11-07 21:47:18','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(30,'ezzomich','2014-11-07 21:47:19','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(31,'ezzomich','2014-11-07 21:47:19','/coach22/messageframe/home/','null','null','null',0,'{}'),(32,'ezzomich','2014-11-07 21:47:20','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(33,'ezzomich','2014-11-07 21:47:20','/coach22/messageframe/home/','null','null','null',0,'{}'),(34,'ezzomich','2014-11-07 21:47:21','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(35,'ezzomich','2014-11-07 21:47:21','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(36,'ezzomich','2014-11-07 21:47:22','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(37,'ezzomich','2014-11-07 21:47:22','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(38,'ezzomich','2014-11-07 21:52:59','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(39,'ezzomich','2014-11-07 21:53:00','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(40,'ezzomich','2014-11-07 21:53:03','/coach22/publisher/copycat/','null','null','null',0,'{}'),(41,'ezzomich','2014-11-07 21:53:04','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(42,'ezzomich','2014-11-07 21:53:04','/coach22/messageframe/home/','null','null','null',0,'{}'),(43,'ezzomich','2014-11-07 21:54:05','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(44,'ezzomich','2014-11-07 21:54:06','/coach22/messageframe/home/','null','null','null',0,'{}'),(45,'ezzomich','2014-11-07 21:54:08','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(46,'ezzomich','2014-11-07 21:54:08','/coach22/messageframe/home/','null','null','null',0,'{}'),(47,'ezzomich','2014-11-07 21:54:11','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(48,'ezzomich','2014-11-07 21:54:11','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(49,'ezzomich','2014-11-07 21:54:12','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(50,'ezzomich','2014-11-07 21:54:12','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(51,'ezzomich','2014-11-07 21:54:13','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(52,'ezzomich','2014-11-07 21:54:13','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(53,'ezzomich','2014-11-07 21:54:17','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(54,'ezzomich','2014-11-07 21:54:17','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(55,'ezzomich','2014-11-07 21:54:18','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(56,'ezzomich','2014-11-07 21:54:18','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(57,'ezzomich','2014-11-07 21:54:19','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(58,'ezzomich','2014-11-07 21:54:22','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(59,'ezzomich','2014-11-07 21:54:22','/coach22/messageframe/home/','null','null','null',0,'{}'),(60,'ezzomich','2014-11-07 21:54:23','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(61,'ezzomich','2014-11-07 21:54:23','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(62,'ezzomich','2014-11-07 21:56:41','/coach22/messageframe/home/','null','null','null',0,'{}'),(63,'ezzomich','2014-11-07 21:56:43','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(64,'ezzomich','2014-11-07 21:56:43','/coach22/messageframe/home/','null','null','null',0,'{}'),(65,'ezzomich','2014-11-07 21:57:11','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(66,'ezzomich','2014-11-07 21:57:11','/coach22/messageframe/home/','null','null','null',0,'{}'),(67,'ezzomich','2014-11-07 21:57:12','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(68,'ezzomich','2014-11-07 21:57:12','/coach22/messageframe/home/','null','null','null',0,'{}'),(69,'ezzomich','2014-11-07 21:59:23','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(70,'ezzomich','2014-11-07 21:59:23','/coach22/messageframe/home/','null','null','null',0,'{}'),(71,'ezzomich','2014-11-07 21:59:57','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(72,'ezzomich','2014-11-07 21:59:58','/coach22/messageframe/home/','null','null','null',0,'{}'),(73,'ezzomich','2014-11-07 22:20:20','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(74,'ezzomich','2014-11-07 22:20:20','/coach22/messageframe/home/','null','null','null',0,'{}'),(75,'ezzomich','2014-11-07 22:20:33','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(76,'ezzomich','2014-11-07 22:20:33','/coach22/messageframe/home/','null','null','null',0,'{}'),(77,'ezzomich','2014-11-07 22:20:37','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(78,'ezzomich','2014-11-07 22:20:37','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(79,'ezzomich','2014-11-07 22:20:39','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(80,'ezzomich','2014-11-07 22:20:39','/coach22/messageframe/home/','null','null','null',0,'{}'),(81,'ezzomich','2014-11-07 22:20:40','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(82,'ezzomich','2014-11-07 22:20:41','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(83,'ezzomich','2014-11-07 22:20:42','/coach22/publisher/copycat/','null','null','null',0,'{}'),(84,'ezzomich','2014-11-07 22:20:44','/coach22/publisher/run_checkout/','null','null','null',0,'{}'),(85,'ezzomich','2014-11-07 22:20:48','/coach22/message/home/','null','null','null',0,'{}'),(86,'ezzomich','2014-11-07 22:20:50','/coach22/message/Welcome/','null','null','null',0,'{}'),(87,'ezzomich','2014-11-07 22:20:51','/coach22/message/home/','null','null','null',0,'{}'),(88,'ezzomich','2014-11-07 22:20:52','/coach22/message/Welcome/','null','null','null',0,'{}'),(89,'ezzomich','2014-11-08 00:50:49','/coach22/message/home/','null','null','null',0,'{}'),(90,'ezzomich','2014-11-08 00:51:48','/coach22/message/home/','null','null','null',0,'{}'),(91,'ezzomich','2014-11-08 00:51:50','/coach22/message/home/','null','null','null',0,'{}'),(92,'ezzomich','2014-11-08 00:51:55','/coach22/message/home/','null','null','null',0,'{}'),(93,'ezzomich','2014-11-08 00:52:07','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(94,'ezzomich','2014-11-08 00:52:18','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(95,'ezzomich','2014-11-08 00:52:24','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(96,'ezzomich','2014-11-08 00:52:38','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(97,'ezzomich','2014-11-08 00:53:12','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(98,'ezzomich','2014-11-08 00:53:18','/coach22/message/home/','null','null','null',0,'{}'),(99,'ezzomich','2014-11-08 00:53:25','/coach22/message/home/','null','null','null',0,'{}'),(100,'ezzomich','2014-11-08 00:53:26','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(101,'ezzomich','2014-11-08 00:53:29','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(102,'ezzomich','2014-11-08 00:54:48','/coach22/message/home/','null','null','null',0,'{}'),(103,'ezzomich','2014-11-08 00:54:58','/coach22/message/Welcome/','null','null','null',0,'{}'),(104,'ezzomich','2014-11-08 00:54:59','/coach22/message/home/','null','null','null',0,'{}'),(105,'ezzomich','2014-11-08 00:55:16','/coach22/message/home/','null','null','null',0,'{}'),(106,'ezzomich','2014-11-08 00:56:22','/coach22/message/home/','null','null','null',0,'{}'),(107,'ezzomich','2014-11-08 00:56:24','/coach22/message/home/','null','null','null',0,'{}'),(108,'ezzomich','2014-11-08 00:56:26','/coach22/message/home/','null','null','null',0,'{}'),(109,'ezzomich','2014-11-08 00:56:27','/coach22/message/home/','null','null','null',0,'{}'),(110,'ezzomich','2014-11-08 00:56:28','/coach22/message/Welcome/','null','null','null',0,'{}'),(111,'ezzomich','2014-11-08 00:56:30','/coach22/staff/','null','null','null',0,'{}'),(112,'ezzomich','2014-11-08 00:56:31','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(113,'ezzomich','2014-11-08 00:56:31','/coach22/messageframe/home/','null','null','null',0,'{}'),(114,'ezzomich','2014-11-08 00:56:33','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(115,'ezzomich','2014-11-08 00:56:33','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(116,'ezzomich','2014-11-08 00:56:34','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(117,'ezzomich','2014-11-08 00:56:34','/coach22/messageframe/home/','null','null','null',0,'{}'),(118,'ezzomich','2014-11-08 00:56:36','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(119,'ezzomich','2014-11-08 00:56:36','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(120,'ezzomich','2014-11-08 00:56:37','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(121,'ezzomich','2014-11-08 00:56:37','/coach22/messageframe/home/','null','null','null',0,'{}'),(122,'ezzomich','2014-11-08 00:56:38','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(123,'ezzomich','2014-11-08 00:56:38','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(124,'ezzomich','2014-11-08 00:57:06','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(125,'ezzomich','2014-11-08 00:57:06','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(126,'ezzomich','2014-11-08 00:57:11','/coach22/message/home/','null','null','null',0,'{}'),(127,'ezzomich','2014-11-08 00:57:13','/coach22/message/Welcome/','null','null','null',0,'{}'),(128,'ezzomich','2014-11-08 00:57:36','/coach22/message/Welcome/','null','null','null',0,'{}'),(129,'ezzomich','2014-11-08 01:06:02','/coach22/message/home/','null','null','null',0,'{}'),(130,'ezzomich','2014-11-08 01:06:07','/coaches/','null','null','null',0,'{}'),(131,'ezzomich','2014-11-08 01:06:09','/coach22/message/home/','null','null','null',0,'{}'),(132,'ezzomich','2014-11-08 01:06:11','/coach22/staff/','null','null','null',0,'{}'),(133,'ezzomich','2014-11-08 01:09:26','/coaches/','null','null','null',0,'{}'),(134,'ezzomich','2014-11-08 01:09:28','/coach22/message/home/','null','null','null',0,'{}'),(135,'ezzomich','2014-11-08 01:09:30','/coach22/message/Welcome/','null','null','null',0,'{}'),(136,'ezzomich','2014-11-08 01:09:43','/coach22/message/Welcome/','null','null','null',0,'{}'),(137,'ezzomich','2014-11-08 01:50:49','/coaches/','null','null','null',0,'{}'),(138,'ezzomich','2014-11-08 01:50:53','/coach22/message/home/','null','null','null',0,'{}'),(139,'ezzomich','2014-11-08 01:50:56','/coach22/message/Welcome/','null','null','null',0,'{}'),(140,'ezzomich','2014-11-08 01:51:12','/coach22/survey/CommonSurvey/1','null','null','null',0,'{}'),(141,'ezzomich','2014-11-08 01:51:15','/coach22/message/home/','null','null','null',0,'{}'),(142,'ezzomich','2014-11-08 01:51:27','/coach22/message/home/','null','null','null',0,'{}'),(143,'ezzomich','2014-11-08 01:51:28','/coach22/message/Welcome/','null','null','null',0,'{}'),(144,'ezzomich','2014-11-08 01:51:33','/coach22/staff/','null','null','null',0,'{}'),(145,'ezzomich','2014-11-08 01:51:35','/coach22/publisher/copycat/','null','null','null',0,'{}'),(146,'ezzomich','2014-11-08 01:51:45','/coach22/publisher/copycat/','staff','copycat','ezzomich',0,'{}'),(147,'ezzomich','2014-11-08 01:51:45','/coach22/publisher/copycat/','null','null','null',0,'{}'),(148,'ezzomich','2014-11-08 01:51:50','/coach22/publisher/copycat/','null','null','null',0,'{}'),(149,'ezzomich','2014-11-08 01:52:11','/coach22/publisher/copycat/','staff','copycat','ezzomich',0,'{}'),(150,'ezzomich','2014-11-08 01:52:12','/coach22/publisher/copycat/','null','null','null',0,'{}'),(151,'ezzomich','2014-11-08 01:52:12','/coach22/publisher/copycat/','staff','copycat','ezzomich',0,'{}'),(152,'ezzomich','2014-11-08 01:52:13','/coach22/publisher/copycat/','null','null','null',0,'{}'),(153,'ezzomich','2014-11-08 01:52:16','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(154,'ezzomich','2014-11-08 01:52:16','/coach22/messageframe/home/','null','null','null',0,'{}'),(155,'ezzomich','2014-11-08 01:52:17','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(156,'ezzomich','2014-11-08 01:52:17','/coach22/messageframe/home/','null','null','null',0,'{}'),(157,'ezzomich','2014-11-08 01:52:18','/coach22/publisher/message_review/inbox/','null','null','null',0,'{}'),(158,'ezzomich','2014-11-08 01:52:18','/coach22/messageframe/inbox/','null','null','null',0,'{}'),(159,'ezzomich','2014-11-08 01:52:20','/coach22/publisher/message_review/home/','null','null','null',0,'{}'),(160,'ezzomich','2014-11-08 01:52:20','/coach22/messageframe/home/','null','null','null',0,'{}'),(161,'ezzomich','2014-11-08 01:52:20','/coach22/publisher/message_review/Welcome/','null','null','null',0,'{}'),(162,'ezzomich','2014-11-08 01:52:20','/coach22/messageframe/Welcome/','null','null','null',0,'{}'),(163,'ezzomich','2014-11-08 01:52:22','/coach22/publisher/copycat/','null','null','null',0,'{}'),(164,'ezzomich','2014-11-08 01:52:24','/coach22/publisher/run_checkout/','null','null','null',0,'{}'),(165,'ezzomich','2014-11-08 01:52:25','/coach22/upload/','null','null','null',0,'{}'),(166,'ezzomich','2014-11-08 01:52:49','/coach22/upload/file_upload/','null','null','null',0,'{}'),(167,'ezzomich','2014-11-08 01:52:50','/coach22/upload/file_upload/','null','null','null',0,'{}'),(168,'ezzomich','2014-11-08 01:52:50','/coach22/upload/file_upload/','null','null','null',0,'{}'),(169,'ezzomich','2014-11-08 01:52:51','/coach22/upload/archive/','null','null','null',0,'{}'),(170,'ezzomich','2014-11-08 01:52:55','/coach22/upload/help/','null','null','null',0,'{}'),(171,'ezzomich','2014-11-08 01:54:17','/coach22/export/','null','null','null',0,'{}'),(172,'ezzomich','2014-11-08 01:54:21','/coach22/export/','null','null','null',0,'{}'),(173,'ezzomich','2014-11-08 01:54:27','/coach22/export/select_columns/','null','null','null',0,'{}'),(174,'ezzomich','2014-11-08 01:54:35','/coach22/export/select_columns/','null','null','null',0,'{}'),(175,'ezzomich','2014-11-08 01:54:37','/coach22/export/download_trigger/','null','null','null',0,'{}'),(176,'ezzomich','2014-11-08 01:54:40','/coach22/export/archive/','null','null','null',0,'{}'),(177,'ezzomich','2014-11-08 01:54:59','/coach22/export/dump_sql/','null','null','null',0,'{}');
/*!40000 ALTER TABLE `mylogger_elog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mypublisher_copycat`
--

DROP TABLE IF EXISTS `mypublisher_copycat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mypublisher_copycat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) NOT NULL,
  `table` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mypublisher_copycat_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_username_416d686f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mypublisher_copycat`
--

LOCK TABLES `mypublisher_copycat` WRITE;
/*!40000 ALTER TABLE `mypublisher_copycat` DISABLE KEYS */;
INSERT INTO `mypublisher_copycat` VALUES (1,'ezzomich','Source1');
/*!40000 ALTER TABLE `mypublisher_copycat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mypublisher_copycat_column`
--

DROP TABLE IF EXISTS `mypublisher_copycat_column`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mypublisher_copycat_column` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `column_name` varchar(100) NOT NULL,
  `copycat_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mypublisher_copycat_column_bba3804e` (`copycat_id`),
  CONSTRAINT `copycat_id_refs_id_1ae75a13` FOREIGN KEY (`copycat_id`) REFERENCES `mypublisher_copycat` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mypublisher_copycat_column`
--

LOCK TABLES `mypublisher_copycat_column` WRITE;
/*!40000 ALTER TABLE `mypublisher_copycat_column` DISABLE KEYS */;
INSERT INTO `mypublisher_copycat_column` VALUES (17,'id',1),(18,'user_id',1),(19,'updated',1),(20,'SLCENROLLED',1),(21,'First_Name',1),(22,'NetID',1),(23,'Gender',1),(24,'Last_Name',1);
/*!40000 ALTER TABLE `mypublisher_copycat_column` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mytailoring_userprofile`
--

DROP TABLE IF EXISTS `mytailoring_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mytailoring_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `accepted_consent` tinyint(1) DEFAULT NULL,
  `withdrawn_reason` varchar(64) DEFAULT NULL,
  `updated` datetime NOT NULL,
  `created` datetime NOT NULL,
  `_prefs` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_8ce576d3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mytailoring_userprofile`
--

LOCK TABLES `mytailoring_userprofile` WRITE;
/*!40000 ALTER TABLE `mytailoring_userprofile` DISABLE KEYS */;
INSERT INTO `mytailoring_userprofile` VALUES (1,1,NULL,NULL,'2014-11-08 01:54:40','2014-11-07 21:37:45','eyJkaWdlc3Rpb25fcGsiOiAxLCAiZG93bmxvYWRfcGsiOiAyfQ==\n');
/*!40000 ALTER TABLE `mytailoring_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surveys_surveystate`
--

DROP TABLE IF EXISTS `surveys_surveystate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `surveys_surveystate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(40) NOT NULL,
  `survey_id` longtext NOT NULL,
  `page_msgid` varchar(40) NOT NULL,
  `running_subject_data` longtext NOT NULL,
  `latest_page_data` longtext NOT NULL,
  `validation_errors` int(11) NOT NULL,
  `previous_state_id` int(11) DEFAULT NULL,
  `valid` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `surveys_surveystate_277fe169` (`previous_state_id`),
  CONSTRAINT `previous_state_id_refs_id_c1167f67` FOREIGN KEY (`previous_state_id`) REFERENCES `surveys_surveystate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveys_surveystate`
--

LOCK TABLES `surveys_surveystate` WRITE;
/*!40000 ALTER TABLE `surveys_surveystate` DISABLE KEYS */;
INSERT INTO `surveys_surveystate` VALUES (1,'ezzomich','CommonSurvey','1','{}','{\"Gender\": \"M\", \"First_Name\": \"Mike\", \"Last_Name\": \"Ezzo\", \"NetID\": \"ezzomich\"}',0,NULL,1,'2014-11-08 00:52:07','2014-11-08 01:51:27');
/*!40000 ALTER TABLE `surveys_surveystate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tracking_event`
--

DROP TABLE IF EXISTS `tracking_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tracking_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `timestamp` datetime NOT NULL,
  `note` varchar(255) NOT NULL,
  `related_content_type_id` int(11) DEFAULT NULL,
  `related_object_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tracking_event_fbfc09f1` (`user_id`),
  KEY `tracking_event_5e4160ae` (`related_content_type_id`),
  CONSTRAINT `related_content_type_id_refs_id_56b86520` FOREIGN KEY (`related_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_2a4558e4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tracking_event`
--

LOCK TABLES `tracking_event` WRITE;
/*!40000 ALTER TABLE `tracking_event` DISABLE KEYS */;
INSERT INTO `tracking_event` VALUES (1,1,'UserLoggedIn','2014-11-07 21:38:43','/coaches/login/',NULL,NULL),(2,1,'UserLoggedIn','2014-11-08 01:09:25','/coaches/login/',NULL,NULL),(3,1,'UserLoggedIn','2014-11-08 01:50:49','/coaches/login/',NULL,NULL);
/*!40000 ALTER TABLE `tracking_event` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-08  1:55:03
