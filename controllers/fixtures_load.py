#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                          template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql='''
    DROP TABLE IF EXISTS ligne_panier;
    DROP TABLE IF EXISTS ligne_commande;
    DROP TABLE IF EXISTS commande;
    DROP TABLE IF EXISTS jean;
    DROP TABLE IF EXISTS etat;
    DROP TABLE IF EXISTS utilisateur;
    DROP TABLE IF EXISTS coupe_jean;
    DROP TABLE IF EXISTS taille;  
    '''
    for statement in sql.split(';'):
        if statement.strip():
            mycursor.execute(statement)


    mycursor.execute('''
    CREATE TABLE taille(
    id_taille INT AUTO_INCREMENT,
    nom_taille VARCHAR(255) NOT NULL,
    PRIMARY KEY(id_taille)) DEFAULT CHARSET=utf8;
    ''')
    mycursor.execute('''
    INSERT INTO taille (id_taille, nom_taille) VALUES
    (1, 'XS'),
    (2, 'S'),
    (3, 'M'),
    (4, 'L'),
    (5, 'XL'),
    (6, '38'),
    (7, '40'),
    (8, '42');
    ''')

    # Table COUPE_JEAN
    mycursor.execute('''
    CREATE TABLE coupe_jean(
    id_coupe_jean INT AUTO_INCREMENT,
    nom_coupe VARCHAR(255) NOT NULL,
    PRIMARY KEY(id_coupe_jean)) DEFAULT CHARSET=utf8;
        ''')
    mycursor.execute('''
    INSERT INTO coupe_jean (id_coupe_jean, nom_coupe) VALUES 
    (1, 'Slim'),
    (2, 'Regular'),
    (3, 'Skinny'),
    (4, 'Bootcut'),
    (5, 'Straight');
    ''')


    mycursor.execute('''
    CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(255),
    PRIMARY KEY(id_etat)) DEFAULT CHARSET=utf8;
    ''')

    mycursor.execute('''
    INSERT INTO etat (id_etat, libelle) VALUES
    (1, 'En attente de paiement'),
    (2, 'Validée'),
    (3, 'En cours de préparation'),
    (4, 'Expédiée'),
    (5, 'Livrée');
    ''')

    mycursor.execute('''
    CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    PRIMARY KEY(id_utilisateur)) DEFAULT CHARSET=utf8;
    ''')

    sql = ''' 
    INSERT INTO utilisateur (login, email, password, role, nom) VALUES
    ('admin', 'admin@admin.fr', 
    'scrypt:32768:8:1$Z7LLPKP7hQDGO5Q7$639cec02ccb15e8b4c0f60ab5c8929b76bdeba9921b9ac0c2b70b119f5c5a671dd018e0a6a5b4054520640f53649e81457777e463f0ef9a640c521794ce01686', 
    'ROLE_admin', 'admin'),

    ('client1', 'client@client.fr', 
    'scrypt:32768:8:1$EWc6JbJYAydwSivu$3fff0e7cb9f58651a8071ce29503d02f9e5f19b93253783d222ac785a25d016dfc0208884f9d2bb564600907c6474c54ee783cdcaef3bc0b96ab77d1734454ff', 
    'ROLE_client', 'client1'),

    ('client2', 'client2@client2.fr', 
    'scrypt:32768:8:1$CXrCpwAYwqjIBSJx$f03f4f3e0517fcd4fc4b47a885f3716973b5ad11fb55b37082ae4ae9b023d4bc5b4865eb26f33f5fceb1655e4023cd0eae6778e42a2e47885657a2a36d6b7d6a', 
    'ROLE_client', 'client2');
    '''
    mycursor.execute(sql)


    sql = '''
    CREATE TABLE jean(
    id_jean INT AUTO_INCREMENT,
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
    FOREIGN KEY(taille_id) REFERENCES taille(id_taille)) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO jean (id_jean, nom_jean, matiere, couleur, description, marque, photo, stock_, fournisseur, prix_jean, coupe_jean_id, taille_id) VALUES
    (1, 'Levi''s 501 Original', '100% Coton', 'Bleu Stone', 'Le jean iconique coupe droite boutonné.', 'Levi''s', 'levis.jpg', 50, 'Levi Strauss', 99.90, 2, 7),
    (2, 'Diesel Thommer', 'Coton/Elasthanne', 'Bleu moyen', 'Jean slim confortable et moderne.', 'Diesel', 'diesel.jpg', 25, 'Diesel Italy', 145.00, 1, 6),
    (3, 'Jack & Jones Glenn', 'Stretch', 'Gris Anthracite', 'Coupe près du corps, effet usé.', 'Jack & Jones', 'glenn.jpg', 100, 'Bestseller', 49.99, 3, 8),
    (4, 'Wrangler Texas', 'Coton', 'Bleu Brut', 'Jean robuste et authentique.', 'Wrangler', 'wrangler.jpg', 15, 'Wrangler Corp', 75.50, 2, 8),
    (5, 'Zara Man Basic', 'Denim Léger', 'Bleu Clair', 'Idéal pour l''été.', 'Zara', 'zara.jpg', 200, 'Inditex', 29.90, 3, 3),
    (6, 'G-Star Raw 3301', 'Denim Selvedge', 'Bleu Foncé', 'Inspiré des vêtements de travail.', 'G-Star', 'gstar.jpg', 10, 'G-Star Raw', 119.95, 5, 4),
    (7, 'Celio Powerflex', 'Super Stretch', 'Bleu Marine', 'Extrêmement élastique et confortable.', 'Celio','celio.jpg', 80, 'Celio France', 39.99, 1, 4),
    (8, 'Pepe Jeans Brighton', 'Coton', 'Bleu Foncé', 'Taille basse et jambes évasées.', 'Pepe Jeans', 'pepe_jeans.jpg', 20, 'Pepe Group', 85.00, 4, 2),
    (9, 'H&M Regular jeans', 'Coton Recyclé', 'Gris', 'Basique indispensable éco-responsable.', 'H&M', 'h&m.jpg', 150, 'H&M Group', 19.99, 2, 2),
    (10, 'Calvin Klein Jeans', 'Coton', 'Bleu Foncé', 'Look urbain et épuré.', 'Calvin Klein', 'ck.jpg', 30, 'PVH Corp', 110.00, 3, 1),
    (11, 'Lee Brooklyn Straight', 'Coton', 'Stone Wash', 'Coupe classique et intemporelle.', 'Lee', 'leebrooklyn.jpg', 45, 'Lee Jeans', 69.90, 5, 7),
    (12, 'Tommy Hilfiger Denton', 'Coton Bio', 'Beige', 'Chino style jean 5 poches.', 'Tommy Hilfiger', 'tommy.jpg', 35, 'PVH Corp', 99.00, 5, 6),
    (13, 'Petrol Industries Sherborne', 'Jeans', 'Bleu Moyen', 'Détails brodés sur les poches.', 'Petrol Industries', 'pi.jpg', 60, ' Petrol Industries US', 55.00, 2, 3),
    (14, 'Uniqlo Ezy Jean', 'Sweat/Denim', 'Bleu Moyen', 'L''apparence du jean, le confort du jogging.', 'Uniqlo', 'uniqlo.jpg', 90, 'Fast Retailing', 39.90, 1, 4),
    (15, 'Hugo Boss Delaware', 'Coton fin', 'Noir Profond', 'Jean habillé pour le bureau.', 'Hugo Boss', 'boss.jpg', 12, 'Hugo Boss AG', 159.00, 1, 7),
    (16, 'Pull&Bear Jean standard', 'Coton', 'Gris Clair', 'Coupe ample en haut, resserrée en bas.', 'Pull&Bear', 'pull_and_bear.jpg', 70, 'Inditex', 35.99, 2, 2),
    (17, 'Replay Anbass', 'Hyperflex', 'Bleu Foncé', 'Technologie stretch révolutionnaire.', 'Replay', 'replay.jpg', 18, 'Fashion Box', 135.00, 1, 5),
    (18, 'Superdry Officer', 'Coton épais', 'Kaki', 'Jean teinté style militaire.', 'Superdry', 'superdry.jpg', 40, 'Superdry PLC', 69.95, 2, 4),
    (19, 'Sullivan slim', '100% Coton', 'Bleu dixon ', 'Style années 90.', 'Ralf Lanren', 'rl.jpg', 55, 'Inditex', 35.99, 1, 3),
    (20, 'Jeans straight', 'Coton', 'Stone demin', 'Coupe mettant en valeur les formes.', 'Bonobo', 'bn.jpg', 22, 'Bonobo Inc', 95.00, 3, 2);
    '''
    mycursor.execute(sql)


    sql = '''
    CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT NOT NULL,
    etat_id INT NOT NULL,
    PRIMARY KEY(id_commande),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY(etat_id) REFERENCES etat(id_etat)) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    mycursor.execute('''
    INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
    (102, '2023-10-28', 3, 2),
    (101, '2023-09-15', 2, 5);
    ''')

    sql = '''
    CREATE TABLE ligne_commande(
    jean_id INT,
    commande_id INT,
    quantite_commande INT,
    prix DECIMAL(15,2),
    PRIMARY KEY(jean_id, commande_id),
    FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
    FOREIGN KEY(commande_id) REFERENCES commande(id_commande)) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)



    sql = '''
    CREATE TABLE ligne_panier(
    jean_id INT,
    utilisateur_id INT,
    quantite_panier INT,
    date_ajout DATE,
    PRIMARY KEY(jean_id, utilisateur_id),
    FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
