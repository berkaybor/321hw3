TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`%` trigger score\n    before insert on written_by for each row\n    begin\n        update institute set score = score + 5\n        where institute_name= NEW.institution;\n    end'
sql_modes=1436549152
definers='root@%'
client_cs_names='utf8mb4'
connection_cl_names='utf8mb4_general_ci'
db_cl_names='latin1_swedish_ci'
created=162360451013
