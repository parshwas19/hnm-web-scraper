import sqlite3
import csv

def setup_database():
    conn = sqlite3.connect('product_details.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist with the new schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS men_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            current_price TEXT,
            original_price TEXT,
            color TEXT,
            brand TEXT,
            size_for_this_color TEXT,
            rating TEXT,
            rating_count TEXT,
            product_link TEXT UNIQUE,
            description TEXT,
            available_colors TEXT,
            all_other_sizes TEXT,
            category TEXT,
            type TEXT,
            gender TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS women_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            current_price TEXT,
            original_price TEXT,
            color TEXT,
            brand TEXT,
            size_for_this_color TEXT,
            rating TEXT,
            rating_count TEXT,
            product_link TEXT UNIQUE,
            description TEXT,
            available_colors TEXT,
            all_other_sizes TEXT,
            category TEXT,
            type TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_product_details(product_details, gender):
    conn = sqlite3.connect('product_details.db')
    cursor = conn.cursor()
    if gender == "male":
        cursor.execute('''
        INSERT OR REPLACE INTO men_products (
            product_name, current_price, original_price, color, brand, size_for_this_color, rating, rating_count,
            product_link, description, available_colors, all_other_sizes, category, type, gender
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', product_details)
    elif gender == "female":
        cursor.execute('''
        INSERT OR REPLACE INTO women_products (
            product_name, current_price, original_price, color, brand, size_for_this_color, rating, rating_count,
            product_link, description, available_colors, all_other_sizes, category, type, gender
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', product_details)
    conn.commit()
    conn.close()

def export_to_csv(gender):
    # Connect to the database
    conn = sqlite3.connect('product_details.db')
    cursor = conn.cursor()

    # Determine the table name based on gender
    table_name = 'men_products' if gender == 'male' else 'women_products'

    # Fetch all records from the specified table
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Write to a CSV file
    with open(f'{gender}_product_details.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # Write the column names as the first row
        writer.writerows(rows)  # Write the data

    # Close the database connection
    conn.close()
