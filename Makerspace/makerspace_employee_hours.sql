-- run this line to create the database
CREATE DATABASE IF NOT EXISTS makerspace DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

-- run this line to work with the makerspace database
USE makerspace;

-- run this section to create the employee_hours table
CREATE TABLE IF NOT EXISTS employee_hours (
	shift_id INT PRIMARY KEY AUTO_INCREMENT,
    signed_in DATETIME,
    signed_out DATETIME,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

-- run to show columns in table
-- DESC employee_hours;

-- run to show all data in table
SELECT * FROM employee_hours;

-- run to delete data from table
-- DELETE FROM employee_hours WHERE shift_id = 4;

-- run to delete the entire table
-- DROP TABLE employee_hours;

-- testing how to select from table
-- SELECT first_name, last_name, signed_in, signed_out FROM accounts
-- JOIN employee_hours ON accounts.user_id = employee_hours.user_id;

-- testing how to select amount of time worked from table based on worker
-- SELECT 
--     accounts.first_name, 
--     SEC_TO_TIME(SUM(TIME_TO_SEC(TIMEDIFF(signed_out, signed_in)))) AS total_hours_worked 
-- FROM 
--     accounts 
--     JOIN employee_hours ON accounts.user_id = employee_hours.user_id 
-- GROUP BY 
--     accounts.user_id;
    
-- testing how to query whether a specific a user that is currently working in the makerspace
-- SELECT 
--     accounts.first_name, 
--     employee_hours.signed_in 
-- FROM 
--     accounts 
--     JOIN employee_hours ON accounts.user_id = employee_hours.user_id 
-- WHERE 
--     accounts.email = 'abhigyan.tripathi@spartans.ut.edu' AND 
--     employee_hours.signed_out IS NULL;
 
 -- testing how to query whether there are any workers in the makerspace
-- SELECT 
--     accounts.first_name, 
--     employee_hours.signed_in 
-- FROM 
--     accounts 
--     JOIN employee_hours ON accounts.user_id = employee_hours.user_id 
-- WHERE 
--     employee_hours.signed_out IS NULL;

-- testing how to query for a user that has been working in the makerspace for more than 1 hours
-- SELECT 
--     accounts.first_name, 
--     employee_hours.signed_in 
-- FROM 
--     accounts 
--     JOIN employee_hours ON accounts.user_id = employee_hours.user_id 
-- WHERE 
--     employee_hours.signed_out IS NULL AND 
--     employee_hours.signed_in < DATE_SUB(NOW(), INTERVAL 1 HOUR);


