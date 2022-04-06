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
        "sue", "Closet Items", "rack")
    catDatabase.create_category(
        "bob", "Closet Items", "drawer")
    catDatabase.create_category(
        "bob", "Kitchen Items", "pantry")
    catDatabase.create_category(
        "bob", "Bathroom Items", "medicine cabinet")

    userCats = catDatabase.get_categories("bob")
    print("\nUser Bob's Items:")
    for cat in userCats:
        print("  " + cat["categoryName"] + " : " + cat["categoryLocation"])

    print("\nDeleting Bob's Kitchen Category")
    catDatabase.delete_category("bob", "Kitchen Items")

    print("\nUpdating Bob's Closet Category")
    catDatabase.update_category_loc(
        "bob", "Closet Items", "Bottom shelf")

    userCats = catDatabase.get_categories("bob")
    print("\nUser Bob's Categories:")
    for cat in userCats:
        print("  " + cat["categoryName"] + " : " + cat["categoryLocation"])

    itemDatabase = ItemDatabase.ItemDatabase()

    print("\nAdding Items for bob and sue")
    itemDatabase.add_item("bob", "White T-Shirt",
                          "Closet Items", "rack", "10-2-2021", "shirt")
    itemDatabase.add_item("bob", "Leather Jacket",
                          "Closet Items", "rack", "10-2-2021", "leather,jacket")
    itemDatabase.add_item("bob", "Blue Jeans", "Closet Items",
                          "drawer", "10-2-2021", "pants,blue")
    itemDatabase.add_item("bob", "Nike Sneakers", "Closet Items",
                          "floor", "10-2-2021", "shoes, sneaker")
    itemDatabase.add_item("bob", "Toothbrush", "Bathroom Items",
                          "medicine cabinet", "", "dental")
    itemDatabase.add_item("sue", "Pink T-Shirt",
                          "Closet Items", "rack", "10-2-2021", "shirt")

    catItems = itemDatabase.get_items_by_category("bob", "Closet Items")
    print("\nUser Bob's Closet Items:")
    for item in catItems:
        print("  " + item["itemName"] + " : " + item["itemLocation"])

    print("\nDeleting Bob's Blue Jeans")
    itemDatabase.delete_item("bob", "Blue Jeans")

    print("\nUpdating Bob's Leather Jacket")
    itemDatabase.update_item("bob", "Leather Jacket",
                             "Closet Items", "drawer")

    catItems = itemDatabase.get_items_by_category("bob", "Closet Items")
    print("\nUser Bob's Closet Items:")
    for item in catItems:
        print("  " + item["itemName"] + " : " + item["itemLocation"])


main()
