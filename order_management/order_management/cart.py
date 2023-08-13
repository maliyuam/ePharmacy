from .product import Product
from .stock import Stock


class Cart:
    """Represents a cart with a list of products and quantity

    Attributes:
        products: a dictionary with the key being the ID of the products, and the value being the quantity
        added
    """

    def __init__(self, stock: Stock) -> None:
        self.products = {}
        self.stock = stock

    def add(self, productCode: str, quantity: int) -> None:
        """Adds a product to the cart with the specified quantity

        Args:
            productCode: the identifier of the product
            quantity: quantity to add

        Returns: None
        """
        # TODO: Make sure the quantity is valid (> 0 and <= to the quantity in the stock)
        # iterate over the list of the

        product = getProductByID(productCode)
        if (product == None):
            raise ValueError("Product code not found")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > product.quantity:
            raise ValueError(
                "Quantity must be less than or equal to the quantity in the stock")
        # TODO: If the product was already in the cart, increment the quantity
        if productCode in self.products:
            self.products[productCode] = +quantity
        else:
            self.products[productCode] = quantity

    def __str__(self) -> str:
        """String representation of the cart
        """
        # TODO: Return a string representation of a cart that shows the products, their quantity, unit price, total price. And also the total price of the cart
        return f""
        # Feel free to format it the way you want to
        return NotImplemented

    def remove(self, code):
        """
        Removes a specific product from the cart """
        # TODO: Removes a product from the cart. safely fail if the product code is not found
        if code in self.products:
            del self.products[code]
        else:
            raise ValueError("Product code not found")

    def clear(self):
        """Clears up the cart.
        """
        self.products.clear();

    @property
    def cost(self):
        """Returns the total cost of the cart"""
        # TODO: implement the function
