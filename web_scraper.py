from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

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

        self.scroll_page("#search > input", 5)  # Fait défiler la page en 15 étapes

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
        for _ in range(2):
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
