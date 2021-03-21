-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Gép: 127.0.0.1
-- Létrehozás ideje: 2021. Már 21. 14:39
-- Kiszolgáló verziója: 10.4.17-MariaDB
-- PHP verzió: 7.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Adatbázis: `cida`
--

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `dobas`
--

CREATE TABLE `dobas` (
  `player_id` int(11) NOT NULL,
  `round_number` int(11) NOT NULL,
  `points` int(11) NOT NULL,
  `leg_id` int(11) NOT NULL,
  `set_id` int(11) NOT NULL,
  `match_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `matches`
--

CREATE TABLE `matches` (
  `match_id` int(11) NOT NULL,
  `leg_id` int(11) NOT NULL,
  `set_id` int(11) NOT NULL,
  `winner_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `match_settings`
--

CREATE TABLE `match_settings` (
  `match_id` int(11) NOT NULL,
  `player1_id` int(11) NOT NULL,
  `player2_id` int(11) NOT NULL,
  `variant` varchar(25) COLLATE utf8_hungarian_ci NOT NULL,
  `sets` int(11) NOT NULL,
  `legsperset` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `network`
--

CREATE TABLE `network` (
  `server_ip` varchar(20) COLLATE utf8_hungarian_ci NOT NULL,
  `server_port` int(11) NOT NULL,
  `station_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

--
-- A tábla adatainak kiíratása `network`
--

INSERT INTO `network` (`server_ip`, `server_port`, `station_id`) VALUES
('127.0.0.1', 9999, 1);

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `players`
--

CREATE TABLE `players` (
  `player_id` int(11) NOT NULL,
  `player_name` varchar(35) COLLATE utf8_hungarian_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

--
-- A tábla adatainak kiíratása `players`
--

INSERT INTO `players` (`player_id`, `player_name`) VALUES
(1, 'Laci'),
(2, 'Fecó'),
(3, 'Jani'),
(4, 'Reni'),
(5, 'Czigány János'),
(6, 'Urr László'),
(7, 'Czigány Dávid'),
(8, 'Guba Ferenc'),
(9, 'Varjú Nándor'),
(10, 'Nagy Gábod'),
(19, 'Totya');

--
-- Indexek a kiírt táblákhoz
--

--
-- A tábla indexei `match_settings`
--
ALTER TABLE `match_settings`
  ADD PRIMARY KEY (`match_id`);

--
-- A tábla indexei `players`
--
ALTER TABLE `players`
  ADD PRIMARY KEY (`player_id`);

--
-- A kiírt táblák AUTO_INCREMENT értéke
--

--
-- AUTO_INCREMENT a táblához `match_settings`
--
ALTER TABLE `match_settings`
  MODIFY `match_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=988553;

--
-- AUTO_INCREMENT a táblához `players`
--
ALTER TABLE `players`
  MODIFY `player_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
