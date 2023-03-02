from random import random, randint, choice as rc

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import GroceryItem, ShoppingCart, Store, grocery_item_store

engine = create_engine('sqlite:///grocery_stores.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def make_grocery_items():
    print("Deleting existing grocery items...")
    session.query(GroceryItem).delete()
    session.commit()

    print("Making grocery items...")
    grocery_items = [GroceryItem(
        name=fake.name(),
        quantity=randint(1, 12),
        price=round(float(randint(0, 19)) + random(), 2), 
    ) for i in range(50)]
    for gi in grocery_items:
        gi.unit_price = round(gi.price / gi.quantity, 2)
    
    session.add_all(grocery_items)
    session.commit()

    return grocery_items

def make_stores():
    print("Deleting existing stores...")
    session.query(Store).delete()
    session.commit()

    print("Making stores...")
    stores = [Store(
        name=fake.name() + "'s",
        address=fake.address(),
    ) for i in range(10)]
    
    session.add_all(stores)
    session.commit()

    return stores

def make_shopping_carts(grocery_items, stores):
    print("Deleting existing shopping carts...")
    session.query(ShoppingCart).delete()
    session.commit()

    print("Making shopping carts...")
    shopping_carts = []
    for i in range(25):
        sc_store = rc(stores)
        sc_grocery_items = [rc(grocery_items) for i in range(15)]
        for gi in sc_grocery_items:
            if gi not in sc_store.grocery_items:
                sc_store.grocery_items.append(gi)
        shopping_carts.append(ShoppingCart(store=sc_store))

    session.add_all(stores)
    session.add_all(shopping_carts)
    session.commit()

    return shopping_carts

if __name__ == '__main__':
    
    session.query(grocery_item_store).delete()
    session.commit()

    grocery_items = make_grocery_items()
    stores = make_stores()
    make_shopping_carts(grocery_items, stores)
