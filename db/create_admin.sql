CREATE LOGIN lms_admin WITH PASSWORD = '20227257';
USE LMS_DB;
CREATE USER [lms-admin] FOR LOGIN lms_admin;
USE LMS_DB;
GRANT ALL PRIVILEGES TO [lms-admin];
