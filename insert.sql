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


-- INSERTION DES PRODUITS (articles)

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

-- Client 1 a une commande "Livrée"
INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
(101, '2023-09-15', 2, 5);

-- par exemple Client2 a une commande "Validée"
INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
(102, '2023-10-28', 3, 2);





