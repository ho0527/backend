-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-01-30 13:50:04
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
-- 資料庫： `45regional`
--

-- --------------------------------------------------------

--
-- 資料表結構 `data`
--

CREATE TABLE `data` (
  `id` int(11) NOT NULL,
  `userid` text NOT NULL,
  `move` text NOT NULL,
  `movetime` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- 傾印資料表的資料 `data`
--

INSERT INTO `data` (`id`, `userid`, `move`, `movetime`) VALUES
(1, '1', '登入', '2023-12-17 17:19:39'),
(2, '49', '登入', '2023-12-17 18:02:33'),
(3, '1', '登入', '2023-12-18 12:29:54'),
(4, '1', '登入', '2023-12-18 12:48:48'),
(5, '1', '登入', '2023-12-30 14:43:30'),
(6, '1', '登入', '2024-01-09 13:38:42'),
(7, '51', '登入', '2024-01-09 13:41:57'),
(8, '51', '登入', '2024-01-09 13:42:19'),
(9, '1', '登入', '2024-01-15 18:12:03');

-- --------------------------------------------------------

--
-- 資料表結構 `todo`
--

CREATE TABLE `todo` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `starttime` text NOT NULL,
  `endtime` text NOT NULL,
  `deal` text NOT NULL,
  `priority` text NOT NULL,
  `description` text NOT NULL,
  `createtime` text NOT NULL,
  `updatetime` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- 傾印資料表的資料 `todo`
--

INSERT INTO `todo` (`id`, `title`, `starttime`, `endtime`, `deal`, `priority`, `description`, `createtime`, `updatetime`) VALUES
(2, 'work', '00', '09', '處理中', '最速件', '123', '2024-01-06 22:40:53', '2024-01-20 18:40:46'),
(3, 'work', '10', '17', '處理中', '最速件', '', '2024-01-06 22:42:03', '2024-01-20 18:41:56'),
(4, 'work', '20', '22', '未處理', '普通', '', '2024-01-08 20:10:45', '2024-01-09 19:26:32');

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `name` text NOT NULL,
  `number` text NOT NULL,
  `permission` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `name`, `number`, `permission`) VALUES
(1, 'admin', '1234', '超級管理者', '0000', '管理者'),
(49, 'test1', '###', '45674dfg', '0048', '一般使用者'),
(51, 'todo', '1234', '一般使用者', '0050', '一般使用者');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `data`
--
ALTER TABLE `data`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `todo`
--
ALTER TABLE `todo`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `data`
--
ALTER TABLE `data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `todo`
--
ALTER TABLE `todo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
