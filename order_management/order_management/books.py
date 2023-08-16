from __future__ import annotations

import json
from datetime import datetime
import os

from typing import List
from .sale import Sale
from .prescription import Prescription
from .product import Product


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

        if (len(self.transactions) == 0):
            return "No purchases have been made yet."
        formatted = "-"*160 + "\n"
        formatted += f"|{'ID':^20} | {'Date':^20} | {'Customer':^20} | {'Medication':^20} | {'Quantity':^20} | {'Purchase Price':^20} | {'Prescription':^20}|\n"
        formatted += "-"*160 + "\n"
        for i, transaction in enumerate(self.transactions):
            # date = datetime.fromtimestamp(transaction.timestamp)
            date_str = datetime.fromtimestamp(
                transaction.timestamp).strftime('%Y-%m-%d')
            prescription_id = transaction.prescriptionID if transaction.prescriptionID != "" else "Not Available"
            formatted += f"|{i:^20} | {date_str:^20} | {transaction.customerID:^20} | {transaction.name:^20} | {transaction.quantity:^20} | {transaction.purchase_price:^20} | {prescription_id:^20}|\n"
            formatted += "_"*160 + "\n"
            return formatted

    def agent_format(self, data) -> str:
        """Returns a string representation of a record.

        Args:

        Returns: A string
        """
        if (len(data) == 0):
            return "No sales have been made yet."
        formatted = "-"*160 + "\n"
        formatted += f"|{'ID':^20} | {'Date':^20} | {'Agent':^20} | {'Medication':^20} | {'Quantity':^20} | {'Purchase Price':^20} | {'Prescription':^20}|\n"
        formatted += "-"*160 + "\n"
        for i, transaction in enumerate(data):
            # date = datetime.fromtimestamp(transaction.timestamp)
            date_str = datetime.fromtimestamp(
                transaction.timestamp).strftime('%Y-%m-%d')
            prescription_id = transaction.prescriptionID if transaction.prescriptionID != "" else "Not Available"
            formatted += f"|{i:^20} | {date_str:^20} | {transaction.salesperson:^20} | {transaction.name:^20} | {transaction.quantity:^20} | {transaction.purchase_price:^20} | {prescription_id:^20}|\n"
            formatted += "_"*160 + "\n"
            return formatted

    def top_prd_format(self, data) -> str:
        """Returns a string representation of a record.

        Args:

        Returns: A string
        """
        if (len(data) == 0):
            return "No sales have been made yet."
        formatted = "-"*183 + "\n"
        formatted += f"|{'ID':^20} | {'Date':^20} | {'Customer':^20} | {'Agent':^20} | {'Medication':^20} | {'Quantity':^20} | {'Purchase Price':^20} | {'Prescription':^20}|\n"
        formatted += "-"*183 + "\n"
        for i, transaction in enumerate(data):
            # date = datetime.fromtimestamp(transaction.timestamp)
            date_str = datetime.fromtimestamp(
                transaction.timestamp).strftime('%Y-%m-%d')
            prescription_id = transaction.prescriptionID if transaction.prescriptionID != "" else "Not Available"
            formatted += f"|{i:^20} | {date_str:^20} | {transaction.customerID:^20} | {transaction.salesperson:^20} | {transaction.name:^20} | {transaction.quantity:^20} | {transaction.purchase_price:^20} | {prescription_id:^20}|\n"
            formatted += "_"*183 + "\n"
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
                    if (prescription.PrescriptionID in prescriptionIds):
                        extractedPrescriptions.append(prescription)
                if (len(extractedPrescriptions) == 0):
                    return "No prescriptions have been processed yet."
                else:
                    formatted = "-"*45 + "\n"
                    formatted += f"|{'Prescription ID':^20} | {'Total Price':^20}|\n"
                    formatted += "-"*45 + "\n"

                    for prescription in extractedPrescriptions:
                        total = 0
                        for medication in prescription.Medications:
                            medicationId = medication['id']
                            product = Product.getProductByID(medicationId)
                            if (product != None):
                                total += product.price
                        formatted += f"|{prescription.PrescriptionID:^20} | {total:^15} RWF |\n"
                        formatted += "_"*45 + "\n"
                    return formatted

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
            if (transaction.customerID == customerID):
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
        return self.agent_format(transactions)

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
        # print(start)
        # print(end)
        # transactions = None
        # formattedData = []
        transactions = []

        for transaction in self.transactions:
            time_data = datetime.fromtimestamp(transaction.timestamp)
            if start < time_data and end > time_data:
                transactions.append(transaction)
    
        sortedTransactions = sorted(
            transactions, key=lambda x: x.purchase_price,reverse=True)
        # print(len(transactions))
        # return the string representation of the transactions.
        formatted  = sortedTransactions[:n]
        return self.top_prd_format(formatted)

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
