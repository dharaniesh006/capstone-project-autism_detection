-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 29, 2024 at 07:20 AM
-- Server version: 5.6.12-log
-- PHP Version: 5.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `autism`
--
CREATE DATABASE IF NOT EXISTS `autism` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `autism`;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `Name` varchar(50) NOT NULL,
  `MailId` varchar(50) NOT NULL,
  `MobileNo` varchar(15) NOT NULL,
  `UserId` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`Name`, `MailId`, `MobileNo`, `UserId`, `Password`) VALUES
('kumar', 'kumar@gmail.com', '9995612345', 'kumar', 'kumar'),
('karthik', 'karthik@gmail.com', '9994512345', 'karthik', 'karthik'),
('vicky', 'vicky@gmail.com', '982736434', 'vi', 'vi'),
('karan', 'karan@gmail.com', '9782364434', 'ka', 'ka'),
('mano', 'mano@gmail.com', '9827364341', 'mano', 'mano');

-- --------------------------------------------------------

--
-- Table structure for table `vfiles`
--

CREATE TABLE IF NOT EXISTS `vfiles` (
  `vid` int(11) NOT NULL AUTO_INCREMENT,
  `vpath` text NOT NULL,
  `vdescr` text NOT NULL,
  PRIMARY KEY (`vid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `vfiles`
--

INSERT INTO `vfiles` (`vid`, `vpath`, `vdescr`) VALUES
(12, '4.mp4', 'autism starting stage');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
