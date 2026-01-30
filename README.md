# SAE-3-4-5
# Projet SAE 3-4-5 : Site E-commerce Flask

Ce projet est une application web e-commerce développée en Python avec le framework **Flask** et une base de données **MySQL**. Il comprend une interface client (boutique, panier, commande) et une interface administrateur (gestion des articles, visualisation des données).

## Auteurs / groupe et sujet SAE
- Decailloz Valentin
- Charton--Cautenet Mael
- Groupe 2, sujet 13

## Prérequis

* **Python 3** installé sur la machine.
* **MySQL** (ou MariaDB) installé et actif.
* **Git** pour la gestion de versions.

## Installation et Configuration

Suivez ces étapes pour installer le projet sur une nouvelle machine.

### 1. Récupérer le code
Clonez le dépôt Git :
git clone [https://github.com/valentinDecaill/SAE-3-4-5.git](https://github.com/valentinDecaill/SAE-3-4-5.git)

### 2. Créer l'environnement virtuel
Créez un environnement virtuel pour isoler les dépendances du projet :
 $ python3 -m venv .venv
 $ source .venv/bin/activate

### 3. Installer les dépendances
Installez toutes les bibliothèques nécessaires:
  $ pip install -r requirements.txt
  
### 4. Configuration de la Base de Données
tables et insert dans **"sae_sql.sql"**
faite un fichier **connexion_db.py*** en utilisant le modèle fournit : **connexion_db_sample.py**

### 5. Lancement de l'application
  $ python app.py
