#Ici, il n'y pas d'importations nécessaires à faire

class DataManager:
    def __init__(self, scraper):
        """
        Initialise le gestionnaire de données.

        Paramètres
        ----------
        scraper : WebScraper
            Instance du WebScraper pour récupérer les données.
        """
        self.scraper = scraper  
        self.all_products = {
            "auchan": {},  
            "carrefour": {}  
        }

    def collect_data(self, course_list):
        """
        Collecte les données de prix pour une liste de courses donnée.

        Paramètres
        ----------
        course_list : list
            Liste des produits à rechercher et à collecter.
        """
        for product in course_list:
            # Collecte les données de prix depuis Auchan
            self.all_products["auchan"][product] = self.scraper.fetch_prices_from_auchan(product)
            
            # Collecte les données de prix depuis Carrefour
            self.all_products["carrefour"][product] = self.scraper.fetch_prices_from_carrefour(product)

    def user_selection(self, course_list):
        """
        Permet à l'utilisateur de sélectionner des produits parmi les résultats.

        Paramètres
        ----------
        course_list : list
            Liste des produits à partir desquels l'utilisateur peut choisir.

        Returns
        -------
        dict
            Dictionnaire contenant les produits sélectionnés, triés par magasin.
        """
        selected_products = {
            "auchan": [],   
            "carrefour": []  
        }

        for product in course_list:
            print(f"Produits pour {product}:")
            for store, products in self.all_products.items():
                print(f"Magasin: {store}")
                for idx, (name, price) in enumerate(products[product], start=1):
                    print(f"{idx}. {name} - {price}€")

                selection = int(input(f"Quel produit voulez-vous choisir pour {store}? (1-10): "))
                selected_products[store].append(products[product][selection-1])

        return selected_products  # Renvoie les produits sélectionnés triés par magasin
