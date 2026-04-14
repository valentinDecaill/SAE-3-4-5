#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    id_declinaison = request.form.get('id_declinaison_article') or request.form.get('id_declinaison')
    id_taille_html = request.form.get('id_taille')
    id_couleur_html = request.form.get('id_couleur')

    try:
        quantite = int(quantite)
    except:
        quantite = 1

    if not id_declinaison and id_taille_html and id_couleur_html:
        sql = "SELECT id_declinaison FROM declinaison WHERE jean_id = %s AND taille_id = %s AND couleur_id = %s"
        mycursor.execute(sql, (id_article, id_taille_html, id_couleur_html))
        res = mycursor.fetchone()
        if res:
            id_declinaison = res['id_declinaison']


    sql_declinaison = "SELECT taille_id, couleur_id, stock FROM declinaison WHERE id_declinaison = %s"
    mycursor.execute(sql_declinaison, (id_declinaison,))
    declinaison = mycursor.fetchone()

    if declinaison and declinaison['stock'] >= quantite:
        id_taille = declinaison['taille_id']
        id_couleur = declinaison['couleur_id']

        sql_verif = "SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s AND taille_id = %s AND couleur_id = %s"
        mycursor.execute(sql_verif, (id_client, id_article, id_taille, id_couleur))
        article_panier = mycursor.fetchone()

        if article_panier is not None:
            sql_update = '''
                UPDATE ligne_panier 
                SET quantite_panier = quantite_panier + %s 
                WHERE utilisateur_id = %s AND jean_id = %s AND taille_id = %s AND couleur_id=%s
            '''
            mycursor.execute(sql_update, (quantite, id_client, id_article, id_taille, id_couleur))
        else:
            sql_insert = '''
                INSERT INTO ligne_panier (utilisateur_id, jean_id, taille_id, couleur_id, quantite_panier, date_ajout) 
                VALUES (%s, %s, %s, %s, %s, NOW())
            '''
            mycursor.execute(sql_insert, (id_client, id_article, id_taille, id_couleur, quantite))

        sql_stock = "UPDATE declinaison SET stock = stock - %s WHERE id_declinaison = %s"
        mycursor.execute(sql_stock, (quantite, id_declinaison))

        get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    id_taille = request.form.get('id_taille')
    id_couleur = request.form.get('id_couleur')
    quantite = 1


    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s AND taille_id =%s AND couleur_id = %s'''
    mycursor.execute(sql, (id_client, id_article, id_taille, id_couleur))
    article_panier = mycursor.fetchone()

    if article_panier is not None and article_panier['quantite_panier'] > 1:
        sql = '''UPDATE ligne_panier SET quantite_panier = quantite_panier-%s  WHERE utilisateur_id = %s AND jean_id=%s AND taille_id = %s AND couleur_id=%s'''
        mycursor.execute(sql, (quantite, id_client, id_article, id_taille, id_couleur))

    else:
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND jean_id=%s AND taille_id = %s AND couleur_id = %s'''
        mycursor.execute(sql, (id_client, id_article, id_taille, id_couleur))

    mycursor.execute("UPDATE declinaison SET stock = stock + %s WHERE jean_id=%s AND taille_id=%s AND couleur_id=%s", (quantite, id_article, id_taille, id_couleur))
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = "SELECT jean_id, taille_id, couleur_id, quantite_panier FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()

    for item in items_panier:
        sql_update = "UPDATE declinaison SET stock = stock + %s WHERE jean_id = %s AND taille_id = %s AND couleur_id=%s"
        mycursor.execute(sql_update, (item['quantite_panier'], item['jean_id'], item['taille_id'], item['couleur_id']))

    sql_delete = "DELETE FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql_delete, (id_client,))
    get_db().commit()

    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    id_taille = request.form.get('id_taille')
    id_couleur = request.form.get('id_couleur')


    sql = "SELECT quantite_panier FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s AND taille_id = %s AND couleur_id = %s"
    mycursor.execute(sql, (id_client, id_article, id_taille, id_couleur))
    article_panier = mycursor.fetchone()

    if article_panier is not None:
        quantite_a_rendre = article_panier['quantite_panier']


        sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s AND taille_id = %s AND couleur_id = %s"
        mycursor.execute(sql, (id_client, id_article, id_taille, id_couleur))


        sql_stock = "UPDATE declinaison SET stock = stock + %s WHERE jean_id = %s AND taille_id = %s AND couleur_id = %s"
        mycursor.execute(sql_stock, (quantite_a_rendre, id_article, id_taille, id_couleur))
        get_db().commit()

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types')
    # test des variables puis
    session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
