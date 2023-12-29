CREATE DATABASE IF NOT EXISTS taskmasterpro;
USE taskmasterpro;

CREATE TABLE IF NOT EXISTS `User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(32) NOT NULL,
  `email` varchar(255) NOT NULL,
  `profile_picture` longtext,
  `last_name` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
);

CREATE TABLE IF NOT EXISTS `Task` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `deadline` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `public` tinyint(1) DEFAULT NULL,
  `importance` int DEFAULT NULL,
  `is_completed` tinyint(1) DEFAULT '0',
  `description` longtext,
  PRIMARY KEY (`ID`),
  KEY `user_id` (`user_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `task_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`)
);

CREATE TABLE IF NOT EXISTS `Friendships` (
  `friendships_id` int NOT NULL AUTO_INCREMENT,
  `user1_id` int DEFAULT NULL,
  `user2_id` int DEFAULT NULL,
  `status` int DEFAULT '0',
  PRIMARY KEY (`friendships_id`),
  KEY `user1_id` (`user1_id`),
  KEY `user2_id` (`user2_id`),
  CONSTRAINT `friendships_ibfk_1` FOREIGN KEY (`user1_id`) REFERENCES `user` (`id`),
  CONSTRAINT `friendships_ibfk_2` FOREIGN KEY (`user2_id`) REFERENCES `user` (`id`)
);

CREATE USER IF NOT EXISTS 'toto'@'%' IDENTIFIED BY 'toto';
GRANT ALL PRIVILEGES ON taskmasterpro.* TO 'toto'@'%';
FLUSH PRIVILEGES;



