-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: iot
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `deviceID` int NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Output` varchar(255) DEFAULT NULL,
  `Status` int DEFAULT NULL,
  PRIMARY KEY (`deviceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diagnose`
--

DROP TABLE IF EXISTS `diagnose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diagnose` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Link_image` text NOT NULL,
  `Diagnose` text NOT NULL,
  `Time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diagnose`
--

LOCK TABLES `diagnose` WRITE;
/*!40000 ALTER TABLE `diagnose` DISABLE KEYS */;
INSERT INTO `diagnose` VALUES (1,'./upload/305819068_1131200254185802_4464402511030800070_n.jpg','Tomato - Bệnh đốm lá Septoria (Septoria Leaf Spot Disease)','2023-11-20 22:30:34');
/*!40000 ALTER TABLE `diagnose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Time` datetime NOT NULL,
  `Temperature` double NOT NULL,
  `Light` double NOT NULL,
  `Humidity` double NOT NULL,
  `Soil` double NOT NULL,
  `pump_state` varchar(45) NOT NULL,
  `light_state` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
INSERT INTO `history` VALUES (1,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(2,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(3,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(4,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(5,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(6,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(7,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(8,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(9,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(10,'2023-11-20 21:39:33',24,6.666666508,46,37,'OFF','OFF'),(11,'2023-11-20 22:00:15',24,6.666666508,46,37,'OFF','OFF'),(12,'2023-11-20 22:00:15',24,6.666666508,46,37,'OFF','OFF'),(13,'2023-11-20 22:00:15',24,6.666666508,46,37,'OFF','OFF'),(14,'2023-11-20 22:00:15',24,6.666666508,46,37,'OFF','OFF'),(15,'2023-11-20 22:00:15',24,6.666666508,46,37,'OFF','OFF'),(16,'2023-11-20 22:00:15',24,6.666666508,46,37,'OFF','OFF'),(17,'2023-11-20 22:30:34',24,6.666666508,46,37,'OFF','OFF');
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `light`
--

DROP TABLE IF EXISTS `light`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `light` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `State` varchar(255) NOT NULL,
  `Time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `light`
--

LOCK TABLES `light` WRITE;
/*!40000 ALTER TABLE `light` DISABLE KEYS */;
INSERT INTO `light` VALUES (1,'OFF','2023-11-20 21:39:33'),(2,'OFF','2023-11-20 21:39:33'),(3,'OFF','2023-11-20 21:39:33'),(4,'OFF','2023-11-20 21:39:33'),(5,'OFF','2023-11-20 21:39:33'),(6,'OFF','2023-11-20 21:39:33'),(7,'OFF','2023-11-20 21:39:33'),(8,'OFF','2023-11-20 21:39:33'),(9,'OFF','2023-11-20 21:39:33'),(10,'OFF','2023-11-20 21:39:33'),(11,'OFF','2023-11-20 22:00:15'),(12,'OFF','2023-11-20 22:00:15'),(13,'OFF','2023-11-20 22:00:15'),(14,'OFF','2023-11-20 22:00:15'),(15,'OFF','2023-11-20 22:00:15'),(16,'OFF','2023-11-20 22:00:15'),(17,'OFF','2023-11-20 22:30:34');
/*!40000 ALTER TABLE `light` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lightsensor`
--

DROP TABLE IF EXISTS `lightsensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lightsensor` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Light_Intensity` double NOT NULL,
  `Time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lightsensor`
--

LOCK TABLES `lightsensor` WRITE;
/*!40000 ALTER TABLE `lightsensor` DISABLE KEYS */;
INSERT INTO `lightsensor` VALUES (1,6.666666508,'2023-11-20 21:39:33'),(2,6.666666508,'2023-11-20 21:39:33'),(3,6.666666508,'2023-11-20 21:39:33'),(4,6.666666508,'2023-11-20 21:39:33'),(5,6.666666508,'2023-11-20 21:39:33'),(6,6.666666508,'2023-11-20 21:39:33'),(7,6.666666508,'2023-11-20 21:39:33'),(8,6.666666508,'2023-11-20 21:39:33'),(9,6.666666508,'2023-11-20 21:39:33'),(10,6.666666508,'2023-11-20 21:39:33'),(11,6.666666508,'2023-11-20 22:00:15'),(12,6.666666508,'2023-11-20 22:00:15'),(13,6.666666508,'2023-11-20 22:00:15'),(14,6.666666508,'2023-11-20 22:00:15'),(15,6.666666508,'2023-11-20 22:00:15'),(16,6.666666508,'2023-11-20 22:00:15'),(17,6.666666508,'2023-11-20 22:30:34');
/*!40000 ALTER TABLE `lightsensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `soilhumiditysensor`
--

DROP TABLE IF EXISTS `soilhumiditysensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `soilhumiditysensor` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `SoilHumidity` float NOT NULL,
  `Time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `soilhumiditysensor`
--

LOCK TABLES `soilhumiditysensor` WRITE;
/*!40000 ALTER TABLE `soilhumiditysensor` DISABLE KEYS */;
INSERT INTO `soilhumiditysensor` VALUES (1,37,'2023-11-20 21:39:33'),(2,37,'2023-11-20 21:39:33'),(3,37,'2023-11-20 21:39:33'),(4,37,'2023-11-20 21:39:33'),(5,37,'2023-11-20 21:39:33'),(6,37,'2023-11-20 21:39:33'),(7,37,'2023-11-20 21:39:33'),(8,37,'2023-11-20 21:39:33'),(9,37,'2023-11-20 21:39:33'),(10,37,'2023-11-20 21:39:33'),(11,37,'2023-11-20 22:00:15'),(12,37,'2023-11-20 22:00:15'),(13,37,'2023-11-20 22:00:15'),(14,37,'2023-11-20 22:00:15'),(15,37,'2023-11-20 22:00:15'),(16,37,'2023-11-20 22:00:15'),(17,37,'2023-11-20 22:30:34');
/*!40000 ALTER TABLE `soilhumiditysensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temperaturehumidity`
--

DROP TABLE IF EXISTS `temperaturehumidity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temperaturehumidity` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Temperature` double NOT NULL,
  `Humidity` double NOT NULL,
  `Time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperaturehumidity`
--

LOCK TABLES `temperaturehumidity` WRITE;
/*!40000 ALTER TABLE `temperaturehumidity` DISABLE KEYS */;
INSERT INTO `temperaturehumidity` VALUES (1,24,46,'2023-11-20 21:39:33'),(2,24,46,'2023-11-20 21:39:33'),(3,24,46,'2023-11-20 21:39:33'),(4,24,46,'2023-11-20 21:39:33'),(5,24,46,'2023-11-20 21:39:33'),(6,24,46,'2023-11-20 21:39:33'),(7,24,46,'2023-11-20 21:39:33'),(8,24,46,'2023-11-20 21:39:33'),(9,24,46,'2023-11-20 21:39:33'),(10,24,46,'2023-11-20 21:39:33'),(11,24,46,'2023-11-20 22:00:15'),(12,24,46,'2023-11-20 22:00:15'),(13,24,46,'2023-11-20 22:00:15'),(14,24,46,'2023-11-20 22:00:15'),(15,24,46,'2023-11-20 22:00:15'),(16,24,46,'2023-11-20 22:00:15'),(17,24,46,'2023-11-20 22:30:34');
/*!40000 ALTER TABLE `temperaturehumidity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `waterpump`
--

DROP TABLE IF EXISTS `waterpump`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waterpump` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `State` varchar(255) NOT NULL,
  `Time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `waterpump`
--

LOCK TABLES `waterpump` WRITE;
/*!40000 ALTER TABLE `waterpump` DISABLE KEYS */;
INSERT INTO `waterpump` VALUES (1,'OFF','2023-11-20 21:39:33'),(2,'OFF','2023-11-20 21:39:33'),(3,'OFF','2023-11-20 21:39:33'),(4,'OFF','2023-11-20 21:39:33'),(5,'OFF','2023-11-20 21:39:33'),(6,'OFF','2023-11-20 21:39:33'),(7,'OFF','2023-11-20 21:39:33'),(8,'OFF','2023-11-20 21:39:33'),(9,'OFF','2023-11-20 21:39:33'),(10,'OFF','2023-11-20 21:39:33'),(11,'OFF','2023-11-20 22:00:15'),(12,'OFF','2023-11-20 22:00:15'),(13,'OFF','2023-11-20 22:00:15'),(14,'OFF','2023-11-20 22:00:15'),(15,'OFF','2023-11-20 22:00:15'),(16,'OFF','2023-11-20 22:00:15'),(17,'OFF','2023-11-20 22:30:34');
/*!40000 ALTER TABLE `waterpump` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-20 22:32:56
