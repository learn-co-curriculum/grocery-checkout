#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Store
from helpers import (create_store_table, create_grocery_item_table,
                     fill_cart, show_cart, remove_from_cart, collect_payment)

engine = create_engine('sqlite:///db/grocery_stores.db')
session = sessionmaker(bind=engine)()

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
    shopping_cart, cart_total = fill_cart(session, store)
    print('Here are the items in your cart:')
    show_cart(shopping_cart)

    # Remove unwanted items from cart
    remove_from_cart(session, shopping_cart, cart_total)

    # Collect payment
    print(f'Your total is ${cart_total:.2f}\n')
    collect_payment(cart_total)

    print('Thank you for using the grocery checkout CLI!\n')
