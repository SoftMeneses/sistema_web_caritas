USE caritas_3;

/*==========================================================
  TRIGGERS DE INVENTARIO
==========================================================*/

/*----------------------------------------------------------
Detalle de actividad
----------------------------------------------------------*/


DROP TRIGGER IF EXISTS detalle_actividad_insumo_BEFORE_INSERT;

DELIMITER $$

CREATE TRIGGER detalle_actividad_insumo_BEFORE_INSERT 
BEFORE INSERT ON detalle_actividad_insumo 
FOR EACH ROW 
BEGIN
    DECLARE stock_disponible DECIMAL(10,2);

    -- Validar que la cantidad sea mayor que cero
    IF NEW.cantidad_usada <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La cantidad utilizada debe ser mayor que cero';
    END IF;

    -- Obtener stock actual
    SELECT stock_actual
    INTO stock_disponible
    FROM insumos
    WHERE id_insumo = NEW.id_insumo;

    -- Validar stock suficiente
    IF stock_disponible < NEW.cantidad_usada THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock insuficiente para esta actividad';

    END IF;
END

$$

DELIMITER ;


DROP TRIGGER IF EXISTS detalle_actividad_insumo_AFTER_INSERT;

DELIMITER $$

CREATE TRIGGER detalle_actividad_insumo_AFTER_INSERT 
AFTER INSERT ON detalle_actividad_insumo 
FOR EACH ROW 
BEGIN
 -- Descontar stock
   UPDATE insumos
   SET stock_actual = stock_actual - NEW.cantidad_usada
   WHERE id_insumo = NEW.id_insumo;
END

$$

DELIMITER ;


/*----------------------------------------------------------
Movimientos de insumos
----------------------------------------------------------*/


DROP TRIGGER IF EXISTS movimientos_insumos_BEFORE_INSERT;

DELIMITER $$

CREATE TRIGGER movimientos_insumos_BEFORE_INSERT 
BEFORE INSERT ON movimientos_insumos 
FOR EACH ROW 
BEGIN
    DECLARE stock_disponible DECIMAL(10,2);

    -- Validar que la cantidad sea mayor que cero
    IF NEW.cantidad <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La cantidad debe ser mayor que cero';
    END IF;

    -- Validar stock unicamente para salida
    IF NEW.tipo_movimiento = 'salida' THEN

        SELECT stock_actual
        INTO stock_disponible
        FROM insumos
        WHERE id_insumo = NEW.id_insumo;

        IF stock_disponible < NEW.cantidad THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Stock insuficiente';
        END IF;

    END IF;
END

$$

DELIMITER ;


DROP TRIGGER IF EXISTS movimientos_insumos_AFTER_INSERT;

DELIMITER $$

CREATE TRIGGER movimientos_insumos_AFTER_INSERT
AFTER INSERT ON movimientos_insumos
FOR EACH ROW 
BEGIN
    IF NEW.tipo_movimiento = 'entrada' THEN

        UPDATE insumos
        SET stock_actual = stock_actual + NEW.cantidad
        WHERE id_insumo = NEW.id_insumo;

    ELSEIF NEW.tipo_movimiento = 'salida' THEN

        UPDATE insumos
        SET stock_actual = stock_actual - NEW.cantidad
        WHERE id_insumo = NEW.id_insumo;

    END IF;
END

$$

DELIMITER ;


/*==========================================================
TRIGGERS DE AUDITORÍA
==========================================================*/


DROP TRIGGER IF EXISTS trg_programa_ai;

DELIMITER $$

CREATE TRIGGER trg_programa_ai 
AFTER INSERT ON programas 
FOR EACH ROW 
BEGIN
    INSERT INTO auditoria (
            tabla_afectada,
            operacion,
            id_registro,
            descripcion,
            fecha_auditoria,
            id_usuario_responsable
        )
        VALUES (
            'programas',
            'INSERT',
            NEW.id_programa,
            CONCAT('Se creó el programa: ', NEW.nombre),
            CURRENT_TIMESTAMP(),
            NEW.id_usuario_responsable
        );
END

$$

DELIMITER ;


DROP TRIGGER IF EXISTS trg_programa_au;

DELIMITER $$

CREATE TRIGGER trg_programa_au 
AFTER UPDATE ON programas 
FOR EACH ROW 
BEGIN
    INSERT INTO auditoria (
            tabla_afectada,
            operacion,
            id_registro,
            descripcion,
            fecha_auditoria,
            id_usuario_responsable
        )
        VALUES (
            'programas',
            'UPDATE',
            NEW.id_programa,
            CONCAT('Se actualizó el programa: ', NEW.nombre),
            CURRENT_TIMESTAMP(),
            NEW.id_usuario_responsable
        );
END

$$

DELIMITER ;


DROP TRIGGER IF EXISTS trg_programa_ad;

DELIMITER $$

CREATE TRIGGER trg_programa_ad 
AFTER DELETE ON programas 
FOR EACH ROW 
BEGIN
    INSERT INTO auditoria (
            tabla_afectada,
            operacion,
            id_registro,
            descripcion,
            fecha_auditoria,
            id_usuario_responsable
        )
        VALUES (
            'programas',
            'DELETE',
            OLD.id_programa,
            CONCAT('Se eliminó el programa: ', OLD.nombre),
            CURRENT_TIMESTAMP(),
            OLD.id_usuario_responsable
        );
END

$$

DELIMITER ;