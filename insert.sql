INSERT INTO utilisateur (id_utilisateur, login, email, password, role, nom) VALUES
(1, 'admin', 'admin@admin.fr',
    'pbkdf2:sha256:600000$DkUBX5uS1445k98Z$81315582236a282914102927806f3661271f653a99285094206c97a7a13d0382',
    'ROLE_admin', 'admin'),
(2, 'client1', 'client@client.fr',
    'pbkdf2:sha256:600000$M7j0v9yr4415z73A$152865766324a29165213645814f3665241c653b99245195206d96a7a13e0491',
    'ROLE_client', 'client1'),
(3, 'client2', 'client2@client2.fr',
    'pbkdf2:sha256:600000$T4k9x2zp7782q15B$263976877435b30276324756925g4776352d764c00356206317e07b8b24f1502',
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


-- INSERTION DES PRODUITS (articles)

INSERT INTO jean (id_jean, nom_jean, matiere, couleur, description, marque, photo, stock_, fournisseur, prix_jean, coupe_jean_id, taille_id) VALUES
(1, 'Levi''s 501 Original', '100% Coton', 'Bleu Stone', 'Le jean iconique coupe droite boutonné.', 'Levi''s', 'img/levis_501.jpg', 50, 'Levi Strauss', 99.90, 2, 7),
(2, 'Diesel Thommer', 'Coton/Elasthanne', 'Noir', 'Jean slim confortable et moderne.', 'Diesel', 'img/diesel_thommer.jpg', 25, 'Diesel Italy', 145.00, 1, 6),
(3, 'Jack & Jones Glenn', 'Stretch', 'Gris Anthracite', 'Coupe près du corps, effet usé.', 'Jack & Jones', 'img/jj_glenn.jpg', 100, 'Bestseller', 49.99, 3, 8),
(4, 'Wrangler Texas', 'Coton', 'Bleu Brut', 'Jean robuste et authentique.', 'Wrangler', 'img/wrangler_texas.jpg', 15, 'Wrangler Corp', 75.50, 2, 8),
(5, 'Zara Man Basic', 'Denim Léger', 'Bleu Clair', 'Idéal pour l''été.', 'Zara', 'img/zara_basic.jpg', 200, 'Inditex', 29.90, 3, 3),
(6, 'G-Star Raw 3301', 'Denim Selvedge', 'Indigo', 'Inspiré des vêtements de travail.', 'G-Star', 'img/gstar_3301.jpg', 10, 'G-Star Raw', 119.95, 5, 4),
(7, 'Celio Powerflex', 'Super Stretch', 'Bleu Marine', 'Extrêmement élastique et confortable.', 'Celio', 'img/celio_power.jpg', 80, 'Celio France', 39.99, 1, 4),
(8, 'Pepe Jeans Venus', 'Coton', 'Bleu Délavé', 'Taille basse et jambes évasées.', 'Pepe Jeans', 'img/pepe_venus.jpg', 20, 'Pepe Group', 85.00, 4, 2),
(9, 'H&M Regular Fit', 'Coton Recyclé', 'Noir', 'Basique indispensable éco-responsable.', 'H&M', 'img/hm_reg.jpg', 150, 'H&M Group', 19.99, 2, 5),
(10, 'Calvin Klein Skinny', 'Denim Premium', 'Gris Clair', 'Look urbain et épuré.', 'Calvin Klein', 'img/ck_skinny.jpg', 30, 'PVH Corp', 110.00, 3, 1),
(11, 'Lee Brooklyn Straight', 'Coton', 'Stone Wash', 'Coupe classique et intemporelle.', 'Lee', 'img/lee_brooklyn.jpg', 45, 'Lee Jeans', 69.90, 5, 7),
(12, 'Tommy Hilfiger Denton', 'Coton Bio', 'Beige', 'Chino style jean 5 poches.', 'Tommy Hilfiger', 'img/th_denton.jpg', 35, 'PVH Corp', 99.00, 5, 6),
(13, 'Kaporal Broz', 'Jeans', 'Bleu Foncé', 'Détails brodés sur les poches.', 'Kaporal', 'img/kaporal_broz.jpg', 60, 'Kaporal Sud', 55.00, 2, 3),
(14, 'Uniqlo Ezy Jean', 'Sweat/Denim', 'Bleu Moyen', 'L''apparence du jean, le confort du jogging.', 'Uniqlo', 'img/uniqlo_ezy.jpg', 90, 'Fast Retailing', 39.90, 1, 4),
(15, 'Hugo Boss Delaware', 'Coton fin', 'Noir Profond', 'Jean habillé pour le bureau.', 'Hugo Boss', 'img/boss_del.jpg', 12, 'Hugo Boss AG', 159.00, 1, 7),
(16, 'Pull&Bear Carrot', 'Denim', 'Blanc', 'Coupe ample en haut, resserrée en bas.', 'Pull&Bear', 'img/pb_carrot.jpg', 70, 'Inditex', 25.99, 2, 2),
(17, 'Replay Anbass', 'Hyperflex', 'Bleu Océan', 'Technologie stretch révolutionnaire.', 'Replay', 'img/replay_anbass.jpg', 18, 'Fashion Box', 135.00, 1, 5),
(18, 'Superdry Officer', 'Coton épais', 'Kaki', 'Jean teinté style militaire.', 'Superdry', 'img/superdry_off.jpg', 40, 'Superdry PLC', 69.95, 2, 4),
(19, 'Bershka Vintage', '100% Coton', 'Bleu Acide', 'Style années 90.', 'Bershka', 'img/bershka_vin.jpg', 55, 'Inditex', 35.99, 5, 3),
(20, 'Guess Sexy Curve', 'Stretch', 'Rouge', 'Coupe mettant en valeur les formes.', 'Guess', 'img/guess_sexy.jpg', 22, 'Guess Inc', 95.00, 3, 2);

-- Client 1 a une commande "Livrée"
INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
(101, '2023-09-15', 2, 5);

-- par exemple Client2 a une commande "Validée"
INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
(102, '2023-10-28', 3, 2);

--  imagine Client 1 a une commande "En attente"
INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
(103, '2023-10-29', 2, 1);



