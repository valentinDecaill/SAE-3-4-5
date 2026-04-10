#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__, template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_article = request.args.get('id_article', None)

    # Liste des commentaires
    sql = '''
          SELECT c.*, IFNULL(u.login, 'Utilisateur Inconnu') AS nom
          FROM commentaire c
                   LEFT JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
          WHERE c.id_jean = %s
          ORDER BY c.etat_validation ASC, c.date_publication DESC 
          '''
    mycursor.execute(sql, (id_article,))
    commentaires = mycursor.fetchall()

    # Détails de l'article
    sql = '''
          SELECT j.id_jean                        AS id_article, 
                 j.nom_jean                       AS nom,
                 COUNT(DISTINCT n.id_utilisateur) AS nb_notes,
                 ROUND(AVG(n.valeur), 1)          AS moyenne_notes
          FROM jean j
                   LEFT JOIN note n ON j.id_jean = n.id_jean
          WHERE j.id_jean = %s
          GROUP BY j.id_jean 
          '''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()

    # Compteurs
    sql = '''
          SELECT COUNT(id_commentaire)               AS nb_commentaires_total, 
                 IFNULL(SUM(etat_validation = 1), 0) AS nb_commentaires_valider
          FROM commentaire
          WHERE id_jean = %s 
          '''
    mycursor.execute(sql, (id_article,))
    nb_commentaires = mycursor.fetchone()

    return render_template('admin/article/show_article_commentaires.html',
                           commentaires=commentaires,
                           article=article,
                           nb_commentaires=nb_commentaires)


@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_commentaire = request.form.get('id_commentaire', None)
    id_article = request.form.get('id_article', None)

    sql = '''DELETE 
             FROM commentaire 
             WHERE id_commentaire = %s'''
    mycursor.execute(sql, (id_commentaire,))
    get_db().commit()

    return redirect('/admin/article/commentaires?id_article=' + str(id_article))


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST', 'GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_commentaire = request.args.get('id_commentaire', None)
        id_article = request.args.get('id_article', None)
        return render_template('admin/article/add_commentaire.html', id_commentaire=id_commentaire,
                               id_article=id_article)

    mycursor = get_db().cursor()
    id_commentaire = request.form.get('id_commentaire', None)
    id_article = request.form.get('id_article', None)
    reponse = request.form.get('reponse', None)

    sql = '''UPDATE commentaire 
             SET reponse_admin = %s 
             WHERE id_commentaire = %s'''
    mycursor.execute(sql, (reponse, id_commentaire))
    get_db().commit()

    return redirect('/admin/article/commentaires?id_article=' + str(id_article))


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['POST', 'GET'])
def admin_comment_valider():
    id_article = request.args.get('id_article', None)
    mycursor = get_db().cursor()

    sql = '''UPDATE commentaire 
             SET etat_validation = 1 
             WHERE id_jean = %s'''
    mycursor.execute(sql, (id_article,))
    get_db().commit()

    return redirect('/admin/article/commentaires?id_article=' + str(id_article))