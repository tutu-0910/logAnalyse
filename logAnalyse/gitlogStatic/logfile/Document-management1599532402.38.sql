-- MySQL dump 10.13  Distrib 5.6.45, for Linux (x86_64)
--
-- Host: localhost    Database: gitlog
-- ------------------------------------------------------
-- Server version	5.6.47

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
-- Table structure for table `logAnalyse_gitlogpubstat`
--

DROP TABLE IF EXISTS `logAnalyse_gitlogpubstat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logAnalyse_gitlogpubstat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `end_time` varchar(10) NOT NULL,
  `author` varchar(50) NOT NULL,
  `commit_count` int(11) NOT NULL,
  `commit_path` varchar(50) NOT NULL,
  `analyze_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logAnalyse_gitlogpubstat_305d2889` (`end_time`),
  KEY `logAnalyse_gitlogpubstat_02bd92fa` (`author`),
  KEY `logAnalyse_gitlogpubstat_0684f772` (`commit_path`)
) ENGINE=InnoDB AUTO_INCREMENT=699 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logAnalyse_gitlogpubstat`
--
-- WHERE:  analyze_id=34

LOCK TABLES `logAnalyse_gitlogpubstat` WRITE;
/*!40000 ALTER TABLE `logAnalyse_gitlogpubstat` DISABLE KEYS */;
INSERT INTO `logAnalyse_gitlogpubstat` VALUES (632,'2015-02-01','all',0,'all',34),(633,'2015-03-01','all',0,'all',34),(634,'2015-04-01','all',0,'all',34),(635,'2015-05-01','all',0,'all',34),(636,'2015-06-01','all',0,'all',34),(637,'2015-07-01','all',0,'all',34),(638,'2015-08-01','all',0,'all',34),(639,'2015-09-01','all',0,'all',34),(640,'2015-10-01','all',0,'all',34),(641,'2015-11-01','all',0,'all',34),(642,'2015-12-01','all',0,'all',34),(643,'2016-01-01','all',0,'all',34),(644,'2016-02-01','all',0,'all',34),(645,'2016-03-01','all',0,'all',34),(646,'2016-04-01','all',0,'all',34),(647,'2016-05-01','all',0,'all',34),(648,'2016-06-01','all',0,'all',34),(649,'2016-07-01','all',0,'all',34),(650,'2016-08-01','all',0,'all',34),(651,'2016-09-01','all',0,'all',34),(652,'2016-10-01','all',0,'all',34),(653,'2016-11-01','all',0,'all',34),(654,'2016-12-01','all',0,'all',34),(655,'2017-01-01','all',0,'all',34),(656,'2017-02-01','all',0,'all',34),(657,'2017-03-01','all',0,'all',34),(658,'2017-04-01','all',0,'all',34),(659,'2017-05-01','all',0,'all',34),(660,'2017-06-01','all',0,'all',34),(661,'2017-07-01','all',0,'all',34),(662,'2017-08-01','all',0,'all',34),(663,'2017-09-01','all',0,'all',34),(664,'2017-10-01','all',0,'all',34),(665,'2017-11-01','all',0,'all',34),(666,'2017-12-01','all',0,'all',34),(667,'2018-01-01','all',0,'all',34),(668,'2018-02-01','all',0,'all',34),(669,'2018-03-01','all',0,'all',34),(670,'2018-04-01','all',0,'all',34),(671,'2018-05-01','all',0,'all',34),(672,'2018-06-01','all',0,'all',34),(673,'2018-07-01','all',0,'all',34),(674,'2018-08-01','all',0,'all',34),(675,'2018-09-01','all',11,'all',34),(676,'2018-10-01','all',1,'all',34),(677,'2018-11-01','all',4,'all',34),(678,'2018-12-01','all',3,'all',34),(679,'2019-01-01','all',0,'all',34),(680,'2019-02-01','all',0,'all',34),(681,'2019-03-01','all',0,'all',34),(682,'2019-04-01','all',0,'all',34),(683,'2019-05-01','all',0,'all',34),(684,'2019-06-01','all',0,'all',34),(685,'2019-07-01','all',0,'all',34),(686,'2019-08-01','all',0,'all',34),(687,'2019-09-01','all',0,'all',34),(688,'2019-10-01','all',0,'all',34),(689,'2019-11-01','all',0,'all',34),(690,'2019-12-01','all',0,'all',34),(691,'2020-01-01','all',0,'all',34),(692,'2020-02-01','all',0,'all',34),(693,'2020-03-01','all',0,'all',34),(694,'2020-04-01','all',0,'all',34),(695,'2020-05-01','all',0,'all',34),(696,'2020-06-01','all',0,'all',34),(697,'2020-07-01','all',0,'all',34),(698,'2020-08-01','all',0,'all',34);
/*!40000 ALTER TABLE `logAnalyse_gitlogpubstat` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-08  2:33:22
