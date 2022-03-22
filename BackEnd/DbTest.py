"""
This Script is to implement our flask methods to connect to our front end
"""

import CategoryDatabase
import ItemDatabase


def main():
    """ Function for the create new category webpage """

    catDatabase = CategoryDatabase.CategoryDatabase()

    print("\nAdding Categories for bob and sue")
    catDatabase.create_category(
        "sue", "Closet Items", "Bottom shelf")
    catDatabase.create_category(
        "bob", "Closet Items", "Top shelf")
    catDatabase.create_category(
        "bob", "Kitchen Items", "Pantry")
    catDatabase.create_category(
        "bob", "Bathroom Items", "Under sink")

    userCats = catDatabase.get_categories("bob")
    print("\nUser Bob's Items:")
    for cat in userCats:
        print("  " + cat["categoryName"] + " : " + cat["description"])

    print("\nDeleting Bob's Kitchen Category")
    catDatabase.delete_category("bob", "Kitchen Items")

    print("\nUpdating Bob's Closet Category")
    catDatabase.update_category_location(
        "bob", "Closet Items", "Bottom shelf")

    userCats = catDatabase.get_categories("bob")
    print("\nUser Bob's Categories:")
    for cat in userCats:
        print("  " + cat["categoryName"] + " : " + cat["description"])

    itemDatabase = ItemDatabase.ItemDatabase()

    print("\nAdding Items for bob and sue")
    itemDatabase.add_item("bob", "White T-Shirt",
                          "A white t-shirt.", "Closet Items")
    itemDatabase.add_item("bob", "Leather Jacket",
                          "New leather jacket.", "Closet Items")
    itemDatabase.add_item("bob", "Blue Jeans",
                          "Ripper blue jeans.", "Closet Items")
    itemDatabase.add_item("bob", "Nike Sneakers",
                          "Favorite sneakers.", "Closet Items")
    itemDatabase.add_item("bob", "Toothbrush",
                          "New toothbrush.", "Bathroom Items")
    itemDatabase.add_item("sue", "Pink T-Shirt",
                          "A pink t-shirt.", "Closet Items")

    catItems = itemDatabase.get_items_by_category("bob", "Closet Items")
    print("\nUser Bob's Closet Items:")
    for item in catItems:
        print("  " + item["itemName"] + " : " + item["description"])

    print("\nDeleting Bob's Blue Jeans")
    itemDatabase.delete_item("bob", "Blue Jeans")

    print("\nUpdating Bob's Leather Jacket")
    itemDatabase.update_item("bob", "Leather Jacket",
                             "Old leather Jacket", "Closet Items")

    catItems = itemDatabase.get_items_by_category("bob", "Closet Items")
    print("\nUser Bob's Closet Items:")
    for item in catItems:
        print("  " + item["itemName"] + " : " + item["description"])


main()
