# ------------------------- LES IMPORTATIONS NECESSAIRES -------------------------#

import pandas as pd
from datetime import date

class PriceDataManager:
    def __init__(self, csv_filename, store):
        """
        Initialise le gestionnaire de données de prix.

        Paramètres
        ----------
        csv_filename : str
            Nom du fichier CSV pour enregistrer les données de prix.
        store : str
            Nom du magasin associé aux données de prix.
        """
        self.csv_filename = csv_filename  # Nom du fichier CSV
        self.store = store  # Nom du magasin associé

    def save_product_to_csv(self, product_name, price):
        """
        Enregistre le prix d'un produit dans un fichier CSV.

        Paramètres
        ----------
        product_name : str
            Nom du produit.
        price : float
            Prix du produit.

        Returns
        -------
        str
            Message confirmant l'enregistrement du produit.
        """
        today_date = date.today().strftime("%d/%m/%Y")
        df = pd.DataFrame({'Product': [product_name], 'Price': [price], 'Date': [today_date]})

        try:
            # Charger le CSV existant
            existing_df = pd.read_csv(self.csv_filename, sep=';')
        except FileNotFoundError:
            # Le CSV n'existe pas encore, créons-le
            existing_df = pd.DataFrame(columns=['Product', 'Price', 'Date'])

        existing_df = existing_df.append(df, ignore_index=True)
        existing_df.to_csv(self.csv_filename, sep=';', index=False)
        return f"Produit enregistré dans {self.csv_filename}"

    def check_price_variation(self, product_name, price, today_date):
        """
        Vérifie la variation de prix d'un produit.

        Paramètres
        ----------
        product_name : str
            Nom du produit.
        price : float
            Prix actuel du produit.
        today_date : str
            Date actuelle au format "dd/mm/yyyy".

        Returns
        -------
        str
            Message indiquant s'il y a eu une variation de prix pour le produit.
        """
        try:
            # Charger le CSV existant
            existing_df = pd.read_csv(self.csv_filename, sep=';')

            # Rechercher le produit dans notre fichier CSV
            product_entry = existing_df[(existing_df['Product'] == product_name) & (existing_df['Store'] == self.store)]

            if not product_entry.empty:
                # Ici, le produit existe, donc nous vérifions la variation de prix
                last_price = product_entry.iloc[-1]['Price']
                if price != last_price:
                    # S'il y a eu une variation de prix, on enregistre une nouvelle entrée
                    self.save_product_to_csv(product_name, price)
                    return f"Le prix de {product_name} a varié. Il était à {last_price}€ le {today_date}."

        except FileNotFoundError:
            pass  # Le CSV n'existe pas encore, il y a aucune variation de prix à vérifier, donc on passe

        return f"Aucun changement de prix pour {product_name} depuis la dernière vérification."
