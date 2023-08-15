from __future__ import annotations

import json
from datetime import datetime
import os

from typing import List
from .sale import Sale
from .prescription import Prescription


class BookRecords:
    """A record of all the sales made through the application.

    Attributes:
        transactions: a list of the transactions
    """

    def __init__(self, transactions: List[Sale]) -> None:
        self.transactions = transactions
        current_folder = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.abspath(
            os.path.join(current_folder, '../../data'))
        self.prescriptionPath = os.path.join(data_folder, 'prescriptions.json')
        self.salesPath = os.path.join(data_folder, 'sales.json')

    def __str__(self) -> str:
        """Returns a string representation of a record.

        Args:

        Returns: A string
        """

        # TODO: In the format below, return a representation of the records
        # |      # | Date                | Customer   | Medication | Quantity | Purchase Price | Prescription |
        # |      1 | 2023-06-03 21:23:25 | doe        | Quinine    |        3 |       1400 RWF | PHA1         |
        formatted = f"|{'Date':^20} | {'Customer':^20} | {'Medication':^20} | {'Quantity':^20} | {'Purchase Price':^20}{'Prescription':^20}|\n"
        for i, transaction in enumerate(self.transactions):
            formatted += f"|{i:<10}{transaction.date:<10}{transaction.customer:<10}{transaction.medication:<10}{transaction.quantity:<10}{transaction.purchase_price:<10}{transaction.prescriptionID:<10}|\n"
        return formatted

    def reportOnPrescriptions(self) -> str:
        """Reports on prescription sales.

        Args: 

        Returns: A string report of the prescriptions processed
        """
        # TODO: From the transactions data, retrieve for each prescription, the actual medications that were processed
        # and aggregate for each, the corresponding total price.

        # TODO: output in the following format, the results:
        # |    # | Prescription ID | Total Price |

        prescriptionIds = []
        for transaction in self.transactions:
            prescriptionIds.append(transaction.prescriptionID)

        with open(self.prescriptionPath, 'r') as f:
            rawPrescriptions = json.load(f)
            prescriptions = []
            for prescription in rawPrescriptions:
                prescriptions.append(Prescription.fromJsonData(prescription))
            if (len(prescriptions) == 0):
                return "No prescriptions have been processed yet."
            else:
                extractedPrescriptions = []
                for prescription in prescriptions:
                    if (prescription.id in prescriptionIds):
                        extractedPrescriptions.append(prescription)
                if (len(extractedPrescriptions) == 0):
                    return "No prescriptions have been processed yet."
                else:
                    formatted = f"|{'Prescription ID':<20}{'Total Price':<20}|\n"
                    for prescription in extractedPrescriptions:
                        total = 0
                        for medication in prescription.medications:
                            medicationId = medication['id']
                            product = Product.getProductByID(medicationId)
                            if (product != None):
                                total += product.price
                            else:
                                formatted += f"|{prescription.id:<20}{total:<20}|\n"
                    return formatted
                    print(formatted)

    def purchasesByUser(self, customerID: str):
        """Reports on the sales performed by a customer.

        Args:
            customerID: Username of the customer.

        Returns: A string representation of the corresponding transactions

        """
        # TODO: Query the transactions to the `transactions` list below
        transactions = None

        formattedData = []
        transactions = []
        for transaction in self.transactions:
            if (transaction.customer == customerID):
                transactions.append(transaction)
        return BookRecords(transactions).__str__()

    def salesByAgent(self, salesperson: str):
        """Reports on the sales performed by a pharmacist.

        Args:
            salesperson: Username of the pharmacist.

        Returns: A string representation of the corresponding transactions

        """
        # TODO: Query the transactions to the `transactions` list below
        transactions = None
        formattedData = []
        transactions = []
        for transaction in self.transactions:
            if (transaction.salesperson == salesperson):
                transactions.append(transaction)
        return BookRecords(transactions).__str__()

    def topNSales(self, start: datetime = datetime.strptime('1970-01-02', '%Y-%m-%d'), end: datetime = datetime.now(), n=10) -> str:
        """Return the top n sales ordered by the total price of purchases.

        Args:
            start: a datetime representing the start period to consider (datetime, default to 01 Jan 1970)
            end: a datetime representing the end period to consider (datetime, default to current timestamp)
            n: number of records to consider (int, default to 10)

        Returns:
        A string representation of the top n 
        """
        # TODO: Query the top transactions and save them to the variable `transactions` below
        transactions = None
        formattedData = []
        transactions = []
        for transaction in self.transactions:
            if (transaction.date >= start and transaction.date <= end):
                transactions.append(transaction)
        transactions = sorted(transactions, key=lambda x: x.purchase_price)
        transactions = transactions[:n]

        # return the string representation of the transactions.
        return BookRecords(transactions).__str__()

    def totalTransactions(self) -> float:
        """Returns the total cost of the transactions considered.

        Args:

        Returns: A floating number representing the total price
        """

        return sum([transaction.purchase_price for transaction in self.transactions])
    # create a method that gets thew data from the sales.json file

    def getSalesData(self):
        with open(self.salesPath, 'r') as f:
            data = json.load(f)
            return data

    @classmethod
    def load(cls, infile: str) -> BookRecords:
        """Loads a JSON file containing a number of sales object

        Args:
            infile: path to the file to be read
        Returns: A new object with the transactions in the file
        """
        # TODO: Implement the function. Make sure to handle the cases where
        if (not os.path.exists(infile)):
            raise FileNotFoundError(f"File {infile} does not exist")
        with open(infile, 'r') as f:
            data = json.load(f)
        formattedData = []
        for transaction in data:
            formattedData.append(Sale.fromJsonData(transaction))
        return BookRecords(formattedData)
