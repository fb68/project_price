# Project : Comparateur de Paniers Supermarchés
Ce projet fait partie du programme du cours Architectures et Langages de Données : Advanced Programming du Master 2 - Data Science de la Faculté des Sciences Économiques et de Gestion, Université de Strasbourg.

Ce projet vise à résoudre les difficultés liées à l'augmentation drastique du coût de la vie. Avec l'augmentation de l'inflation ces dernières années, de nombreuses personnes pourraient avoir du mal à survivre financièrement dans de telles circonstances. Notre Comparateur de Paniers Supermarchés permet aux utilisateurs d'avoir un aperçu des prix de leur panier d'achat dans différents supermarchés. Les principales chaînes de supermarchés en France (Auchan et Carrefour) ont été choisies pour ce projet.

Le code prend les saisies des utilisateurs pour rechercher des produits chez Auchan et Carrefour. Pour la comparaison des prix, ce projet prend en compte les comportements d'achat des utilisateurs. Il se compose de 2 modes.
          (1) Manuel - cela permet aux utilisateurs de choisir manuellement leurs articles préférés
          (2) Automatique - cela choisit automatiquement l'article au prix le plus bas

La structure de ce projet est composée de 4 parties : [####ce n'est pas la version finale.]

# 1. Web-Scrapping
Nous avons choisi Selenium pour ce projet. En exécutant le code, les utilisateurs doivent saisir le(s) article(s) qu'ils souhaitent acheter. Ils peuvent entrer un ou plusieurs produits (séparés par une virgule (,)). Pour effectuer les étapes suivantes de ce projet, nous avons extrait les données des sites Web des différents supermarchés (Auchan et Carrefour). Dans le cas d'Auchan, la localisation géographique et la connexion sont requises et nous avons choisi la succursale d'Auchan située près du centre de Strasbourg. Le script effectue l'automatisation Web et fait défiler progressivement les pages Web.
# 2. Comparaison des Prix (Taux d'Inflation)
Après la récupération des données, le script enregistre les informations sur le type de produit, le nom du produit, le magasin, le prix et la date dans le fichier CSV. Ceci est ensuite utilisé pour calculer le changement de prix entre la recherche précédente et la recherche récente. Il affiche la différence de prix en termes de taux d'inflation. Cela s'applique aux modes manuel et automatique.
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
Une fois que le code a terminé l'analyse, il envoie un rapport par email indiquant le prix des produits dans les deux magasins, lequel des deux magasins est moins cher pour ces produits, combien d'argent l'utilisateur peut économiser et quel est le taux d'inflation depuis la dernière recherche de l'utilisateur.

