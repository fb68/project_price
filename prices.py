# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:10:03 2023

@author: ferve
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import date
import csv

# Initialiser le webdriver
def initialize_driver():
    # Configuration du driver Chrome
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(10)  # Attente implicite pour les éléments
    return driver

class WebScraper:
    def __init__(self, driver):
        self.driver = driver

    def login_if_needed(self, url, username, password):
        """Connect to the Auchan site if needed."""
        self.driver.get(url)

        try:
            # Remplir les champs de connexion et se connecter
            self.driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
            self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, "#kc-login").click()
            time.sleep(5)  # Attendre quelques secondes pour la connexion
        except Exception as e:
            print(f"Erreur lors de la tentative de connexion : {e}")

    def accept_cookies(self):
        """Accept cookies on the website."""
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler")))
            cookie_button.click()
            time.sleep(5)
        except:
            print("Impossible de trouver le bouton des cookies ou de cliquer dessus.")

    def scroll_page(self, css_selector, n=0):
        """Scroll through the page progressively."""
        element = self.driver.find_element(By.CSS_SELECTOR, "#wrapper > div.list__container")
        element.click()

        for i in range(n):
            try:
                action_chains = ActionChains(self.driver)
                action_chains.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(2)
            except Exception as e:
                print(str(e))

    def fetch_prices_from_auchan(self, product):
        """Retrieve product prices from Auchan."""
        self.accept_cookies()

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#search > input")
        search_box.clear()
        search_box.send_keys(product)
        search_box.submit()
        
        products = []
        seen_products = set()  # Pour garder une trace des produits déjà vus

        self.scroll_page("#search > input", 15)  # Fait défiler la page en 15 étapes

        wait = WebDriverWait(self.driver, 20)
        products_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#wrapper > div.list__container > article")))

        for product_element in products_elements:
            try:
                name_element = product_element.find_element(By.CSS_SELECTOR, "div.product-thumbnail__content-wrapper > a > div > p")
                name = name_element.text
                price_element = product_element.find_element(By.CSS_SELECTOR, "div.product-thumbnail__content-wrapper > footer > div.product-thumbnail__footer-wrapper > div.product-thumbnail__price.product-price__container > div")
                price = float(price_element.text.replace('€', '').replace(',', '.'))
                
                if name not in seen_products:
                    seen_products.add(name)
                    products.append((name, price))
                    print(f"Produit ajouté : {name} - {price}€")
            except Exception as e:
                print(f"Erreur lors de la récupération du produit : {e}")

        return sorted(products, key=lambda x: x[1])[:10]
    
    def fetch_prices_from_carrefour(self, product):
        """Retrieve product prices from Carrefour."""
        self.driver.get('https://www.carrefour.fr/')  # Site web de carrefour
        self.accept_cookies()
        WebDriverWait(self.driver, 20)
        search_box_carrefour = self.driver.find_element(By.CSS_SELECTOR, "#search-bar > form > div > div.pl-input-text-group__control > div > input")  # Recherche la barre de recherche
        search_box_carrefour.clear()
        search_box_carrefour.send_keys(product)
        search_box_carrefour.submit()

        products = []

        # Boucle pour gérer la pagination (par exemple, 3 pages en plus de la première)
        for _ in range(4):
            # Attendre que les produits apparaissent
            wait = WebDriverWait(self.driver, 20)
            products_elements_car = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#products .product-grid-item")))
            time.sleep(5)
            
            for product_element in products_elements_car:
                try:
                    name_element = product_element.find_element(By.CSS_SELECTOR, ".product-card-title") 
                    name = name_element.text
                    price_element = product_element.find_element(By.CSS_SELECTOR, ".product-price__amount-value")
                    price = float(price_element.text.replace('€', '').replace(',', '.'))
                    products.append((name, price))
                    print(f"Produit ajouté : {name} - {price}€")
                except Exception as e:
                    print(f"Erreur lors de la récupération du produit : {e}")
            
            # Cliquez sur le bouton "Next" pour aller à la page suivante
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, "#data-voir-plus > div.pagination__button-wrap > button > span")
                next_button.click()
                # Attendez un instant pour s'assurer que la nouvelle page est chargée
                time.sleep(5)
            except Exception as e:
                print(f"Erreur lors de la navigation vers la page suivante : {e}")
                break
        
        return sorted(products, key=lambda x: x[1])[:10]

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

    def calculate_mean_price(self, prices):
        """Calculate the average price of the cheapest products from each store."""
        if not prices:
            return 0.0
        return sum(prices) / len(prices)

class EmailManager:
    def __init__(self):
        pass

    def send_email_with_hotmail(self, df_auchan, df_carrefour, savings, inflation_rate_auchan, inflation_rate_carrefour):
        """Send an email via Hotmail with the shopping basket comparison."""
        smtp_server = 'smtp-mail.outlook.com'
        port = 587
        sender_email = 'ferventbatina07@gmail.com'
        sender_password = 'qttovcccoqqgteem'
        recipient_email = 'projetpythonm2@gmail.com'
        
        auchan_message = "No historical data for Auchan."
        carrefour_message = "No historical data for Carrefour."

        if inflation_rate_auchan is not None:
            auchan_message = f"Pour votre information : \nle taux d'inflation d'Auchan est de {inflation_rate_auchan:.2f}% d'après votre dernière recherche."

        if inflation_rate_carrefour is not None:
            carrefour_message = f"le taux d'inflation de Carrefour est de {inflation_rate_carrefour:.2f}% d'après votre dernière recherche."

        msg = MIMEText(f"Voici le panier Auchan :\n\n{df_auchan.to_string()}\n\nVoici le panier Carrefour:\n\n{df_carrefour.to_string()}\n\n{savings}\n\n"
                       f"{auchan_message}\n{carrefour_message}")
        
        msg['From'] = sender_email
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'Comparaison des coûts de panier'
        
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        print("E-mail envoyé avec succès!")

def main(driver):
    """Main function to execute the shopping basket comparison."""
    url = "https://compte.auchan.fr/auth/realms/auchan.fr/protocol/openid-connect/auth?client_id=lark-crest&state=8798f4c2-d76e-4373-a6b3-d6f9a065d3b5&redirect_uri=https%3A%2F%2Fwww.auchan.fr%2Fauth%2Flogin%2F68747470733a2f2f7777772e61756368616e2e66722f6f75766572747572652d61756368616e2d706965746f6e2f65702d6f75766572747572652d61756368616e2d706965746f6e3f736f757263653d676f6f676c65266d656469756d3d7365612675746d5f63616d706169676e3d3137323237363737373231267465726d3d61756368616e25323063253236632663757374706172616d7472616669633d31373232373637373732312d3133363630373239353833372d3632353030393438313233322671745f69643d7169645f6761645f6331373232373637373732315f673133363630373239353833375f613632353030393438313233322667636c69643d4541496149516f6243684d49752d6631684f756967514d5630716a56436831387351473745414159415341414567494c5a5f445f4277452667636c7372633d61772e6473%3Fauth_callback%3D1&scope=openid&response_type=code"
    username = "projetpythonm2@gmail.com"
    password = "Strasbourg2023."
    scraper = WebScraper(driver)
    scraper.login_if_needed(url, username, password)
    manager = DataManager(scraper)
    email_manager = EmailManager()
    shopping_list_auchan = []
    shopping_list_carrefour = []

    # Initialiser le dictionnaire
    all_products = {
        "auchan": {},
        "carrefour": {}
    }

    course_list = input("Entrez votre liste de courses séparée par des virgules: ").split(',')
    selection_mode = input("Voulez-vous sélectionner les produits manuellement ou automatiquement? (1 pour Manuel, 2 pour Auto): ")

    # Enregistrer la date actuelle en CSV
    today_date = date.today()  
    date_str = today_date.strftime('%Y-%m-%d')
    
    # Ouvrir le fichier CSV 
    with open('shopping_results.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Product', 'Store', 'Name', 'Price', 'Date'])
    
        # Récupération des produits pour Auchan
        for product in course_list:
            product = product.strip()
            all_products["auchan"][product] = scraper.fetch_prices_from_auchan(product)

        # Récupération des produits pour Carrefour
        for product in course_list:
            product = product.strip()
            all_products["carrefour"][product] = scraper.fetch_prices_from_carrefour(product)
    
    
        # Faire la sélection ou prendre les produits automatiquement
        for product in course_list:
            product = product.strip()
            
            auchan_prices = all_products["auchan"][product]
            carrefour_prices = all_products["carrefour"][product]
        
            if selection_mode == "1":
                # Affichez les produits des deux magasins
                print("Produits disponibles pour", product, ":\n")
                for idx, (name, price) in enumerate(auchan_prices, start=1):
                    print(f"{idx}. Auchan: {name} - {price}€")
                    
                    for name, price in auchan_prices:
                        csv_writer.writerow([product, 'Auchan', name, price, date_str])
                        
                for idx, (name, price) in enumerate(carrefour_prices, start=11):
                    print(f"{idx}. Carrefour: {name} - {price}€")
                    # Save the product data to CSV
                    for name, price in carrefour_prices:
                        csv_writer.writerow([product, 'Carrefour', name, price, date_str])

                # Demandez à l'utilisateur de choisir pour Auchan
                choice_auchan = int(input("Quel produit voulez-vous choisir chez Auchan? (1-10): "))
                
                # Demandez à l'utilisateur de choisir pour Carrefour
                choice_carrefour = int(input("Quel produit voulez-vous choisir chez Carrefour? (11-20): "))
     
                shopping_list_auchan.append(auchan_prices[choice_auchan-1])
                shopping_list_carrefour.append(carrefour_prices[choice_carrefour-11])
                
            elif selection_mode == "2":
                #Enregistrez les produits dans le CSV également pour mode Automatique pour calculer le taux d'inflation
                shopping_list_auchan.append(auchan_prices[0])
                for name, price in auchan_prices:
                   csv_writer.writerow([product, 'Auchan', name, price, date_str])
                shopping_list_carrefour.append(carrefour_prices[0])
                for name, price in carrefour_prices:
                    csv_writer.writerow([product, 'Carrefour', name, price, date_str])

    # Créer un DataFrame avec les résultats pour chaque magasin
    df_auchan = pd.DataFrame(shopping_list_auchan, columns=['Product_Auchan', 'Price_Auchan'])
    df_carrefour = pd.DataFrame(shopping_list_carrefour, columns=['Product_carrefour', 'Price_carrefour'])
    
    # Combinez les deux dataframes
    df = pd.concat([df_auchan, df_carrefour], axis=1)
    print(df)

    # Calculez et affichez le total pour chaque magasin
    total_auchan = df_auchan["Price_Auchan"].sum()
    total_carrefour = df_carrefour["Price_carrefour"].sum()
    print(f"Total Auchan: {total_auchan:.2f}€")
    print(f"Total carrefour: {total_carrefour:.2f}€")
    savings = abs(total_carrefour - total_auchan)
    
    #Lirez les données précédentes du fichier CSV
    historical_data = []
    with open('shopping_results.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            historical_data.append(row)
    
    #Calculez le prix moyen de chaque magasin à partir des données précédentes
    auchan_prices = []
    carrefour_prices = []
    for row in historical_data:
        if row['Store'] == 'Auchan':
            auchan_prices.append(float(row['Price']))
        elif row['Store'] == 'Carrefour':
            carrefour_prices.append(float(row['Price']))
    
    # Calculez le prix moyen de chaque magasin à partir des données précédentes
    mean_auchan_price_historical = manager.calculate_mean_price(auchan_prices)
    mean_carrefour_price_historical = manager.calculate_mean_price(carrefour_prices)
    
    # Calculez le prix moyen de chaque magasin à partir des résultats de recherche les plus récents
    mean_auchan_price_recent = manager.calculate_mean_price([price for _, price in shopping_list_auchan])
    mean_carrefour_price_recent = manager.calculate_mean_price([price for _, price in shopping_list_carrefour])
   
    # Vérifiez s'il existe des données précédentes pour Auchan et Carrefour
    if auchan_prices:
        inflation_rate_auchan = ((mean_auchan_price_recent - mean_auchan_price_historical) / mean_auchan_price_historical) * 100
        print(f"Taux d'inflation (Auchan): {inflation_rate_auchan:.2f}%")
    else:
        inflation_rate_auchan = None
        print("Aucune données précédentes disponible pour Auchan.")

    if carrefour_prices:
        inflation_rate_carrefour = ((mean_carrefour_price_recent - mean_carrefour_price_historical) / mean_carrefour_price_historical) * 100
        print(f"Taux d'inflation (Carrefour): {inflation_rate_carrefour:.2f}%")
    else:
        inflation_rate_carrefour = None
        print("Aucune données précédentes disponible pour Carrefour.")
        
    # Calculez les taux d'inflation
    inflation_rate_auchan = ((mean_auchan_price_recent - mean_auchan_price_historical) / mean_auchan_price_historical) * 100
    inflation_rate_carrefour = ((mean_carrefour_price_recent - mean_carrefour_price_historical) / mean_carrefour_price_historical) * 100
  
    
    if total_auchan < total_carrefour:
        store = "Auchan"
        savings_msg = f"Si vous allez chez Auchan, vous économiserez {savings:.2f}€"
    else:
        store = "Carrefour"
        savings_msg = f"Si vous allez chez Carrefour, vous économiserez {savings:.2f}€"

    email_manager.send_email_with_hotmail(df_auchan, df_carrefour, savings_msg, inflation_rate_auchan, inflation_rate_carrefour)    

if __name__ == "__main__":
    driver = initialize_driver()
    main(driver)
    driver.close()
