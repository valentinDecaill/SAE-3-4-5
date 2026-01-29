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
   taille_id INT,
   nom_taille VARCHAR(255) NOT NULL,
   PRIMARY KEY(taille_id)
);

CREATE TABLE coupe_jean(
   coupe_jean_id INT,
   nom_coupe VARCHAR(255) NOT NULL,
   PRIMARY KEY(coupe_jean_id)
);

CREATE TABLE utilisateur(
   utilisateur_id INT,
   login VARCHAR(255),
   email VARCHAR(255),
   nom VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   PRIMARY KEY(utilisateur_id)
);

CREATE TABLE etat(
   etat_id INT,
   libelle VARCHAR(255),
   PRIMARY KEY(etat_id)
);

CREATE TABLE jean(
   jean_id INT,
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
   PRIMARY KEY(jean_id),
   FOREIGN KEY(coupe_jean_id) REFERENCES coupe_jean(coupe_jean_id),
   FOREIGN KEY(taille_id) REFERENCES taille(taille_id)
);

CREATE TABLE commande_(
   commande_id INT,
   date_achat DATE,
   utilisateur_id INT NOT NULL,
   etat_id INT NOT NULL,
   PRIMARY KEY(commande_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(utilisateur_id),
   FOREIGN KEY(etat_id) REFERENCES etat(etat_id)
);

CREATE TABLE ligne_commande(
   jean_id INT,
   commande_id INT,
   quantite INT,
   prix INT,
   PRIMARY KEY(jean_id, commande_id),
   FOREIGN KEY(jean_id) REFERENCES jean(jean_id),
   FOREIGN KEY(commande_id) REFERENCES commande_(commande_id)
);

CREATE TABLE ligne_panier(
   jean_id INT,
   utilisateur_id INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(jean_id, utilisateur_id),
   FOREIGN KEY(jean_id) REFERENCES jean(jean_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(utilisateur_id)
);



-- MLD
-- taille = (taille_id INT, nom_taille VARCHAR(255));
-- coupe_jean = (coupe_jean_id INT, nom_coupe VARCHAR(255));
-- utilisateur = (utilisateur_id INT, login VARCHAR(255), email VARCHAR(255), nom VARCHAR(255), password VARCHAR(255), role VARCHAR(255));
-- etat = (etat_id INT, libelle VARCHAR(255));
-- jean = (jean_id INT, nom_jean VARCHAR(255), matiere VARCHAR(255), couleur VARCHAR(255), description VARCHAR(255), marque VARCHAR(255), photo VARCHAR(255), stock_ INT, fournisseur VARCHAR(255), prix_jean DECIMAL(15,2), #coupe_jean_id, #taille_id);
-- commande_ = (commande_id INT, date_achat DATE, #utilisateur_id, #etat_id);
-- ligne_commande = (#jean_id, #commande_id, quantite INT, prix INT);
-- ligne_panier = (#jean_id, #utilisateur_id, quantite INT, date_ajout DATE);

