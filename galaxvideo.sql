-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           8.4.0 - MySQL Community Server - GPL
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para galaxvideo
CREATE DATABASE IF NOT EXISTS `galaxvideo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `galaxvideo`;

-- Copiando estrutura para tabela galaxvideo.favoritos
CREATE TABLE IF NOT EXISTS `favoritos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_Id` int NOT NULL,
  `filme_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_fav` (`usuario_Id`),
  KEY `fk_filme_fav` (`filme_id`),
  CONSTRAINT `fk_filme_fav` FOREIGN KEY (`filme_id`) REFERENCES `filmes` (`idFilme`),
  CONSTRAINT `fk_user_fav` FOREIGN KEY (`usuario_Id`) REFERENCES `usuario` (`idUser`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Copiando estrutura para tabela galaxvideo.filmes
CREATE TABLE IF NOT EXISTS `filmes` (
  `idFilme` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nomeFilme` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `AnoLanc` year NOT NULL,
  `Categoria` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `imagem` text COLLATE utf8mb4_general_ci NOT NULL,
  `Trailer` text COLLATE utf8mb4_general_ci NOT NULL,
  `Classificação` char(5) COLLATE utf8mb4_general_ci NOT NULL,
  `Sinopse` text COLLATE utf8mb4_general_ci NOT NULL,
  `NotaPublico` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`idFilme`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela galaxvideo.filmes: ~14 rows (aproximadamente)
INSERT IGNORE INTO `filmes` (`idFilme`, `nomeFilme`, `AnoLanc`, `Categoria`, `imagem`, `Trailer`, `Classificação`, `Sinopse`, `NotaPublico`) VALUES
	(1, 'Até o Ultimo Homem', '2016', 'Ação', 'https://image.tmdb.org/t/p/w400/k7hj6dAgCTzjaelpC1hdGruXOW9.jpg', 'https://www.youtube.com/watch?v=4s4UCxCv_OE', '+16', 'Desmond T. Doss, foi o médico do Exército Americano da Segunda Guerra Mundial, que serviu durante a Batalha de Okinawa, se recusando a matar pessoas, tornando-se o primeiro homem da história americana a receber a Medalha de Honra sem disparar um tiro.', '9,6'),
	(2, 'Um Filme Minecraft', '2025', 'Comédia', 'https://image.tmdb.org/t/p/w400/4VtkIaj76TpQNfhDHXQDdT9uBN5.jpg', 'https://www.youtube.com/watch?v=EVKYAAES6JQ', 'Livre', 'Quatro desajustados enfrentam problemas comuns do dia a dia quando, de repente, são sugados por um portal misterioso para o Overworld: uma terra fascinante e cúbica, movida pela imaginação. Para voltarem para casa, eles precisarão dominar esse novo mundo enquanto embarcam em uma jornada mágica ao lado de um crafter experiente e inesperado: Steve.', '8,0'),
	(3, 'Godzilla 2', '2019', 'Ficção Cientifica', 'https://image.tmdb.org/t/p/w400/2umU3r6V4V2gTmSnZJmH61nTorF.jpg', 'https://www.youtube.com/watch?v=1BWV-3YEp6k', '+12', 'Membros da agência Monarch enfrentam monstros gigantescos, incluindo o poderoso Godzilla, que entra em choque com Mothra, Rodan e seu maior inimigo, King Ghidorah, o monstro de três cabeças. Essas antigas superespécies disputam a supremacia, deixando a própria existência da humanidade em risco.', '7.8'),
	(4, 'Godzilla vs. Kong', '2021', 'Ficção Cientifica', 'https://image.tmdb.org/t/p/w400/teW53VSLdZMMSmkn5xBBowu3tEr.jpg', 'https://www.youtube.com/watch?v=ur0rw-SaFmU', '+12', 'Em uma época em que os monstros andam na Terra, a luta da humanidade por seu futuro coloca Godzilla e Kong em rota de colisão que verá as duas forças mais poderosas da natureza no planeta se confrontarem em uma batalha espetacular para as idades. Enquanto Monarch embarca em uma missão perigosa em terreno desconhecido e descobre pistas sobre as origens dos Titãs, uma conspiração humana ameaça tirar as criaturas, boas e más, da face da terra para sempre.', '7.3'),
	(5, 'Vingadores Ultimato', '2019', 'Ação', 'https://image.tmdb.org/t/p/w400/q6725aR8Zs4IwGMXzZT8aC8lh41.jpg', 'https://www.youtube.com/watch?v=spJoZReeIeQ', '+12', 'Após os eventos devastadores de "Vingadores: Guerra Infinita", o universo está em ruínas devido aos esforços do Titã Louco, Thanos. Com a ajuda de aliados remanescentes, os Vingadores devem se reunir mais uma vez a fim de desfazer as ações de Thanos e restaurar a ordem no universo de uma vez por todas, não importando as consequências.', '9.7'),
	(6, 'Gente Grande 2', '2013', 'Comédia', 'https://image.tmdb.org/t/p/w400/fKYW0oKPvy6HF8x5egL1ljC36xb.jpg', '', '+12', 'Lenny Feder e sua família se mudam para sua cidade natal para ficar perto dos amigos, mas acabam tendo que enfrentar alguns fantasmas do passado, como a covardia diante de valentões e o famigerado bullying na escola.', '8.6'),
	(7, 'Nascido para Matar', '1987', 'Ação', 'https://image.tmdb.org/t/p/w400/qHm54HjL1F6CFVyYOz6Q2HAPTfS.jpg ', 'https://www.youtube.com/watch?v=n2i917l5RFc', '+16', 'Um sargento treina de forma fanática e sádica os recrutas em uma base de treinamentos, na intenção de transformá-los em máquinas de guerra para combater na Guerra do Vietnã. Após serem transformados em fuzileiros navais, eles são enviados para a guerra e quando lá chegam se deparam com seus horrores.', '8.1'),
	(8, 'Halloween ', '2018', 'Terror', 'https://image.tmdb.org/t/p/w400/cdvd03HL4JoTd9yKvQ10dcmwi8c.jpg', 'https://www.youtube.com/watch?v=Kkdddjea9kk', '+18', 'Quatro década depois de escapar do ataque de Michael Myers em uma noite de Halloween, Laurie Strode precisa confrontar o assassino mascarado mais uma vez após ele escapar de uma instituição. Mas, agora Laurie está preparada.', '7.5'),
	(9, 'Alien Romulus', '2024', 'Ficção Cientifica', 'https://image.tmdb.org/t/p/w400/jB0W9tn4w07MFn7sTfqRTBLVytF.jpg', 'https://www.youtube.com/watch?v=IPMxNH2sz7E', '+14', 'Enquanto vasculham as profundezas de uma estação espacial abandonada, um grupo de jovens colonizadores espaciais se depara com a forma de vida mais aterrorizante do universo.', '8.3'),
	(10, 'Transformers 4', '2014', 'Ação', 'https://image.tmdb.org/t/p/w400/cLNIRQ2oyJhaUId41aGmSDfD5MI.jpg', 'https://www.youtube.com/watch?v=yrE6f7ynX0g', '+12', 'Após a batalha entre os Autobots e os Decepticons, que arrasou Chicago, os gigantescos robôs alienígenas desapareceram. Atualmente, eles são caçados pelos humanos, que não desejam passar por apuros novamente. Porém, enquanto a humanidade tenta se recuperar dessa terrível batalha, uma nova ameaça paira sobre a Terra.', '6.8'),
	(11, 'Homem-Aranha: Sem Volta Para Casa', '2021', 'Ação', 'https://image.tmdb.org/t/p/w400/8qBccgSj0Ru9Odm1Mjv82cxDr7l.jpg', 'https://www.youtube.com/watch?v=bHzGeci_8wc', '+12', 'Peter Parker é desmascarado e não consegue mais separar sua vida normal dos grandes riscos de ser um super-herói. Quando ele pede ajuda ao Doutor Estranho, os riscos se tornam ainda mais perigosos, e o forçam a descobrir o que realmente significa ser o Homem-Aranha...', '9.1'),
	(12, 'Capitão América 4', '2025', 'Ação', 'https://image.tmdb.org/t/p/w400/t81XT7pvqOIRwZyJ51LADDdPQ5p.jpg', 'https://www.youtube.com/watch?v=U7JG6FMoEdM', '+14', 'Após se encontrar com o recém-eleito presidente dos EUA, Thaddeus Ross, Sam se vê no meio de um incidente internacional. Ele deve descobrir o motivo por trás de uma conspiração global nefasta antes que o verdadeiro gênio faça o mundo inteiro ser dominado pelo vermelho.', '7.5'),
	(13, ' Mufasa: O Rei Leão', '2024', 'Aventura', 'https://image.tmdb.org/t/p/w400/iMVuv6Gz5fj7vZ51IjRF3AiW87y.jpg', 'https://www.youtube.com/watch?v=3H9IG_4liiI', '+10', 'Acompanhe a história épica da ascensão improvável do amado rei das Terras do Reino. Órfão e sozinho, Mufasa se perde até encontrar Taka, herdeiro de uma linhagem real. Isso dá início a uma jornada épica que testa os laços entre os dois enquanto enfrentam um inimigo mortal.', '8.8'),
	(14, 'Sempre ao Seu Lado', '2009', 'Drama', 'https://image.tmdb.org/t/p/w400/jVTFkYhlbW7P3YxoA2rsF10nx2T.jpg', 'https://www.youtube.com/watch?v=UFY8vW5IedY', 'livre', 'Um gênio da computação invade sistemas secretos do governo.', '9.0');

-- Copiando estrutura para tabela galaxvideo.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `idUser` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `Email` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `senha` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`idUser`),
  UNIQUE KEY `Usuario` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela galaxvideo.usuario: ~2 rows (aproximadamente)
INSERT IGNORE INTO `usuario` (`idUser`, `Nome`, `Email`, `senha`) VALUES
	(1, 'Matheus Guilherme dos Santos de Lima', 'matheusguilherme06062005@gmail.com', 'matheusgalax'),
	(2, 'Murilo Lustosa', 'murilindosgame@gmail.com', 'murilin'),
	

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
