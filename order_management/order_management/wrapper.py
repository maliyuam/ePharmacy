from .cart import Cart
from .stock import Stock
from .product import Product
from .sale import Sale
from .prescription import Prescription
from datetime import datetime
from typing import List

import os
import json

# would need to create a new object for each new order


class Wrapper:
    """
    Main class used to m    anage orders and carts.

    Attributes:
        sales: A list of the sales done during the program's execution
        stock: The stock used in the execution
        agentID: the username of the pharmacist running the program
    """

    def __init__(self, stock: Stock, agentID: str) -> None:
        self.sales = []
        self.stock = stock
        self.agentID = agentID
        current_folder = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.abspath(
            os.path.join(current_folder, '../../data'))
        self.prescription_file = os.path.join(
            data_folder, 'prescriptions.json')
        self.sale_file = os.path.join(data_folder, 'sales.json')
        self.products_file = os.path.join(data_folder, 'products.json')

    def checkout(self, cart: Cart, customerID: str, prescription: Prescription = None):
        """Handles the checkout procedure of the program.

        Args:
            cart: The cart to pay for
            prescription: the prescription that accompanies the order (default: None)
        """

        # TODO: First check that all the product that require a prescription have all the criteria met

        # (i.e., (1) there is a prescription that (2) matches the customer's ID, and (3) contains the medication
        # in the specified quantity).
        # Raise an exception if either of those conditions is unmet.
        keys = list(cart.products.keys())
        # fetch medications fron the keys
        products = []
        for i, product in enumerate(cart.stock.products):
            if product.code in keys:
                products.append(product)
        for i, item in enumerate(products):
            print(item.requires_prescription)
            if item.requires_prescription:
                if prescription == None:
                    raise Exception(
                        f'Prescription is required for {item.name}')
                for j, medication in enumerate(prescription.Medications):
                    if medication["id"] == item.code:
                        if medication.quantity != cart.products[item.code]:
                            raise Exception(
                                "Quantity does not match prescription by the Doctor")

        # TODO: Get the current datetime and save a Sale information for each product sold with the following schema
        # {"name": "<name>", "quantity": <quantity>, "price": <unit price>, "purchase_price": <total price>, "timestamp": <timestamp>,
        # "customerID": <customer username>, "salesperson": <pharmacist username>}
        # and append it to the sales list.
        salesData = []

        for i, product in enumerate(products):
            salesData.append(Sale.create(product.name, cart.products[product.code], product.price, product.price * cart.products[product.code],
                             datetime.now().strftime("%d/%m/%Y %H:%M:%S"), customerID, self.agentID, prescription.PrescriptionID if prescription != None else ""))
        updated_products = []
        for item in cart.stock.products:
            if item.code in keys:
                item.quantity -= cart.products[item.code]
                updated_products.append(item)
            else:
                updated_products.append(item)

        self.stock.products = updated_products

        self.handle_quantity_change(updated_products)

        # TODO: Append the list to the current sales
        self.sales = salesData
        self.update_sales(self.sale_file)

        # TODO: Make sure that the sold products are marked as complete in the prescriptions.
        # for i, product in enumerate(cart.stock.products):
        if prescription != None:
            for i, product in enumerate(prescription.Medications):
                prescription.Medications[i]["ProcessedStatus"] = True
            self.dump(self.prescription_file, prescription)

    def dump(self, outfile: str, prescription: Prescription = None):
        """Dumps the current sales data to a file

        Args:
            outfile: the path to the output file
        """
        # TODO: Load the content, if any of the existing file

        with open(outfile, "r") as f:
            content = json.load(f)
            prescriptions = []
            for item in content:
                prescriptions.append(Prescription.fromJsonData(item))
        if prescription != None:
            for i in range(len(prescriptions)):
                if prescriptions[i].PrescriptionID == prescription.PrescriptionID:
                    prescriptions[i] = prescription
                    break
                else:
                    prescriptions.append(prescription)
            with open(outfile, "w") as f:
                json.dump([prescription.toJsonData()
                          for prescription in prescriptions], f)

        # TODO: Update the content by appending the new entries to it, and save to the file
    def update_sales(self, outfile: str):
        """Dumps the current sales data to a file

        Args:
            outfile: the path to the output file
        """
        with open(outfile, "r") as f:
            content = json.load(f)
            sales = []
            for item in content:
                sales.append(Sale.fromJsonData(item))
            for item in self.sales:
                sales.append(item)
            with open(outfile, "w") as f:
                json.dump([sale.toJsonData() for sale in sales], f)

    def handle_quantity_change(self, products: List[Product]):
        """Handles the quantity change of a product

        Args:
            product: the product to update
            quantity: the new quantity
        """
        with open(self.products_file, "w") as f:
            json.dump([product.to_json()
                      for product in products], f)
