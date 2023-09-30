# ------------------------- LES IMPORTATIONS NECESSAIRES -------------------------#

from selenium import webdriver  
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains  
import time  

# Initialisation le webdriver
def initialize_driver():
    '''
    Description
    -----------
    Initialise un Chrome WebDriver avec des options spécifiques.

    Returns
    -------
    driver : WebDriver
        WebDriver Chrome initialisé.
    '''
    # Configuration du driver Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')  # Ignore les erreurs de certificat SSL 
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  # WebDriver Manager pour gérer le pilote Chrome
    driver.implicitly_wait(10)
    return driver

# Section : Classe WebScraper

class WebScraper:
    '''
    Description
    -----------
    Classe WebScraper pour les opérations de web scraping.
    Il est important de noter que ce compte Auchan a été créé expressement pour ce projet.
    Attributes
    ----------
    driver : WebDriver
        WebDriver Selenium pour l'interaction web.
    '''

    def __init__(self, driver):
        self.driver = driver

    def login_if_needed(self, url, username, password):
        """Se connecte au site Auchan car sans se connecter dans un compte, on ne peut pas voir les prix des produits."""
        self.driver.get(url) 

        try:
            #  On remplit les champs de connexion 
            self.driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)  
            self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)  
            self.driver.find_element(By.CSS_SELECTOR, "#kc-login").click()  
            time.sleep(5) 
        except Exception as e:
            print(f"Erreur lors de la tentative de connexion : {e}")

    def accept_cookies(self):
        """Accepter les cookies sur le site web."""
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler")))
            cookie_button.click()  
            time.sleep(5)  
        except:
            print("Impossible de trouver le bouton des cookies ou de cliquer dessus.")

    def scroll_page(self, css_selector, n=0):
        """Faire défiler la page progressivement."""
        element = self.driver.find_element(By.CSS_SELECTOR, "#wrapper > div.list__container")
        element.click()  

        for i in range(n):
            try:
                action_chains = ActionChains(self.driver)
                action_chains.send_keys(Keys.PAGE_DOWN).perform()  # On scrolle
                time.sleep(2)  # On attend 2 secondes entre chaque scroll
            except Exception as e:
                print(str(e))

    def fetch_prices_from_auchan(self, product):
        """Récupérer les prix des produits depuis Auchan."""
        self.accept_cookies()

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#search > input")  
        search_box.clear()  
        search_box.send_keys(product)  
        search_box.submit()  

        products = []  # Liste pour stocker les produits récupérés depuis Auchan
        seen_products = set()  # Ensemble pour garder une trace des produits déjà vus prck chez Auchan...
                                #... les produits apparaissent au fur et à mesure qu'on scrolle

        self.scroll_page("#search > input", 15)  # On scrolle 15 fois

        wait = WebDriverWait(self.driver, 20)
        products_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#wrapper > div.list__container > article")))

        for product_element in products_elements:
            try:
                name_element = product_element.find_element(By.CSS_SELECTOR, "div.product-thumbnail__content-wrapper > a > div > p")  
                name = name_element.text  # Obtenir le texte du nom du produit
                price_element = product_element.find_element(By.CSS_SELECTOR, "div.product-thumbnail__content-wrapper > footer > div.product-thumbnail__footer-wrapper > div.product-thumbnail__price.product-price__container > div")  
                price = float(price_element.text.replace('€', '').replace(',', '.'))  # On supprile le symbole € et on remplace la virgule par le point
                
                if name not in seen_products:
                    seen_products.add(name)  # Ajoute le nom du produit à l'ensemble des produits déjà vus
                    products.append((name, price))  # Ajoute le produit et son prix à la liste des produits
                    print(f"Produit ajouté : {name} - {price}€")  # Affiche le produit ajouté pour qu'on visualise à la console les produits qui s'ajoutent
            except Exception as e:
                print(f"Erreur lors de la récupération du produit : {e}")

        return sorted(products, key=lambda x: x[1])[:10]  # Renvoie les 10 produits les moins chers de Auchan triés par prix

    def fetch_prices_from_carrefour(self, product):
        """Récupérer les prix des produits depuis Carrefour."""
        self.driver.get('https://www.carrefour.fr/')  
        self.accept_cookies()  
        WebDriverWait(self.driver, 20)  
        search_box_carrefour = self.driver.find_element(By.CSS_SELECTOR, "#search-bar > form > div > div.pl-input-text-group__control > div > input")
        search_box_carrefour.clear() 
        search_box_carrefour.send_keys(product)  
        search_box_carrefour.submit()  

        products = []  # Liste pour stocker les produits récupérés depuis Carrefour

        # Boucle pour gérer la pagination vu que chez Carrefour, il y a différentes pages contrairement à Auchan où on scrolle
        for _ in range(2):
            
            wait = WebDriverWait(self.driver, 20)
            products_elements_car = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#products .product-grid-item")))  
            time.sleep(5)  
            
            for product_element in products_elements_car:
                try:
                    name_element = product_element.find_element(By.CSS_SELECTOR, ".product-card-title")  
                    name = name_element.text  
                    price_element = product_element.find_element(By.CSS_SELECTOR, ".product-price__amount-value")  
                    price = float(price_element.text.replace('€', '').replace(',', '.'))  # Pareil comme à Auchan
                    products.append((name, price))  
                    print(f"Produit ajouté : {name} - {price}€")  # Pareil comme chez Auchan, ça affiche le produit ajouté
                except Exception as e:
                    print(f"Erreur lors de la récupération du produit : {e}")

            # Ici, on essaie de cliquer sur le bouton "Next" pour aller à la page suivante, si ça ne le trouve pas, ça print le message de except
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, "#data-voir-plus > div.pagination__button-wrap > button > span")
                next_button.click()
                time.sleep(5)
            except Exception as e:
                print(f"Erreur lors de la navigation vers la page suivante : {e}")
                break

        return sorted(products, key=lambda x: x[1])[:10]  # Renvoie les 10 produits les moins chers de Carrefour triés par prix


