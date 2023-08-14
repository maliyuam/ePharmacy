import json

from typing import List, Dict, Union
from .product import Product


class Prescription:
    """Represents a prescription object

    Attributes:
        DoctorName: the name of the doctor who gave the prescription
        PrescriptionID: ID of the prescription
        Medications: list of the medications, this is the quantity, the ID, the name, and whether it was processed or not
        # see format in prescriptions.json
        CustomerID: ID of the customer
    """

    def __init__(self, DoctorName: str, PrescriptionID: str, Medications: List[Dict[str, Union[int, str, bool]]],
                 CustomerID: str, Date: str) -> None:
        self.DoctorName = DoctorName
        self.PrescriptionID = PrescriptionID
        self.Medications = Medications
        self.CustomerID = CustomerID
        current_folder = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.abspath(
            os.path.join(current_folder, '../../data'))
        self.prescriptionPath = os.path.join(data_folder, 'prescriptions.json')
        self.Date = Date

    def medecineInPrescription(self, product: Product, quantity: int) -> bool:
        """Verifies if a medecine with the specified quantity is included in a prescription

        Args:
            product: the product to verify
            quantity: the quantity to be added

        Returns: A boolean denoting whether the value was found
        """
        # create and format the document path

        prescription = self.get(self.prescriptionPath, self.PrescriptionID)
        if prescription is None:
            return False
        for medication in prescription['Medications']:
            if medication['ProductID'] == product.ProductID and medication['quantity'] == quantity:

                return True
        return False

    def markComplete(self, product: Product):
        """Mark a product's sale complete in the prescriptions file

        Args:
            product: the product sold

        Returns: None
        """
        # TODO: Change the value "ProcessedStatus" of the relevant product to True
        prescription = self.get(self.prescriptionPath, self.PrescriptionID)
        if prescription is None:
            print("Prescription not found")
            return

        for medication in len(prescription['Medications']):
            if medication['ProductID'] == product.ProductID:
                medication['ProcessedStatus'] = True
                break
        # performing the reading of the prescription file and performing tha update th change the value of the processed status to true
        with (open(self.prescriptionPath, 'r')) as file:
            data = json.load(file)
            for prescription in data:
                if prescription['PrescriptionID'] == self.PrescriptionID:
                    prescription = prescription
                    break
        with (open(self.prescriptionPath, 'w')) as file:
            json.dump(data, file)

    def dump(self, outfile: str):
        """Dumps the updated prescription to the specified file

        Args: 
            outfile: path to the file where the output should be written

        Returns: None
        """
        # TODO: Read the output file (safely).
        with (open(outfile, 'r')) as file:
            data = json.load(file)
            for prescription in data:
                if prescription['PrescriptionID'] == self.PrescriptionID:
                    prescription = self
                    break

        # TODO: Update the prescription that is being edited in the loaded data
        # TODO: Save the updated object
        with (open(outfile, 'w')) as file:
            json.dump(data, file)
    @staticmethod
    def fromJsonData(self, data:str) -> self:
        """Loads all prescriptions from the file
        Returns: A list of prescription objects
        """
        return Prescription(
            DoctorName=data['DoctorName'],
            PrescriptionID=data['PrescriptionID'],
            Medications=data['Medications'],
            CustomerID=data['CustomerID'],
            Date=data['Date']
        )



    @classmethod
    def get(cls, infile: str, id: str):
        """Retrieves a specific prescription from a file

        Args:
            infile: path to the input file
            id: identifier of the prescription to add

        Returns: A prescription object as a dictionary
        """
        # TODO: Load the file and find the object with the relevant ID
        with (open(infile, 'r')) as file:
            data = json.load(file)
            prescriptions = [p for p in data if p['PrescriptionID'] == id]
            if len(prescriptions) > 0:
                return prescriptions[0]
        return None

    # TODO: Return the relevant prescription
