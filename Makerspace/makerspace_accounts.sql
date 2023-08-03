-- run this line to create the database
CREATE DATABASE IF NOT EXISTS makerspace DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

-- run this line to work within the makerspace database
USE makerspace;

-- run this section to create the accounts table that will store general user information
CREATE TABLE IF NOT EXISTS accounts (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(45) NOT NULL UNIQUE,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    privilege_level ENUM('public', 'student', 'worker', 'administrator') NOT NULL,
    last_login DATETIME,
    last_modified DATETIME,
    created DATETIME
);

-- run the following code ONLY IF you want to create fake user accounts for testing and ONLY ONE TIME
-- INSERT INTO accounts(email, first_name, last_name, privilege_level, created) VALUES
-- -- rebecca's test account : student
-- ('rebecca.wilson@spartans.ut.edu', 'Rebecca', 'Wilson', 2, now()),
-- -- abhigyan's test account : worker
-- ('abhigyan.tripathi@spartans.ut.edu', 'Abhigyan', 'Tripathi', 3, now()),
-- -- lorielle's test account : worker
-- ('lorielle.raab@spartans.ut.edu', 'Lorielle', 'Raab', 3, now()),
-- -- mason's test account : worker
-- ('mason.brill@spartans.ut.edu', 'Mason', 'Brill', 3, now()),
-- -- dr. gourd's test account : admin
-- ('jgourd@ut.edu', 'Jean', 'Gourd', 4, now()),
-- -- dr. lori's test account : admin
-- ('ljacques@ut.edu', 'Lori', 'Jacques', 4, now());


-- HELPFUL CODE 
-- NOTE: You need to uncomment the code before running it (on a mac you comment/uncomment using command /)

-- run this ONLY IF you need to delete the entire accounts table 
-- DROP TABLE accounts;

-- run to show columns in table
-- DESC accounts;

-- run this to show all data in table
SELECT * FROM accounts;

-- run this to show all users with stated privilege level
-- SELECT * FROM accounts WHERE privilege_level = 'administrator';
-- SELECT * FROM accounts WHERE privilege_level = 'worker';
-- SELECT * FROM accounts WHERE privilege_level = 'student';

-- edit and run this to show all users with given name
-- SELECT * FROM accounts WHERE first_name = 'first_name' AND last_name = 'last_name';
-- SELECT * FROM accounts WHERE first_name = 'first_name';
-- SELECT * FROM accounts WHERE last_name = 'last_name';

-- edit and run this to change a user's privilege_level
-- UPDATE accounts SET privilege_level = 'worker' WHERE user_id = 1;

-- edit and run this to change a user's first_name
-- UPDATE accounts SET first_name = 'new_name' WHERE user_id = 0;

-- edit and run this to change a user's last_name
-- UPDATE accounts SET last_name = 'last_name' WHERE user_id = 0;

-- edit and run this to change a user's email
-- UPDATE accounts SET email = 'new_email' WHERE user_id = 0;

-- run to delete a specific user based on id
-- DELETE FROM accounts WHERE user_id = 0;

-- run this to obtain a user's password based on their email address
-- SELECT passwords.password FROM passwords
-- JOIN accounts ON passwords.user_id = accounts.user_id 
-- WHERE accounts.email = 'rebecca.wilson@spartans.ut.edu';

