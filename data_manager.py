class DataManager:
    def __init__(self, scraper):
        self.scraper = scraper
        self.all_products = {
            "auchan": {},
            "carrefour": {}
        }

    def collect_data(self, course_list):
        for product in course_list:
            self.all_products["auchan"][product] = self.scraper.fetch_prices_from_auchan(product)
            self.all_products["carrefour"][product] = self.scraper.fetch_prices_from_carrefour(product)

    def user_selection(self, course_list):
        """Let the user select products."""
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

        return selected_products