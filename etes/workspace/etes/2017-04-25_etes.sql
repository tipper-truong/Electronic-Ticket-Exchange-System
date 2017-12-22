-- MySQL dump 10.13  Distrib 5.5.53, for debian-linux-gnu (x86_64)
--
-- Host: 0.0.0.0    Database: etes_db
-- ------------------------------------------------------
-- Server version	5.5.53-0ubuntu0.14.04.1

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
-- Current Database: `etes_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `etes_db` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `etes_db`;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `venue` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `starttime` varchar(100) DEFAULT NULL,
  `endtime` varchar(100) DEFAULT NULL,
  `imgpath` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `price` decimal(15,2) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (2,'The Chainsmokers','Electronic Dance Music','Bill Graham Civic Auditorium','San Francisco, CA','Fri, 05/05/17','8:00pm','12:00pm','/static/images/event1.jpg',2,75.00,85),(3,'Chris Brown: The Party Tour','Hip-hop/R&B','Golden 1 Center','Sacramento, CA','Sat, 05/13/17','7:30pm','11:30pm','/static/images/chris-brown.jpg',2,45.00,90),(4,'Bottlerock Napa Valley','Alternative Rock','Napa Valley Expo','Napa, CA','Fri, 05/26/17','12:00pm','9:00pm','/static/images/bottle-rock.png',1,95.00,99),(5,'John Legend','R&B','Greek Theatre-U.C. Berkeley','Berkeley, CA','Sat, 05/27/17','7:30pm','11:30pm','/static/images/john-legend.jpg',1,75.00,99),(6,'Lady Gaga Joanne World Tour','Pop','Oracle Arena','Oakland, CA','Tues, 08/15/2017','8:00pm','11:00pm','/static/images/event2.jpg',1,100.00,100),(7,'Lady Antebellum: You Look Good Tour 2017','Country/Pop','Shoreline Amphitheatre','Mountain View, CA','Sat, 05/27/17','7:30pm','11:30pm','/static/images/lady-tour.jpg',1,45.00,100),(8,'Coldplay: A Head Full of Dreams Tour','Pop','Levi\'s Stadium','Santa Clara, CA','Wed, 10/04/17','7:00pm','11:00pm','/static/images/coldplay.jpg',1,80.00,99),(10,'Kehlani','Hip-hop/R&B','Bill Graham Civic Auditorium','San Francisco, CA','Sat, 06/17/17','8:00pm','11:00pm','/static/images/kehlani.jpg',2,50.00,98),(11,'Coachella','Music Festival','Empire Polo Club','Indio, CA','Fri, 4/14/18','All-Day','All-Day','/static/images/c0a3fdbc-efa1-4e81-8b24-139cdb54b676.jpg',2,600.00,2),(19,'Coldplay: A Head Full of Dreams Tour','Pop','Levi\'s Stadium','Santa Clara, CA','Wed, 10/04/17','7:00pm','11:00pm','/static/images/coldplay.jpg',2,80.00,99),(20,'Bruno Mars: 24K Magic World Tour','Pop','SAP Center','San Jose, CA','Fri, 07/07/17','7:00pm','11:00pm','/static/images/bruno-mars.jpg',2,60.00,91),(23,'Sold Out! If you see this there is a problem!','Hip-hop/R&B','Bill Graham Civic Auditorium','San Francisco, CA','Sat, 06/17/17','8:00pm','11:00pm','/static/images/kehlani.jpg',7,50.00,0),(46,'Event ended! If you see this there is a problem!','Hip-hop/R&B','Bill Graham Civic Auditorium','San Francisco, CA','Sat, 01/02/17','8:00pm','11:00pm','/static/images/kehlani.jpg',7,50.00,100),(47,'a','9','b','c','01/02/17','11:00 pm','01:00 am','static/images/a076d712-5b0b-4190-9d50-b14b1c56f65e.jpg',3,100.00,12);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `seller_id` int(11) DEFAULT NULL,
  `buyer_id` int(11) DEFAULT NULL,
  `bought` int(1) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `cardnum` varchar(100) DEFAULT NULL,
  `expiry` varchar(100) DEFAULT NULL,
  `cvv` varchar(100) DEFAULT NULL,
  `timestamp` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (5,2,3,2,1,'Tipper','Truong','4157938223','574 22nd Ave San Francisco','CA 94121','CA','','United States','124567890987654','Mar/18','654',NULL),(6,11,1,2,1,'Tipper','Truong','','574 22nd Ave',' San Francisco','CA','94121','United States','123456787654','Sep/17','456',NULL),(7,3,3,2,1,'Tipper','Truong','4157938331','574 22nd Ave','San Francisco','CA','94121','United States','1234565432','Dec/23','345',NULL),(8,21,7,3,1,'Hansen','Wu','1234567896',' 1 Washington Sq','San Jose','CA','95192','United States','12345676543','Apr/21','231',NULL),(9,20,3,2,1,'Tipper','Truong','4157938331','574 22nd Ave','San Francisco','CA','94121','United States','2345676543','Mar/20','987',NULL),(10,2,2,3,1,'Hansen','Wu','',' 1 Washington Sq','San Jose','CA','95192','United States','98765456789','Apr/20','098',NULL),(11,20,2,3,1,'Hansen','Wu','',' 1 Washington Sq','San Jose','CA','95192','United States','22676543456765','May/21','765',NULL),(12,2,2,3,1,'Hansen','Wu','',' 1 Washington Sq','San Jose','CA','95192','United States','24565432345','Jul/21','236',NULL),(13,2,2,3,1,'Hansen','Wu','4151234567',' 1 Washington Sq','San Jose','CA','95192','United States','23456798765','Apr/20','546',NULL),(14,20,2,3,1,'Hansen','Wu','',' 1 Washington Sq','San Jose','CA','95192','United States','6789876578','Jan/17','',NULL),(15,4,1,3,1,'Hansen','Wu','',' 1 Washington Sq','San Jose','CA','95192','United States','','Jan/17','',NULL),(16,20,2,4,1,'Patrick','Solis','','49 S 1st Street','San Jose','CA','','United States','','Jan/17','',NULL),(17,5,1,4,1,'Patrick','Solis','','49 S 1st Street','San Jose','CA','','United States','','Jan/17','',NULL),(18,26,4,4,1,'Patrick','Solis','','49 S 1st Street','San Jose','CA','','United States','','Jan/17','',NULL),(42,2,NULL,3,0,'Hansen','Wu',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2017-04-24 19:59:32'),(43,2,NULL,3,0,'Hansen','Wu',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2017-04-24 20:11:51'),(44,2,NULL,11,0,'Testing','test',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2017-04-24 23:46:49'),(45,2,2,11,0,'Testing','test','','1 Washington Sq. San Jose 95192','','CA','','United States','1234234123412134','Jan/17','','2017-04-24 23:47:36'),(46,3,NULL,11,0,'Testing','test',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2017-04-24 23:49:10'),(47,3,2,11,0,'Testing','test','','1 Washington Sq. San Jose 95192','','CA','','United States','','Jan/17','','2017-04-24 23:49:11'),(48,2,NULL,3,0,'Hansen','Wu',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2017-04-25 20:05:47'),(49,2,NULL,3,0,'Hansen','Wu',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2017-04-25 20:12:01');
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(80) DEFAULT NULL,
  `email` varchar(35) DEFAULT NULL,
  `username` varchar(25) DEFAULT NULL,
  `password` varchar(80) DEFAULT NULL,
  `address` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
-- INSERT INTO `user` VALUES (1,'Sanjana Shetty','sanjana@gmail.com','sanjana','tester','87 E San Fernando St, San Jose, CA 95113'),(2,'Tipper Truong','tqtruong95@gmail.com','tipper.truong','test','574 22nd Ave San Francisco, CA 94121'),(3,'Hansen Wu','hansenwu@gmail.com','hansen','test',' 1 Washington Sq, San Jose, CA 95192'),(4,'Patrick Solis','psolis00@gmail.com','Patrick','test','49 S 1st Street, San Jose, CA, 95113'),(6,'Thomas Wilson','thomas.wilson@sjsu.edu','Wilson','password','1 Washington Square, San Jose, CA'),(7,'Jane Doe','janedoe@yahoo.com','jane','test','780 S Airport Blvd San Francisco, CA 94128'),(8,'Jimmy Neutron','jimmyneutron@gmail.com','jimmy','$2b$12$9DZRIA0k.YqM58TCdRslaucbEzxDoTmEkx/M7DComIZ1KsgA1wQ8y','4900 Marie P DeBartolo Way, Santa Clara, CA 95054'),(9,'Frank Butt','frank123@gmail.com','frank123','$2b$12$w9y5Ib6lWiARoqnXqtXC6OE0XH5Pbn//HxGt11p6IFrj.qPu8EWO.','7000 Coliseum Way, Oakland, CA 94621'),(10,'testing tester','tester@gmail.org','testing','$2b$12$riTjIlTqvU1yWVMot.bXQ.CKfKeAJPWr7U/ZvcgwE517h9lnrrVqi','49 S 1st Street, San Jose, 95113'),(11,'Testing test','tester@test.com','tester','$2b$12$p54/f2eB.kZgUj/DS8SheuwbrTpsEQc9L4i2L4SkKMh8cxHzy8Pwy','1 Washington Sq. San Jose 95192');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-25 20:25:21
