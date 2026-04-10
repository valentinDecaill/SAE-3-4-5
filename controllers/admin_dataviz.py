#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template
from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__, template_folder='templates')


@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()
    id_categorie = request.args.get('id_categorie', None)

    if id_categorie is None:

        sql = '''
              SELECT c.id_coupe_jean, 
                     c.nom_coupe                                 AS libelle, 
                     COUNT(DISTINCT n.id_utilisateur, n.id_jean) AS nb_notes, 
                     IFNULL(ROUND(AVG(n.valeur), 1), 0)          AS note_moyenne, 
                     COUNT(DISTINCT com.id_commentaire)          AS nb_commentaires
              FROM coupe_jean c
                       LEFT JOIN jean j ON c.id_coupe_jean = j.coupe_jean_id
                       LEFT JOIN note n ON j.id_jean = n.id_jean
                       LEFT JOIN commentaire com ON j.id_jean = com.id_jean
              GROUP BY c.id_coupe_jean, c.nom_coupe 
              '''
        mycursor.execute(sql)
        datas_show = mycursor.fetchall()

        # données pour les graphiques
        labels = [d['libelle'] for d in datas_show]
        valeurs_notes = [d['nb_notes'] for d in datas_show]
        valeurs_moyennes = [d['note_moyenne'] for d in datas_show]
        valeurs_commentaires = [d['nb_commentaires'] for d in datas_show]

        return render_template('admin/dataviz/dataviz_etat_1.html',
                               datas_show=datas_show,
                               labels=labels,
                               valeurs_notes=valeurs_notes,
                               valeurs_moyennes=valeurs_moyennes,
                               valeurs_commentaires=valeurs_commentaires)

    else:

        # nom de la catégorie pour l'affichage
        mycursor.execute("SELECT nom_coupe FROM coupe_jean WHERE id_coupe_jean = %s", (id_categorie,))
        cat_info = mycursor.fetchone()
        nom_categorie = cat_info['nom_coupe'] if cat_info else "Catégorie"

        sql = '''
              SELECT j.nom_jean                         AS libelle, 
                     COUNT(DISTINCT n.id_utilisateur)   AS nb_notes, 
                     IFNULL(ROUND(AVG(n.valeur), 1), 0) AS note_moyenne, 
                     COUNT(DISTINCT com.id_commentaire) AS nb_commentaires
              FROM jean j
                       LEFT JOIN note n ON j.id_jean = n.id_jean
                       LEFT JOIN commentaire com ON j.id_jean = com.id_jean
              WHERE j.coupe_jean_id = %s
              GROUP BY j.id_jean, j.nom_jean 
              '''
        mycursor.execute(sql, (id_categorie,))
        datas_detail = mycursor.fetchall()

        # données pour les graphiques détaillés
        labels = [d['libelle'] for d in datas_detail]
        valeurs_notes = [d['nb_notes'] for d in datas_detail]
        valeurs_moyennes = [d['note_moyenne'] for d in datas_detail]
        valeurs_commentaires = [d['nb_commentaires'] for d in datas_detail]

        return render_template('admin/dataviz/dataviz_etat_1.html',
                               datas_detail=datas_detail,
                               nom_categorie=nom_categorie,
                               labels=labels,
                               valeurs_notes=valeurs_notes,
                               valeurs_moyennes=valeurs_moyennes,
                               valeurs_commentaires=valeurs_commentaires)