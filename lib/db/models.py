from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

grocery_item_store = Table(
    'grocery_item_stores',
    Base.metadata,
    Column('grocery_item_id', ForeignKey('grocery_items.id'), primary_key=True),
    Column('store_id', ForeignKey('stores.id'), primary_key=True),
)

class GroceryItem(Base):
    __tablename__ = 'grocery_items'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    quantity = Column(Integer())
    price = Column(Float())
    unit_price = Column(Float())

    shopping_cart_id = Column(Integer(), ForeignKey('shopping_carts.id'))
    stores = relationship('Store', secondary=grocery_item_store, back_populates='grocery_items')


    def __repr__(self):
        return f'GroceryItem(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'

class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    address = Column(String())

    shopping_carts = relationship('ShoppingCart', backref=backref('store'))
    grocery_items = relationship('GroceryItem', secondary=grocery_item_store, back_populates='stores')


    def __repr__(self):
        return f'Store(id={self.id}), ' + \
            f'name={self.name}'
    
class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'

    id = Column(Integer(), primary_key=True)

    grocery_items = relationship('GroceryItem', backref=backref('shopping_cart'))

    store_id = Column(Integer(), ForeignKey('stores.id'))
    
    def __repr__(self):
        return f'ShoppingCart(id={self.id})'