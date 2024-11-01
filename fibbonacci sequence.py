# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 20:13:23 2024

@author: HP
"""

def fibbo(n)
    main = [0,1]
    while main[-1]+main[-2]<n:
        main.append(main[-1]+main[-2])
    print(main)



# Example usage:
inventory = BookInventory()

# Adding books
inventory.add("The Great Gatsby", 180, "F. Scott Fitzgerald")
inventory.add("1984", 328, "George Orwell")

# Viewing all books
inventory.view()

# Editing a book (you can update one or more fields)
inventory.edit(1, new_name="Brave New World")

# Deleting a book
inventory.delete(1)

# Viewing the updated inventory
inventory.view()
