-- Script para crear la base de datos del Mundial 2026
-- Ejecutar en MySQL Workbench o cliente MySQL

-- 1. Crear base de datos
CREATE DATABASE IF NOT EXISTS mundial_2026 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mundial_2026;

-- 2. Crear tablas
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(40) NOT NULL UNIQUE,
    nombre_completo VARCHAR(120) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('ADMIN', 'TRADICIONAL', 'ESPORADICO') NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bitacora_sesiones (
    id_bitacora BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora_entrada DATETIME NOT NULL,
    fecha_hora_salida DATETIME NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS confederaciones (
    id_confederacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS paises (
    id_pais INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    es_anfitrion TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ciudades (
    id_ciudad INT AUTO_INCREMENT PRIMARY KEY,
    id_pais INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES paises(id_pais),
    UNIQUE KEY uq_ciudad_pais (id_pais, nombre)
);

CREATE TABLE IF NOT EXISTS estadios (
    id_estadio INT AUTO_INCREMENT PRIMARY KEY,
    id_ciudad INT NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    capacidad INT NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad),
    UNIQUE KEY uq_estadio_ciudad (id_ciudad, nombre)
);

CREATE TABLE IF NOT EXISTS equipos (
    id_equipo INT AUTO_INCREMENT PRIMARY KEY,
    id_pais INT NOT NULL,
    id_confederacion INT NOT NULL,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    valor_mercado_total DECIMAL(14,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_pais) REFERENCES paises(id_pais),
    FOREIGN KEY (id_confederacion) REFERENCES confederaciones(id_confederacion)
);

CREATE TABLE IF NOT EXISTS directores_tecnicos (
    id_dt INT AUTO_INCREMENT PRIMARY KEY,
    id_equipo INT NOT NULL UNIQUE,
    nombre_completo VARCHAR(120) NOT NULL,
    nacionalidad VARCHAR(80) NOT NULL,
    edad INT NOT NULL,
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo)
);

CREATE TABLE IF NOT EXISTS jugadores (
    id_jugador INT AUTO_INCREMENT PRIMARY KEY,
    id_equipo INT NOT NULL,
    nombre_completo VARCHAR(120) NOT NULL,
    posicion VARCHAR(40) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    estatura_m DECIMAL(3,2) NOT NULL,
    peso_kg DECIMAL(5,2) NOT NULL,
    valor_mercado DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo)
);

CREATE TABLE IF NOT EXISTS grupos (
    id_grupo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS grupo_equipos (
    id_grupo INT NOT NULL,
    id_equipo INT NOT NULL,
    PRIMARY KEY (id_grupo, id_equipo),
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo),
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo)
);

CREATE TABLE IF NOT EXISTS partidos (
    id_partido BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_grupo INT NOT NULL,
    id_estadio INT NOT NULL,
    id_equipo_local INT NOT NULL,
    id_equipo_visitante INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    fase ENUM('GRUPOS') NOT NULL DEFAULT 'GRUPOS',
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo),
    FOREIGN KEY (id_estadio) REFERENCES estadios(id_estadio),
    FOREIGN KEY (id_equipo_local) REFERENCES equipos(id_equipo),
    FOREIGN KEY (id_equipo_visitante) REFERENCES equipos(id_equipo)
);

-- 3. Insertar datos iniciales
INSERT IGNORE INTO confederaciones (nombre)
VALUES ('AFC'), ('CAF'), ('CONMEBOL'), ('CONCACAF'), ('UEFA'), ('OFC');

INSERT IGNORE INTO paises (nombre, es_anfitrion) VALUES ('Mexico', 1), ('USA', 1), ('Canada', 1);

INSERT IGNORE INTO grupos (nombre) VALUES ('A'), ('B'), ('C'), ('D'), ('E'), ('F'), ('G'), ('H'), ('I'), ('J'), ('K'), ('L');

-- 4. Insertar usuario admin
-- Contraseña: admin123
INSERT INTO usuarios (username, nombre_completo, password_hash, tipo_usuario, activo) 
VALUES ('admin', 'Administrador', '120000$c6ccca74cb4398fb1d5f50559619a63e$03493ea0765d2464035e555106061393f213ff4acfffe6e4495443fcab4abe05', 'ADMIN', 1)
ON DUPLICATE KEY UPDATE id_usuario = id_usuario;
