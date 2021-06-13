TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`%` trigger protein_deletion\n    before delete on\n    protein for each row\n    begin\n        delete from binds_to where protein = OLD.uniprot_id;\n    end'
sql_modes=1436549152
definers='root@%'
client_cs_names='utf8mb4'
connection_cl_names='utf8mb4_general_ci'
db_cl_names='latin1_swedish_ci'
created=162360520230
