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
   quantite_commande INT,
   prix INT,
   PRIMARY KEY(jean_id, commande_id),
   FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   jean_id INT,
   utilisateur_id INT,
   quantite_panier INT,
   date_ajout DATE,
   PRIMARY KEY(jean_id, utilisateur_id),
   FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

INSERT INTO taille (id_taille, nom_taille) VALUES
(1, 'XS / 36'),
(2, 'S / 38'),
(3, 'M / 40'),
(4, 'L / 42'),
(5, 'XL / 44');

INSERT INTO coupe_jean (id_coupe_jean, nom_coupe) VALUES
(1, 'Skinny'),
(2, 'Slim'),
(3, 'Regular'),
(4, 'Straight'),
(5, 'Bootcut'),
(6, 'Tapered'),
(7, 'Loose');

INSERT INTO jean (id_jean, nom_jean, prix_jean, taille_id, coupe_jean_id, matiere, couleur, description, fournisseur, marque, photo, stock) VALUES
-- 1. Regular
(1, 'Levi''s 501 Original', 110.00, 3, 1, '100% Coton', 'Bleu Indigo', 'Le jean original à braguette boutonnée, coupe droite classique.', 'Levi Strauss', 'Levi''s', 'img/levis_501.jpg', 45),
(2, 'Diesel Thommer', 145.50, 3, 2, 'Coton Stretch', 'Gris Délavé', 'Jean coupe slim avec taille basse et jambe étroite.', 'OTB Group', 'Diesel', 'img/diesel_thommer.jpg', 12),
(3, 'Calvin Klein Skinny', 99.00, 2, 3, 'Denim Power', 'Bleu Clair', 'Coupe très ajustée effet seconde peau.', 'PVH Corp', 'Calvin Klein', 'img/ck_skinny.jpg', 25),
(4, 'Celio C25 Regular', 39.99, 4, 1, 'Coton Bio', 'Stone', 'Le basique indispensable au quotidien.', 'Celio France', 'Celio', 'img/celio_c25.jpg', 80),
(5, 'Wrangler Texas', 79.90, 5, 4, 'Coton/Elasthanne', 'Noir', 'Coupe authentique idéale avec des bottes.', 'Wrangler Inc', 'Wrangler', 'img/wrangler_texas.jpg', 30),
(6, 'Jack & Jones Glenn', 49.99, 3, 2, 'Jean souple', 'Bleu Marine', 'Coupe moderne pour tous les jours.', 'Bestseller', 'Jack & Jones', 'img/jj_glenn.jpg', 60),
(7, 'Pepe Jeans Cash', 85.00, 4, 1, 'Coton', 'Bleu Foncé', 'Un style décontracté avec une taille régulière.', 'Pepe Jeans London', 'Pepe Jeans', 'img/pepe_cash.jpg', 22),
(8, 'G-Star Raw 3301', 120.00, 3, 2, 'Denim Recyclé', 'Raw (Brut)', 'Le denim pur dans sa forme la plus propre.', 'G-Star RAW', 'G-Star', 'img/gstar_3301.jpg', 15),
(9, 'Zara Man Carrot', 45.90, 2, 5, 'Synthétique', 'Kaki', 'Coupe ample aux cuisses et resserrée aux chevilles.', 'Inditex', 'Zara', 'img/zara_carrot.jpg', 55),
(10, 'Lee Brooklyn Straight', 75.00, 5, 1, 'Coton Confort', 'Bleu Moyen', 'Taille légèrement plus haute pour plus de confort.', 'Kontoor Brands', 'Lee', 'img/lee_brooklyn.jpg', 40),
(11, 'H&M Super Skinny', 29.99, 1, 3, 'Super Stretch', 'Noir', 'Le skinny accessible et ultra extensible.', 'H&M Group', 'H&M', 'img/hm_skinny.jpg', 100),
(12, 'Levi''s 511 Slim', 105.00, 3, 2, 'Coton/Lyocell', 'Bleu Délavé', 'Une alternative moderne au jean droit.', 'Levi Strauss', 'Levi''s', 'img/levis_511.jpg', 35),
(13, 'Carhartt WIP Klondike', 95.00, 4, 5, 'Toile Japonaise', 'Beige', 'Robuste et tendance, coupe fuselée régulière.', 'Carhartt', 'Carhartt', 'img/carhartt_klon.jpg', 18),
(14, 'Boss Maine', 139.00, 5, 1, 'Coton Premium', 'Gris Anthracite', 'Élégance et confort pour un look business casual.', 'Hugo Boss', 'Boss', 'img/boss_maine.jpg', 10),
(15, 'April77 Joey', 110.00, 1, 3, 'Coton/Elasthanne', 'Gris Rock', 'Esprit rock n roll avec médiator inclus.', 'April77', 'April77', 'img/april77_joey.jpg', 5),
(16, 'Diesel Zatiny', 155.00, 4, 4, 'Coton', 'Bleu Nuit', 'Coupe bootcut moderne avec poches arrières stylisées.', 'OTB Group', 'Diesel', 'img/diesel_zatiny.jpg', 8),
(17, 'Tommy Hilfiger Scanton', 115.00, 3, 2, 'Coton Bio', 'Bleu Vif', 'Coupe ajustée avec détails signature.', 'PVH Corp', 'Tommy Hilfiger', 'img/tommy_scanton.jpg', 28),
(18, 'Uniqlo Selvedge', 49.90, 3, 1, 'Coton Selvedge', 'Indigo Brut', 'La qualité japonaise à prix abordable.', 'Fast Retailing', 'Uniqlo', 'img/uniqlo_selv.jpg', 70),
(19, 'Replay Anbass', 130.00, 4, 5, 'Hyperflex', 'Bleu Usé', 'Technologie hyperflex pour une liberté de mouvement totale.', 'Fashion Box', 'Replay', 'img/replay_anbass.jpg', 14),
(20, 'Kaporal 5 Broz', 65.00, 2, 1, 'Coton', 'Bleu Sale', 'Le style vintage français.', 'Kaporal', 'Kaporal', 'img/kaporal_broz.jpg', 50);
-- MLD
-- taille = (id_taille INT, nom_taille VARCHAR(10));
-- coupe_jean = (id_coupe_jean INT, nom_coupe VARCHAR(10));
-- jean = (id_jean INT, nom_jean VARCHAR(20), matiere VARCHAR(50), couleur VARCHAR(10), description VARCHAR(200), marque VARCHAR(20), photo VARCHAR(20), stock_ INT, fournisseur VARCHAR(20), prix_jean DECIMAL(15,2), #id_coupe_jean, #id_taille);


-- MLD
-- taille = (id_taille INT, nom_taille VARCHAR(255));
-- coupe_jean = (id_coupe_jean INT, nom_coupe VARCHAR(255));
-- utilisateur = (id_utilisateur INT, login VARCHAR(255), email VARCHAR(255), nom VARCHAR(255), password VARCHAR(255), role VARCHAR(255));
-- etat = (id_etat INT, libelle VARCHAR(255));
-- jean = (id_jean INT, nom_jean VARCHAR(255), matiere VARCHAR(255), couleur VARCHAR(255), description VARCHAR(255), marque VARCHAR(255), photo VARCHAR(255), stock_ INT, fournisseur VARCHAR(255), prix_jean DECIMAL(15,2), #coupe_jean_id, #taille_id);
-- commande_ = (id_commande INT, date_achat DATE, #utilisateur_id, #etat_id);
-- ligne_commande = (#jean_id, #commande_id, quantite_commande INT, prix INT);
-- ligne_panier = (#jean_id, #utilisateur_id, quantite_panier INT, date_ajout DATE);

