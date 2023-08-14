import json
import os


class Product:
    """Class representing a medication / product in the project.

    Attributes:
        code: unique identifier of the product (string)
        name: name of the product (string)
        brand: the brand of the product (string)
        description: a textual description of the project (string)
        quantity: the quantity of products available in the stock (int)
        price: unit price of the project (float)
        dosage_instruction: instructions to take the medicine (string, optional)
        requires_prescription: whether the medication requires a prescription (bool)

    """

    def __init__(
            self,
            code: str,
            name: str,
            brand: str,
            description: str,
            quantity: int,
            price: float,
            dosage_instruction: str,
            requires_prescription: bool,
            category: str) -> None:
        self.code = code
        self.name = name
        self.brand = brand
        self.quantity = quantity
        self.category = category
        self.description = description
        self.price = price
        self.dosage_instruction = dosage_instruction
        self.requires_prescription = (requires_prescription != 0)

    def to_json(self) -> str:
        """Returns a valid JSON representation of the object

        Arguments:

        Returns: A JSON string.
        """
        json_str = json.dumps(self.__dict__)
        return json_str

    @staticmethod
    def getProductByID(id: str)->Product|None:
        current_folder = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.abspath(
            os.path.join(current_folder, '../../data'))
        prescriptionPath = os.path.join(data_folder, 'products.json')
        with open(prescriptionPath, 'r') as f:
            prescriptions = json.load(f)
        for prescription in prescriptions:
            if prescription['code'] == id:
                return Product(prescription['code'],
                               prescription['name'],
                               prescription['brand'],
                               prescription['description'],
                               prescription['quantity'],
                               prescription['price'],
                               prescription['dosage_instruction'],
                               prescription['requires_prescription'],
                               prescription['category'])
        return None

    def __str__(self) -> str:
        return self.name
