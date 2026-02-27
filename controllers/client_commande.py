#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' selection des articles d'un panier 
    '''
    articles_panier = []
    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']


    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s"
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()

    if items_panier is None or len(items_panier) < 1:
        flash(u'Pas d\'articles dans le panier', 'alert-warning')
        return redirect('/client/article/show')


    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande, id_client, 1)
    sql = "INSERT INTO commande(date_achat, utilisateur_id, etat_id) VALUES (%s, %s, %s)"
    mycursor.execute(sql, tuple_insert)


    sql = "SELECT last_insert_id() as last_insert_id"
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()['last_insert_id']


    for item in items_panier:

        tuple_delete = (id_client, item['jean_id'])
        sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s"
        mycursor.execute(sql, tuple_delete)


        sql = "SELECT prix_jean as prix FROM jean WHERE id_jean = %s"
        mycursor.execute(sql, (item['jean_id'],))
        prix = mycursor.fetchone()['prix']


        sql = "INSERT INTO ligne_commande(commande_id, jean_id, prix, quantite_commande) VALUES (%s, %s, %s, %s)"
        tuple_insert_ligne = (commande_id, item['jean_id'], prix, item['quantite_panier'])
        mycursor.execute(sql, tuple_insert_ligne)


    get_db().commit()
    flash(u'Commande ajoutée avec succès !', 'alert-success')


    return redirect('/client/article/show')


@client_commande.route('/client/commande/show', methods=['get', 'post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''  
        SELECT 
            c.id_commande,
            c.date_achat,
            c.etat_id,
            e.libelle,
            SUM(lc.quantite_commande) AS nbr_articles,
            SUM(lc.quantite_commande * lc.prix) AS prix_total
        FROM commande c
        JOIN etat e ON c.etat_id = e.id_etat
        JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        WHERE c.utilisateur_id = %s
        GROUP BY c.id_commande, c.date_achat, c.etat_id, e.libelle
        ORDER BY c.etat_id, c.date_achat DESC;
    '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None

    id_commande = request.args.get('id_commande', None)

    if id_commande != None:
        print("ID de la commande sélectionnée :", id_commande)

        sql_details = ''' 
            SELECT 
                j.nom_jean AS nom,
                lc.quantite_commande AS quantite,
                lc.prix,
                (lc.quantite_commande * lc.prix) AS prix_ligne
            FROM ligne_commande lc
            JOIN jean j ON lc.jean_id = j.id_jean
            WHERE lc.commande_id = %s
        '''
        mycursor.execute(sql_details, (id_commande,))
        articles_commande = mycursor.fetchall()

        commande_adresses = None

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )
