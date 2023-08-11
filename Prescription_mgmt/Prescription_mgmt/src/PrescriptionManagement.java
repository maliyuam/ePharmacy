import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.util.ArrayList;

import org.json.simple.parser.ParseException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import org.json.simple.parser.JSONParser;

public class PrescriptionManagement {

    public static void main(String[] args) throws IOException, ParseException {

        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        int choice, numMedications;
        Prescription prescription = new Prescription();
        FileHandler fileHandler = new FileHandler();

        while (true) {
            System.out.println("Prescription Management System");
            System.out.println("1. Add Prescription");
            System.out.println("2. View Prescriptions");
            System.out.println("3. Delete Prescription");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");
            // check that the input is not null and can be parsed to an integer
            String input = reader.readLine();
            if (input == null || input.isEmpty()) {
                System.out.println("Choice cannot be empty");
                break;
            }
            try {
                choice = Integer.parseInt(input);
            } catch (NumberFormatException e) {
                System.out.println("Choice must be an integer");
                break;
            }
            switch (choice) {
                case 1:
                    System.out.print("Enter Prescription ID: ");
                    // check that the input is not null
                    String prescrID = reader.readLine();
                    if (prescrID == null || prescrID.isEmpty()) {
                        System.out.println("Prescription ID cannot be empty");
                        break;
                    }
                    prescription.setPrescriptionID(prescrID);

                    System.out.print("Enter Customer ID: ");
                    // check that the input is not null
                    String custID = reader.readLine();
                    if (custID == null || custID.isEmpty()) {
                        System.out.println("Customer ID cannot be empty");
                        break;
                    }
                    prescription.setCustomerID(custID);

                    System.out.print("Enter Doctor's Name: ");
                    // check that the input is not null
                    String docName = reader.readLine();
                    if (docName == null || docName.isEmpty()) {
                        System.out.println("Doctor's Name cannot be empty");
                        break;
                    }
                    prescription.setDoctorName(docName);
                    prescription.setDate(LocalDate.now());
                    System.out.println("Enter the number of medications to add: ");
                    // check that the input is not null and can be parsed to an integer
                    String numMeds = reader.readLine();
                    if (numMeds == null || numMeds.isEmpty()) {
                        System.out.println("Number of medications cannot be empty");
                        break;
                    }
                    try {
                        numMedications = Integer.parseInt(numMeds);
                    } catch (NumberFormatException e) {
                        System.out.println("Number of medications must be an integer");
                        break;
                    }

                    ArrayList<Medication> medications = new ArrayList<>();

                    displayMedications("src/products.json");
                    for (int i = 1; i <= numMedications; i++) {
                        String medicationName, medicationDetails, dosage, medicationID;
                        int quantity;
                        System.out.println("Enter details for Medication " + i + ":");
                        System.out.print("Enter Medication ID: ");
                        // check that the input is not null
                        String medID = reader.readLine();
                        if (medID.trim() == null || medID.isEmpty()) {
                            System.out.println("Medication ID cannot be empty");
                            break;
                        }
                        medicationID = medID;

                        System.out.print("Enter Medication Name: ");
                        // check that the input is not null
                        String medName = reader.readLine();
                        if (medName.trim() == null || medName.isEmpty()) {
                            System.out.println("Medication Name cannot be empty");
                            break;
                        }
                        medicationName = medName.trim();

                        System.out.print("Enter Medication Details: ");
                        // check that the input is not null
                        String medDetails = reader.readLine();
                        if (medDetails.trim() == null || medDetails.isEmpty()) {
                            System.out.println("Medication Details cannot be empty");
                            break;
                        }
                        medicationDetails = medDetails.trim();

                        System.out.print("Enter Medication Dosage: ");
                        // check that the input is not null
                        String medDosage = reader.readLine();
                        if (medDosage.trim() == null || medDosage.isEmpty()) {
                            System.out.println("Medication Dosage cannot be empty");
                            break;
                        }

                        System.out.print("Enter Medication Quantity: ");
                        // check that the input is not null
                        String medQuantity = reader.readLine();
                        if (medQuantity.trim() == null || medQuantity.isEmpty()) {
                            System.out.println("Medication Quantity cannot be empty");
                            break;
                        }
                        try {
                            quantity = Integer.parseInt(medQuantity);
                        } catch (NumberFormatException e) {
                            System.out.println("Medication Quantity must be an integer");
                            break;
                        }

                        dosage = medDosage.trim();
                        Medication medication = new Medication(medicationID, medicationName, medicationDetails, dosage,
                                quantity);
                        medications.add(medication);
                    }
                    prescription.setMedications(medications);
                    prescription.addPrescription();
                    System.out.println("Prescription added successfully");

                    break;
                case 2:
                    ArrayList<Prescription> prescriptions = new ArrayList<>();
                    prescriptions = prescription.viewPrescription();

                    if (prescriptions.size() == 0) {
                        System.out.println("No precriptions available\n");
                    } else {
                        System.out.println("| PrescriptionID |  DoctorName   |    CustomerID | \tDate\t | ");
                        System.out.println("******************************************************************");

                        for (Prescription p : prescriptions) {
                            System.out.println("|\t " + p.getPrescriptionID() + "\t" + p.getDoctorName() + "\t\t  "
                                    + p.getCustomerID() + "\t\t" + p.getDate());

                            System.out.println("");
                            System.out.println("| MedicationID |  \tName    | \t Quantity | ");
                            for (Medication med : p.getMedications()) {
                                System.out.println(
                                        "|\t " + med.getID() + "\t\t" + med.getName() + "\t\t\t"
                                                + med.getQuantity());
                            }

                            System.out.print("\n");
                            System.out.println("*****************************************************************");
                        }

                        System.out.println("");
                    }

                    break;
                case 3:
                    System.out.print("Enter the ID of the prescription you want to delete: ");
                    // String prescrID = reader.readLine();
                    String enteredId = reader.readLine();
                    if (enteredId.trim() == null || enteredId.isEmpty()) {
                        System.out.println("Prescription ID cannot be empty");
                        break;
                    }
                    prescription.deletePrescription(enteredId);
                    break;
                case 4:
                    System.out.println("Exiting the Precription Management section...");
                    System.exit(0);
                default:
                    System.out.println("Invalid choice. Please try again.");
            }

        }

    }

    public static void displayMedications(String filePath) throws FileNotFoundException, IOException, ParseException {

        JSONParser parser = new JSONParser();
        try (FileReader fileReader = new FileReader(filePath)) {
            if (fileReader.read() == -1) {
                return;
            } else {
                fileReader.close();
                JSONArray jsonArray = (JSONArray) parser.parse(new FileReader(filePath));

                System.out.println(
                        "---------------------------------------------------------------------------------------");
                System.out.println("|\t" + "\t\t  " + "\t\t\t\t");
                System.out.println("|\t" + "\t\t" + "Available Medications" + "\t\t");
                System.out.println("|\t" + "\t\t  " + "\t\t\t\t");
                System.out.println(
                        "---------------------------------------------------------------------------------------");
                System.out.println(
                        "| Medication ID |  Medication Name   |    Medication Price ||    Medication Quantity |");
                System.out.println(
                        "---------------------------------------------------------------------------------------");

                for (Object obj : jsonArray) {
                    JSONObject jsonObject = (JSONObject) obj;

                    // TODO: Add code to get medication ID (it's named as code from
                    // medications/products file), name, price and quantity
                    // medication ID, name, price and quantity should be casted to String
                    System.out.println("|\t" + jsonObject.get("code") + "\t\t" + jsonObject.get("name") + "\t\t"
                            + jsonObject.get("price") + "\t\t" + jsonObject.get("quantity") + "\t\t"
                            + "\t\t\t\t");
                    // System.out.println("|\t" + medicationID + "\t\t" + medicationName + "\t\t " +
                    // medicationPrice
                    // + "\t\t\t " + medicationQuantity + "\t\t");

                }
                System.out.println(
                        "---------------------------------------------------------------------------------------");

            }
        }

    }

}
