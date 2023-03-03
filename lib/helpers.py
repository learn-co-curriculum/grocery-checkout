from db.models import GroceryItem, ShoppingCart

YES = ['y', 'ye', 'yes']
NO = ['n', 'no']

def create_store_table(stores):
    print('-' * 50)
    print(f'|ID  |NAME{" " * 39}|')
    print('-' * 50)
    for store in stores:
        id_spaces = 4 - len(str(store.id))
        name_spaces = 43 - len(store.name)
        print(f'|{store.id}{" " * id_spaces}|{store.name}{" " * name_spaces}|')
    print('-' * 50)

def create_grocery_item_table(store):
    print('-' * 50)
    print(f'|ID  |ITEM NAME{" " * 24}|PRICE{" " * 4}|')
    print('-' * 50)
    for grocery_item in sorted(store.grocery_items, key=lambda g: g.id):
        id_spaces = 4 - len(str(grocery_item.id))
        name_spaces = 33 - len(grocery_item.name)
        price_spaces = 8 - len(f'{grocery_item.price:.2f}')
        output_string = f'|{grocery_item.id}{" " * id_spaces}|' + \
            f'{grocery_item.name}{" " * name_spaces}|' + \
            f'${grocery_item.price:.2f}{" " * price_spaces}|'
        print(output_string)
    print('-' * 50)

def fill_cart(session, store):
    shopping_cart = ShoppingCart(store=store)
    grocery_item_id = input('Please enter the ID of your first item: ')
    cart_total = 0
    while grocery_item_id:
        grocery_item = session.query(GroceryItem).filter(
            GroceryItem.id==grocery_item_id).first()
        if grocery_item in store.grocery_items:
            shopping_cart.grocery_items.append(grocery_item)
            cart_total += grocery_item.price
            print(f'Cart total is now ${cart_total:.2f}\n')
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

    return shopping_cart, cart_total

def show_cart(shopping_cart):
    print('-' * 50)
    print(f'|ID  |NAME{" " * 29}|PRICE{" " * 4}|')
    print('-' * 50)
    for grocery_item in sorted(shopping_cart.grocery_items, key=lambda g: g.id):
        id_spaces = 4 - len(str(grocery_item.id))
        name_spaces = 33 - len(grocery_item.name)
        price_spaces = 8 - len(f'{grocery_item.price:.2f}')
        output_string = f'|{grocery_item.id}{" " * id_spaces}|' + \
            f'{grocery_item.name}{" " * name_spaces}|' + \
            f'${grocery_item.price:.2f}{" " * price_spaces}|'
        print(output_string)
    cart_total = sum([g.price for g in shopping_cart.grocery_items])
    total_spaces = 8 - len(str(cart_total))
    print(f'|{" " * 5}TOTAL{" " * 28}|${cart_total:.2f}{" " * total_spaces}|')
    print('-' * 50)

def remove_from_cart(session, shopping_cart, cart_total):
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

def collect_payment(cart_total):
    paid = False
    while not paid:
        payment_method = input(f'Will you be paying with cash or card? ')
        if payment_method.lower() == 'card':
            print('Processing...\n')
            paid = True
        elif payment_method.lower() == 'cash':
            payment = input('How much will you be paying with today? ' )
            try:
                payment = float(payment)
                change = payment - cart_total
                print(f'Your change is ${change:.2f}\n')
                paid = True
            except:
                print('Please enter a valid number.')
        else:
            print('Please select a valid payment method.')
