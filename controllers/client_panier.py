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
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    #sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article
    quantite = int(quantite) if quantite else 1

    # 2. On regarde si l'article est déjà dans le panier
    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s"
    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()

    if article_panier is not None:
        # Il y est déjà : on fait +1 (ou +quantite)
        # (Attention : si ta colonne s'appelle quantite_panier, modifie le mot "quantite" ici !)
        sql_update = "UPDATE ligne_panier SET quantite_panier = quantite_panier + %s WHERE utilisateur_id = %s AND jean_id = %s"
        mycursor.execute(sql_update, (quantite, id_client, id_article))
    else:
        # Il n'y est pas : on le crée
        sql_insert = "INSERT INTO ligne_panier (utilisateur_id, jean_id, quantite_panier) VALUES (%s, %s, %s)"
        mycursor.execute(sql_insert, (id_client, id_article, quantite))

    # 3. On baisse le stock de la table jean
    sql_stock = "UPDATE jean SET stock_ = stock_ - %s WHERE id_jean = %s"
    mycursor.execute(sql_stock, (quantite, id_article))

    # On valide les changements dans la base de données
    get_db().commit()



    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()

    if not(article_panier is None) and article_panier['quantite_panier'] > 1:
        sql = '''UPDATE ligne_panier SET quantite_panier = quantite_panier-%s  WHERE utilisateur_id = %s AND jean_id=%s'''
        mycursor.execute(sql, (quantite, id_client, id_article))

    else:
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND jean_id=%s'''
        mycursor.execute(sql, (id_client, id_article))

    # mise à jour du stock de l'article disponible
    get_db().commit()
    mycursor.execute("UPDATE jean SET stock_ = stock_ + %s WHERE id_jean=%s", (quantite, id_article))
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'article pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

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
