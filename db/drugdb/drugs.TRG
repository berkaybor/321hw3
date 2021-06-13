TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`%` trigger drug_deletion\n    before delete on\n    drugs for each row\n    begin\n        delete from interactions where interacted_drug = OLD.drugbank_id;\n    end'
sql_modes=1436549152
definers='root@%'
client_cs_names='utf8mb4'
connection_cl_names='utf8mb4_general_ci'
db_cl_names='latin1_swedish_ci'
created=162360533700
