import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
from db import insert_product_details
import time

def setup_webdriver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Run in headless mode if needed
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_products(gender, type_, category, init_url):
    driver = setup_webdriver()

    # Open the webpage
    driver.get(init_url)

    # Handle the cookie consent popup if it appears
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept all cookies")]'))
        )
        cookie_button.click()
        print("Cookie consent popup clicked.")
    except Exception as e:
        print("Cookie consent popup not found or could not be closed.", e)

    # Get the page source after handling the cookie popup
    html_content_after_cookie = driver.page_source
    soup_after_cookie = BeautifulSoup(html_content_after_cookie, 'html.parser')

    # Extract the number of pages
    product_pages = soup_after_cookie.find('ul', class_='ed2eb5')
    if product_pages:
        li_page_number_elements = product_pages.find_all('li')
        if len(li_page_number_elements) > 1:
            second_last_li = li_page_number_elements[-2]
            number_of_pages = int(second_last_li.text.strip())
    else:
        number_of_pages = 1

    # Limit the number of pages for the basic implementation
    number_of_pages = min(number_of_pages, 2)

    # Loop through each page and each product item
    for i in range(number_of_pages):
        url = init_url + '?page=' + str(i + 1)
        driver.get(url)
        html_content_after_cookie = driver.page_source
        soup_after_cookie = BeautifulSoup(html_content_after_cookie, 'html.parser')
        product_items = soup_after_cookie.find_all('div', class_='eed2a5 ec329a d5728c')

        for item in product_items:
            # Extract the product link
            link_tag = item.find('a', class_='db7c79')
            product_link = link_tag.get('href') if link_tag else None

            if product_link:
                # Visit the product page
                driver.get(product_link)
                time.sleep(0.5)
                product_page_source = driver.page_source
                product_soup = BeautifulSoup(product_page_source, 'html.parser')

                product_schema_script = product_soup.find('script', id='product-schema')

                # Check if the script tag is found
                if product_schema_script:
                    # Parse the JSON data within the script tag
                    product_data = json.loads(product_schema_script.string)

                    # Extract the required fields
                    product_name = product_data.get('name', 'N/A')
                    product_color = product_data.get('color', 'N/A')
                    product_description = product_data.get('description', 'N/A')
                    brand_name = product_data.get('brand', {}).get('name', 'N/A')
                    current_price = product_data.get('offers', [{}])[0].get('price', 'N/A')

                    original_price_tag = product_soup.find('span', class_='e98f30 ac3d9e e29fbf')
                    original_price = original_price_tag.text.strip() if original_price_tag else None

                else:
                    product_name = 'N/A'
                    product_color = 'N/A'
                    product_description = 'N/A'
                    brand_name = 'N/A'
                    current_price = 'N/A'
                    original_price = None

                reviews_summary_tag = product_soup.find('hm-product-reviews-summary-w-c', class_='wc-product-reviews-summary-w-c')
                if reviews_summary_tag:
                    # Extract average rating and total ratings
                    average_rating = reviews_summary_tag.get('average-rating', 'N/A')
                    total_ratings = reviews_summary_tag.get('ratings', 'N/A')
                else:
                    average_rating = 'N/A'
                    total_ratings = 'N/A'

                mini_slider = product_soup.find('div', class_='mini-slider')
                colors = []
                if mini_slider:
                    list_items = mini_slider.find_all('li', class_='list-item')
                    colors = [li.find('a').get('title') for li in list_items if li.find('a')]

                sizes_container = product_soup.find('ul', class_='ListGrid-module--listGrid__3gCNA SizeButtonGroup-module--gridLargeButtons__1qG5O ListGrid-module--itemFlex__3yxlw')
                available_sizes = []
                unavailable_sizes = []
                if sizes_container:
                    size_items = sizes_container.find_all('li', class_='ListGrid-module--item__3n3A-')
                    for item in size_items:
                        label = item.find('label')
                        size = label.get('for')
                        aria_disabled = label.get('aria-disabled')

                        if aria_disabled == 'true':
                            unavailable_sizes.append(size)
                        else:
                            available_sizes.append(size)

                # Insert data into SQLite database
                product_details = (
                    product_name,
                    current_price,
                    original_price,
                    product_color,
                    brand_name,
                    ', '.join(available_sizes),
                    average_rating,
                    total_ratings,
                    product_link,
                    product_description,
                    ', '.join(colors),
                    ', '.join(available_sizes + unavailable_sizes),
                    category,
                    type_,
                    gender
                )

                insert_product_details(product_details, gender)

    driver.quit()
