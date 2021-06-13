stmt = """
drop trigger if exists score1;
drop trigger if exists score2;
drop trigger if exists score3;
drop trigger if exists delete_protein;
drop trigger if exists delete_drug;

create trigger score
    before insert on written_by for each row
    begin
        update institute set score = score + 5 where institute_name= NEW.institution;
    end;

create trigger score2
    before insert on author_list for each row
    begin
        update institute set score = score+2
        where institute_name = (select institution from written_by where doi = new.doi);
    end;

create trigger score3
    before delete on author_list for each row
    begin
        update institute set score = score-2
        where institute_name = (select institution from written_by where doi = old.doi);
    end;

create trigger protein_deletion
    before delete on
    protein for each row
    begin
        delete from binds_to where protein = OLD.uniprot_id;
    end;

create trigger drug_deletion
    before delete on
    drugs for each row
    begin
        delete from interactions where interacted_drug = OLD.drugbank_id;
    end;
"""