
-- create the user 
--create user 'ecoach'@'localhost' identified by 'ecoach';

drop database if exists ecoach_select;
create database ecoach_select;
grant all privileges on ecoach_select.* to 'ecoach'@'localhost';

drop database if exists common1;
create database common1;
grant all privileges on common1.* to 'ecoach'@'localhost';

drop database if exists ecoach2;
create database ecoach2;
grant all privileges on ecoach2.* to 'ecoach'@'localhost';


