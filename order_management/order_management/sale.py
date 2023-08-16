import uuid
import datetime


class Sale:
    """Class repreenting a sale that was successfully committed to the records.

    Attributes:
        id: unique identifier of the product sold (string)
        name: name of the product sold
        quantity: the quantity sold during the sale
        price: unit price of the product
        purchase_price: the total price at which the product was sold
        timestamp: the UNIX timestamp of the sale
        customerID: username of the buying customer (string)
        salesperson: username of the pharmacist making the sale (string)
        prescriptionID: identifier of the prescription used in the sale
    """

    def __init__(self, id: str, name: str, quantity: int,
                 price: float, purchase_price: float, timestamp: float,
                 customerID: str, salesperson: str, prescriptionID: str) -> None:
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.purchase_price = purchase_price
        self.timestamp = timestamp
        self.customerID = customerID
        self.salesperson = salesperson
        self.prescriptionID = prescriptionID

    def __str__(self) -> str:
        """Returns a string representation of a Sale object.

        Args: None

        Returns: A string
        """
        # TODO: Return a string that shows the product sold, its unit price
        # the quantity, timestamp, and the total cost in a nice way.
        return f"{self.name} was sold at {self.price} per unit. {self.quantity} units were sold at {self.timestamp} for a total of {self.purchase_price}."

    def toJsonData(self):
        """Returns a JSON object representing a Sale object.

        Args: None

        Returns: A JSON object
        """
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'purchase_price': self.purchase_price,
            'timestamp': self.timestamp,
            'customerID': self.customerID,
            'salesperson': self.salesperson,
            'prescriptionID': self.prescriptionID
        }

    @staticmethod
    def fromJsonData(data):
        """Returns a Sale object from a JSON object.

        Args:
            data: A JSON object representing a Sale

        Returns: A Sale object
        """
        return Sale(data['id'], data['name'], data['quantity'], data['price'], data['purchase_price'], data['timestamp'], data['customerID'], data['salesperson'], data['prescriptionID'])

    @classmethod
    def create(cls, name: str, quantity: int, price: float, purchase_price: float, timestamp: float, customerID: str, salesperson: str, prescriptionID: str):
        id = "SL-" + str(uuid.uuid4())
        return cls(id, name, quantity, price, purchase_price, timestamp, customerID, salesperson, prescriptionID)
