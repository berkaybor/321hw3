TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`%` trigger score2\n    before insert on author_list for each row\n    begin\n        update institute set score = score+2\n        where institute_name = (select institution from written_by where doi = new.doi);\n    end' 'CREATE DEFINER=`root`@`%` trigger score3\n    before delete on author_list for each row\n    begin\n        update institute set score = score-2\n        where institute_name = (select institution from written_by where doi = old.doi);\n    end'
sql_modes=1436549152 1436549152
definers='root@%' 'root@%'
client_cs_names='utf8mb4' 'utf8mb4'
connection_cl_names='utf8mb4_general_ci' 'utf8mb4_general_ci'
db_cl_names='latin1_swedish_ci' 'latin1_swedish_ci'
created=162360482063 162360506993
