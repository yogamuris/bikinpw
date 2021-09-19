CREATE DATABASE bikinpw_shortener;
use bikinpw_shortener;

DROP TABLE IF EXISTS `urlshortener`;

CREATE TABLE `urlshortener` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `longurl` varchar(255) NOT NULL,
  `shorturl` varchar(255) NOT NULL,
  `tanggal` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;