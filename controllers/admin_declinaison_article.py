#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                                      template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['GET'])
def add_declinaison_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()

    # 1. On récupère le jean (en renommant les colonnes pour ton HTML)
    mycursor.execute("SELECT id_jean AS id_article, nom_jean, photo AS image FROM jean WHERE id_jean = %s", id_article)
    article = mycursor.fetchone()


    mycursor.execute("SELECT DISTINCT taille_id FROM declinaison WHERE jean_id = %s", (id_article,))
    tailles_utilisees = [row['taille_id'] for row in mycursor.fetchall()]

    if 1 in tailles_utilisees:
    # S'il y a déjà une Taille Unique, on ne propose QUE Taille Unique
        mycursor.execute("SELECT id_taille, nom_taille AS libelle FROM taille WHERE id_taille = 1")
    elif len(tailles_utilisees) > 0:
    # S'il y a des tailles normales, on CACHE la Taille Unique (id 1)
        mycursor.execute("SELECT id_taille, nom_taille AS libelle FROM taille WHERE id_taille > 1 ORDER BY id_taille")
    else:
    # S'il n'y a aucune déclinaison, on propose tout
        mycursor.execute("SELECT id_taille, nom_taille AS libelle FROM taille ORDER BY id_taille")
    tailles = mycursor.fetchall()

# --- LOGIQUE POINT 14 : GESTION DES COULEURS UNIQUES ---
    mycursor.execute("SELECT DISTINCT couleur_id FROM declinaison WHERE jean_id = %s", (id_article,))
    couleurs_utilisees = [row['couleur_id'] for row in mycursor.fetchall()]

    if 1 in couleurs_utilisees:
        mycursor.execute("SELECT id_couleur, nom_couleur AS libelle FROM couleur WHERE id_couleur = 1")
    elif len(couleurs_utilisees) > 0:
        mycursor.execute("SELECT id_couleur, nom_couleur AS libelle FROM couleur WHERE id_couleur > 1 ORDER BY id_couleur")
    else:
        mycursor.execute("SELECT id_couleur, nom_couleur AS libelle FROM couleur ORDER BY id_couleur")
    couleurs = mycursor.fetchall()

    return render_template('admin/article/add_declinaison_article.html',
                       article=article,
                       tailles=tailles,
                       couleurs=couleurs)


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()

    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    taille_id = request.form.get('taille')
    couleur_id = request.form.get('couleur')

    # Vérification anti-doublon
    sql_check = "SELECT * FROM declinaison WHERE jean_id = %s AND taille_id = %s AND couleur_id = %s"
    mycursor.execute(sql_check, (id_article, taille_id, couleur_id))
    decli_existante = mycursor.fetchone()

    if decli_existante:
        flash(u'Cette variante existe déjà ! Veuillez plutôt modifier son stock.', 'alert-warning')
    else:
        sql_insert = "INSERT INTO declinaison (jean_id, taille_id, couleur_id, stock) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql_insert, (id_article, taille_id, couleur_id, stock))
        get_db().commit()
        flash(u'Déclinaison ajoutée avec succès !', 'alert-success')

    return redirect('/admin/article/edit?id_article=' + str(id_article))


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article')
    mycursor = get_db().cursor()

    # On récupère la déclinaison ET les infos de l'article pour ton HTML
    sql_decli = '''
        SELECT d.id_declinaison AS id_declinaison_article, 
               d.stock, d.taille_id, d.couleur_id, d.jean_id AS article_id,
               j.nom_jean AS nom, j.photo AS image_article
        FROM declinaison d
        JOIN jean j ON d.jean_id = j.id_jean
        WHERE d.id_declinaison = %s
    '''
    mycursor.execute(sql_decli, id_declinaison_article)
    declinaison_article = mycursor.fetchone()
    id_article = declinaison_article['article_id']

    mycursor.execute("SELECT id_taille, nom_taille AS libelle FROM taille ORDER BY id_taille")
    tailles = mycursor.fetchall()

    mycursor.execute("SELECT id_couleur, nom_couleur AS libelle FROM couleur ORDER BY id_couleur")
    couleurs = mycursor.fetchall()

    mycursor.execute("SELECT DISTINCT taille_id FROM declinaison WHERE jean_id = %s", (id_article,))
    tailles_utilisees = [row['taille_id'] for row in mycursor.fetchall()]
    d_taille_uniq = 1 if 1 in tailles_utilisees else 0

    mycursor.execute("SELECT DISTINCT couleur_id FROM declinaison WHERE jean_id = %s", (id_article,))
    couleurs_utilisees = [row['couleur_id'] for row in mycursor.fetchall()]
    d_couleur_uniq = 1 if 1 in couleurs_utilisees else 0

    return render_template('admin/article/edit_declinaison_article.html',
                           declinaison_article=declinaison_article,
                           tailles=tailles,
                           couleurs=couleurs,
                           d_taille_uniq=d_taille_uniq,
                           d_couleur_uniq=d_couleur_uniq,)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    mycursor = get_db().cursor()

    id_declinaison_article = request.form.get('id_declinaison_article')
    id_article = request.form.get('id_article')
    stock = request.form.get('stock')

    taille_id = request.form.get('id_taille') or request.form.get('taille')
    couleur_id = request.form.get('id_couleur') or request.form.get('couleur')

    sql = "UPDATE declinaison SET taille_id = %s, couleur_id = %s, stock = %s WHERE id_declinaison = %s"
    mycursor.execute(sql, (taille_id, couleur_id, stock, id_declinaison_article))
    get_db().commit()

    flash(u'Déclinaison modifiée avec succès !', 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article')
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()

    try:
        mycursor.execute("DELETE FROM declinaison WHERE id_declinaison = %s", id_declinaison_article)
        get_db().commit()
        flash(u'Déclinaison supprimée avec succès.', 'alert-success')
    except:
        flash(u'Impossible : cette déclinaison est déjà dans le panier ou la commande d\'un client.', 'alert-warning')

    return redirect('/admin/article/edit?id_article=' + str(id_article))