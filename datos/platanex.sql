-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-05-2023 a las 21:22:33
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `platanex`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caja`
--

CREATE TABLE `caja` (
  `idEmbarque` int(11) NOT NULL COMMENT 'Identificador para cada embarque insertado',
  `cantidad` double NOT NULL COMMENT 'Cantidad de cajas que se producieron',
  `precio` double NOT NULL COMMENT 'Precio por caja segun la calidad',
  `pagos_idpago` int(11) NOT NULL,
  `calidad_idcalidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `caja`
--

INSERT INTO `caja` (`idEmbarque`, `cantidad`, `precio`, `pagos_idpago`, `calidad_idcalidad`) VALUES
(1, 62, 2790, 1, 2),
(2, 80, 4800, 2, 1),
(3, 67, 3015, 3, 2),
(4, 100, 4500, 4, 2),
(5, 93, 5580, 5, 1),
(6, 72, 4260, 4, 1),
(7, 51, 2295, 7, 2),
(8, 89, 4005, 8, 2),
(9, 98, 5880, 9, 1),
(10, 61, 2745, 10, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calculos`
--

CREATE TABLE `calculos` (
  `semana` int(11) NOT NULL,
  `cantidadCinta` double NOT NULL,
  `cantidadCaja` double NOT NULL,
  `ratio` double NOT NULL,
  `estimacion` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `calculos`
--

INSERT INTO `calculos` (`semana`, `cantidadCinta`, `cantidadCaja`, `ratio`, `estimacion`) VALUES
(1, 123, 62, 1.9838709677419355, 80.14634146341463),
(2, 159, 80, 1.9875, 66.91823899371069),
(3, 133, 67, 1.9850746268656716, 100.75187969924812),
(4, 200, 100, 2, 93),
(5, 186, 93, 2, 70.5),
(6, 141, 71, 1.9859154929577465, 50.858156028368796),
(7, 101, 51, 1.9803921568627452, 89.37623762376238),
(8, 177, 89, 1.9887640449438202, 98.05084745762711),
(9, 195, 98, 1.989795918367347, 61.31282051282051),
(10, 122, 61, 2, 86.5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calidad`
--

CREATE TABLE `calidad` (
  `idcalidad` int(11) NOT NULL COMMENT 'Identificador de la calidad que se ingresa.',
  `tipo` varchar(45) NOT NULL COMMENT 'Tipo de produccion sale de la finca segun la calidad'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `calidad`
--

INSERT INTO `calidad` (`idcalidad`, `tipo`) VALUES
(1, 'ExportaciÃ³n'),
(2, 'Nacional');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cosecha`
--

CREATE TABLE `cosecha` (
  `semana` int(11) NOT NULL COMMENT 'Semana en la que se pusieron las cintas',
  `colorCinta` varchar(45) NOT NULL COMMENT 'Color de la cinta que se esta cosechando',
  `ubicacion` int(11) NOT NULL COMMENT 'Identifica el lote en donde se puso dicha la cinta',
  `cantidadCinta` double NOT NULL COMMENT 'Cantidad de cinta que se puso',
  `pagos_idpago` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `cosecha`
--

INSERT INTO `cosecha` (`semana`, `colorCinta`, `ubicacion`, `cantidadCinta`, `pagos_idpago`) VALUES
(2, 'verde', 1, 159, 2),
(3, 'azulada', 1, 133, 4),
(5, 'rojo', 1, 186, 5),
(6, 'amarillaaa', 1, 141, 3),
(7, 'negro', 1, 101, 7),
(8, 'blanco', 1, 177, 8),
(9, 'cafe', 1, 195, 9),
(10, 'gris', 1, 122, 10),
(11, 'habano', 1, 173, 9),
(12, 'magenta', 1, 123, 9),
(13, 'rojo', 1, 145, 7),
(14, 'asdsad', 1, 134, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `exportacion`
--

CREATE TABLE `exportacion` (
  `idExportacion` int(11) NOT NULL COMMENT 'Identificador de cada registro de exportacion.',
  `ratio` double NOT NULL COMMENT 'Dato que relaciona la cantidad de cajas que se producen con la cantidad de racimos cosechados, es decir, cuantos racimos se necesitaron para producir x cajas. De esta forma.\n\ncantidadCinta/cantidadCajas',
  `indicePerdida` double NOT NULL COMMENT 'Este indice relaciona, la cantidad de cinta que se puso prematuramente vs la que se cosecho, de esta forma:\n\ncintaPrematura - cintaCosechada',
  `estimacion` double NOT NULL COMMENT 'En este dato se relaciona el ratio con la cantidad de cintas puestas prematuramente en la semana siguiente a la que se calculo el ratio, para asi poder dar un dato estimado de cuantas cajas se podran producir basados en los datos de la semana anterior.\n\nse calcula de esta forma: cintaPrematura/ratio',
  `caja_idEmbarque` int(11) NOT NULL,
  `cosecha_semana` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login`
--

CREATE TABLE `login` (
  `id` int(11) NOT NULL,
  `usuario` varchar(200) NOT NULL,
  `contraseña` varchar(200) NOT NULL,
  `tipo` bit(1) NOT NULL DEFAULT b'0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `login`
--

INSERT INTO `login` (`id`, `usuario`, `contraseña`, `tipo`) VALUES
(1, 'anderson', '1234', b'0'),
(2, 'felipe', '1234', b'1'),
(5, '', '', b'0'),
(6, '', '', b'1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `idpago` int(11) NOT NULL COMMENT 'Identificador de cada pago a realizar',
  `pago` double NOT NULL COMMENT 'Operacion que nos da el total a pagar que esta dado por la multiplicacion entre la tarifa por horas que cuesta el trabajo y las horas que se trabajaron.\n\ntarifa x horas',
  `trabajo_idtrabajo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`idpago`, `pago`, `trabajo_idtrabajo`) VALUES
(1, 400, 1),
(2, 1500, 2),
(3, 2500, 3),
(4, 1200, 4),
(5, 1000, 5),
(6, 1500, 6),
(7, 800, 7),
(8, 2200, 8),
(9, 800, 9),
(10, 10, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipotrabajo`
--

CREATE TABLE `tipotrabajo` (
  `idtipoTrabajo` int(11) NOT NULL,
  `nombreTrabajo` varchar(45) NOT NULL,
  `tarifa` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `tipotrabajo`
--

INSERT INTO `tipotrabajo` (`idtipoTrabajo`, `nombreTrabajo`, `tarifa`) VALUES
(1, 'encintar', 200),
(2, 'embarque', 500);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajador`
--

CREATE TABLE `trabajador` (
  `cedula` varchar(15) NOT NULL COMMENT 'Identificador de cada trabajador registrado',
  `nombreTrabajador` varchar(45) NOT NULL COMMENT 'Nombre del trabajador',
  `apellido` varchar(45) NOT NULL COMMENT 'Apellido del trabajador'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `trabajador`
--

INSERT INTO `trabajador` (`cedula`, `nombreTrabajador`, `apellido`) VALUES
('1000332654', 'Jose', 'Murillo'),
('1000557163', 'Alejandro', 'Cadavid'),
('1002354965', 'Juan', 'Perez'),
('1333652148', 'Felipe', 'Jimenez'),
('1530214896', 'Mateo', 'Restrepo'),
('2351648953', 'Ximena', 'Arredondo'),
('23615420', 'German', 'Garmendia'),
('32650147', 'Sebastian', 'Martinez'),
('98362415', 'Raul', 'Hinestroza'),
('98509642', 'Pablo', 'Maya');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajo`
--

CREATE TABLE `trabajo` (
  `idtrabajo` int(11) NOT NULL COMMENT 'Identificador para cada registro de un trabajo',
  `horas` double NOT NULL COMMENT 'Cantidad de horas que se realiza el trabajo',
  `tipoTrabajo_idtipoTrabajo` int(11) NOT NULL,
  `trabajador_cedula` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `trabajo`
--

INSERT INTO `trabajo` (`idtrabajo`, `horas`, `tipoTrabajo_idtipoTrabajo`, `trabajador_cedula`) VALUES
(1, 2, 1, '1000557163'),
(2, 3, 2, '1002354965'),
(3, 5, 2, '98362415'),
(4, 6, 1, '98509642'),
(5, 2, 2, '2351648953'),
(6, 3, 2, '1530214896'),
(7, 4, 1, '23615420'),
(8, 11, 1, '1333652148'),
(9, 4, 1, '32650147'),
(10, 2500, 2, '1000332654');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `caja`
--
ALTER TABLE `caja`
  ADD PRIMARY KEY (`idEmbarque`),
  ADD KEY `fk_caja_pagos1_idx` (`pagos_idpago`),
  ADD KEY `fk_caja_calidad1_idx` (`calidad_idcalidad`);

--
-- Indices de la tabla `calculos`
--
ALTER TABLE `calculos`
  ADD PRIMARY KEY (`semana`);

--
-- Indices de la tabla `calidad`
--
ALTER TABLE `calidad`
  ADD PRIMARY KEY (`idcalidad`);

--
-- Indices de la tabla `cosecha`
--
ALTER TABLE `cosecha`
  ADD PRIMARY KEY (`semana`),
  ADD KEY `fk_cosecha_pagos1_idx` (`pagos_idpago`);

--
-- Indices de la tabla `exportacion`
--
ALTER TABLE `exportacion`
  ADD PRIMARY KEY (`idExportacion`,`caja_idEmbarque`,`cosecha_semana`),
  ADD KEY `fk_exportacion_caja1_idx` (`caja_idEmbarque`),
  ADD KEY `fk_exportacion_cosecha1_idx` (`cosecha_semana`);

--
-- Indices de la tabla `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`idpago`),
  ADD KEY `fk_pagos_trabajo1_idx` (`trabajo_idtrabajo`);

--
-- Indices de la tabla `tipotrabajo`
--
ALTER TABLE `tipotrabajo`
  ADD PRIMARY KEY (`idtipoTrabajo`);

--
-- Indices de la tabla `trabajador`
--
ALTER TABLE `trabajador`
  ADD PRIMARY KEY (`cedula`);

--
-- Indices de la tabla `trabajo`
--
ALTER TABLE `trabajo`
  ADD PRIMARY KEY (`idtrabajo`),
  ADD KEY `fk_trabajo_tipoTrabajo_idx` (`tipoTrabajo_idtipoTrabajo`),
  ADD KEY `fk_trabajo_trabajador1_idx` (`trabajador_cedula`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `caja`
--
ALTER TABLE `caja`
  MODIFY `idEmbarque` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identificador para cada embarque insertado', AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `calculos`
--
ALTER TABLE `calculos`
  MODIFY `semana` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `calidad`
--
ALTER TABLE `calidad`
  MODIFY `idcalidad` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identificador de la calidad que se ingresa.', AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `cosecha`
--
ALTER TABLE `cosecha`
  MODIFY `semana` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Semana en la que se pusieron las cintas', AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `exportacion`
--
ALTER TABLE `exportacion`
  MODIFY `idExportacion` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identificador de cada registro de exportacion.';

--
-- AUTO_INCREMENT de la tabla `login`
--
ALTER TABLE `login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `idpago` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identificador de cada pago a realizar', AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `tipotrabajo`
--
ALTER TABLE `tipotrabajo`
  MODIFY `idtipoTrabajo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `trabajo`
--
ALTER TABLE `trabajo`
  MODIFY `idtrabajo` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identificador para cada registro de un trabajo', AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `caja`
--
ALTER TABLE `caja`
  ADD CONSTRAINT `fk_caja_calidad1` FOREIGN KEY (`calidad_idcalidad`) REFERENCES `calidad` (`idcalidad`),
  ADD CONSTRAINT `fk_caja_pagos1` FOREIGN KEY (`pagos_idpago`) REFERENCES `pagos` (`idpago`);

--
-- Filtros para la tabla `cosecha`
--
ALTER TABLE `cosecha`
  ADD CONSTRAINT `fk_cosecha_pagos1` FOREIGN KEY (`pagos_idpago`) REFERENCES `pagos` (`idpago`);

--
-- Filtros para la tabla `exportacion`
--
ALTER TABLE `exportacion`
  ADD CONSTRAINT `fk_exportacion_caja1` FOREIGN KEY (`caja_idEmbarque`) REFERENCES `caja` (`idEmbarque`),
  ADD CONSTRAINT `fk_exportacion_cosecha1` FOREIGN KEY (`cosecha_semana`) REFERENCES `cosecha` (`semana`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `fk_pagos_trabajo1` FOREIGN KEY (`trabajo_idtrabajo`) REFERENCES `trabajo` (`idtrabajo`);

--
-- Filtros para la tabla `trabajo`
--
ALTER TABLE `trabajo`
  ADD CONSTRAINT `fk_trabajo_tipoTrabajo` FOREIGN KEY (`tipoTrabajo_idtipoTrabajo`) REFERENCES `tipotrabajo` (`idtipoTrabajo`),
  ADD CONSTRAINT `fk_trabajo_trabajador1` FOREIGN KEY (`trabajador_cedula`) REFERENCES `trabajador` (`cedula`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
