-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.5.8-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for loan_management
CREATE DATABASE IF NOT EXISTS `loan_management` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `loan_management`;

-- Dumping structure for table loan_management.customer
CREATE TABLE IF NOT EXISTS `customer` (
  `CustomerId` int(11) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(50) NOT NULL,
  `customer_phone` varchar(50) DEFAULT NULL,
  `customer_address` varchar(50) NOT NULL,
  `balance` decimal(38,2) NOT NULL,
  PRIMARY KEY (`CustomerId`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Dumping data for table loan_management.customer: ~10 rows (approximately)
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` (`CustomerId`, `customer_name`, `customer_phone`, `customer_address`, `balance`) VALUES
	(1, 'Farrah Dobbie', '3688961901', '49862 Kingsford Junction', 69687.54),
	(2, 'Malcolm Orbell', '8867727382', '385 Lawn Terrace', 55592.51),
	(3, 'Filippa Bucknill', '6677805329', '1898 Michigan Road', 53826.01),
	(4, 'Dido Vanezis', '2887691797', '57689 Myrtle Park', 30581.83),
	(5, 'Annelise Aspland', '2096293966', '3922 Cherokee Place', 87026.91),
	(6, 'Herminia Newby', '8111478402', '19 Chive Center', 5414.47),
	(7, 'Lind Hanley', '7504959822', '7534 Village Green Center', 25921.26),
	(8, 'Mimi Gilhooley', '6594140488', '16033 Pond Avenue', 62834.94),
	(9, 'Ileana Parkes', '1281389203', '095 Warner Hill', 76939.31),
	(10, 'Larissa Yeldham', '2812360584', '220 Shopko Parkway', 15790.59);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;

-- Dumping structure for table loan_management.customerloan
CREATE TABLE IF NOT EXISTS `customerloan` (
  `CustomerLoanId` int(11) NOT NULL AUTO_INCREMENT,
  `CustomerId` int(11) NOT NULL,
  `LoanId` int(11) NOT NULL,
  PRIMARY KEY (`CustomerLoanId`),
  KEY `CustomerLoan_FK1` (`CustomerId`),
  KEY `CustomerLoan_FK2` (`LoanId`),
  CONSTRAINT `CustomerLoan_FK1` FOREIGN KEY (`CustomerId`) REFERENCES `customer` (`CustomerId`),
  CONSTRAINT `CustomerLoan_FK2` FOREIGN KEY (`LoanId`) REFERENCES `loan` (`LoanId`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Dumping data for table loan_management.customerloan: ~10 rows (approximately)
/*!40000 ALTER TABLE `customerloan` DISABLE KEYS */;
INSERT INTO `customerloan` (`CustomerLoanId`, `CustomerId`, `LoanId`) VALUES
	(1, 7, 6),
	(2, 8, 8),
	(3, 8, 7),
	(4, 8, 1),
	(5, 8, 10),
	(6, 7, 9),
	(7, 5, 3),
	(8, 2, 2),
	(9, 4, 4),
	(10, 4, 5);
/*!40000 ALTER TABLE `customerloan` ENABLE KEYS */;

-- Dumping structure for table loan_management.loan
CREATE TABLE IF NOT EXISTS `loan` (
  `LoanId` int(11) NOT NULL AUTO_INCREMENT,
  `loan_amount` decimal(38,2) NOT NULL,
  PRIMARY KEY (`LoanId`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Dumping data for table loan_management.loan: ~10 rows (approximately)
/*!40000 ALTER TABLE `loan` DISABLE KEYS */;
INSERT INTO `loan` (`LoanId`, `loan_amount`) VALUES
	(1, 135532.99),
	(2, 34367.53),
	(3, 45086.74),
	(4, 140123.37),
	(5, 57800.21),
	(6, 13165.14),
	(7, 82062.24),
	(8, 12416.32),
	(9, 17250.83),
	(10, 46431.85);
/*!40000 ALTER TABLE `loan` ENABLE KEYS */;

-- Dumping structure for table loan_management.payment
CREATE TABLE IF NOT EXISTS `payment` (
  `PaymentId` int(11) NOT NULL AUTO_INCREMENT,
  `LoanId` int(11) NOT NULL,
  `payment_date` date NOT NULL,
  `payment_amount` decimal(38,2) NOT NULL,
  PRIMARY KEY (`PaymentId`),
  KEY `CustomerLoan_FK` (`LoanId`),
  CONSTRAINT `CustomerLoan_FK` FOREIGN KEY (`LoanId`) REFERENCES `loan` (`LoanId`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Dumping data for table loan_management.payment: ~10 rows (approximately)
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` (`PaymentId`, `LoanId`, `payment_date`, `payment_amount`) VALUES
	(1, 1, '2022-02-20', 35532.99),
	(2, 6, '2022-03-19', 7818.63),
	(3, 4, '2022-01-12', 74562.54),
	(4, 4, '2022-03-21', 51364.06),
	(5, 3, '2022-01-17', 16363.67),
	(6, 1, '2022-01-03', 26544.58),
	(7, 1, '2022-02-27', 30534.71),
	(8, 9, '2022-02-27', 17250.83),
	(9, 2, '2022-02-19', 34367.53),
	(10, 7, '2022-02-08', 31003.82);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
