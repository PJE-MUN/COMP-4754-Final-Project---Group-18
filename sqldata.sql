CREATE DATABASE  IF NOT EXISTS `hospital_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hospital_db`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital_db
-- ------------------------------------------------------
-- Server version	8.0.40

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
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Patient','Nurse','Doctor') NOT NULL,
  `role_id` int DEFAULT NULL,
  `patient_id` int DEFAULT NULL,
  `nurse_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_patient_id` (`patient_id`),
  CONSTRAINT `fk_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'patient1','$2b$12$SwbGamz8K8gLWSqLymJE5O./QXaiZMTC3WXbLBuSNdEVmXwIIl35q','Patient',1,1,NULL,NULL),(2,'nurse1','$2b$12$7yfuGBbcJloiQM8OgTfwneATGDcYCaHznYyBZBMuoWYBOkB0xJMne','Nurse',2,NULL,1,NULL),(3,'doctor1','$2b$12$TQmd/EAkCPaRbHcEtMTpIuC1a7JnFjX7IiePE1TU6p1XxGLq64/6O','Doctor',3,NULL,NULL,1),(4,'patient2','$2b$12$.WTBw8Vi/vtt5hx8YSKJ9OL1jSKaCRQYsLLOOSMMxC6Z9s9H/tCyS','Patient',NULL,2,NULL,NULL),(5,'doctor2','$2b$12$df15dRkbIn0FbeFyG/fT1uaHB79PRA/ir9xNk5xr5as21QlgYtwQi','Doctor',NULL,NULL,NULL,2),(7,'patient3','$2b$12$i/MEE.yzrUR0oneHe5Iaqu6h7SkuM9TfmXqiDXWL3tXRXuNjk78uK','Patient',NULL,3,NULL,NULL),(8,'nurse2','$2b$12$B3SsGrDcP6NX3Ei6Ic9X8uv6Q7toOn1lzurUZQY5ZPVhkhOU4n.tq','Nurse',NULL,NULL,NULL,NULL),(9,'dihan1','$2b$12$NpkzwfSQgnBlLmYRxHmFeO2DZcBiF/P3k3vx1r8bZxGdaiCN5I4s2','Patient',NULL,1,NULL,NULL);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `time` varchar(8) NOT NULL,
  `reason` text,
  `doctor_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `priority` enum('Low','Medium','High') DEFAULT 'Low',
  `nurse_id` int NOT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `patient_id` (`patient_id`),
  KEY `nurse_id` (`nurse_id`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`) ON DELETE CASCADE,
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `appointment_ibfk_3` FOREIGN KEY (`nurse_id`) REFERENCES `nurse` (`nurse_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,'2024-12-12','4:00 PM','covid',1,1,'High',1),(2,'2024-07-10','5:00 PM','Fever for 4 days',2,2,'Medium',1);
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointment_creation`
--

DROP TABLE IF EXISTS `appointment_creation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment_creation` (
  `creation_id` int NOT NULL AUTO_INCREMENT,
  `nurse_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `appointment_id` int NOT NULL,
  PRIMARY KEY (`creation_id`),
  KEY `nurse_id` (`nurse_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `appointment_id` (`appointment_id`),
  CONSTRAINT `appointment_creation_ibfk_1` FOREIGN KEY (`nurse_id`) REFERENCES `nurse` (`nurse_id`) ON DELETE CASCADE,
  CONSTRAINT `appointment_creation_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`) ON DELETE CASCADE,
  CONSTRAINT `appointment_creation_ibfk_3` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`appointment_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment_creation`
--

LOCK TABLES `appointment_creation` WRITE;
/*!40000 ALTER TABLE `appointment_creation` DISABLE KEYS */;
INSERT INTO `appointment_creation` VALUES (1,1,1,1),(2,1,2,2);
/*!40000 ALTER TABLE `appointment_creation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `nurse_id` int NOT NULL,
  `department_id` int NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `specialty` varchar(100) NOT NULL,
  `hired_date` date NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`doctor_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  KEY `nurse_id` (`nurse_id`),
  CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`nurse_id`) REFERENCES `nurse` (`nurse_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (1,1,1,'John','Doe','Cardiology','2020-06-15','john.doe@example.com','1234567891'),(2,2,2,'Alice','Brown','Neurology','2018-09-23','alice.brown@example.com','0987654322');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nurse`
--

DROP TABLE IF EXISTS `nurse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurse` (
  `nurse_id` int NOT NULL AUTO_INCREMENT,
  `department_id` int NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`nurse_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurse`
--

LOCK TABLES `nurse` WRITE;
/*!40000 ALTER TABLE `nurse` DISABLE KEYS */;
INSERT INTO `nurse` VALUES (1,1,'Jane','Doe','jane.doe@example.com','1234567890'),(2,2,'Emily','Smith','emily.smith@example.com','0987654321');
/*!40000 ALTER TABLE `nurse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `nurse_id` int NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `dob` date NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`),
  KEY `nurse_id` (`nurse_id`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`nurse_id`) REFERENCES `nurse` (`nurse_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,1,'Michael','Johnson','1990-05-12','1234567892','michael.johnson@example.com','A1B2C3'),(2,2,'Sarah','Williams','1985-11-23','0987654323','sarah.williams@example.com','D4E5F6'),(3,2,'Miah','Rahim','1999-11-04','3298479302','miah@rahim@hotmail.com','A1B1T8'),(4,1,'dihan1','na','1999-12-05','8989898989','na@ga.com','a1a2s1');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription`
--

DROP TABLE IF EXISTS `prescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription` (
  `drug_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `doses` int NOT NULL,
  `start_date` date NOT NULL,
  `duration` varchar(50) NOT NULL,
  PRIMARY KEY (`drug_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `prescription_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`) ON DELETE CASCADE,
  CONSTRAINT `prescription_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription`
--

LOCK TABLES `prescription` WRITE;
/*!40000 ALTER TABLE `prescription` DISABLE KEYS */;
INSERT INTO `prescription` VALUES (1,1,1,3,'2024-11-28','2 weeks'),(2,1,2,1,'2024-09-01','1 month');
/*!40000 ALTER TABLE `prescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- View to fetch prescription details
--

CREATE VIEW PrescriptionDetails AS
	SELECT drug_id, doctor_id, patient_id, doses, start_date, duration
		FROM prescription

--
-- Update prescription medical records
--

DELIMITER //
CREATE PROCEDURE UpdatePrescription(
    IN new_drug_id INT,
	IN new_doctor_id INT,
	IN new_patient_id INT,
    IN new_doses INT,
	IN new_start_date DATE,
	IN new_duration TEXT
)
BEGIN
    UPDATE prescription
    SET drug_id = new_drug_id,
        doctor_id = new_doctor_id,
        patient_id = new_patient_id,
        doses = new_doses,
        start_date = new_start_date,
        duration = new_duration
    WHERE drug_id = new_drug_id;
END //
DELIMITER ;

--
-- Table structure for table `drugs`
--

DROP TABLE IF EXISTS `drugs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drugs` (
  `drug_id` int NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`drug_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drugs`
--

LOCK TABLES `drugs` WRITE;
/*!40000 ALTER TABLE `drugs` DISABLE KEYS */;
INSERT INTO `drugs` VALUES (1,'Acetaminophen'),(2,'Buprenorphine'),(3,'Citalopram'),(4,'Tylenol'),(5,'Ibuprofen');
/*!40000 ALTER TABLE `drugs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `procedure`
--

DROP TABLE IF EXISTS `procedures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procedures` (
  `procedure_id` int NOT NULL,
  `appointment_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `procedure_date` date NOT NULL,
  `notes` text NOT NULL,
  PRIMARY KEY (`procedure_id`),
  KEY `appointment_id` (`appointment_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `procedures_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`appointment_id`),
  CONSTRAINT `procedures_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`doctor_id`) ON DELETE CASCADE,
  CONSTRAINT `procedures_ibfk_3` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procedure`
--

LOCK TABLES `procedures` WRITE;
/*!40000 ALTER TABLE `procedures` DISABLE KEYS */;
INSERT INTO `procedures` VALUES (1,1,2,1,'2023-07-10','patient needs post op care'),(2,2,1,2,'2023-09-12','successful procedure'),(3,1,2,3,'2024-07-10','faulty anesthesia machine'),(4,2,1,4,'2024-09-11','Patient was impatient');
/*!40000 ALTER TABLE `procedures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Create a view to fetch procedures details
--

CREATE VIEW ProcedureDetails AS
	SELECT procedure_id, appointment_id, doctor_id, patient_id, procedure_date, notes
		FROM procedures

--
-- Update procedures records
--

DELIMITER //
CREATE PROCEDURE UpdateProcedure(
    IN new_procedure_id INT,
	IN new_appointment_id INT,
	IN new_doctor_id INT,
	IN new_patient_id INT,
	IN new_date DATE,
	IN new_notes TEXT
)
BEGIN
    UPDATE procedures
    SET procedure_id = new_procedure_id,
        appointment_id = new_appointment_id,
        doctor_id = new_doctor_id,
        patient_id = new_patient_id,
        procedure_date = new_date,
        notes = new_notes
    WHERE procedure_id = new_procedure_id;
END //
DELIMITER ;

--
-- Table structure for table `operations`
--

DROP TABLE IF EXISTS `operations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operations` (
  `procedure_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `duration` varchar(50) NOT NULL,
  `cost` int NOT NULL,
  PRIMARY KEY (`procedure_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operations`
--

LOCK TABLES `operations` WRITE;
/*!40000 ALTER TABLE `operations` DISABLE KEYS */;
INSERT INTO `operations` VALUES (1,'Cholecystectomy','2 hours',5000),(2,'Arthroscopy','4 hours',7500),(3,'Mastectomy','30 minutes',2000),(4,'Colostomy','8 hours',12500);
/*!40000 ALTER TABLE `operations` ENABLE KEYS */;
UNLOCK TABLES;








/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-24 22:11:12