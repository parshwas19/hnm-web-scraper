def get_user_input():
    valid_genders = ["male", "female"]
    valid_types = ["new arrival", "sale"]
    valid_categories_new_arrival = ["clothes", "accessories", "shoes", "activewear"]
    valid_categories_sale = ["tshirts and tanks", "pants", "jeans", "hoodies and sweatshirt", "shorts", "shoes"]

    while True:
        gender = input("Please enter your gender preference (Male/Female): ").strip().lower()
        if gender not in valid_genders:
            print("Invalid gender. Please enter 'Male' or 'Female'.")
            continue

        type_ = input("Please enter the type (New Arrival/Sale): ").strip().lower()
        if type_ not in valid_types:
            print("Invalid type. Please choose 'New Arrival' or 'Sale'.")
            continue

        if type_ == "new arrival":
            category = input("Please choose a category (Clothes/Accessories/Shoes/Activewear): ").strip().lower()
            if category not in valid_categories_new_arrival:
                print("Invalid category. Please choose from 'Clothes', 'Accessories', 'Shoes', or 'Activewear'.")
                continue
        elif type_ == "sale":
            category = input("Please choose a category (Tshirts and Tanks/Pants/Jeans/Hoodies and Sweatshirt/Shorts/Shoes): ").strip().lower()
            if category not in valid_categories_sale:
                print("Invalid category. Please choose from 'Tshirts and Tanks', 'Pants', 'Jeans', 'Hoodies and Sweatshirt', 'Shorts', or 'Shoes'.")
                continue

        return gender, type_, category

def construct_url(gender, type_, category):
    base_url = "https://www2.hm.com/en_ca"
    gender_map = {
        "male": "men",
        "female": "women"
    }
    type_map = {
        "new arrival": "new-arrivals",
        "sale": "sale"
    }
    category_map_new_arrival = {
        "clothes": "clothes.html",
        "accessories": "accessories.html",
        "shoes": "shoes.html",
        "activewear": "activewear.html"
    }
    category_map_sale = {
        "tshirts and tanks": "tshirtstanks.html",
        "pants": "trousers.html",
        "jeans": "jeans.html",
        "hoodies and sweatshirt": "hoodiessweatshirts.html" if gender == "male" else "hoodies-sweatshirts.html",
        "shorts": "shorts.html",
        "shoes": "shoes.html"
    }

    gender_path = gender_map.get(gender)
    type_path = type_map.get(type_)
    category_path = category_map_new_arrival.get(category) if type_ == "new arrival" else category_map_sale.get(category)

    if not (gender_path and type_path and category_path):
        raise ValueError("Invalid input combination provided.")

    return f"{base_url}/{gender_path}/{type_path}/{category_path}"
