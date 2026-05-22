-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: fake_file_system
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'minnu','minnu@gmail.com','scrypt:32768:8:1$l05E6kzMM1Or2wRp$7ad502e890899f7257eb1096bd457311e9a4a2739f63b72484d7bfb2ac696add5649b09dcbf30862afbfdcf92cf33cc74210164eaeed314a6714890317cba3a7','2026-05-07 12:40:29');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) DEFAULT NULL,
  `filetype` varchar(50) DEFAULT NULL,
  `filesize` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `uploaded_by` varchar(10) DEFAULT NULL,
  `sha512` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `uploaded_by` (`uploaded_by`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (8,'1001847629.pdf','application/pdf',36205,'genuine','02','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:28:46'),(9,'1001847629.pdf','application/pdf',36205,'duplicate','02','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:28:58'),(10,'7th_bonafide.pdf.jpg','image/jpeg',89107,'genuine','02','e0d1ae23e46f1bd75676072b2674bd84b1cac0c4a7a2e937a1901e29688a85430acfd4410736ec8361e18a6de784f31bc07be4fee99702335fef0f8707823c16','2026-04-23 07:29:08'),(11,'1001847629.pdf','application/pdf',36205,'duplicate','02','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:29:48'),(12,'CapCut.exe','application/x-msdownload',1576104,'genuine','02','18477d2bcd2176292df149cef3a6a6d18bcf63d0e9d970954e5cef0c7ac2bbca9a3cc08d21e05d8b04b9aa191deec4b687315583b578b6865e102f7e443308de','2026-04-23 07:30:02'),(13,'POSTAL_GSD.pdf','application/pdf',332873,'genuine','02','7899c86e21cf405a673f3b58b9bf36b4f1796ccf2cbbaa864bde074dddfc48ef5ca83e8b242af53d97bd8d07c7d49d8f7fc7e88826aec2e05e17f182d77a1e07','2026-04-23 07:30:35'),(14,'virus.bat','application/octet-stream',79,'genuine','02','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 07:31:10'),(15,'virus.bat','application/octet-stream',79,'genuine','03','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 07:32:52'),(16,'1001847629.pdf','application/pdf',36205,'genuine','03','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:33:13'),(17,'1001847629.pdf','application/pdf',36205,'duplicate','03','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:43:20'),(18,'1001847629.pdf','application/pdf',36205,'genuine','04','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:44:43'),(19,'1001847629.pdf','application/pdf',36205,'genuine','05','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:46:29'),(20,'1001847629.pdf','application/pdf',36205,'duplicate','05','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 07:59:33'),(21,'1001847629.pdf','application/pdf',36205,'genuine','06','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:00:26'),(22,'1001847629.pdf','application/pdf',36205,'duplicate','06','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:04:49'),(23,'virus.bat','application/octet-stream',79,'genuine','06','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:05:01'),(24,'virus.bat','application/octet-stream',79,'duplicate','06','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:15:30'),(25,'virus.bat','application/octet-stream',79,'genuine','08','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:16:46'),(26,'1001847629.pdf','application/pdf',36205,'genuine','08','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:16:59'),(27,'1001847629.pdf','application/pdf',36205,'duplicate','08','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:28:49'),(28,'1001847629.pdf','application/pdf',36205,'genuine','10','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:30:57'),(29,'virus.bat','application/octet-stream',79,'genuine','10','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:31:15'),(30,'virus.bat','Unknown',79,'harmful','11','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:41:59'),(31,'1001847629.pdf','PDF Document',36205,'genuine','11','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:42:13'),(32,'7th_bonafide.pdf.jpg','Unknown',89107,'harmful','11','e0d1ae23e46f1bd75676072b2674bd84b1cac0c4a7a2e937a1901e29688a85430acfd4410736ec8361e18a6de784f31bc07be4fee99702335fef0f8707823c16','2026-04-23 08:42:42'),(33,'degree_bonafide.jpg','JPEG Image',88950,'genuine','11','2e69979316dda226e2a0aa8694774a5b39a3be4906fceba7cd0b6f18d08f247bd0e40ec7ec37ab429dd41bc0cfc44ef4d042ecbeb54329684464aaaa9a18458c','2026-04-23 08:42:53'),(34,'fake_from_user_image.pdf','JPEG Image',1305,'fake','11','e57f5d410311846caf36aed33e2df29bc5ac2229c48a3b6b7b6344dfc372c97ca3e88e751eb9db606b2bbdb7507a4fe6a7ad2d71a5095406007dde5a30f770bb','2026-04-23 08:43:07'),(35,'virus.bat','Unknown',79,'duplicate','11','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:44:36'),(36,'1001847629.pdf','Unknown',36205,'fake','12','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:56:15'),(37,'1001847629.pdf','Unknown',36205,'duplicate','12','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-23 08:56:29'),(38,'virus.bat','Unknown',79,'harmful','12','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:56:44'),(39,'virus.bat','Unknown',79,'duplicate','12','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-23 08:56:53'),(40,'7th_bonafide.pdf.jpg','Unknown',89107,'harmful','12','e0d1ae23e46f1bd75676072b2674bd84b1cac0c4a7a2e937a1901e29688a85430acfd4410736ec8361e18a6de784f31bc07be4fee99702335fef0f8707823c16','2026-04-23 08:57:01'),(41,'7th_bonafide.pdf.jpg','Unknown',89107,'duplicate','12','e0d1ae23e46f1bd75676072b2674bd84b1cac0c4a7a2e937a1901e29688a85430acfd4410736ec8361e18a6de784f31bc07be4fee99702335fef0f8707823c16','2026-04-23 08:57:07'),(42,'aadhar.jpg','JPEG Image',49417,'genuine','12','207d254d7007a6c084ba19564622a5b5435e1a9e28aee96dfb5afdc3cdd229fae30c68be868bd27dbf9d88a80b60383b824b9c44e9dc259201a25d42c2aa140d','2026-04-23 08:57:14'),(43,'aadhar.jpg','JPEG Image',49417,'duplicate','12','207d254d7007a6c084ba19564622a5b5435e1a9e28aee96dfb5afdc3cdd229fae30c68be868bd27dbf9d88a80b60383b824b9c44e9dc259201a25d42c2aa140d','2026-04-23 08:57:24'),(47,'1001847629.pdf','unknown',36205,'Duplicate','13','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-29 03:49:58'),(48,'1001847629.pdf','unknown',36205,'Duplicate','13','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-29 04:01:24'),(49,'fake_from_user_image.pdf','jpeg',1305,'Fake','13','e57f5d410311846caf36aed33e2df29bc5ac2229c48a3b6b7b6344dfc372c97ca3e88e751eb9db606b2bbdb7507a4fe6a7ad2d71a5095406007dde5a30f770bb','2026-04-29 04:17:13'),(50,'7th bonafide.pdf.jpg','jpeg',89107,'Genuine','13','e0d1ae23e46f1bd75676072b2674bd84b1cac0c4a7a2e937a1901e29688a85430acfd4410736ec8361e18a6de784f31bc07be4fee99702335fef0f8707823c16','2026-04-29 04:17:55'),(51,'aadhar.jpg','jpeg',49417,'Genuine','13','207d254d7007a6c084ba19564622a5b5435e1a9e28aee96dfb5afdc3cdd229fae30c68be868bd27dbf9d88a80b60383b824b9c44e9dc259201a25d42c2aa140d','2026-04-29 04:28:55'),(52,'virus.bat',NULL,79,'Harmful','13','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-04-29 04:29:31'),(53,'1001847629.pdf','pdf',36205,'Fake','14','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-04-29 04:36:08'),(55,'fake_from_user_image.pdf','jpeg',1305,'Fake','14','e57f5d410311846caf36aed33e2df29bc5ac2229c48a3b6b7b6344dfc372c97ca3e88e751eb9db606b2bbdb7507a4fe6a7ad2d71a5095406007dde5a30f770bb','2026-04-29 04:44:22'),(56,'POSTAL GSD.pdf','pdf',332873,'Genuine','14','7899c86e21cf405a673f3b58b9bf36b4f1796ccf2cbbaa864bde074dddfc48ef5ca83e8b242af53d97bd8d07c7d49d8f7fc7e88826aec2e05e17f182d77a1e07','2026-04-29 04:44:33'),(57,'POSTAL GSD.pdf','pdf',332873,'Duplicate','14','7899c86e21cf405a673f3b58b9bf36b4f1796ccf2cbbaa864bde074dddfc48ef5ca83e8b242af53d97bd8d07c7d49d8f7fc7e88826aec2e05e17f182d77a1e07','2026-04-29 04:45:00'),(58,'ugc net.pdf','pdf',169521,'Genuine','14','2c6b9ba90beb9679e9ed9fdfc41ff900d65e495d0cf14af10f2119ceb3b048d89e3faa17f9f6ee7fbc05fc0e2389431012a2e820ab1bd1fe4c37b44b48e0d3af','2026-04-29 04:50:36'),(59,'rrb ntpc receipt.pdf','pdf',211481,'Genuine','14','f36fcec1f9515ba7c5bf09a5759497b0d0bc25e09f5a45937269bae2ffef2352755e5e0caef65cabc630f786527926494b3abec064081bfda0b73264cdb5706f','2026-04-29 04:56:01'),(60,'POSTAL GSD.pdf','pdf',332873,'Duplicate','14','7899c86e21cf405a673f3b58b9bf36b4f1796ccf2cbbaa864bde074dddfc48ef5ca83e8b242af53d97bd8d07c7d49d8f7fc7e88826aec2e05e17f182d77a1e07','2026-04-29 04:56:53'),(75,'1001847629.pdf','pdf',36205,'Fake','01','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-05-04 07:14:14'),(76,'virus.bat',NULL,79,'Harmful','01','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-05-04 07:14:31'),(77,'fake_from_user_image.pdf','jpeg',1305,'Fake','01','e57f5d410311846caf36aed33e2df29bc5ac2229c48a3b6b7b6344dfc372c97ca3e88e751eb9db606b2bbdb7507a4fe6a7ad2d71a5095406007dde5a30f770bb','2026-05-04 07:14:44'),(78,'7th bonafide.pdf.jpg','jpeg',89107,'Genuine','01','e0d1ae23e46f1bd75676072b2674bd84b1cac0c4a7a2e937a1901e29688a85430acfd4410736ec8361e18a6de784f31bc07be4fee99702335fef0f8707823c16','2026-05-04 07:15:01'),(79,'7th bonafide.pdf.jpg','jpeg',89107,'Duplicate','01','e0d1ae23e46f1bd75676072b2674bd84b1cac0c4a7a2e937a1901e29688a85430acfd4410736ec8361e18a6de784f31bc07be4fee99702335fef0f8707823c16','2026-05-04 07:15:15'),(80,'virus.bat',NULL,79,'Harmful','14','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-05-04 08:13:14'),(81,'virus.bat',NULL,79,'Duplicate','01','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-05-07 06:30:11'),(82,'1001847629.pdf','pdf',36205,'Duplicate','01','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-05-07 06:37:39'),(83,'fake file detection.pptx','zip',780826,'Fake','01','9c6723e7c57b9a14bb6688487b7591a4cfed2559d5a067fe14db182198012497132014580cd779797e14b1e3bb254279cd2ba12adfa91c3d2e6fce522c58f81f','2026-05-07 06:38:30'),(84,'aadhar.jpg','jpeg',49417,'Genuine','01','207d254d7007a6c084ba19564622a5b5435e1a9e28aee96dfb5afdc3cdd229fae30c68be868bd27dbf9d88a80b60383b824b9c44e9dc259201a25d42c2aa140d','2026-05-07 08:45:20'),(85,'report (1).txt',NULL,26,'Fake','01','71d6cc45e0d1cd2357b4d5722e065e43a9f772dca18731e0eae3da73dc2d9e4dd87d6b2e3f54d883c7e9a4de018b2e7f83eb2dfc0ab51e8487c070ac378b4bd5','2026-05-08 09:54:09'),(86,'1001847629.pdf','pdf',36205,'Fake','22','78185bb5fe152e4384702c5d65b1604ef7c18b7a94f13538a10fdb2b44cc958d9cfe8ff4ab298de6e3249efbd4495145f4355dcf07801cd28dd9853b2612dcd5','2026-05-08 09:56:30'),(87,'report (1).txt',NULL,26,'Fake','22','71d6cc45e0d1cd2357b4d5722e065e43a9f772dca18731e0eae3da73dc2d9e4dd87d6b2e3f54d883c7e9a4de018b2e7f83eb2dfc0ab51e8487c070ac378b4bd5','2026-05-08 09:56:40'),(88,'virus.bat',NULL,79,'Harmful','22','54ac728abdc4219b07f88452c115eb031f453d6cbc312aff4dedc8bf85d387de3ef71841b3ac96e1d7118849d1fa6674b186afe26cbd4e06043a6333cdee6920','2026-05-08 09:56:56'),(89,'aadhar.jpg','jpeg',49417,'Genuine','22','207d254d7007a6c084ba19564622a5b5435e1a9e28aee96dfb5afdc3cdd229fae30c68be868bd27dbf9d88a80b60383b824b9c44e9dc259201a25d42c2aa140d','2026-05-08 09:57:15'),(91,'degree bonafide.jpg','jpeg',88950,'Genuine','01','2e69979316dda226e2a0aa8694774a5b39a3be4906fceba7cd0b6f18d08f247bd0e40ec7ec37ab429dd41bc0cfc44ef4d042ecbeb54329684464aaaa9a18458c','2026-05-09 08:47:27'),(92,'photo.jpg','jpeg',26876,'Genuine','01','fd94155dc4ad883fd035f997cc3c955674c1f85066acc26473198755858fdc2e8cb28bb8e73d2e18207758b90a83092d3bfde51ad877b118f63dafe90b3a6379','2026-05-15 18:03:00'),(93,'minnu project.html',NULL,6686,'Fake','01','5d5ff332b9df8e4dfbb97b996e0a6b562ce64f62415414537f8b50788a6e03dc7a92afceae1bcf0fa8d8b2bd15c6bd8c7b1ddee34c3dd335d51234b40fc8d3e7','2026-05-19 07:16:52'),(94,'minnu project.html',NULL,6686,'Fake','03','5d5ff332b9df8e4dfbb97b996e0a6b562ce64f62415414537f8b50788a6e03dc7a92afceae1bcf0fa8d8b2bd15c6bd8c7b1ddee34c3dd335d51234b40fc8d3e7','2026-05-19 08:12:22');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_activity`
--

DROP TABLE IF EXISTS `login_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_activity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uploaded_by` varchar(20) DEFAULT NULL,
  `login_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_activity`
--

LOCK TABLES `login_activity` WRITE;
/*!40000 ALTER TABLE `login_activity` DISABLE KEYS */;
INSERT INTO `login_activity` VALUES (1,'1','2026-05-12 07:04:31'),(2,'1','2026-05-15 18:02:25'),(3,'1','2026-05-19 04:14:53'),(4,'1','2026-05-19 07:16:34'),(5,'3','2026-05-19 08:12:11'),(6,'1','2026-05-19 10:09:41'),(7,'1','2026-05-19 10:13:36');
/*!40000 ALTER TABLE `login_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `register`
--

DROP TABLE IF EXISTS `register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `register` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `register`
--

LOCK TABLES `register` WRITE;
/*!40000 ALTER TABLE `register` DISABLE KEYS */;
INSERT INTO `register` VALUES (1,'lokesh','patelbandilokesh@gmail.com','scrypt:32768:8:1$gkR4ahWUaGuejlNN$2382f68e92de9af864761b1af6a06785e478c4cf9738eea5703c2aa7a8a420d7b510376406c98190b4ca65c3b5ba41646e5282f876126518083a3ab24c28857b','2026-04-23 06:02:51'),(2,'Minnu','minnuuthkam@gmail.com','scrypt:32768:8:1$iU2axNL1iq8C6ERL$26ebaccf63c58d7a1b6321a6dbf86c3039d12654f47407cded2c29ce1a12cc15a673f41818b2e23f64f9e215c548df15b84b62cb2f901255d0c5e7ab02e3afd9','2026-04-23 07:28:18'),(3,'rashu','rashu@gmail.com','scrypt:32768:8:1$Ksqhi7b2jdTWwYvK$fe79d3c0680035eca4f03bfa5e44894aa126642bcff411a6ae7250db34e09dcc1770e6afaa5958feda0b0819db72dd84b2bc472401f66be4fc694166410d336c','2026-04-23 07:32:23'),(4,'chinnu','chinnu@gmail.com','scrypt:32768:8:1$iSmh7wHEsD17euje$5fe58de38f3c048c4d67574271ed1bdfd1b8ac510fd8707b2d2a8b160159faae41c1de14b1026804beefc945e3ae149882e6841475c284146378367e5b66da9a','2026-04-23 07:44:12'),(5,'vinay','vinay@gmail.com','scrypt:32768:8:1$O8of0WUUVAfSnPpF$742be679945a239f87c2f445fa1a64856fe19b6fa25fb721facf1eb36899853a5cbba4ae79b3dd627324d44fa9fc2774a58a6e65f4ba87beb4a304bf3e0963bc','2026-04-23 07:46:05'),(6,'shiva','shiva@gmail.com','scrypt:32768:8:1$EodpJwKZu5PYrOz7$4ba3b0b71a27849c832565f0c088918c404fde9d802b0b71cadfe8d43c134a406f1a39b69eaac7c0e2c33c70b048c13a80787bf62cf54c871daa1d21cdc1bd31','2026-04-23 08:00:04'),(7,'shiva','shivakumar@gmail.com','scrypt:32768:8:1$6bE0sV4gJJTdCygb$e4c50daf2ed7b5eca8c8108dac51abfc5e8a68a24871b24cae899ccb4308f5b75911f7272a81e4d116b466553b57d223e86d428f8e2c143d86f5f4e0b600a7e2','2026-04-23 08:15:14'),(8,'praveen','praveen@gmail.com','scrypt:32768:8:1$4ntselOdBbN0v1ny$b91d613ec8b24e89e60b7dd073f101e8e4de9f12a29d475c1f10cab7c024bd8d307eaa420b1c8ea33c2938c848a36376e2d33ded5964fb1da6b95d9bfe02c1f4','2026-04-23 08:16:22'),(10,'mahesh','mahesh@gmail.com','scrypt:32768:8:1$5BlFOxN7LwmVAshF$3c208163f164c7b09759a6acfeafd1af6fcc7578986aab1b712c376fa7865907305d5b5767029c97380caf67b14a8c171502b47a621d9c89ec033eddc459fca8','2026-04-23 08:30:32'),(11,'bunny','bunny@gmail.com','scrypt:32768:8:1$XZF82oAOcpdoZSQc$0080efe59880536f99e5934e9a2e34f8ba2af0f80033f50e0ecc6604e60284aeb7838d7467bcfa5f689a3a40959ca475e61649f9abe6272540ea2a84453cad81','2026-04-23 08:41:34'),(12,'anshu','anshu@gmail.com','scrypt:32768:8:1$IAJThJQmA802GDKC$d98aa0146551ad616f608e4dffdd2ac60fd563dac778b26a4dd9c8d1ffbd7f7d2a4bce1e32c21c16387a8093a0dc8e4593b0cdec8732238183214aa8c911d212','2026-04-23 08:55:51'),(13,'rajesh','rajesh@gmail.com','scrypt:32768:8:1$RfbW2fYneCQJvyLA$153ee8c6dc9cf87cf6187689166390e56318421f8573a3afc8f7c153a70e49f66545691e94d3fda898741af229bba67049097ea13cfac4b4673c77f11787cda3','2026-04-29 03:29:05'),(14,'laxmi','laxmi@gmail.com','scrypt:32768:8:1$FGmm8gtQBC7DP2R4$9f5731fcf55fe574e881e5f73dd512a5489a5482b7aeed893f580c74c81980aeaed3df86d383340fbe01e2799bf5da9a412bc1c927cca427ac649056cf7b5115','2026-04-29 04:35:37'),(16,'lokesh','prabhavathi@gmail.com','scrypt:32768:8:1$JIKL30WR1zf6yvzi$ad26f8c6dfc275a082dce7d9982d2a5b8ed91a599ecf6ef41aad06139295412dba59e6c716c6f8429816d3fd3f80c49a11f69d3dbe5ef844dc31ba20532a8337','2026-05-07 07:55:22'),(20,'ravi','ravi@gmail.com','scrypt:32768:8:1$YamhWpYD7gJlwOD9$e660dc3fc41e4b6006f21c2ed1fc0d44c4a1eb30dea675f9cba09373db6f425752a4a772122ebce67aedfff7e236189169ee698764505674a1f215cdc2cfa25e','2026-05-07 08:13:44'),(21,'admin','admin@gmail.com','scrypt:32768:8:1$YIqoyrRi8erHaKwj$4249b425be5e47060c2e64da0538e0a828e39a23f05a917932fc76e166dff388e1620e25dc87611a1ef81530e27f2da070e5c7cbba025cbb99458bd850099289','2026-05-07 11:40:40'),(22,'manu','manu@gmail.com','scrypt:32768:8:1$cQtK6pHzpGFOSLGJ$249fda58f22886a4c29e2d6d8bfe4b70143209f3e258d2c7d01dab7b0e56a6a2cd4a92592aca5200dc4058518c2623795ee2516da18d2078001dfe48a0abb87b','2026-05-08 09:55:51');
/*!40000 ALTER TABLE `register` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-22 12:43:05
