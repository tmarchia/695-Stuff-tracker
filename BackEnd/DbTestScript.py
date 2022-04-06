"""
This Script is to implement our flask methods to connect to our front end
"""

import CategoryDatabase
import ItemDatabase


def main():
    """ Function for the create new category webpage """

    cat_database = CategoryDatabase.CategoryDatabase()

    print("\nAdding Categories for bob and sue")
    cat_database.create_category(
        "sue", "Closet Items", "rack")
    cat_database.create_category(
        "bob", "Closet Items", "drawer")
    cat_database.create_category(
        "bob", "Kitchen Items", "pantry")
    cat_database.create_category(
        "bob", "Bathroom Items", "medicine cabinet")

    user_cats = cat_database.get_categories("bob")
    print("\nUser Bob's Items:")
    for cat in user_cats:
        print("  " + cat["categoryName"] + " : " + cat["categoryLocation"])

    print("\nDeleting Bob's Kitchen Category")
    cat_database.delete_category("bob", "Kitchen Items")

    print("\nUpdating Bob's Closet Category")
    cat_database.update_category_loc(
        "bob", "Closet Items", "Bottom shelf")

    user_cats = cat_database.get_categories("bob")
    print("\nUser Bob's Categories:")
    for cat in user_cats:
        print("  " + cat["categoryName"] + " : " + cat["categoryLocation"])

    item_database = ItemDatabase.ItemDatabase()

    print("\nAdding Items for bob and sue")
    item_database.add_item("bob", "White T-Shirt",
                           "Closet Items", "rack", "10-2-2021", "shirt")
    item_database.add_item("bob", "Leather Jacket",
                           "Closet Items", "rack", "10-2-2021", "leather,jacket")
    item_database.add_item("bob", "Blue Jeans", "Closet Items",
                           "drawer", "10-2-2021", "pants,blue")
    item_database.add_item("bob", "Nike Sneakers", "Closet Items",
                           "floor", "10-2-2021", "shoes, sneaker")
    item_database.add_item("bob", "Toothbrush", "Bathroom Items",
                           "medicine cabinet", "", "dental")
    item_database.add_item("sue", "Pink T-Shirt",
                           "Closet Items", "rack", "10-2-2021", "shirt")

    cat_items = item_database.get_items_by_category("bob", "Closet Items")
    print("\nUser Bob's Closet Items:")
    for item in cat_items:
        print("  " + item["itemName"] + " : " + item["itemLocation"])

    print("\nDeleting Bob's Blue Jeans")
    item_database.delete_item("bob", "Blue Jeans")

    print("\nUpdating Bob's Leather Jacket")
    item_database.update_item("bob", "Leather Jacket",
                              "Closet Items", "drawer")

    cat_items = item_database.get_items_by_category("bob", "Closet Items")
    print("\nUser Bob's Closet Items:")
    for item in cat_items:
        print("  " + item["itemName"] + " : " + item["itemLocation"])


main()
