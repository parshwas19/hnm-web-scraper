from scraper import scrape_products
from db import export_to_csv, setup_database
from utils import get_user_input, construct_url

def main():
    setup_database()

    # Get user input and construct the URL
    gender, type_, category = get_user_input()
    init_url = construct_url(gender, type_, category)

    # Scrape the products
    scrape_products(gender, type_, category, init_url)

    # Export the data to CSV
    export_to_csv(gender)

if __name__ == "__main__":
    main()
