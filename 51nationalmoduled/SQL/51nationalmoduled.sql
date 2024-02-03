-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-02-03 13:53:29
-- 伺服器版本： 10.4.27-MariaDB
-- PHP 版本： 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `51nationalmoduled`
--

-- --------------------------------------------------------

--
-- 資料表結構 `ads`
--

CREATE TABLE `ads` (
  `id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `expired_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- 資料表結構 `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `status` enum('APPROVE','REJECT') NOT NULL,
  `applied_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- 資料表結構 `houses`
--

CREATE TABLE `houses` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `price` int(11) NOT NULL,
  `square` mediumint(9) NOT NULL,
  `room` mediumint(9) NOT NULL,
  `floor` mediumint(9) NOT NULL,
  `total_floor` mediumint(9) NOT NULL,
  `age` mediumint(9) NOT NULL,
  `address` text NOT NULL,
  `publised_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- 資料表結構 `images`
--

CREATE TABLE `images` (
  `houses_id` int(11) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `image` longtext NOT NULL,
  `is_cover` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `role` enum('ADMIN','USER') NOT NULL,
  `token` char(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `nickname`, `role`, `token`) VALUES
(1, 'admin@localhost', '$2b$12$Qa1MDKBFyluXuHtMLWzFnufuyOunyBR//96VINbT8p/T2GB/MBfv.', 'admin', 'ADMIN', '7ba684f146c9445720e4b9a8d6ed775de4804bc2dbe01fb6490b8cce05db9f43'),
(2, 'user1@localhost', '$2b$12$Tr9QubdwZ8Poak/h3Ua9TuD5JsazAqo/rV3VM85lBLG2dXoojSyJK', 'user1', 'USER', ''),
(3, 'user2@localhost', '$2b$12$/rJd3Kz7XUhs2yn3/C3Fo.lv2/OHDETkYRXuYJHV3hd0UMp/eSOLu', 'user2', 'USER', ''),
(4, 'user3@localhost', '$2b$12$Aj1mVPxlERwZTpN9QP6o1uGqlKJ8gmAAcnJdjf8mgI0FHPoPJIkCi', 'user3', 'USER', ''),
(5, 'user4@localhost', '$2b$12$cANyyRXoQvneDmk7bakk5ueT3/gPtUySBBnJcFpORhBtkq5NFb3cS', 'user4', 'USER', ''),
(6, 'user5@localhost', '$2b$12$SYhH1xMBQrMFRy2xESVui.WTtBfb8FGSl6lTMoiuAn43Nit2NHCke', 'user5', 'USER', '');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `ads`
--
ALTER TABLE `ads`
  ADD PRIMARY KEY (`id`),
  ADD KEY `house_id` (`house_id`);

--
-- 資料表索引 `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `house_id` (`house_id`);

--
-- 資料表索引 `houses`
--
ALTER TABLE `houses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `images`
--
ALTER TABLE `images`
  ADD KEY `houses_id` (`houses_id`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `ads`
--
ALTER TABLE `ads`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `houses`
--
ALTER TABLE `houses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `ads`
--
ALTER TABLE `ads`
  ADD CONSTRAINT `ads_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `houses` (`id`);

--
-- 資料表的限制式 `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `houses` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `houses`
--
ALTER TABLE `houses`
  ADD CONSTRAINT `houses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- 資料表的限制式 `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`houses_id`) REFERENCES `houses` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
