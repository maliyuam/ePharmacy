import json
from typing import List
from .product import Product


class Stock:
    """Represents the catalog of products

    Attributes:
        products: the list of products
    """

    def __init__(self, products: List[Product]) -> None:
        self.products = products

    def update(self, id: str, change: int):
        """Update the quantity of a product by adding or removing

        Args:
            id: identifier of the product
            change: the value by which the quantity should be update (+1 adds 1, -2 removes 2 for example)
        """
        # TODO: Make sure the product exists, and that by making the change, the value is still >= 0
        for product in self.products:
            if product.code == id:
                product.quantity -= change
                return
        raise Exception("Product not found")

    def getProductByID(self, id: str) -> Product:
        """Gets a product by its ID
        Args:
            id: identifier of the product

        Returns: the product's object
        """
        for product in self.products:
            if product.code == id:
                return product
        return None

    def dump(self, outfile: str):
        """Saves the stock to a JSON file"""
        # TODO: Implement the function
        with open(outfile, 'w') as f:
            json.dump(self.products, f)

    @staticmethod
    def load(infile: str):
        """Loads the stock from an existing file

        Args: 
            infile: input file to the function
        """
        with open(infile, 'r') as f:
            data = json.load(f)
            # print(data)
            products = [
                Product(
                    code=product['code'],
                    name=product['name'],
                    brand=product['brand'],
                    description=product['description'],
                    quantity=product['quantity'],
                    price=product['price'],
                    requires_prescription=product['requires_prescription'],
                    category=product['category'],
                    dosage_instruction=product['dosage_instruction'],


                )
                for product in data
            ]

            return Stock(products)
        # TODO: Implement the function

    def __str__(self) -> str:
        """Returns a string representation of the stock
        """
        # TODO: Return the description of the stock with a nice output showing the ID, Name, Brand, Description, Quantity, Price, and the requires_prescription field
        formatted = f"|{'ID':^10} | {'Name':^20} | {'Brand':^20} | {'Description':^20} | {'Quantity':^10} | {'Price':^10} | {'Requires Prescription':^10}\n |"
        for product in self.products:
            formatted += f"{product.code:<10}{product.name:<20}{product.brand:<20}{product.description:<20}{product.quantity:<10}{product.price:<10}{product.requires_prescription:<10}\n"
        return formatted
