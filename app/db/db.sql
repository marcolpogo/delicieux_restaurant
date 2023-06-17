create table contrevenants(
    id integer primary key,
    id_poursuite integer,
    business_id integer,
    date text,
    description text,
    adresse text,
    date_jugement text,
    etablissement text,
    montant integer,
    proprietaire text,
    ville text,
    statut text,
    date_statut text,
    categorie text
);


create table user(
    username text primary key,
    password text,
    salt text
);


insert into user values(
    'admin1234',
    'd61c571aa22765a648d106d0da125a110921622489fe6f58e121b1a2002d2131921d0ff23b8a29b58982696ce72fcdd47ff5174c31be277548909f93fbd1e8d2',
    'b1a6b61c16504b1291934e36ffbb977a'
);

create table flag(
    id integer primary key,
    msg text
);

insert into flag(msg) values(
    'UQAM{n3v3r_bl4l1st_ch4r4ct3rs...y0u_w1ll_f0rg3t_s0m3}'
);