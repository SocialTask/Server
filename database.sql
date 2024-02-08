-- --------------------------------------------------------
-- Host:                         SocialTask
-- Versión del servidor:         8.0.29-21 - Percona Server (GPL), Release 21, Revision c59f87d2854
-- SO del servidor:              Linux
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura para tabla socialtask.follows
CREATE TABLE IF NOT EXISTS `follows` (
  `follower_id` int NOT NULL,
  `followed_id` int NOT NULL,
  `read_status` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla socialtask.posts
CREATE TABLE IF NOT EXISTS `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `img_raw` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `img_compressed` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `video_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `video_thumbnail` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `text` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla socialtask.tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `TaskID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Category` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Feature1` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Feature2` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Feature3` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Explanation` text COLLATE utf8mb4_general_ci,
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Status` int DEFAULT '1',
  PRIMARY KEY (`TaskID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla socialtask.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `profile_pic_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `followers_count` int DEFAULT '0',
  `following_count` int DEFAULT '0',
  `privacy_setting` varchar(10) COLLATE utf8mb4_general_ci DEFAULT 'public',
  `made_tasks` int DEFAULT '0',
  `points` int DEFAULT '0',
  `verified` tinyint(1) DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cover_photo_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla socialtask.user_votes
CREATE TABLE IF NOT EXISTS `user_votes` (
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  `vote_type` enum('upvote','downvote') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `read_status` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
