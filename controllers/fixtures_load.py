from flask import Blueprint, redirect, url_for
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__)


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    sql = '''
        DROP TABLE IF EXISTS ligne_panier;
        DROP TABLE IF EXISTS ligne_commande;
        DROP TABLE IF EXISTS commande;
        DROP TABLE IF EXISTS declinaison;
        DROP TABLE IF EXISTS couleur;
        DROP TABLE IF EXISTS jean;
        DROP TABLE IF EXISTS etat;
        DROP TABLE IF EXISTS utilisateur;
        DROP TABLE IF EXISTS coupe_jean;
        DROP TABLE IF EXISTS taille;
        DROP TABLE IF EXISTS note;
        DROP TABLE IF EXISTS commentaire;
        
        CREATE TABLE taille(
           id_taille INT AUTO_INCREMENT,
           nom_taille VARCHAR(255) NOT NULL,
           PRIMARY KEY(id_taille)
        );
        
        CREATE TABLE coupe_jean(
           id_coupe_jean INT AUTO_INCREMENT,
           nom_coupe VARCHAR(255) NOT NULL,
           PRIMARY KEY(id_coupe_jean)
        );
        
        CREATE TABLE utilisateur(
           id_utilisateur INT AUTO_INCREMENT,
           login VARCHAR(255),
           email VARCHAR(255),
           nom VARCHAR(255),
           password VARCHAR(255),
           role VARCHAR(255),
           PRIMARY KEY(id_utilisateur)
        );
        
        CREATE TABLE etat(
           id_etat INT AUTO_INCREMENT,
           libelle VARCHAR(255),
           PRIMARY KEY(id_etat)
        );
        
        CREATE TABLE jean(
           id_jean INT AUTO_INCREMENT,
           nom_jean VARCHAR(255) NOT NULL,
           matiere VARCHAR(255),
           description VARCHAR(255),
           marque VARCHAR(255),
           photo VARCHAR(255),
           stock_ INT,
           fournisseur VARCHAR(255),
           prix_jean DECIMAL(15,2) NOT NULL,
           coupe_jean_id INT NOT NULL,
           PRIMARY KEY(id_jean),
           FOREIGN KEY(coupe_jean_id) REFERENCES coupe_jean(id_coupe_jean)
        );
        
        CREATE TABLE commande(
           id_commande INT AUTO_INCREMENT,
           date_achat DATE,
           utilisateur_id INT NOT NULL,
           etat_id INT NOT NULL,
           PRIMARY KEY(id_commande),
           FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(etat_id) REFERENCES etat(id_etat)
        );
        
        CREATE TABLE couleur(
          id_couleur INT AUTO_INCREMENT,
          nom_couleur VARCHAR(255) NOT NULL,
          PRIMARY KEY(id_couleur)
        );

        CREATE TABLE declinaison(
          id_declinaison INT AUTO_INCREMENT,
          stock INT,
          jean_id INT NOT NULL,
          taille_id INT NOT NULL,
          couleur_id INT NOT NULL,
          PRIMARY KEY(id_declinaison),
          FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
          FOREIGN KEY(taille_id) REFERENCES taille(id_taille),
          FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur)
        ) ;
        
        CREATE TABLE ligne_commande(
           jean_id INT,
           commande_id INT,
           taille_id INT,
           couleur_id INT NOT NULL,
           quantite_commande INT,
           prix INT,
           PRIMARY KEY(jean_id, commande_id, taille_id, couleur_id),
           FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
           FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
           FOREIGN KEY(taille_id) REFERENCES taille(id_taille),
           FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur)
        );
        
        CREATE TABLE ligne_panier(
           jean_id INT,
           utilisateur_id INT,
           taille_id INT,
           couleur_id INT NOT NULL,
           quantite_panier INT,
           date_ajout DATE,
           PRIMARY KEY(jean_id, utilisateur_id, taille_id, couleur_id),
           FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
           FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(taille_id) REFERENCES taille(id_taille),
           FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur)
        );
        
        
        CREATE TABLE note (
           id_utilisateur INT,
           id_jean INT NOT NULL,
           valeur INT NOT NULL CHECK (valeur >= 1 AND valeur <= 5),
           PRIMARY KEY(id_utilisateur, id_jean),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(id_jean) REFERENCES jean(id_jean)
        );
        
        CREATE TABLE commentaire (
           id_commentaire INT AUTO_INCREMENT,
           contenu VARCHAR(255) NOT NULL,
           date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
           etat_validation TINYINT(1) DEFAULT 0,
           reponse_admin VARCHAR(255) DEFAULT NULL,
           id_utilisateur INT,
           id_jean INT NOT NULL,
           PRIMARY KEY(id_commentaire),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(id_jean) REFERENCES jean(id_jean)
        );
            
            
        INSERT INTO utilisateur (login, email, password, role, nom) VALUES
        ('admin', 'admin@admin.fr',
            'scrypt:32768:8:1$Z7LLPKP7hQDGO5Q7$639cec02ccb15e8b4c0f60ab5c8929b76bdeba9921b9ac0c2b70b119f5c5a671dd018e0a6a5b4054520640f53649e81457777e463f0ef9a640c521794ce01686',
            'ROLE_admin', 'admin'),
        ('client1', 'client@client.fr',
            'scrypt:32768:8:1$EWc6JbJYAydwSivu$3fff0e7cb9f58651a8071ce29503d02f9e5f19b93253783d222ac785a25d016dfc0208884f9d2bb564600907c6474c54ee783cdcaef3bc0b96ab77d1734454ff',
            'ROLE_client', 'client1'),
        ( 'client2', 'client2@client2.fr',
            'scrypt:32768:8:1$CXrCpwAYwqjIBSJx$f03f4f3e0517fcd4fc4b47a885f3716973b5ad11fb55b37082ae4ae9b023d4bc5b4865eb26f33f5fceb1655e4023cd0eae6778e42a2e47885657a2a36d6b7d6a',
            'ROLE_client', 'client2');
        
        
        INSERT INTO taille (id_taille, nom_taille) VALUES
        (1, 'XS'),
        (2, 'S'),
        (3, 'M'),
        (4, 'L'),
        (5, 'XL'),
        (6, '38'),
        (7, '40'),
        (8, '42');
        
        INSERT INTO coupe_jean (id_coupe_jean, nom_coupe) VALUES -- (type article)
        (1, 'Slim'),
        (2, 'Regular'),
        (3, 'Skinny'),
        (4, 'Bootcut'),
        (5, 'Straight');
        
        INSERT INTO etat (id_etat, libelle) VALUES
        (1, 'En attente de paiement'),
        (2, 'Validée'),
        (3, 'En cours de préparation'),
        (4, 'Expédiée'),
        (5, 'Livrée');
        
        INSERT INTO couleur (id_couleur, nom_couleur) VALUES
        (1, 'Couleur Unique'),
        (2, 'Bleu'),
        (3, 'Noir'),
        (4, 'Gris'),
        (5, 'Rouge');
        
        
        INSERT INTO jean (id_jean, nom_jean, matiere, description, marque, photo, stock_, fournisseur, prix_jean, coupe_jean_id) VALUES
        (1, 'Levi''s 501 Original', '100% Coton', 'Le jean iconique coupe droite boutonné.', 'Levi''s', 'levis.jpg', 50, 'Levi Strauss', 99.90, 2),
        (2, 'Diesel Thommer', 'Coton/Elasthanne', 'Jean slim confortable et moderne.', 'Diesel', 'diesel.jpg', 25, 'Diesel Italy', 145.00, 1),
        (3, 'Jack & Jones Glenn', 'Stretch',  'Coupe près du corps, effet usé.', 'Jack & Jones', 'glenn.jpg', 100, 'Bestseller', 49.99, 3),
        (4, 'Wrangler Texas', 'Coton', 'Jean robuste et authentique.', 'Wrangler', 'wrangler.jpg', 15, 'Wrangler Corp', 75.50, 2),
        (5, 'Zara Man Basic', 'Denim Léger', 'Idéal pour l''été.', 'Zara', 'zara.jpg', 200, 'Inditex', 29.90, 3),
        (6, 'G-Star Raw 3301', 'Denim Selvedge', 'Inspiré des vêtements de travail.', 'G-Star', 'gstar.jpg', 10, 'G-Star Raw', 119.95, 5),
        (7, 'Celio Powerflex', 'Super Stretch',  'Extrêmement élastique et confortable.', 'Celio','celio.jpg', 80, 'Celio France', 39.99, 1),
        (8, 'Pepe Jeans Brighton', 'Coton',  'Taille basse et jambes évasées.', 'Pepe Jeans', 'pepe_jeans.jpg', 20, 'Pepe Group', 85.00, 4),
        (9, 'H&M Regular jeans', 'Coton Recyclé',  'Basique indispensable éco-responsable.', 'H&M', 'h&m.jpg', 150, 'H&M Group', 19.99, 2),
        (10, 'Calvin Klein Jeans', 'Coton',  'Look urbain et épuré.', 'Calvin Klein', 'ck.jpg', 30, 'PVH Corp', 110.00, 3),
        (11, 'Lee Brooklyn Straight', 'Coton', 'Coupe classique et intemporelle.', 'Lee', 'leebrooklyn.jpg', 45, 'Lee Jeans', 69.90, 5),
        (12, 'Tommy Hilfiger Denton', 'Coton Bio', 'Chino style jean 5 poches.', 'Tommy Hilfiger', 'tommy.jpg', 35, 'PVH Corp', 99.00, 5),
        (13, 'Petrol Industries Sherborne', 'Jeans', 'Détails brodés sur les poches.', 'Petrol Industries', 'pi.jpg', 60, ' Petrol Industries US', 55.00, 2),
        (14, 'Uniqlo Ezy Jean', 'Sweat/Denim', 'L''apparence du jean, le confort du jogging.', 'Uniqlo', 'uniqlo.jpg', 90, 'Fast Retailing', 39.90, 1),
        (15, 'Hugo Boss Delaware', 'Coton fin', 'Jean habillé pour le bureau.', 'Hugo Boss', 'boss.jpg', 12, 'Hugo Boss AG', 159.00, 1),
        (16, 'Pull&Bear Jean standard', 'Coton', 'Coupe ample en haut, resserrée en bas.', 'Pull&Bear', 'pull_and_bear.jpg', 70, 'Inditex', 35.99, 2),
        (17, 'Replay Anbass', 'Hyperflex', 'Technologie stretch révolutionnaire.', 'Replay', 'replay.jpg', 18, 'Fashion Box', 135.00, 1),
        (18, 'Superdry Officer', 'Coton épais',  'Jean teinté style militaire.', 'Superdry', 'superdry.jpg', 40, 'Superdry PLC', 69.95, 2),
        (19, 'Sullivan slim', '100% Coton', 'Style années 90.', 'Ralf Lanren', 'rl.jpg', 55, 'Inditex', 35.99, 1),
        (20, 'Jeans straight', 'Coton', 'Coupe mettant en valeur les formes.', 'Bonobo', 'bn.jpg', 22, 'Bonobo Inc', 95.00, 3);
        
        -- Client 1 a une commande "Livrée"
        INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
        (101, '2023-09-15', 2, 5);
        
        -- par exemple Client2 a une commande "Validée"
        INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
        (102, '2023-10-28', 3, 2);
        
        -- insert partie commentaires et notes
        
        INSERT INTO utilisateur (id_utilisateur, login, password, role, nom) VALUES
        (10, 'client10', 'pbkdf2:sha256:600000$xxxxxx$xxxxxx', 'ROLE_client', 'Petit'),
        (11, 'client11', 'pbkdf2:sha256:600000$xxxxxx$xxxxxx', 'ROLE_client', 'Leroy');


        INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
        (201, '2024-01-01 10:00:00', 2, 1),
        (202, '2024-01-02 11:00:00', 3, 1),
        (203, '2024-01-03 12:00:00', 10, 1),
        (204, '2024-01-04 14:00:00', 11, 1);
    
        INSERT INTO ligne_commande (commande_id, jean_id, taille_id, couleur_id, prix, quantite_commande) VALUES
        (201, 1, 2, 2, 49.99, 1), (201, 3, 3, 3, 45.00, 1), (201, 4, 2, 2, 65.00, 1),
        (202, 2, 1, 4, 59.99, 1), (202, 5, 2, 4, 55.00, 1), (202, 1, 3, 2, 49.99, 1),
        (203, 3, 4, 3, 45.00, 1), (203, 5, 3, 5, 55.00, 2),
        (204, 1, 4, 2, 49.99, 1), (204, 2, 2, 4, 59.99, 1), (204, 4, 3, 2, 65.00, 1);
    
    
        INSERT INTO note (id_utilisateur, id_jean, valeur) VALUES
        (2, 1, 5), (2, 3, 4), (2, 4, 3),
        (3, 2, 2), (3, 5, 4), (3, 1, 5),
        (10, 3, 5), (10, 5, 3),
        (11, 1, 4), (11, 2, 4), (11, 4, 5);
    
        INSERT INTO commentaire (contenu, etat_validation, reponse_admin, id_utilisateur, id_jean) VALUES
        ('client1test1', 1, 'admintest1', 2, 1),
        ('client1test2', 0, NULL, 2, 3),
        ('client1test3', 1, 'admintest2', 2, 4),
    
        ('client2test1', 1, NULL, 3, 2),
        ('client2test2', 1, 'admintest3', 3, 5),
        ('client2test3', 0, NULL, 3, 1),
    
        ('client10test1', 1, 'admintest4', 10, 3),
        ('client10test2', 0, NULL, 10, 5),
    
        ('client11test1', 1, NULL, 11, 1),
        ('client11test2', 1, 'admintest5', 11, 2),
        ('client11test3', 0, NULL, 11, 4);
        
        INSERT INTO declinaison (jean_id, taille_id, couleur_id, stock) VALUES
        (1, 2, 2, 15), (1, 3, 2, 25), (1, 4, 2, 10), (1, 3, 3, 20),
        (2, 5, 4, 5),  (2, 2, 4, 18), (2, 3, 2, 20), (2, 4, 2, 8),
        (3, 3, 3, 30), (3, 4, 3, 15),
        (4, 2, 2, 12), (4, 3, 2, 14), (4, 5, 2, 6),
        (5, 2, 4, 10), (5, 3, 5, 10),
        (6, 3, 2, 20), (6, 4, 3, 15),
        (7, 2, 2, 8),  (7, 4, 3, 12),
        (8, 1, 4, 5),  (8, 1, 5, 15),
        (9, 3, 2, 25), (9, 5, 3, 5),
        (10, 3, 3, 12), (10, 4, 4, 18),
        (11, 3, 2, 22),
        (12, 2, 3, 14),
        (13, 4, 2, 30),
        (14, 3, 4, 18),
        (15, 5, 2, 10),
        (16, 2, 2, 10), (16, 3, 3, 15), (16, 4, 4, 20),
        (17, 4, 2, 5),  (17, 2, 3, 12), (17, 3, 4, 18),
        (18, 3, 2, 25), (18, 4, 3, 15), (18, 5, 5, 8),
        (19, 2, 2, 20), (19, 3, 3, 30), (19, 4, 4, 10),
        (20, 2, 2, 8),  (20, 3, 3, 15), (20, 5, 4, 12);
        
          '''

    for requete in sql.split(";"):
        if requete.strip():
            mycursor.execute(requete)

    get_db().commit()
    return redirect('/')