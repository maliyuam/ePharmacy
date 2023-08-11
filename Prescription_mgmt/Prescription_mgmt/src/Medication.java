public class Medication {

   private String ID;
   private String name;
   private String details;
   private String dosage;
   private int quantity;
   private Boolean processedStatus;

   public Medication() {
      this.processedStatus = false;
   }

   public Medication(String _id, String _name, int qty) {
      this.ID = _id;
      this.name = _name;
      this.quantity = qty;
      this.processedStatus = false;
   }

   public Medication(String _id, String _name, String _details, String _dosage, int qty) {
      this.ID = _id;
      this.name = _name;
      this.details = _details;
      this.dosage = _dosage;
      this.quantity = qty;
      this.processedStatus = false;
   }

   public String getID() {
      return this.ID;
   }

   public String getName() {
      return this.name;
   }

   public String getDetails() {
      return this.details;
   }

   public String getDosage() {
      return this.dosage;
   }

   public int getQuantity() {
      return this.quantity;
   }

   public Boolean getProcessedStatus() {
      return this.processedStatus;
   }
   // creating the setters

   public void setName(String _name) {
      this.name = _name;
   }

   public void setDetails(String _details) {
      this.details = _details;
   }

   public void setDosage(String _dosage) {
      this.dosage = _dosage;
   }

   public void setQuantity(int qty) {
      this.quantity = qty;
   }

   public void setProcessedStatus(Boolean _processedStatus) {
      this.processedStatus = _processedStatus;
   }

   public String toString() {
      return this.ID + "," + this.name + "," + this.quantity + "," + this.processedStatus;
   }
}