import csv
import locale

# Represent a product
class Product:
    def __init__(self, product_id, name, desc, price, quantity):
        self.id = product_id
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"ID: {self.id} \t {self.name} \t {self.desc} \t {locale.currency(self.price, grouping=True)} \t Quantity: {self.quantity}"

# Manage the inventory
class Inventory:
    def __init__(self):
        self.products = []

    def load_data(self, filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    product_id=int(row['id']),
                    name=row['name'],
                    desc=row['desc'],
                    price=float(row['price']),
                    quantity=int(row['quantity'])
                )
                self.products.append(product)

    def get_products(self):
        return "\n".join(str(product) for product in self.products)

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_id):
        self.products = [product for product in self.products if product.id != product_id]

    def update_product(self, product_id, field, new_value):
        product = self.get_product_by_id(product_id)
        if product:
            setattr(product, field, new_value)

    def save_data(self, filename):
        fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'id': product.id,
                    'name': product.name,
                    'desc': product.desc,
                    'price': product.price,
                    'quantity': product.quantity
                })

# Funktion för att visa inventarielistan
def show_inventory_list(inventory):
    print("\nInventarielista:")
    print(inventory.get_products())

# Main program
if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

    inventory = Inventory()
    inventory.load_data('db_products.csv')

    while True:
        # Huvudmeny för att välja alternativ
        print("\nAlternativ: ")
        print("'L' - Lägg till produkt")
        print("'U' - Uppdatera produkt")
        print("'T' - Ta bort produkt")
        print("'V' - Visa lista")
        print("'Q' - Avsluta programmet")

        choice = input("Ange ditt val: ").upper()

        if choice == 'Q':
            print("\nProgrammet avslutas.")
            break
        elif choice == 'L':
            try:
                new_id = int(input("Ange produkt-ID: "))
                new_name = input("Ange produktens namn: ")
                new_desc = input("Ange produktbeskrivning: ")
                new_price = float(input("Ange pris: "))
                new_quantity = int(input("Ange antal: "))

                new_product = Product(new_id, new_name, new_desc, new_price, new_quantity)
                inventory.add_product(new_product)
                inventory.save_data('db_products.csv')

                print("\nNy produkt har lagts till.")
            except ValueError:
                print("\nFelaktig inmatning, försök igen.")
        elif choice == 'U':
            try:
                product_id = int(input("Ange ID på produkten du vill uppdatera: "))
                product = inventory.get_product_by_id(product_id)

                if product:
                    print(f"\nUppdaterar produkt med ID {product_id}:")
                    field = input("Vilket fält vill du ändra? (name, desc, price, quantity): ").lower()
                    new_value = input(f"Nytt värde för {field}: ")

                    # Convert input to correct type
                    if field == 'price':
                        new_value = float(new_value)
                    elif field == 'quantity':
                        new_value = int(new_value)

                    inventory.update_product(product_id, field, new_value)
                    inventory.save_data('db_products.csv')

                    print("\nProdukten har uppdaterats.")
                else:
                    print("\nIngen produkt med det ID:t hittades.")
            except ValueError:
                print("\nFelaktig inmatning, försök igen.")
        elif choice == 'T':
            try:
                product_id_to_remove = int(input("Ange ID på produkten du vill ta bort: "))
                product = inventory.get_product_by_id(product_id_to_remove)

                if product:
                    inventory.remove_product(product_id_to_remove)
                    inventory.save_data('db_products.csv')
                    print(f"\nProdukt med ID {product_id_to_remove} har tagits bort.")
                else:
                    print("\nIngen produkt med det ID:t hittades.")
            except ValueError:
                print("\nFelaktigt ID, försök igen.")
        elif choice == 'V':
            show_inventory_list(inventory)
        else:
            print("\nOgiltigt val, försök igen.")
