-- phpMyAdmin SQL Dump
-- version 4.8.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2018 at 06:54 PM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 7.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `finishedexp`
--

CREATE TABLE `finishedexp` (
  `subjectid` int(5) UNSIGNED DEFAULT NULL,
  `participant` int(6) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ipaddr`
--

CREATE TABLE `ipaddr` (
  `participant` int(6) UNSIGNED NOT NULL,
  `ips` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `subjectsavail`
--

CREATE TABLE `subjectsavail` (
  `subjectid` int(5) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `subjectsavail`
--

INSERT INTO `subjectsavail` (`subjectid`) VALUES
(3),
(8),
(9);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `finishedexp`
--
ALTER TABLE `finishedexp`
  ADD KEY `participant` (`participant`);

--
-- Indexes for table `ipaddr`
--
ALTER TABLE `ipaddr`
  ADD PRIMARY KEY (`participant`);

--
-- Indexes for table `subjectsavail`
--
ALTER TABLE `subjectsavail`
  ADD UNIQUE KEY `subjectid` (`subjectid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ipaddr`
--
ALTER TABLE `ipaddr`
  MODIFY `participant` int(6) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `finishedexp`
--
ALTER TABLE `finishedexp`
  ADD CONSTRAINT `finishedexp_ibfk_1` FOREIGN KEY (`participant`) REFERENCES `ipaddr` (`participant`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
