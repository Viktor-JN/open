import csv
import os
import locale
from time import sleep
from msvcrt import getwch


def load_data(filename): 
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(        #list
                {                    #dictionary
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

def save_data(filename, list):
    with open(filename, 'w', newline='') as file:
        fields = ["id", "name", "desc", "price", "quantity"]
        rows = []
        for i in range(len(list)):
            append_row = []
            append_row.append(list[i]['id'])
            append_row.append(list[i]['name'])
            append_row.append(list[i]['desc'])
            append_row.append(list[i]['price'])
            append_row.append(list[i]['quantity'])
            rows.append(append_row)
        write = csv.writer(file)  
        write.writerow(fields)
        write.writerows(rows)



#gör en funktion som hämtar en produkt

    
def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break  # Avsluta loopen så snart produkten hittas

    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"


def view_product(products, id):
    # Go through each product in the list
    for product in products:
        # Check if the product's id matches the given id
        if product["id"] == id:
            # If it matches, return the product's name and description
            return f"Visar produkt: {product['name']} {product['desc']}"
    
    # If no matching product is found, return this message
    return "Produkten hittas inte"


def view_products(products):
    product_list = []
    for index, product in enumerate(products,1 ):
        product_info = f"{index}) (#{product['id']}) {product['name']} \t {product['desc']} \t {locale.currency(product['price'], grouping=True)}"
        product_list.append(product_info)
    
    return "\n".join(product_list)

#TODO: gör om så du slipper använda global-keyword (flytta inte "product = []")
#TODO: skriv en funktion som returnerar en specifik produkt med hjälp av id

def add_product(name,desc,price,quantity):
    max_id_dic = max(products, key=lambda id: id["id"])
    max_id = max_id_dic["id"]
    identification = max_id+1
    products.append(        #list
                {                    #dictionary
                    "id": identification,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )

def edit(products, identification):
    inputt = input("""Vad vill du ändra
(N)amn
(B)eskrivining
(P)ris
(A)ntal\n""").strip().upper()
    if inputt in ["N", "B", "P", "A"]:
        if inputt == "N":
            new_name = input("Nya namnet: ")
            selected_product["name"] = new_name
        elif inputt == "B":
            new_desc = input("Nya beskrivningen: ")
            selected_product["desc"] = new_desc
        elif inputt == "P":
            new_price = input("Nya priset: ")
            selected_product["price"] = new_price
        elif inputt == "A":
            new_quantity = input("Nya antalet: ")
            selected_product["quantity"] = new_quantity
    else:
        print("Välj något i listan")
        sleep(0.3)

def view_inventory(products):
    # skapa sidhuvudet av tabellen:
    header = f"{'#':<6} {'NAMN':<26} {'BESKRIVNING':<51} {'PRIS':<15} {'KVANTITET':<10}"
    separator = "-" * 110           #linje
    
    # rader för varje produkt:
    rows = []

    for index, product in enumerate(products, 1):
        name = product['name']
        desc = product['desc']
        price = product['price']
        quantity = product['quantity']
        
        price = locale.currency(price, grouping=True)
        row = f"{index:<5} {name:<25} {desc:<50} {price:<14} {quantity:<10}"

        rows.append(row)
    
    # kombinera sidhuvud och rader:
    inventory_table = "\n".join([header, separator] + rows)
    
    return f"{inventory_table}"

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('db_products.csv')
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))  # Show ordered list of products

        choice = input("""(V)isa produkt
(T)a bort en produkt
(L)ägga till en produkt
(Ä)ndra produkt
(S)para listan\n""").strip().upper()


        if choice in ["V", "L", "T", "Ä"]:
            index = int(input("Enter product ID: "))
            
            if choice == "V":   #visa
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product
                    print(view_product(products, id))  # Remove product using the actual ID
                    done = input()
                    
                else:
                    print("Ogiltig produkt")
                    sleep(0.3)

            elif choice == "T": #ta bort
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product

                    print(remove_product(products, id))  # Remove product using the actual ID
                    sleep(0.5)            

                else:
                    print("Ogiltig produkt")
                    sleep(0.3)
            
            elif choice == "Ä": #ändra
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]
                    identification = selected_product["id"]
                    edit(products, identification)
                else:
                    print("Ogiltig produkt")
                    sleep(0.3)

            elif choice == "L":
                    name = input("Namn: ")
                    desc = input("Beskrivning: ")
                    price = float(input("Pris: "))
                    quantity = int(input("Antal: "))
                    add_product(name,desc,price,quantity)

        elif choice == "S":
            save_data('db_products.csv', products)

    except ValueError:
        print("Välj en produkt med siffor")
        sleep(0.5)
