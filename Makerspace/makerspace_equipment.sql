-- run this line to create the database
CREATE DATABASE IF NOT EXISTS makerspace DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

-- run this line to work with the makerspace database
USE makerspace;

-- run this section to create the equipment table
CREATE TABLE IF NOT EXISTS equipment (
	equipment_id INT PRIMARY KEY AUTO_INCREMENT,
	category ENUM('Design, Prototyping, and Testing', 'Fabrication', 'Assembly', 'Production') NOT NULL,
	subcategory VARCHAR(45) NOT NULL,
    equipment_name VARCHAR(45),
    quantity INT NOT NULL,
    description_file_name VARCHAR(45),
    image_file_name VARCHAR(45),
    created DATETIME,
    last_modified DATETIME,
    is_visible BOOL
);

-- run the following code one time to create starting equipment database:
-- INSERT INTO equipment(category, subcategory, equipment_name, quantity, created, is_visible) VALUES
-- (1, 'Desktop Computers', 'HP EliteOne 800 G6', 4, now(), TRUE),
-- (1, 'Soldering Stations', NULL, 1, now(), TRUE),
-- (1, 'Electronics Station', NULL, 1, now(), TRUE),
-- (2, 'Lasers', 'Glowforge Pro', 2, now(), TRUE),
-- (2, '3D Printers', 'Makerbot Replicator+', 2, now(), TRUE),
-- (2, '3D Printers', 'Ultimaker S3', 1, now(), TRUE),
-- (2, 'CNC Machines', 'Bantam Tools Desktop CNC milling machine', 1, now(), TRUE),
-- (2, 'Vacuum Former', 'Formech Compac Mini desktop vacuum former', 1, now(), TRUE),
-- (2, 'Vinyl Cutter', 'Roland CAMM-1 GS-24 desktop cutter', 1, now(), TRUE),
-- (2, 'Heat Press', 'PowerPress', 1, now(), TRUE),
-- (3, 'Assembly Station', NULL, 1, now(), TRUE),
-- (4, 'Photography', NULL, 1, now(), TRUE),
-- (4, 'Printers', 'HP DesignJet T230', 1, now(), TRUE);

-- run the following code one time to add file names:
-- SET SQL_SAFE_UPDATES = 0;
-- UPDATE equipment SET description_file_name = CONCAT('description_', CAST(equipment_id AS CHAR));
-- UPDATE equipment SET image_file_name = CONCAT('image_', CAST(equipment_id AS CHAR));
-- SET SQL_SAFE_UPDATES = 1;

SELECT * FROM equipment;

-- DROP TABLE equipment;
-- DELETE FROM equipment WHERE equipment_id = 14;



