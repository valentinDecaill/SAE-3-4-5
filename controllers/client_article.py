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
          SELECT jean.id_jean                               AS id_article,
                 jean.nom_jean                              AS nom,
                 jean.prix_jean                             AS prix,
                 jean.photo                                 AS image,
                 coupe_jean.nom_coupe,
                 COUNT(DISTINCT commentaire.id_commentaire) AS nb_avis,
                 COUNT(DISTINCT note.id_utilisateur)        AS nb_notes,
                 ROUND(AVG(note.valeur), 1)                 AS moy_notes,
                 COUNT(DISTINCT declinaison.id_declinaison) AS nb_declinaisons,
                 IFNULL(SUM(declinaison.stock), 0) AS stock
          FROM jean
                   INNER JOIN coupe_jean ON jean.coupe_jean_id = coupe_jean.id_coupe_jean
                   LEFT JOIN commentaire ON jean.id_jean = commentaire.id_jean
                   LEFT JOIN note ON jean.id_jean = note.id_jean
                   LEFT JOIN declinaison ON jean.id_jean = declinaison.jean_id
          WHERE 1 = 1
          '''

    mycursor.execute(sql)
    articles = mycursor.fetchall()
    list_param = []
    condition_and = ""

    if session.get('filter_word'):
        condition_and += " AND nom_jean LIKE %s "
        list_param.append(f"%{session['filter_word']}%")

    if session.get('filter_prix_min'):
        condition_and += " AND prix_jean >= %s "
        list_param.append(session['filter_prix_min'])

    if session.get('filter_prix_max'):
        condition_and += " AND prix_jean <= %s "
        list_param.append(session['filter_prix_max'])

    if session.get('filter_types') and session.get('filter_types') != []:
        placeholders = ', '.join(['%s'] * len(session['filter_types']))
        condition_and += f" AND coupe_jean_id IN ({placeholders}) "
        list_param.extend(session['filter_types'])

    sql += condition_and + " GROUP BY jean.id_jean ORDER BY nom_jean;"

    mycursor.execute(sql, tuple(list_param))
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

        sql_check = "SELECT COUNT(*) AS nb FROM declinaison WHERE jean_id = %s"
        mycursor.execute(sql_check, (id_article,))
        nb_declinaison = mycursor.fetchone()['nb']

        if nb_declinaison > 1:
            return redirect(f'/client/article/details?id_article={id_article}')

        sql = "SELECT * FROM jean WHERE id_jean = %s"
        mycursor.execute(sql, (id_article,))
        article = mycursor.fetchone()

        if id_article is not None:
            return redirect(f'/client/article/details?id_article={id_article}')



    sql = '''
        SELECT ligne_panier.jean_id AS id_article,
               ligne_panier.taille_id,
               ligne_panier.couleur_id,
               ligne_panier.quantite_panier AS quantite, 
               jean.nom_jean AS nom, 
               jean.prix_jean AS prix,
               taille.nom_taille AS taille,
               couleur.nom_couleur AS couleur,
               declinaison.stock AS stock
        FROM ligne_panier
        JOIN jean ON ligne_panier.jean_id = jean.id_jean
        JOIN taille ON ligne_panier.taille_id = taille.id_taille
        JOIN couleur ON ligne_panier.couleur_id = couleur.id_couleur
        LEFT JOIN declinaison ON ligne_panier.jean_id = declinaison.jean_id AND ligne_panier.taille_id = declinaison.taille_id AND ligne_panier.couleur_id = declinaison.couleur_id
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






@client_article.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    id_article = request.args.get('id_article')


    sql_article = '''
        SELECT id_jean AS id_article,
            nom_jean AS nom,
            prix_jean AS prix,
            photo AS image
        FROM jean
        WHERE id_jean = %s
    '''

    mycursor.execute(sql_article, (id_article,))
    article = mycursor.fetchone()


    sql_declinaisons = '''
        SELECT d.id_declinaison AS id_declinaison_article, 
        d.stock, 
        t.nom_taille, 
        t.id_taille,
        c.nom_couleur
        FROM declinaison d
        JOIN taille t ON d.taille_id = t.id_taille
        JOIN couleur c ON d.couleur_id = c.id_couleur
        WHERE d.jean_id = %s
    '''
    mycursor.execute(sql_declinaisons, (id_article,))
    declinaisons = mycursor.fetchall()

    return render_template('client/boutique/declinaison_article.html', article=article, declinaisons=declinaisons)

