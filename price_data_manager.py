import pandas as pd
from datetime import date

class PriceDataManager:
    def __init__(self, csv_filename, store):
        self.csv_filename = csv_filename
        self.store = store

    def save_product_to_csv(self, product_name, price):
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
        print(f"Produit enregistré dans {self.csv_filename}")


    def check_price_variation(self, product_name, price, today_date):
        try:
            # Charger le CSV existant
            existing_df = pd.read_csv(self.csv_filename, sep=';')

            # Rechercher le produit dans le CSV
            product_entry = existing_df[(existing_df['Product'] == product_name) & (existing_df['Store'] == self.store)]

            if not product_entry.empty:
                # Le produit existe, vérifions la variation de prix
                last_price = product_entry.iloc[-1]['Price']
                if price != last_price:
                    # Il y a eu une variation de prix, enregistrons la nouvelle entrée
                    self.save_product_to_csv(product_name, price)
                    return f"Le prix de {product_name} a varié. Il était à {last_price}€ le {today_date}."

        except FileNotFoundError:
            pass  # Le CSV n'existe pas encore, aucune variation de prix à vérifier

        return f"Aucun changement de prix pour {product_name} depuis la dernière vérification."
