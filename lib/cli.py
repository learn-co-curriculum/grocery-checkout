#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import GroceryItem, Store, ShoppingCart
from helpers import create_store_table, create_grocery_item_table, show_cart

engine = create_engine('sqlite:///db/grocery_stores.db')
session = sessionmaker(bind=engine)()

YES = ['y', 'ye', 'yes']
NO = ['n', 'no']

if __name__ == '__main__':
    # Intro: welcome to the CLI, pick a store
    print('''
  ________                                                                       
 /  _____/______  ____   ____  ___________ ___.__.                               
/   \  __\_  __ \/  _ \_/ ___\/ __ \_  __ <   |  |                               
\    \_\  \  | \(  <_> )  \__\  ___/|  | \/\___  |                               
 \______  /__|   \____/ \___  >___  >__|   / ____|                               
        \/                  \/    \/       \/                                    
_________ .__                   __                 __    _________ .____    .___ 
\_   ___ \|  |__   ____   ____ |  | ______  __ ___/  |_  \_   ___ \|    |   |   |
/    \  \/|  |  \_/ __ \_/ ___\|  |/ /  _ \|  |  \   __\ /    \  \/|    |   |   |
\     \___|   Y  \  ___/\  \___|    <  <_> )  |  /|  |   \     \___|    |___|   |
 \______  /___|  /\___  >\___  >__|_ \____/|____/ |__|    \______  /_______ \___|
        \/     \/     \/     \/     \/                           \/        \/    

''')
    print('Hello! Welcome to the grocery checkout CLI.')
    print('Here is a list of available stores:')
    stores = session.query(Store)
    create_store_table(stores)

    # Get a choice of store, retrieve an object from the DB
    store = None
    while not store:
        store_id = input('Please enter the ID of the store where you wish to shop: ')
        store = session.query(Store).filter(Store.id == store_id).one_or_none()

    # Display list of items at the store
    print('Here is a list of our offerings:')
    create_grocery_item_table(store)

    # Start adding items to cart
    grocery_item_id = input('Please enter the ID of your first item: ')
    shopping_cart = ShoppingCart(store=store)
    cart_total = 0
    while grocery_item_id:
        grocery_item = session.query(GroceryItem).filter(
            GroceryItem.id==grocery_item_id).first()
        if grocery_item in store.grocery_items:
            shopping_cart.grocery_items.append(grocery_item)
            cart_total += grocery_item.price
            print(f'Cart total is now ${cart_total:.2f}.')
        else:
            grocery_item_id = input('Please enter a valid grocery item ID: ')
            continue

        yes_no = None
        while yes_no not in YES + NO:
            yes_no = input('Would you like to add another item to your cart? (Y/n) ')
            if yes_no.lower() in YES:
                grocery_item_id = input('Please enter the ID of your next item: ')
            elif yes_no.lower() in NO:
                grocery_item_id = None

    print('Here are the items in your cart:')
    show_cart(shopping_cart)

    # Remove unwanted items from cart
    yes_no = input('Would you like to remove any items from your cart? (Y/n) ')
    while yes_no in YES:
        grocery_item_id = input('Please enter the ID of the item you would like to remove: ')
        grocery_item = session.query(GroceryItem).filter(
            GroceryItem.id==grocery_item_id).first()
        if grocery_item in shopping_cart.grocery_items:
            shopping_cart.grocery_items.remove(grocery_item)
            cart_total -= grocery_item.price
        else:
            print('Item not found.')
        print('Here are the items in your cart:')
        show_cart(shopping_cart)

        yes_no = input('Would you like to remove another item from your cart? (Y/n) ')

    # Collect payment
    print(f'Your total is ${cart_total}')
    paid = False
    while not paid:
        payment_method = input(f'Will you be paying with cash or card? ')
        if payment_method.lower() == 'card':
            print('Processing...')
            print('Thank you for using the grocery checkout CLI!')
            paid = True
        elif payment_method.lower() == 'cash':
            payment = input('How much will you be paying with today? ' )
            try:
                payment = float(payment)
                change = payment - cart_total
                print(f'Your change is ${change:.2f}.')
                print('Thank you for using the grocery checkout CLI!')
                paid = True
            except:
                print('Please enter a valid number.')
        else:
            print('Please select a valid payment method.')
