-- MCD

CREATE TABLE taille(
   id_taille INT,
   nom_taille VARCHAR(10) NOT NULL,
   PRIMARY KEY(id_taille)
);

CREATE TABLE coupe_jean(
   id_coupe_jean INT,
   nom_coupe VARCHAR(10) NOT NULL,
   PRIMARY KEY(id_coupe_jean)
);

CREATE TABLE jean(
   id_jean INT,
   nom_jean VARCHAR(20) NOT NULL,
   matiere VARCHAR(50),
   couleur VARCHAR(10),
   description VARCHAR(200),
   marque VARCHAR(20),
   photo VARCHAR(20),
   stock_ INT,
   fournisseur VARCHAR(20),
   prix_jean DECIMAL(15,2) NOT NULL,
   id_coupe_jean INT NOT NULL,
   id_taille INT NOT NULL,
   PRIMARY KEY(id_jean),
   FOREIGN KEY(id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean),
   FOREIGN KEY(id_taille) REFERENCES taille(id_taille)
);


-- MLD
-- taille = (id_taille INT, nom_taille VARCHAR(10));
-- coupe_jean = (id_coupe_jean INT, nom_coupe VARCHAR(10));
-- jean = (id_jean INT, nom_jean VARCHAR(20), matiere VARCHAR(50), couleur VARCHAR(10), description VARCHAR(200), marque VARCHAR(20), photo VARCHAR(20), stock_ INT, fournisseur VARCHAR(20), prix_jean DECIMAL(15,2), #id_coupe_jean, #id_taille);
