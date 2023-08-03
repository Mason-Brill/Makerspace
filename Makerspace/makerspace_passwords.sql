-- run this line to create the database
CREATE DATABASE IF NOT EXISTS makerspace DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

-- run this line to work with the makerspace database
USE makerspace;

-- run this section to create the passwords table
CREATE TABLE IF NOT EXISTS passwords (
user_id INT,
password VARCHAR(60) NOT NULL,
created DATETIME,
last_changed DATETIME,
FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

-- run this section one time ONLY IF you already created user test accounts
-- all test passwords are the same: abcdef123456
-- all passwords MUST be created using bcrypt
-- INSERT INTO passwords(user_id, password, created) VALUES
-- (1, '$2a$10$6lXykfe6oc4V4ehUW1/PHO7GX1ahsvq5Q6F/DIARpJ3/S9y5DH.BO', now()),
-- (2, '$2a$10$mx5.j4gKiOFyFC8fxuvsPeAYTVdIrxdqI3B7FhndT.c8On8jeeSly', now()),
-- (3, '$2a$10$V175mnhq9HiuejbHUv3Jcuj.XeDGi8rDdrajxISPDxRDi85gJbetO', now()),
-- (4, '$2a$10$vjt.6dB2arY8G4r9yQhAe.x0KIzNCdddE8mRabF94VBYWCBGa.16K', now()),
-- (5, '$2a$10$7NQw5sFGnHNGFOimbWwDWu2SVLvkVwPjyzJAS.G0VMIV9msGiDKMS', now()),
-- (6, '$2a$10$C.5ehhVP7t8p4snPxq49NOu0mC.6Rj8Th6TxkeApuzfsgdAZckvge', now());

SELECT * FROM passwords;