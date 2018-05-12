/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : localhost:3306
 Source Schema         : car

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 12/05/2018 10:55:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for base_tuhu_car
-- ----------------------------
DROP TABLE IF EXISTS `base_tuhu_car`;
CREATE TABLE `base_tuhu_car` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `product_id` varchar(60) NOT NULL,
  `remote_logo` varchar(255) DEFAULT NULL,
  `brand_name` varchar(60) DEFAULT NULL,
  `factory_name` varchar(60) DEFAULT NULL,
  `is_baoyang` tinyint(1) NOT NULL DEFAULT '0',
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2308 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for base_tuhu_car_brand
-- ----------------------------
DROP TABLE IF EXISTS `base_tuhu_car_brand`;
CREATE TABLE `base_tuhu_car_brand` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `remote_logo` varchar(255) DEFAULT NULL,
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for base_tuhu_car_displacement
-- ----------------------------
DROP TABLE IF EXISTS `base_tuhu_car_displacement`;
CREATE TABLE `base_tuhu_car_displacement` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` varchar(60) NOT NULL,
  `displacement` varchar(20) NOT NULL,
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`,`displacement`)
) ENGINE=InnoDB AUTO_INCREMENT=4160 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for base_tuhu_car_displacement2year
-- ----------------------------
DROP TABLE IF EXISTS `base_tuhu_car_displacement2year`;
CREATE TABLE `base_tuhu_car_displacement2year` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` varchar(60) NOT NULL,
  `displacement` varchar(20) NOT NULL,
  `year` smallint(3) NOT NULL,
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`,`displacement`,`year`)
) ENGINE=InnoDB AUTO_INCREMENT=21513 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for base_tuhu_car_version
-- ----------------------------
DROP TABLE IF EXISTS `base_tuhu_car_version`;
CREATE TABLE `base_tuhu_car_version` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `t_id` int(10) NOT NULL DEFAULT '0',
  `product_id` varchar(60) NOT NULL,
  `displacement` varchar(20) NOT NULL,
  `year` smallint(3) NOT NULL,
  `accessory_data` text,
  `maintenance_plan_data` text,
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `t_id` (`t_id`)
) ENGINE=InnoDB AUTO_INCREMENT=93704 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for base_tuhu_spider_logs
-- ----------------------------
DROP TABLE IF EXISTS `base_tuhu_spider_logs`;
CREATE TABLE `base_tuhu_spider_logs` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `page_name` varchar(100) DEFAULT NULL,
  `page_uid` varchar(64) DEFAULT NULL,
  `page_url` varchar(4000) DEFAULT NULL,
  `data_uid` varchar(64) DEFAULT NULL,
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_page_uid` (`page_uid`)
) ENGINE=InnoDB AUTO_INCREMENT=28166 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
