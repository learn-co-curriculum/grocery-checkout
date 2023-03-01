from random import random, randint, choice as rc

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import GroceryItem, ShoppingCart, Store

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
        price=round(float(randint(0, 19)), 2) + random(), 
    ) for i in range(500)]
    for gi in grocery_items:
        gi.unit_price = gi.price / gi.quantity
    
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
    ) for i in range(25)]
    
    session.add_all(stores)
    session.commit()

    return stores

def make_shopping_carts(grocery_items, stores):
    print("Deleting existing shopping carts...")
    session.query(ShoppingCart).delete()
    session.commit()

    print("Making shopping carts...")
    shopping_carts = [ShoppingCart(
        grocery_items=[rc(grocery_items) for i in range(20)],
        store=rc(stores),
    ) for i in range(500)]
    session.add_all(shopping_carts)
    session.commit()

    return shopping_carts

if __name__ == '__main__':
    grocery_items = make_grocery_items()
    stores = make_stores()
    make_shopping_carts(grocery_items, stores)
