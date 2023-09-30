# Project : Comparateur de Paniers Supermarchés
Ce projet fait partie du programme du cours Architectures et Langages de Données : Advanced Programming du Master 2 - Data Science de la Faculté des Sciences Économiques et de Gestion, Université de Strasbourg.

Ce projet vise à résoudre les difficultés liées à l'augmentation drastique du coût de la vie. Avec l'augmentation de l'inflation ces dernières années, des nombreuses personnes pourraient avoir du mal à survivre financièrement dans de telles circonstances. Notre Comparateur de Paniers Supermarchés permet aux utilisateurs d'avoir un aperçu des prix de leur panier d'achat dans différents supermarchés. Les principales chaînes de supermarchés en France (Auchan et Carrefour) ont été choisies pour ce projet.
Il utilise un scraper web pour collecter les données, gère les variations de prix, enregistre les résultats dans un fichier CSV, et envoie des e-mails de comparaison.

Le code prend les saisies des utilisateurs pour rechercher des produits chez Auchan et Carrefour. Pour la comparaison des prix, ce projet prend en compte les comportements d'achat des utilisateurs. Il se compose de 2 modes.
          (1) Manuel - cela permet aux utilisateurs de choisir manuellement leurs articles préférés
          (2) Automatique - cela choisit automatiquement l'article au prix le plus bas

La structure de ce projet est composée de 4 parties :

# 1. Web-Scrapping
Nous avons choisi Selenium pour ce projet. En exécutant le code, les utilisateurs doivent saisir le(s) article(s) qu'ils souhaitent acheter. Ils peuvent entrer un ou plusieurs produits (séparés par une virgule (,)). Pour effectuer les étapes suivantes de ce projet, nous avons extrait les données des sites Web des différents supermarchés (Auchan et Carrefour). Dans le cas d'Auchan, la localisation géographique et la connexion sont requises et nous avons choisi la succursale d'Auchan située près du centre de Strasbourg. Le script effectue l'automatisation Web et fait défiler progressivement les pages Web tout en récupérant les noms et les prix des produits.
# 2. Comparaison des Prix
Après la récupération des données, le script enregistre les informations sur le type de produit, le nom du produit, le magasin, le prix et la date dans le fichier CSV (si le fichier CSV n'existe pas, il le crée automatiquement). Les données stockées dans le fichier CSV est ensuite utilisées pour visualiser le variation des prix des produits sélectionnés entre la recherche précédente et la recherche récente. S'il n'y a aucun changement depuis la dernière recherche, il nous précise que le prix n'a pas varié depuis la dernière fois. Cela s'applique aux modes manuel et automatique.
# 3. Interface/Dashboard
Streamlit, qui est une application web en open-source, a été choisie comme plateforme pour notre projet.
Pour lancer Streamlit :
(1)En Python : pip install streamlit
(2)Dans votre Commandes/Anaconda prompt:
cd chemin/vers/le/répertoire/de/votre/projet
conda activate base
streamlit run Stream_lit_V1.py
(3)Par défaut, cela ouvrira un nouvel onglet dans votre navigateur web avec l'adresse http://localhost:8501
# 4. Rapport par Email
Une fois que le code a terminé l'analyse, il envoie un rapport par email indiquant le prix des produits dans les deux magasins, lequel des deux magasins est moins cher pour ces produits, combien d'argent l'utilisateur peut économiser et les produits qui ont eu des variations de leurs prix la dernière recherche de l'utilisateur.
# 5. Fichiers du Projet

- **main.py**: Ce fichier est le point d'entrée de l'application. Il exécute la fonction principale `main`, qui coordonne l'ensemble du processus de comparaison.

- **web_scraper.py**: Contient la classe `WebScraper`, qui permet d'extraire des données à partir de sites web. Elle est utilisée pour récupérer les prix des produits.

- **data_manager.py**: Le fichier `data_manager.py` contient la classe `DataManager`. Elle gère la structuration des données collectées depuis le scraper.

- **price_data_manager.py**: Dans ce fichier, vous trouverez la classe `PriceDataManager`, responsable de l'enregistrement des prix des produits dans un fichier CSV. Elle permet de suivre les variations de prix au fil du temps.

- **email_manager.py**: Le fichier `email_manager.py` contient la classe `EmailManager`. Elle gère l'envoi d'e-mails contenant les informations de comparaison de prix entre Auchan et Carrefour.

- **Autres fichiers**: En plus de ces fichiers principaux, d'autres modules et fichiers peuvent être présents pour des fonctionnalités spécifiques ou des utilitaires.

## Utilisation

Pour utiliser ce projet, suivez les instructions suivantes :
1. Exécutez `main.py` pour démarrer la comparaison de prix.
2. Suivez les invites pour entrer votre liste de courses et sélectionner les produits à comparer.
3. Les résultats seront affichés, et vous recevrez un e-mail de comparaison des prix.

N'hésitez pas à explorer les fichiers individuels pour plus de détails sur chaque composant de l'application.

Pour des informations plus détaillées sur l'utilisation et les fonctionnalités, consultez le code source de chaque fichier.

**Note** : - Assurez-vous d'avoir les bibliothèques Python nécessaires installées en utilisant `pip install -r requirements.txt`.
           - Avant d'exécuter `main.py`, vous devez compléter votre adresse mail dans "recipient_email" pour recevoir le mail de                comparaison des prix
           - Pour une meilleur utilisation, exécutez ce code dans un environnement de développement Python plutôt que directement               dans le terminal.

# Nos équipes
Fervent BATINA-AGASA et Nattirat PROMWANG
