-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 29, 2025 at 03:00 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `casa_campestre`
--

-- --------------------------------------------------------

--
-- Table structure for table `casa`
--

CREATE TABLE `casa` (
  `id_casa` bigint(20) NOT NULL,
  `nom_casa` varchar(50) NOT NULL,
  `radio_perimetro` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `casa`
--

INSERT INTO `casa` (`id_casa`, `nom_casa`, `radio_perimetro`) VALUES
(1, 'Mercedes', '500m2');

-- --------------------------------------------------------

--
-- Table structure for table `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` bigint(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `correo_cliente` varchar(50) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `direccion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre`, `apellido`, `correo_cliente`, `telefono`, `direccion`) VALUES
(1234, 'Deivi', 'Gonzalez', '', '4323454345', 'Ibague'),
(1234567, 'jhoan', 'ramirez', '', '3009876543', 'Cr 42 No 3-08 B/Casa Club'),
(1080293179, 'jhoan sebastin', 'ramirez galindo', 'jhoansebastianramirezgalindo@gmail.com', '3203456765', 'Ibague');

-- --------------------------------------------------------

--
-- Table structure for table `factura`
--

CREATE TABLE `factura` (
  `numero_factura` bigint(20) NOT NULL,
  `id_producto` bigint(20) NOT NULL,
  `id_propietario` bigint(20) NOT NULL,
  `id_cliente` bigint(20) NOT NULL,
  `cantidad` bigint(20) NOT NULL,
  `valor_venta` bigint(20) NOT NULL,
  `fecha_venta` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `factura`
--

INSERT INTO `factura` (`numero_factura`, `id_producto`, `id_propietario`, `id_cliente`, `cantidad`, `valor_venta`, `fecha_venta`) VALUES
(1, 1234, 123, 1234, 1, 333333, '2025-10-08 02:21:56');

-- --------------------------------------------------------

--
-- Table structure for table `inventario`
--

CREATE TABLE `inventario` (
  `id_inventario` bigint(20) NOT NULL,
  `fecha_inventario` datetime NOT NULL,
  `id_producto` bigint(20) NOT NULL,
  `cantidad` bigint(20) NOT NULL,
  `ubicacion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario`
--

INSERT INTO `inventario` (`id_inventario`, `fecha_inventario`, `id_producto`, `cantidad`, `ubicacion`) VALUES
(1, '2025-10-08 03:32:58', 12, 1, 'iBAGUE');

-- --------------------------------------------------------

--
-- Table structure for table `producto`
--

CREATE TABLE `producto` (
  `id_producto` bigint(20) NOT NULL,
  `id_tipoproducto` bigint(20) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `valor_venta` bigint(20) NOT NULL,
  `valor_compra` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `producto`
--

INSERT INTO `producto` (`id_producto`, `id_tipoproducto`, `descripcion`, `valor_venta`, `valor_compra`) VALUES
(12, 1, 'Alquiler', 333333, 3333333),
(1234, 1, 'Alquiler', 333333, 3333333);

-- --------------------------------------------------------

--
-- Table structure for table `propietario`
--

CREATE TABLE `propietario` (
  `id_propietario` bigint(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `sexo` varchar(50) NOT NULL,
  `id_casa` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `propietario`
--

INSERT INTO `propietario` (`id_propietario`, `nombre`, `apellido`, `sexo`, `id_casa`) VALUES
(123, 'MAURICIO', 'ramirez', 'masculino', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tipo_producto`
--

CREATE TABLE `tipo_producto` (
  `id_tipoproducto` bigint(20) NOT NULL,
  `descripcion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tipo_producto`
--

INSERT INTO `tipo_producto` (`id_tipoproducto`, `descripcion`) VALUES
(1, 'Alquiler');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `casa`
--
ALTER TABLE `casa`
  ADD PRIMARY KEY (`id_casa`);

--
-- Indexes for table `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indexes for table `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`numero_factura`),
  ADD KEY `id_producto` (`id_producto`),
  ADD KEY `id_propietario` (`id_propietario`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indexes for table `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_inventario`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indexes for table `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_tipoproducto` (`id_tipoproducto`);

--
-- Indexes for table `propietario`
--
ALTER TABLE `propietario`
  ADD PRIMARY KEY (`id_propietario`),
  ADD KEY `id_casa` (`id_casa`);

--
-- Indexes for table `tipo_producto`
--
ALTER TABLE `tipo_producto`
  ADD PRIMARY KEY (`id_tipoproducto`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `factura`
--
ALTER TABLE `factura`
  MODIFY `numero_factura` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_inventario` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tipo_producto`
--
ALTER TABLE `tipo_producto`
  MODIFY `id_tipoproducto` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `factura_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `factura_ibfk_3` FOREIGN KEY (`id_propietario`) REFERENCES `propietario` (`id_propietario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

--
-- Constraints for table `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`id_tipoproducto`) REFERENCES `tipo_producto` (`id_tipoproducto`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `propietario`
--
ALTER TABLE `propietario`
  ADD CONSTRAINT `propietario_ibfk_1` FOREIGN KEY (`id_casa`) REFERENCES `casa` (`id_casa`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
