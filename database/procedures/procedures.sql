USE caritas_3;

-- ==========================================================
-- STORED PROCEDURES DE INVENTARIO
-- ==========================================================


-- ----------------------------------------------------------
-- Registrar movimiento de insumo
-- ----------------------------------------------------------

DROP PROCEDURE IF EXISTS sp_registrar_movimiento_insumo;

DELIMITER $$

CREATE PROCEDURE sp_registrar_movimiento_insumo(
    IN p_id_insumo INT,
    IN p_tipo_movimiento VARCHAR(10),
    IN p_cantidad DECIMAL(10,2),
    IN p_observacion VARCHAR(200),
    IN p_id_usuario_responsable INT
)
BEGIN

    INSERT INTO movimientos_insumos (
        tipo_movimiento,
        cantidad,
        fecha_movimiento,
        observacion,
        id_insumo,
        id_usuario_responsable
    )
    VALUES (
        p_tipo_movimiento,
        p_cantidad,
        NOW(),
        p_observacion,
        p_id_insumo,
        p_id_usuario_responsable
    );

END$$

DELIMITER ;


-- ----------------------------------------------------------
-- Registrar consumo de insumo en actividad
-- ----------------------------------------------------------

DROP PROCEDURE IF EXISTS sp_registrar_consumo_insumo;

DELIMITER $$

CREATE PROCEDURE sp_registrar_consumo_insumo(
    IN p_id_actividad INT,
    IN p_id_insumo INT,
    IN p_cantidad_usada DECIMAL(10,2)
)
BEGIN

    INSERT INTO detalle_actividad_insumo (
        cantidad_usada,
        id_actividad,
        id_insumo
    )
    VALUES (
        p_cantidad_usada,
        p_id_actividad,
        p_id_insumo
    );

END$$

DELIMITER ;