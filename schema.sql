DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT timezone('UTC'::TEXT, NOW()),
    created_at TIMESTAMP DEFAULT timezone('UTC'::TEXT, NOW())
);
INSERT INTO users (username, full_name, password) VALUES ('johns', 'John Smith', 'P@ssw07d!');
CREATE OR REPLACE FUNCTION select_user_by_username(p_username TEXT)
RETURNS TABLE (
    id INTEGER,
    username TEXT,
    full_name TEXT,
    password TEXT,
    updated_at TIMESTAMP,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        u.id, u.username, u.full_name, u.password, u.updated_at, u.created_at
    FROM users u
    WHERE u.username = p_username;
END;
$$ LANGUAGE plpgsql;



DROP TABLE IF EXISTS manufacturers;
CREATE TABLE manufacturers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT timezone('UTC'::TEXT, NOW()),
    created_at TIMESTAMP NOT NULL DEFAULT timezone('UTC'::TEXT, NOW())
);
INSERT into manufacturers(id, name) VALUES (1, 'Arburg'), (2, 'ABB');

CREATE OR REPLACE FUNCTION select_all_manufacturers()
RETURNS TABLE (
    id INTEGER,
    name TEXT,
    updated_at TIMESTAMP,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.id, m.name, m.updated_at, m.created_at
    FROM manufacturers m;
END;
$$ LANGUAGE plpgsql;


DROP TYPE IF EXISTS machine_status;
CREATE TYPE MACHINE_STATUS AS ENUM ('0', '1');

DROP TABLE IF EXISTS machines;
CREATE TABLE machines(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    manufacturer_id INTEGER NOT NULL,
    purchased_at TIMESTAMP NOT NULL,
    year_of_manufacture INTEGER NOT NULL,
    status machine_status NOT NULL,
    capacity_in_percent float NOT NULL,
    updated_at TIMESTAMP DEFAULT timezone('UTC'::TEXT, NOW()),
    created_at TIMESTAMP DEFAULT timezone('UTC'::TEXT, NOW())
);

CREATE TEMP SEQUENCE temp_id_sequence START 1;

-- Insert 100 records into the machines table
DO $$DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..100 LOOP
        INSERT INTO machines (id, name, manufacturer_id, purchased_at, year_of_manufacture, status, capacity_in_percent, updated_at, created_at)
        VALUES (
            nextval('temp_id_sequence'),
            'Machine_' || i,
            (i % 2) + 1,
            NOW() - (i * INTERVAL '1 day'),
            2000 + (i % 24),
            CASE WHEN i % 2 = 0 THEN '0' ELSE '1' END,
            (i - 1) / 99.0,
            NOW() - (i * INTERVAL '1 hour'),
            NOW() - ((i - 1) * INTERVAL '1 day')
        );
    END LOOP;
END$$;

SELECT setval('temp_id_sequence', (SELECT max(id) FROM machines));
SELECT setval('machines_id_seq', (SELECT max(id) FROM machines));

DROP TABLE IF EXISTS machine_images;
CREATE TABLE machine_images(
    id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL UNIQUE,
    image_url TEXT NOT NULL UNIQUE,
    updated_at TIMESTAMP DEFAULT timezone('UTC'::TEXT, NOW()),
    created_at TIMESTAMP DEFAULT timezone('UTC'::TEXT, NOW()),
    FOREIGN KEY (machine_id) REFERENCES machines(id) on DELETE CASCADE
);
CREATE OR REPLACE FUNCTION insert_machine_image(
    p_machine_id INTEGER,
    p_image_url TEXT
)
RETURNS TEXT AS $$
DECLARE
    output_image_url TEXT;
BEGIN
    INSERT INTO machine_images (machine_id, image_url)
    VALUES (p_machine_id, p_image_url)
    RETURNING image_url INTO output_image_url;

    RETURN output_image_url;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_machine_image_and_get_url(
    p_machine_id INTEGER
)
RETURNS TEXT AS $$
DECLARE
    output_image_url TEXT;
BEGIN
    DELETE FROM machine_images
    WHERE machine_id = p_machine_id
    RETURNING image_url INTO output_image_url;
    RETURN output_image_url;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_machine(
    machine_name TEXT,
    manufacturer_id INTEGER,
    purchased_at TIMESTAMP,
    year_of_manufacture INTEGER,
    machine_status TEXT,
    capacity_in_percent fLOAT
)
RETURNS INTEGER AS $$
DECLARE
    machine_id INTEGER;
BEGIN
    INSERT INTO machines (name, manufacturer_id, purchased_at, year_of_manufacture, status, capacity_in_percent)
    VALUES (machine_name, manufacturer_id, purchased_at, year_of_manufacture, machine_status::MACHINE_STATUS, capacity_in_percent)
    RETURNING id INTO machine_id;

    RETURN machine_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_machine(
    p_id INTEGER,
    p_name TEXT,
    p_manufacturer_id INTEGER,
    p_purchased_at TIMESTAMP,
    p_year_of_manufacture INTEGER,
    p_machine_status TEXT,
    p_capacity_in_percent FLOAT
)
RETURNS INTEGER AS $$
DECLARE
    machine_id INTEGER;
BEGIN
    UPDATE machines
    SET name = p_name, manufacturer_id = p_manufacturer_id, purchased_at = p_purchased_at,
        year_of_manufacture = p_year_of_manufacture, status = p_machine_status::MACHINE_STATUS,
        capacity_in_percent = p_capacity_in_percent,
        updated_at = timezone('UTC'::TEXT, NOW())
    WHERE id = p_id
    RETURNING id INTO machine_id;
    RETURN machine_id;
END;
$$ LANGUAGE plpgsql;


DROP function if exists select_single_machine(p_machine_id INTEGER);
CREATE OR REPLACE FUNCTION select_single_machine(p_machine_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    name TEXT,
    manufacturer_id INTEGER,
    purchased_at TIMESTAMP,
    year_of_manufacture INTEGER,
    status TEXT,
    capacity_in_percent FLOAT,
    updated_at TIMESTAMP,
    created_at TIMESTAMP,
    image_url TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.id, m.name, m.manufacturer_id, m.purchased_at, m.year_of_manufacture, m.status::TEXT, m.capacity_in_percent,
        m.updated_at, m.created_at,
        mi.image_url
    FROM machines m
    LEFT JOIN machine_images mi ON mi.machine_id = m.id
    WHERE m.id = p_machine_id;
END;
$$ LANGUAGE plpgsql;

DROP function if exists select_all_machines();
CREATE OR REPLACE FUNCTION select_all_machines()
RETURNS TABLE (
    id INTEGER,
    name TEXT,
    manufacturer_id INTEGER,
    purchased_at TIMESTAMP,
    year_of_manufacture INTEGER,
    status TEXT,
    capacity_in_percent FLOAT,
    updated_at TIMESTAMP,
    created_at TIMESTAMP,
    image_url TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.id, m.name, m.manufacturer_id, m.purchased_at, m.year_of_manufacture, m.status::TEXT, m.capacity_in_percent,
        m.updated_at, m.created_at,
        mi.image_url
    FROM machines m
    LEFT JOIN machine_images mi ON mi.machine_id = m.id;
END;
$$ LANGUAGE plpgsql;

DROP function if exists delete_machine(p_id INTEGER);
CREATE OR REPLACE FUNCTION delete_machine(p_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    deleted_machine_id INTEGER;
BEGIN
    DELETE FROM machines
    WHERE id = p_id
    RETURNING id INTO deleted_machine_id;
    RETURN deleted_machine_id;
END;
$$ LANGUAGE plpgsql;
