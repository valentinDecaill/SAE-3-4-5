#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')
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
          '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    list_param = []
    condition_and = ""

    sql3 = ''' SELECT id_coupe_jean, nom_coupe 
               FROM coupe_jean '''
    mycursor.execute(sql3)
    types_article = mycursor.fetchall()

    sql_panier = '''
                 SELECT jean.nom_jean, 
                        jean.prix_jean, 
                        ligne_panier.quantite_panier, 
                        ligne_panier.jean_id, 
                        (jean.prix_jean * ligne_panier.quantite_panier) as sous_total
                 FROM ligne_panier
                          INNER JOIN jean ON ligne_panier.jean_id = jean.id_jean
                 WHERE ligne_panier.utilisateur_id = %s 
                 '''
    mycursor.execute(sql_panier, (id_client,))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql_total = '''
                    SELECT SUM(jean.prix_jean * ligne_panier.quantite_panier)
                    FROM ligne_panier
                             INNER JOIN jean ON ligne_panier.jean_id = jean.id_jean
                    WHERE ligne_panier.utilisateur_id = %s 
                    '''
        mycursor.execute(sql_total, (id_client,))
        res = mycursor.fetchone()
        prix_total = res[0]
    else:
        prix_total = None

    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )