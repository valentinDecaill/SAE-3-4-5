#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show', methods=['GET', 'POST'])
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
            SELECT id_jean AS id_article, 
                   nom_jean AS nom, 
                   prix_jean AS prix, 
                   stock_ AS stock, 
                   photo AS image, 
                   nom_coupe, 
                   nom_taille
            FROM jean
            INNER JOIN coupe_jean ON jean.coupe_jean_id = coupe_jean.id_coupe_jean
            INNER JOIN taille ON jean.taille_id = taille.id_taille
            ORDER BY nom_jean;
          '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    sql = '''SELECT id_coupe_jean AS id_type_article, nom_coupe AS libelle FROM coupe_jean ORDER BY nom_coupe'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    id_article = request.form.get('id_article')

    if id_article is not None:
        quantite = request.form.get('quantite')
        try:
            quantite = int(quantite)
        except:
            quantite = 1

        sql = "SELECT * FROM jean WHERE id_jean = %s"
        mycursor.execute(sql, (id_article,))
        article = mycursor.fetchone()

        if article is not None and article['stock_'] >= quantite:

            sql = "SELECT * FROM ligne_panier WHERE jean_id = %s AND utilisateur_id = %s"
            mycursor.execute(sql, (id_article, id_client))
            article_panier = mycursor.fetchone()

            if article_panier is not None and article_panier['quantite_panier'] >= 1:

                sql = "UPDATE ligne_panier SET quantite_panier = quantite_panier + %s WHERE utilisateur_id = %s AND jean_id = %s"
                mycursor.execute(sql, (quantite, id_client, id_article))
            else:
                sql = "INSERT INTO ligne_panier(utilisateur_id, jean_id, quantite_panier, date_ajout) VALUES (%s, %s, %s, NOW())"
                mycursor.execute(sql, (id_client, id_article, quantite))

            sql = "UPDATE jean SET stock_ = stock_ - %s WHERE id_jean = %s"
            mycursor.execute(sql, (quantite, id_article))

            get_db().commit()

    sql = '''
        SELECT ligne_panier.jean_id AS id_article, 
               ligne_panier.quantite_panier AS quantite, 
               jean.nom_jean AS nom, 
               jean.prix_jean AS prix,
               jean.stock_ AS stock
        FROM ligne_panier
        JOIN jean ON ligne_panier.jean_id = jean.id_jean
        WHERE ligne_panier.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    prix_total = 0
    if articles_panier is not None:
        for ligne in articles_panier:
            if ligne['prix'] is None: ligne['prix'] = 0
            if ligne['quantite'] is None: ligne['quantite'] = 0
            prix_total += ligne['prix'] * ligne['quantite']

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=types_article)


@client_article.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    # On récupère l'ID envoyé par le formulaire caché
    id_article = request.form.get('id_article')

    sql = "SELECT quantite_panier FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s"
    mycursor.execute(sql, (id_client, id_article))
    panier = mycursor.fetchone()
    quantite_a_rendre = 0
    if panier is not None:
        quantite_a_rendre = panier['quantite_panier']

    sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s"
    mycursor.execute(sql, (id_client, id_article))
    sql = "UPDATE jean SET stock_ = stock_ + %s WHERE id_jean = %s"
    mycursor.execute(sql, (quantite_a_rendre, id_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_article.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = "SELECT jean_id, quantite_panier FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        id_article = item['jean_id']
        quantite = item['quantite_panier']
        sql_update = "UPDATE jean SET stock_ = stock_ + %s WHERE id_jean = %s"
        mycursor.execute(sql_update, (quantite, id_article))

    sql_delete = "DELETE FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql_delete, (id_client,))

    get_db().commit()
    return redirect('/client/article/show')