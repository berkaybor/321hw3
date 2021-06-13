from django.apps import AppConfig
from django.db import connection
from dtbank.settings import CREATE_TABLES

stmt = """
create table database_managers
(
    managerusername varchar(20) not null
        primary key,
    password        varchar(64) not null
);

create table drugs
(
    drugbank_id varchar(7)    not null
        primary key,
    drug_name   varchar(30)   not null,
    description varchar(1000) not null
);

create table protein
(
    uniprot_id   varchar(6)     not null
        primary key,
    sequence     varchar(10000) not null,
    protein_name varchar(200)   not null
);

create table reaction
(
    reaction_id varchar(8)  not null
        primary key,
    measure     varchar(10) not null,
    affinity    double      not null
);

create table side_effects
(
    umls_cui         varchar(8)  not null
        primary key,
    side_effect_name varchar(30) not null
);

create table users
(
    username    varchar(20) not null,
    institution varchar(40) not null,
    password    varchar(64) not null,
    primary key (username, institution)
);

create table institute
(
    institute_name varchar(100)  not null
        primary key,
    score          int default 0 not null
);

create table author_list
(
    doi    varchar(200) not null,
    author varchar(30)  not null,
    primary key (doi, author),
    constraint author_list_written_by__fk
        foreign key (doi) references written_by (doi)
            on update cascade on delete cascade
);

create table binds_to
(
    protein  varchar(6) not null,
    reaction varchar(8) not null,
    primary key (protein, reaction),
    constraint binds_to_protein__fk
        foreign key (protein) references protein (uniprot_id)
            on update cascade on delete cascade,
    constraint binds_to_reaction__fk
        foreign key (reaction) references reaction (reaction_id)
            on update cascade on delete cascade
);

create table causes
(
    drug        varchar(7) not null,
    side_effect varchar(8) not null,
    primary key (drug, side_effect),
    constraint drug
        foreign key (drug) references drugs (drugbank_id)
            on update cascade on delete cascade,
    constraint side_effect
        foreign key (side_effect) references side_effects (umls_cui)
            on update cascade on delete cascade
);


create table interactions
(
    drug            varchar(7) not null,
    interacted_drug varchar(7) not null,
    primary key (drug, interacted_drug),
    constraint interactions_drugs__fk
        foreign key (drug) references drugs (drugbank_id)
            on update cascade on delete cascade
);

create table notation
(
    drug_id varchar(7)   not null
        primary key,
    smiles  varchar(100) not null,
    constraint notation_ibfk_1
        foreign key (drug_id) references drugs (drugbank_id)
            on update cascade on delete cascade
);

create table undergoes
(
    reaction varchar(8) not null
        primary key,
    drug     varchar(7) not null,
    constraint undergoes_ibfk_1
        foreign key (drug) references drugs (drugbank_id)
            on update cascade on delete cascade,
    constraint undergoes_ibfk_2
        foreign key (reaction) references reaction (reaction_id)
            on update cascade on delete cascade
);

create index drug
    on undergoes (drug);

create table written_by
(
    reaction    varchar(200) not null,
    institution varchar(100) not null,
    username    varchar(20)  not null,
    doi         varchar(200) not null
        primary key,
    constraint reaction
        unique (reaction, institution, username)
);

drop trigger if exists score;
drop trigger if exists score2;
drop trigger if exists score3;
drop trigger if exists protein_deletion;
drop trigger if exists drug_deletion;

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

class DrugappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drugapp'
    def ready(self):
        if CREATE_TABLES:
            with connection.cursor() as cursor:
                cursor.execute(stmt)