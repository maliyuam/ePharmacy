import java.io.IOException;
import java.time.LocalDate;
import java.util.ArrayList;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import org.json.simple.parser.ParseException;

public class Prescription {
	private String prescriptionID;
	private String customerID;
	private String doctorName;
	private ArrayList<Medication> medications;
	private LocalDate date;
	private static JSONArray prescriptionList;
	private FileHandler fileHandler;

	public Prescription() {
		prescriptionList = new JSONArray();
		fileHandler = new FileHandler();
	}

	public Prescription(String _prescriptionID, String _customerID, String _doctorName,
			ArrayList<Medication> _medication) {
		this.prescriptionID = _prescriptionID;
		this.customerID = _customerID;
		this.doctorName = _doctorName;
		this.medications = _medication;
		this.date = LocalDate.now();
				fileHandler = new FileHandler();

	}

	public Prescription(String _prescriptionID, String _customerID, String _doctorName,
			ArrayList<Medication> _medication, LocalDate _date) {
		this.prescriptionID = _prescriptionID;
		this.customerID = _customerID;
		this.doctorName = _doctorName;
		this.medications = _medication;
		this.date = _date;
				fileHandler = new FileHandler();
	}

	public String getPrescriptionID() {
		return this.prescriptionID;
	}
	public void setPrescriptionID(String id) {
		this.prescriptionID = id;
	}
	public String getCustomerID() {
		return this.customerID;
	}

	public void setCustomerID(String id) {
		this.customerID = id;
	}

	public String getDoctorName() {
		return this.doctorName;
	}

	public void setDoctorName(String docName) {
		this.doctorName = docName;
	}

	public ArrayList<Medication> getMedications() {
		return this.medications;
	}
	public void setMedications(ArrayList<Medication> _medications) {
		this.medications = _medications;
	}

	public LocalDate getDate() {
		return this.date;
	}

	public void setDate(LocalDate date) {
		this.date = date;
	}
	public static void setPrescriptionList(JSONArray _prescriptionList) {
		prescriptionList = _prescriptionList;
	}

	private JSONObject getJSONObject() {
		JSONObject jsonObject = new JSONObject();
		jsonObject.put("DoctorName", this.doctorName);
		jsonObject.put("PrescriptionID", this.prescriptionID);
		jsonObject.put("CustomerID", this.customerID);

		JSONArray medicationsArray = new JSONArray();
		for (Medication medication : this.medications) {
			JSONObject medicationObject = new JSONObject();
			medicationObject.put("id", medication.getID());
			medicationObject.put("name", medication.getName());
			medicationObject.put("quantity", medication.getQuantity());
			medicationObject.put("processedStatus", medication.getProcessedStatus());
			medicationsArray.add(medicationObject);
		}
		jsonObject.put("Medications", medicationsArray);
		jsonObject.put("Date", this.date.toString());
		return jsonObject;
	}

	public void addPrescription() throws IOException, ParseException {
		JSONArray existingPrescriptions = fileHandler.readJSONArrayFromFile(true);
		existingPrescriptions.add(
				new Prescription(this.prescriptionID, this.customerID, this.doctorName, this.medications)
						.getJSONObject());

		fileHandler.writeJSONArrayToFile(existingPrescriptions);
	}



	public JSONArray getMedicationsOnPrescription(Prescription prescription) {
		JSONArray jsonArray = new JSONArray();
		try {
			JSONArray existingPrescriptions = fileHandler.readJSONArrayFromFile(true);
			for (int i = 0; i < existingPrescriptions.size(); i++) {
				JSONObject jsonObject = (JSONObject) existingPrescriptions.get(i);
				String existingPrescriptionID = (String) jsonObject.get("prescriptionID");
				if (existingPrescriptionID == prescription.getPrescriptionID()) {
					jsonArray = (JSONArray) jsonObject.get("medications");
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return jsonArray;

	}

	public ArrayList<Prescription> viewPrescription() throws IOException, ParseException {

		JSONArray jsonArray = fileHandler.readJSONArrayFromFile(true);
		ArrayList<Prescription> prescriptions = new ArrayList<Prescription>();
		for (Object obj : jsonArray) {
			JSONObject jsonObject = (JSONObject) obj;

			String doctorName = (String) jsonObject.get("DoctorName");
			String prescriptionID = (String) jsonObject.get("PrescriptionID");
			String customerID = (String) jsonObject.get("CustomerID");
			String date = (String) jsonObject.get("Date");
			LocalDate dateToPrint = LocalDate.parse(date);

			ArrayList<Medication> medications = new ArrayList<>();

			JSONArray medicationsArray = (JSONArray) jsonObject.get("Medications");

			for (Object medObj : medicationsArray) {
				JSONObject medication = (JSONObject) medObj;

				String medicationID = (String) medication.get("id");
				Long defQuantity = (Long) medication.get("quantity");
				int quantity = defQuantity.intValue();
				
				String medicationName = (String) medication.get("name");
				
				medications.add(new Medication(medicationID, medicationName, quantity));
			}

			prescriptions.add(new Prescription(prescriptionID, customerID, doctorName, medications, dateToPrint));

		}
		return prescriptions;

	}

	public void deletePrescription(
			String prescriptionID) throws IOException, ParseException {
		JSONArray existingPrescriptions = fileHandler.readJSONArrayFromFile(true);
		int indexToDelete = -1;
		for (int i = 0; i < existingPrescriptions.size(); i++) {
			JSONObject jsonObject = (JSONObject) existingPrescriptions.get(i);
			String existingPrescriptionID = (String) jsonObject.get("PrescriptionID");
			if (existingPrescriptionID == prescriptionID) {
				indexToDelete = i;
				break;
			}
		}

		if (indexToDelete != -1) {
			existingPrescriptions.remove(indexToDelete);
			fileHandler.writeJSONArrayToFile(existingPrescriptions);
		}
	}

}
