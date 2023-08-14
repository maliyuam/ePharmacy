from .cart import Cart
from .stock import Stock
from .product import Product
from .prescription import Prescription
from datetime import datetime

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
        if prescription == None:
            raise Exception("Prescription is required for this order")

        if prescription.customerID != customerID:
            raise Exception("Customer ID does not match prescription")
        for i, product in enumerate(cart.stock.products):
            if product.requires_prescription:
                # a prescription has a list of dictionaries called Medications which has a name, quantity, id and ProcessedStatus
                for medication in prescription.medications:
                    if product.code == medication["id"]:
                        if product.quantity != medication["quantity"]:
                            raise Exception(
                                "Quantity does not match prescription by the Doctor")
                        # if medication["ProcessedStatus"] == False:
                        #     raise Exception("Prescription has not been processed")
                        # if medication["ProcessedStatus"] == True:
                        #     print("Prescription has been processed")
                            break
        # TODO: Get the current datetime and save a Sale information for each product sold with the following schema
        # {"name": "<name>", "quantity": <quantity>, "price": <unit price>, "purchase_price": <total price>, "timestamp": <timestamp>,
        # "customerID": <customer username>, "salesperson": <pharmacist username>}
        # and append it to the sales list.
        salesData = []
        for i, product in enumerate(cart.stock.products):
            salesData.append(Sale.create(product.name, product.quantity, product.price, product.price * product.quantity,
                             datetime.now().strftime("%d/%m/%Y %H:%M:%S"), customerID, self.agentID, prescription.PrescriptionID))
        # TODO: Append the list to the current sales
        self.sales = salesData
        # TODO: Make sure that the sold products are marked as complete in the prescriptions.
        # for i, product in enumerate(cart.stock.products):

        for i, product in enumerate(prescription.Medications):
            prescription.Medications[i]["ProcessedStatus"] = True

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
                else :
                    prescriptions.append(prescription)
            with open(outfile, "w") as f:
                json.dump([prescription.toJsonData()
                          for prescription in prescriptions], f, indent=4)

        # TODO: Update the content by appending the new entries to it, and save to the file
