#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')



@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    id_article = request.args.get('id_article', None)
    id_client = session['id_user']

    # détail de l article et note moyenne globale
    sql = '''
        SELECT jean.*, 
               COUNT(DISTINCT note.id_utilisateur) AS nb_notes,
               ROUND(AVG(note.valeur), 1) AS moyenne_notes
        FROM jean
        LEFT JOIN note ON jean.id_jean = note.id_jean
        WHERE jean.id_jean = %s
        GROUP BY jean.id_jean
    '''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()

    if article is None:
        abort(404, "pb id article")

    # liste des commentaire
    sql = '''
          SELECT c.*, u.login
          FROM commentaire c
          JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
          WHERE c.id_jean = %s
          ORDER BY c.date_publication DESC 
          '''
    mycursor.execute(sql, (id_article,))
    commentaires = mycursor.fetchall()

    # combien de fois l'utilisateur a-t-il acheté l'article
    sql = '''
          SELECT COUNT(lc.jean_id) AS nb_commandes_article
          FROM ligne_commande lc 
          JOIN commande c ON lc.commande_id = c.id_commande
          WHERE c.utilisateur_id = %s AND lc.jean_id = %s
          '''
    mycursor.execute(sql, (id_client, id_article))
    commandes_articles = mycursor.fetchone()

    # Récupérer la note de l'utilisateur
    sql = '''SELECT valeur AS note FROM note WHERE id_utilisateur = %s AND id_jean = %s'''
    mycursor.execute(sql, (id_client, id_article))
    note_row = mycursor.fetchone()
    note = note_row['note'] if note_row else None

    # Quotas
    sql = '''
          SELECT COUNT(id_commentaire) AS total, 
                 IFNULL(SUM(etat_validation = 1), 0) AS total_valide, 
                 IFNULL(SUM(id_utilisateur = %s), 0) AS user_total, 
                 IFNULL(SUM(id_utilisateur = %s AND etat_validation = 1), 0) AS user_valide
          FROM commentaire
          WHERE id_jean = %s 
          '''
    mycursor.execute(sql, (id_client, id_client, id_article))
    nb_commentaires = mycursor.fetchone()

    return render_template('client/article_info/article_details.html'
                           , article=article
                           , commentaires=commentaires
                           , commandes_articles=commandes_articles
                           , note=note
                           , nb_commentaires=nb_commentaires
                           )



@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/article/details?id_article='+id_article)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/article/details?id_article='+id_article)

    sql_verif_quota = '''
                      SELECT COUNT(*) AS nb_com_user
                      FROM commentaire
                      WHERE id_utilisateur = %s 
                        AND id_jean = %s 
                      '''
    mycursor.execute(sql_verif_quota, (id_client, id_article))
    resultat = mycursor.fetchone()

    if resultat['nb_com_user'] >= 3:
        flash(u'Quota atteint : Vous ne pouvez publier que 3 commentaires maximum pour cet article.', 'alert-danger')
        return redirect('/client/article/details?id_article=' + id_article)

    # Si le quota n'est pas atteint on peut ajouter le commentaire
    tuple_insert = (commentaire, id_client, id_article)
    sql = '''
          INSERT INTO commentaire (contenu, id_utilisateur, id_jean)
          VALUES (%s, %s, %s) 
          '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    flash(u'Votre commentaire a été ajouté avec succès.', 'alert-success')
    return redirect('/client/article/details?id_article=' + id_article)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)

    # On supprime uniquement si l'utilisateur est bien l'auteur du commentaire
    sql = '''
          DELETE 
          FROM commentaire
          WHERE id_utilisateur = %s 
            AND id_jean = %s 
            AND date_publication = %s 
          '''
    tuple_delete = (id_client, id_article, date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article=' + id_article)


@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)

    tuple_insert = (note, id_client, id_article)
    sql = '''
          INSERT INTO note (valeur, id_utilisateur, id_jean)
          VALUES (%s, %s, %s) 
          '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article=' + id_article)


@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)

    tuple_update = (note, id_client, id_article)
    sql = '''
          UPDATE note 
          SET valeur = %s
          WHERE id_utilisateur = %s 
            AND id_jean = %s 
          '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?id_article=' + id_article)


@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)

    tuple_delete = (id_client, id_article)
    sql = '''
          DELETE 
          FROM note
          WHERE id_utilisateur = %s 
            AND id_jean = %s 
          '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article=' + id_article)