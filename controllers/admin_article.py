#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()

    sql = '''
          SELECT jean.id_jean                                    AS id_article,
                 jean.nom_jean                                   AS nom,
                 jean.prix_jean                                  AS prix,
                 jean.photo                                      AS image,
                 coupe_jean.nom_coupe                            AS libelle,
                 coupe_jean.id_coupe_jean                        AS type_article_id,
                 COUNT(commentaire.id_commentaire)               AS nb_commentaires_total,
                 IFNULL(SUM(commentaire.etat_validation = 1), 0) AS nb_commentaires_valides,
                 IFNULL(SUM(commentaire.etat_validation = 0), 0) AS nb_commentaires_nouveaux,
                 COUNT(DISTINCT declinaison.id_declinaison)      AS nb_declinaisons,
                 IFNULL(SUM(declinaison.stock = 0), 0)           AS nb_ruptures,
                 IFNULL(SUM(declinaison.stock), jean.stock_)     AS stock
          FROM jean
                   LEFT JOIN coupe_jean ON jean.coupe_jean_id = coupe_jean.id_coupe_jean
                   LEFT JOIN commentaire ON jean.id_jean = commentaire.id_jean
                   LEFT JOIN declinaison ON jean.id_jean = declinaison.jean_id
          GROUP BY jean.id_jean, coupe_jean.nom_coupe, coupe_jean.id_coupe_jean
          ORDER BY jean.nom_jean 
          '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    sql = "SELECT id_coupe_jean AS id_type_article, nom_coupe AS libelle FROM coupe_jean ORDER BY nom_coupe"
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    return render_template('admin/article/add_article.html'
                           ,types_article=types_article
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', 0)
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''
     INSERT INTO jean (nom_jean, photo, prix_jean, coupe_jean_id, stock_) 
        VALUES (%s, %s, %s, %s, %s)'''

    tuple_add = (nom, filename, prix, type_article_id, stock)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix,
          ' - description:', stock, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - stock:' + stock + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' 
     SELECT COUNT(*) AS nb_commandes FROM ligne_commande WHERE jean_id = %s
     '''
    mycursor.execute(sql, id_article)
    resultat = mycursor.fetchone()

    if resultat['nb_commandes'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' SELECT photo AS image FROM jean WHERE id_jean = %s '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        print(article)
        image = article['image'] if article else None

        mycursor.execute("DELETE FROM ligne_panier WHERE jean_id = %s", (id_article,))
        mycursor.execute("DELETE FROM declinaison WHERE jean_id = %s", (id_article,))
        mycursor.execute("DELETE FROM note WHERE id_jean = %s", (id_article,))
        mycursor.execute("DELETE FROM commentaire WHERE id_jean = %s", (id_article,))

        sql_delete_declinaison = "DELETE FROM declinaison WHERE jean_id = %s"
        mycursor.execute(sql_delete_declinaison, id_article)

        sql = ''' DELETE FROM jean WHERE id_jean = %s  '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
    SELECT id_jean AS id_article, 
               nom_jean AS nom, 
               prix_jean AS prix, 
               photo AS image, 
               coupe_jean_id AS type_article_id,
               description
        FROM jean 
        WHERE id_jean = %s 
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    print(article)
    sql = '''
    SELECT id_coupe_jean AS id_type_article, nom_coupe AS libelle FROM coupe_jean ORDER BY nom_coupe
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql_declinaison = '''
     SELECT d.id_declinaison AS id_declinaison_article, 
               d.stock, 
               t.nom_taille AS libelle_taille,
               c.nom_couleur AS libelle_couleur,
               d.jean_id AS article_id
        FROM declinaison d
        JOIN taille t ON d.taille_id = t.id_taille
        JOIN couleur c ON d.couleur_id = c.id_couleur
        WHERE d.jean_id = %s
     '''
    mycursor.execute(sql_declinaison, id_article)
    declinaisons_article = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                           ,article=article
                           ,types_article=types_article
                           ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    sql = '''
       SELECT photo AS image FROM jean WHERE id_jean = %s
       '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''
     UPDATE jean 
        SET nom_jean = %s, photo = %s, prix_jean = %s, coupe_jean_id = %s, description = %s 
        WHERE id_jean = %s
        '''
    mycursor.execute(sql, (nom, image_nom, prix, type_article_id, description, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
