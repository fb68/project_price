# ------------------------- LES IMPORTATIONS NECESSAIRES -------------------------#

from web_scraper import WebScraper, initialize_driver  
from data_manager import DataManager 
from price_data_manager import PriceDataManager  
from email_manager import EmailManager  
import pandas as pd  
from datetime import date  

# Notre fonction principale

def main(driver):
    """C'est notre Fonction principale pour exécuter la comparaison des paniers d'achat"""
    today_date = date.today().strftime("%d/%m/%Y")
    
    #url = l'url de connexion de Auchan
    url = "https://compte.auchan.fr/auth/realms/auchan.fr/protocol/openid-connect/auth?client_id=lark-crest&state=8798f4c2-d76e-4373-a6b3-d6f9a065d3b5&redirect_uri=https%3A%2F%2Fwww.auchan.fr%2Fauth%2Flogin%2F68747470733a2f2f7777772e61756368616e2e66722f6f75766572747572652d61756368616e2d706965746f6e2f65702d6f75766572747572652d61756368616e2d706965746f6e3f736f757263653d676f6f676c65266d656469756d3d7365612675746d5f63616d706169676e3d3137323237363737373231267465726d3d61756368616e25323063253236632663757374706172616d7472616669633d31373232373637373732312d3133363630373239353833372d3632353030393438313233322671745f69643d7169645f6761645f6331373232373637373732315f673133363630373239353833375f613632353030393438313233322667636c69643d4541496149516f6243684d49752d6631684f756967514d5630716a56436831387351473745414159415341414567494c5a5f445f4277452667636c7372633d61772e6473%3Fauth_callback%3D1&scope=openid&response_type=code"
    username = "projetpythonm2@gmail.com"  
    password = "Strasbourg2023." 
    scraper = WebScraper(driver)  
    scraper.login_if_needed(url, username, password)
    manager = DataManager(scraper)  
    email_manager = EmailManager()  # Ici on a crée une instance de la classe EmailManager

    shopping_list_auchan = []  
    shopping_list_carrefour = []  

    # On initialise un dictionnaire pour stocker les produits de chaque magasin
    all_products = {
        "auchan": {},
        "carrefour": {}
    }

    # 
    course_list = input("Entrez votre liste de courses séparée par des virgules: ").split(',')
    selection_mode = input("Voulez-vous sélectionner les produits manuellement ou automatiquement? (1 pour Manuel, 2 pour Auto): ")
   
    # Récupération des produits pour Auchan
    for product in course_list:
        product = product.strip()  
        all_products["auchan"][product] = scraper.fetch_prices_from_auchan(product)

    # Récupération des produits pour Carrefour
    for product in course_list:
        product = product.strip()  # Supprime les espaces autour du produit
        all_products["carrefour"][product] = scraper.fetch_prices_from_carrefour(product)
        
    # On crée des instances de la classe PriceDataManager pour Auchan et Carrefour
    auchan_price_manager = PriceDataManager('auchan_prices.csv', 'auchan')
    carrefour_price_manager = PriceDataManager('carrefour_prices.csv', 'carrefour')

    # On a fait une boucle pour sélectionner les produits des magasins
    for product in course_list:
        product = product.strip()  
    
        auchan_prices = all_products["auchan"][product]  
        carrefour_prices = all_products["carrefour"][product] 
    
        if selection_mode == "1":
            
            # Affiche les produits des deux magasins pet demande à l'utilisateur de faire ses choix manuellement
            print("Produits disponibles pour", product, ":\n")
            for idx, (name, price) in enumerate(auchan_prices, start=1):
                print(f"{idx}. Auchan: {name} - {price}€")
                        
            for idx, (name, price) in enumerate(carrefour_prices, start=11):
                print(f"{idx}. Carrefour: {name} - {price}€")

            choice_auchan = int(input("Quel produit voulez-vous choisir chez Auchan? (1-10): "))
                
            choice_carrefour = int(input("Quel produit voulez-vous choisir chez Carrefour? (11-20): "))
    
            product_name_auchan, price_auchan = auchan_prices[choice_auchan-1]
            product_name_carrefour, price_carrefour = carrefour_prices[choice_carrefour-11]
    
            # Utilisation des instances pour gérer les prix et la variation des prix
            auchan_msg = auchan_price_manager.check_price_variation(product_name_auchan, price_auchan, today_date)
            carrefour_msg = carrefour_price_manager.check_price_variation(product_name_carrefour, price_carrefour, today_date)
    
            shopping_list_auchan.append((product_name_auchan, price_auchan))
            shopping_list_carrefour.append((product_name_carrefour, price_carrefour))
    
        elif selection_mode == "2":
            
            # ici, ça choisit automatiquement le produit le moins cher
            product_name_auchan, price_auchan = auchan_prices[0]
            product_name_carrefour, price_carrefour = carrefour_prices[0]
    
            # On utilise des instances pour gérer les prix et la variation
            auchan_msg = auchan_price_manager.check_price_variation(product_name_auchan, price_auchan, today_date)
            carrefour_msg = carrefour_price_manager.check_price_variation(product_name_carrefour, price_carrefour, today_date)
    
            shopping_list_auchan.append((product_name_auchan, price_auchan))
            shopping_list_carrefour.append((product_name_carrefour, price_carrefour))
    
                
    # On crée un DataFrame pour entrer les résultats de chaque magasin
    df_auchan = pd.DataFrame(shopping_list_auchan, columns=['Product_Auchan', 'Price_Auchan'])
    df_carrefour = pd.DataFrame(shopping_list_carrefour, columns=['Product_carrefour', 'Price_carrefour'])
    
    # Combine les deux dataframes et on le print pour une visualisation 
    df = pd.concat([df_auchan, df_carrefour], axis=1)
    print(df)

    # Calcule et affiche le total pour chaque magasin et on les print
    total_auchan = df_auchan["Price_Auchan"].sum()
    total_carrefour = df_carrefour["Price_carrefour"].sum()
    print(f"Total Auchan: {total_auchan:.2f}€")
    print(f"Total Carrefour: {total_carrefour:.2f}€")
    savings = abs(total_carrefour - total_auchan)
     
    if total_auchan < total_carrefour:
        store = "Auchan"
        savings_msg = f"Si vous allez chez Auchan, vous économiserez {savings:.2f}€"
    else:
        store = "Carrefour"
        savings_msg = f"Si vous allez chez Carrefour, vous économiserez {savings:.2f}€"
        
    print(auchan_msg)
    print(carrefour_msg)
    email_manager.send_email_with_hotmail(df_auchan, df_carrefour, savings_msg, auchan_msg, carrefour_msg)

if __name__ == "__main__":
    driver = initialize_driver()  
    main(driver)  
    driver.close()  
