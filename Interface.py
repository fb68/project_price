import streamlit as st
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from BaseInterface import initialize_driver, login_if_needed, fetch_prices_from_auchan, fetch_prices_from_carrefour

#To catch an exception encountered during web scraping 
def fetch_prices_safely(fetch_function, driver, product_list):
    try:
        return fetch_function(driver, product_list)
    except ElementClickInterceptedException as e:
        st.error(f"Error occurred: {e}")
        st.warning("Element click intercepted. Continuing to fetch data...")
        return []  # Return an empty list or handle the error as needed

#To display selected products with names and pricea
def display_selected_products(products, store_name):
    st.write(f"Selected {store_name} Products:")
    for product, (name, price) in products.items():
        st.write(f"{product}: {name} - {price}€")

def main(driver):
    try:
        if driver is None:
            st.error("WebDriver initialization failed. Please check your setup.")
            return
    
        st.title("Comparateur de Paniers Supermarchés")
        st.sidebar.title("Votre Liste de Courses")
    
        # Streamlit components for user input
        product_list = st.sidebar.text_input("Entrez votre liste de courses séparée par des virgules").split(',')
        selection_mode = st.sidebar.radio("Voulez-vous sélectionner les produits manuellement ou automatiquement", ["Manual", "Automatique"])
        
        #Click to launch the search
        if st.sidebar.button("Lancez"):
            with st.spinner("Chargement en cours..."):
                
                #For Manual mode
                if selection_mode == "Manual":
                    selected_products_auchan = {}
                    selected_products_carrefour = {}
                    for product in product_list:
                        # Fetch prices for Auchan and Carrefour
                        auchan_prices = fetch_prices_from_auchan(driver, product)
                        carrefour_prices = fetch_prices_from_carrefour(driver, product)
                        # Display product options to the user
                        st.write(f"Products for {product}:")
                        auchan_options = [f"{name} - {price}€" for name, price in auchan_prices]
                        carrefour_options = [f"{name} - {price}€" for name, price in carrefour_prices]
                        
                        auchan_choice_idx:str = st.selectbox(f"Select Auchan product for {product}", auchan_options, index=0)
                        carrefour_choice_idx:str = st.selectbox(f"Select Carrefour product for {product}", carrefour_options, index=0)

                        # Parse user choices and add selected products to the list
                        auchan_name, auchan_price = auchan_choice_idx.split(' - ')
                        carrefour_name, carrefour_price = carrefour_choice_idx.split(' - ')

                        selected_products_auchan[product] = (auchan_name, float(auchan_price[:-1]))  # remove '€' and convert to float
                        selected_products_carrefour[product] = (carrefour_name, float(carrefour_price[:-1]))  # remove '€' and convert to float

                        # Calculate total prices for Auchan and Carrefour
                        total_price_auchan = sum(price for _, price in selected_products_auchan.values())
                        total_price_carrefour = sum(price for _, price in selected_products_carrefour.values())
                        # Calculate savings
                        savings = total_price_carrefour - total_price_auchan
    
                        # Display total prices and savings
                        st.write(f"Total Price Auchan: {total_price_auchan}€")
                        st.write(f"Total Price Carrefour: {total_price_carrefour}€")
                        st.write(f"Savings: {savings}€")
    
                        # Display the selected products
                        st.write("Selected Auchan Products:")
                        st.write(selected_products_auchan)
                        st.write("Selected Carrefour Products:")
                        st.write(selected_products_carrefour)
                        
                    #For automatic mode
                    else:
                        selected_products_auchan = {}
                        selected_products_carrefour = {}
    
                    for product in product_list:
                        cheapest_auchan_product = min(auchan_prices, key=lambda x: x[1])
                        cheapest_carrefour_product = min(carrefour_prices, key=lambda x: x[1])
    
                        selected_products_auchan[product] = cheapest_auchan_product
                        selected_products_carrefour[product] = cheapest_carrefour_product
    
                    # Display the automatically selected products
                    display_selected_products(selected_products_auchan, "Auchan")
                    display_selected_products(selected_products_carrefour, "Carrefour")
    
                    # Display results using Streamlit components
                    st.write("Auchan Prices:")
                    st.write(auchan_prices)
                    st.write("Carrefour Prices:")
                    st.write(carrefour_prices)
    
                    # Calculate total prices for Auchan and Carrefour
                    total_price_auchan = sum(price for _, price in selected_products_auchan.values())
                    total_price_carrefour = sum(price for _, price in selected_products_carrefour.values())
                    # Calculate savings
                    savings = total_price_carrefour - total_price_auchan
    
                    # Display total prices and savings
                    st.write(f"Total Price Auchan: {total_price_auchan}€")
                    st.write(f"Total Price Carrefour: {total_price_carrefour}€")
                    st.write(f"Savings: {savings}€")
    
                    # Display the selected products
                    st.write("Selected Auchan Products:")
                    st.write(selected_products_auchan)
                    st.write("Selected Carrefour Products:")
                    st.write(selected_products_carrefour)
    # To catch other exceptions
    except NoSuchElementException as e:
        st.error(f"Element not found. Check your selector or wait for the element to be present. {e}")
    except ElementClickInterceptedException as e:
        st.error(f"Element click intercepted. Please try again. {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
   
if __name__ == "__main__":
    try:
        driver = initialize_driver()
        login_if_needed(driver)
        main(driver) 
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    finally:
        if driver is not None:
            driver.close()





