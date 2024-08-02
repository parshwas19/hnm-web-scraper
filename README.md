# H&M Web Scraper

This project is a web scraper for extracting product details from the H&M Canada website. It allows users to select their gender, product type (new arrivals or sale), and category, then scrapes the relevant product details and stores them in a SQLite database. The data is then exported to separate CSV files for men and women.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Features

- Scrapes product details from H&M Canada's website based on user preferences.
- Stores product details in a SQLite database.
- Supports different categories for men and women.
- Automatically exports data to CSV files.

## Requirements

- Python 3.7+
- Google Chrome browser
- Google ChromeDriver

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/hm-web-scraper.git
    cd hm-web-scraper
    ```

2. **Install the required Python packages:**

    Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Download and set up ChromeDriver:**

    - Download ChromeDriver (Sometimes it is already installed with python chromedriver package).
    - Ensure ChromeDriver is in your PATH, or specify its location in the script.

## Usage

1. **Run the main script:**

    ```bash
    python main.py
    ```

2. **Follow the prompts:**

    - Enter your gender preference (Male/Female).
    - Enter the type (New Arrival/Sale).
    - Choose a category based on the selected type.

3. **The scraper will:**

    - Visit the H&M Canada website.
    - Scrape product details based on your preferences.
    - Store the data in a SQLite database.
    - Export the data to CSV files.

**Note:**
- For each category, the scraper will only process the first 2 pages to make it fast for checking.
- This is a basic implementation with a 0.5s sleep after each product loads to correctly load all details and ensure no data is missed.
- For each category, the scraper will run for a total of approximately 3 minutes and at the end, it will provide CSV files exported from the SQLite database for a quick glance at the extracted data.


## Project Structure

```plaintext
hm-web-scraper/
│
├── scraper.py          # Contains the web scraping logic
├── db.py               # Handles database operations and CSV export
├── utils.py            # Utility functions for user input and URL construction
├── main.py             # Main script to run the scraper
├── requirements.txt    # Python dependencies
├── README.md           # This readme file
├── product_details.db  # SQLite database file (generated after running the scraper)
├── men_product_details.csv  # CSV file for men (generated after running the export script)
└── women_product_details.csv  # CSV file for women (generated after running the export script)
