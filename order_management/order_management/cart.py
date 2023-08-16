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

        product = Product.getProductByID(productCode)
        if (product == None):
            raise ValueError("Product code not found")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > product.quantity:
            raise ValueError(
                "Quantity must be less than or equal to the quantity in the stock")
        # TODO: If the product was already in the cart, increment the quantity
        if productCode in self.products.keys():
            self.products[productCode] += quantity
        else:
            self.products[productCode] = quantity

    def __str__(self) -> str:
        """String representation of the cart
        """
        # TODO: Return a string representation of a cart that shows the products, their quantity, unit price, total price. And also the total price of the cart
        
        productData = f""
        for i,product in enumerate(self.stock.products):
            keys = list(self.products.keys())
            if product.code in self.products.keys():
                productData += f"{product.code} - Name:{product.name} - Unit Price:{product.price} - Brand:{product.brand} Quantity:{self.products[product.code]} - Total:{product.price * self.products[product.code]}\n"
        return productData

        # Feel free to format it the way you want to

    def remove(self, code):
        """
        Removes a specific product from the cart """
        # TODO: Removes a product from the cart. safely fail if the product code is not found
        keys = list(self.products.keys())
        print(keys)
        if code in self.products.keys():    
            del self.products[code]
        else:
            raise ValueError("Product code not found")

    def clear(self):
        """Clears up the cart.
        """
        self.products.clear()

    @property
    def cost(self):
        """Returns the total cost of the cart"""
        # TODO: implement the function
        productData = []
        for product in self.products:
            if product.code in self.products:
                productData.append(product)

        totalCost = 0
        for product in productData:
            totalCost += product.price * self.products[product.code]
        return totalCost
