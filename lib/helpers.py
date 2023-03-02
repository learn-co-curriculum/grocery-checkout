def create_store_table(stores):
    print('-' * 50)
    for store in stores:
        id_spaces = 4 - len(str(store.id))
        name_spaces = 43 - len(store.name)
        print(f'|{store.id}{" " * id_spaces}|{store.name}{" " * name_spaces}|')
    print('-' * 50)

def create_grocery_item_table(store):
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

def show_cart(shopping_cart):
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
    print(f'|TOTAL{" " * 33}|${cart_total:.2f}{" " * total_spaces}|')
    print('-' * 50)