-- MCD
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS jean;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS coupe_jean;
DROP TABLE IF EXISTS taille;

CREATE TABLE taille(
   id_taille INT,
   nom_taille VARCHAR(255) NOT NULL,
   PRIMARY KEY(id_taille)
);

CREATE TABLE coupe_jean(
   id_coupe_jean INT,
   nom_coupe VARCHAR(255) NOT NULL,
   PRIMARY KEY(id_coupe_jean)
);

CREATE TABLE utilisateur(
   id_utilisateur INT,
   login VARCHAR(255),
   email VARCHAR(255),
   nom VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat(
   id_etat INT,
   libelle VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE jean(
   id_jean INT,
   nom_jean VARCHAR(255) NOT NULL,
   matiere VARCHAR(255),
   couleur VARCHAR(255),
   description VARCHAR(255),
   marque VARCHAR(255),
   photo VARCHAR(255),
   stock_ INT,
   fournisseur VARCHAR(255),
   prix_jean DECIMAL(15,2) NOT NULL,
   coupe_jean_id INT NOT NULL,
   taille_id INT NOT NULL,
   PRIMARY KEY(id_jean),
   FOREIGN KEY(coupe_jean_id) REFERENCES coupe_jean(id_coupe_jean),
   FOREIGN KEY(taille_id) REFERENCES taille(id_taille)
);

CREATE TABLE commande(
   id_commande INT,
   date_achat DATE,
   utilisateur_id INT NOT NULL,
   etat_id INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat)
);

CREATE TABLE ligne_commande(
   jean_id INT,
   commande_id INT,
   quantite INT,
   prix INT,
   PRIMARY KEY(jean_id, commande_id),
   FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   jean_id INT,
   utilisateur_id INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(jean_id, utilisateur_id),
   FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);



-- MLD
-- taille = (id_taille INT, nom_taille VARCHAR(255));
-- coupe_jean = (id_coupe_jean INT, nom_coupe VARCHAR(255));
-- utilisateur = (id_utilisateur INT, login VARCHAR(255), email VARCHAR(255), nom VARCHAR(255), password VARCHAR(255), role VARCHAR(255));
-- etat = (id_etat INT, libelle VARCHAR(255));
-- jean = (id_jean INT, nom_jean VARCHAR(255), matiere VARCHAR(255), couleur VARCHAR(255), description VARCHAR(255), marque VARCHAR(255), photo VARCHAR(255), stock_ INT, fournisseur VARCHAR(255), prix_jean DECIMAL(15,2), #coupe_jean_id, #taille_id);
-- commande_ = (id_commande INT, date_achat DATE, #utilisateur_id, #etat_id);
-- ligne_commande = (#jean_id, #commande_id, quantite INT, prix INT);
-- ligne_panier = (#jean_id, #utilisateur_id, quantite INT, date_ajout DATE);

