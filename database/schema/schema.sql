-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: caritas_3
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actividad_usuario`
--

DROP TABLE IF EXISTS `actividad_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actividad_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_actividad` int NOT NULL,
  `id_usuario` int NOT NULL,
  `rol_en_actividad` varchar(50) NOT NULL,
  `fecha_asignacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_actividad_usuario` (`id_actividad`,`id_usuario`),
  KEY `idx_actividad_usuario_usuario` (`id_usuario`),
  CONSTRAINT `fk_actividad_usuario_actividad` FOREIGN KEY (`id_actividad`) REFERENCES `actividades` (`id_actividad`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_actividad_usuario_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_rol_en_actividad_no_vacio` CHECK ((`rol_en_actividad` <> _utf8mb4''))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actividad_usuario`
--

LOCK TABLES `actividad_usuario` WRITE;
/*!40000 ALTER TABLE `actividad_usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `actividad_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actividades`
--

DROP TABLE IF EXISTS `actividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actividades` (
  `id_actividad` int NOT NULL AUTO_INCREMENT,
  `id_programa` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `fecha_actividad` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint(1) NOT NULL DEFAULT '1',
  `id_usuario_creador` int NOT NULL,
  PRIMARY KEY (`id_actividad`),
  KEY `idx_actividad_programa` (`id_programa`),
  KEY `idx_actividad_usuario` (`id_usuario_creador`),
  CONSTRAINT `fk_actividad_programa` FOREIGN KEY (`id_programa`) REFERENCES `programas` (`id_programa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_actividad_usuario` FOREIGN KEY (`id_usuario_creador`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_actividades_nombre_no_vacio` CHECK ((`nombre` <> _utf8mb4''))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actividades`
--

LOCK TABLES `actividades` WRITE;
/*!40000 ALTER TABLE `actividades` DISABLE KEYS */;
/*!40000 ALTER TABLE `actividades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auditoria`
--

DROP TABLE IF EXISTS `auditoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria` (
  `id_auditoria` int NOT NULL AUTO_INCREMENT,
  `tabla_afectada` varchar(50) NOT NULL,
  `operacion` enum('INSERT','UPDATE','DELETE') NOT NULL,
  `id_registro` int NOT NULL,
  `descripcion` text,
  `fecha_auditoria` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario_responsable` int NOT NULL,
  PRIMARY KEY (`id_auditoria`),
  KEY `idx_auditoria_tabla` (`tabla_afectada`),
  KEY `idx_auditoria_usuario` (`id_usuario_responsable`),
  KEY `idx_auditoria_fecha` (`fecha_auditoria`),
  CONSTRAINT `fk_auditoria_usuario` FOREIGN KEY (`id_usuario_responsable`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_auditoria_tabla_afectada_no_vacia` CHECK ((`tabla_afectada` <> _utf8mb3''))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria`
--

LOCK TABLES `auditoria` WRITE;
/*!40000 ALTER TABLE `auditoria` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beneficiarios`
--

DROP TABLE IF EXISTS `beneficiarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beneficiarios` (
  `id_beneficiario` int NOT NULL AUTO_INCREMENT,
  `cedula` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(25) DEFAULT NULL,
  `direccion` text,
  `fecha_registro` date NOT NULL DEFAULT (curdate()),
  `estado` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_beneficiario`),
  UNIQUE KEY `cedula_UNIQUE` (`cedula`),
  CONSTRAINT `chk_beneficiarios_apellido_no_vacio` CHECK ((`apellido` <> _utf8mb3'')),
  CONSTRAINT `chk_beneficiarios_nombre_no_vacio` CHECK ((`nombre` <> _utf8mb3''))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beneficiarios`
--

LOCK TABLES `beneficiarios` WRITE;
/*!40000 ALTER TABLE `beneficiarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `beneficiarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_actividad_insumo`
--

DROP TABLE IF EXISTS `detalle_actividad_insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_actividad_insumo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_actividad` int NOT NULL,
  `id_insumo` int NOT NULL,
  `cantidad_usada` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_detalle_actividad_insumo` (`id_actividad`,`id_insumo`),
  KEY `idx_detalle_actividad_insumo_insumo` (`id_insumo`),
  CONSTRAINT `fk_detalle_actividad_insumo_actividad` FOREIGN KEY (`id_actividad`) REFERENCES `actividades` (`id_actividad`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_detalle_actividad_insumo_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_cantidad_usada` CHECK ((`cantidad_usada` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_actividad_insumo`
--

LOCK TABLES `detalle_actividad_insumo` WRITE;
/*!40000 ALTER TABLE `detalle_actividad_insumo` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_actividad_insumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `id_insumo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `stock_actual` decimal(10,2) NOT NULL DEFAULT '0.00',
  `unidad_medida` varchar(20) NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_insumo`),
  KEY `idx_insumos_nombre` (`nombre`),
  CONSTRAINT `chk_insumos_nombre_no_vacio` CHECK ((`nombre` <> _utf8mb4'')),
  CONSTRAINT `chk_insumos_stock_positivo` CHECK ((`stock_actual` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_insumos`
--

DROP TABLE IF EXISTS `movimientos_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_insumos` (
  `id_movimiento` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int NOT NULL,
  `tipo_movimiento` enum('entrada','salida') NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `fecha_movimiento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario_responsable` int NOT NULL,
  `observacion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_movimiento`),
  KEY `idx_movimientos_insumos_insumo` (`id_insumo`),
  KEY `idx_movimientos_insumos_usuario` (`id_usuario_responsable`),
  CONSTRAINT `fk_movimientos_insumos_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_movimientos_insumos_usuario` FOREIGN KEY (`id_usuario_responsable`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_cantidad_movimiento` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_insumos`
--

LOCK TABLES `movimientos_insumos` WRITE;
/*!40000 ALTER TABLE `movimientos_insumos` DISABLE KEYS */;
/*!40000 ALTER TABLE `movimientos_insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programa_beneficiario`
--

DROP TABLE IF EXISTS `programa_beneficiario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programa_beneficiario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_programa` int NOT NULL,
  `id_beneficiario` int NOT NULL,
  `fecha_asignacion` date NOT NULL DEFAULT (curdate()),
  `estado` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_programa_beneficiario` (`id_programa`,`id_beneficiario`),
  KEY `idx_programa_beneficiario_beneficiario` (`id_beneficiario`),
  CONSTRAINT `fk_programa_beneficiario_beneficiario` FOREIGN KEY (`id_beneficiario`) REFERENCES `beneficiarios` (`id_beneficiario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_programa_beneficiario_programa` FOREIGN KEY (`id_programa`) REFERENCES `programas` (`id_programa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_programa_beneficiario_estado_valido` CHECK ((`estado` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programa_beneficiario`
--

LOCK TABLES `programa_beneficiario` WRITE;
/*!40000 ALTER TABLE `programa_beneficiario` DISABLE KEYS */;
/*!40000 ALTER TABLE `programa_beneficiario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programa_usuario`
--

DROP TABLE IF EXISTS `programa_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programa_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_programa` int NOT NULL,
  `id_usuario` int NOT NULL,
  `rol_en_programa` varchar(50) NOT NULL,
  `fecha_asignacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_programa_usuario` (`id_programa`,`id_usuario`),
  KEY `idx_programa_usuario_usuario` (`id_usuario`),
  CONSTRAINT `fk_programa_usuario_programa` FOREIGN KEY (`id_programa`) REFERENCES `programas` (`id_programa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_programa_usuario_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_rol_en_programa_no_vacio` CHECK ((`rol_en_programa` <> _utf8mb4''))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programa_usuario`
--

LOCK TABLES `programa_usuario` WRITE;
/*!40000 ALTER TABLE `programa_usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `programa_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programas`
--

DROP TABLE IF EXISTS `programas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programas` (
  `id_programa` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT '1',
  `id_usuario_responsable` int NOT NULL COMMENT 'Usuario responsable del programa',
  PRIMARY KEY (`id_programa`),
  KEY `idx_programa_usuario` (`id_usuario_responsable`),
  CONSTRAINT `fk_programa_usuario` FOREIGN KEY (`id_usuario_responsable`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_programas_fecha_fin_valida` CHECK (((`fecha_fin` is null) or (`fecha_fin` >= `fecha_inicio`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programas`
--

LOCK TABLES `programas` WRITE;
/*!40000 ALTER TABLE `programas` DISABLE KEYS */;
/*!40000 ALTER TABLE `programas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `descripcion` text,
  `estado` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(128) NOT NULL,
  `telefono` varchar(25) NOT NULL,
  `date_joined` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `is_staff` tinyint(1) NOT NULL DEFAULT '0',
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0',
  `id_rol` int NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `cedula_UNIQUE` (`cedula`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `fk_usuario_rol_idx` (`id_rol`),
  CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_email_formato` CHECK (regexp_like(`email`,_utf8mb4'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')),
  CONSTRAINT `chk_usuarios_username_no_vacio` CHECK ((`username` <> _utf8mb3''))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-16 21:17:24
