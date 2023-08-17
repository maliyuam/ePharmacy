
// import java.io.BufferedReader;
// import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class FileHandler {
    String projectRoot = System.getProperty("user.dir");
    Path rawPrescriptionsPath = Paths.get(projectRoot, "..", "data", "prescriptions.json");
    Path rawProductsPath = Paths.get(projectRoot, "..", "data", "products.json");
    private String filePath = rawPrescriptionsPath.toString();
    private String productsPath = rawProductsPath.toString();

    public JSONArray readJSONArrayFromFile(Boolean def) throws IOException, ParseException {
        JSONParser parser = new JSONParser();
        try (FileReader fileReader = new FileReader(def ? filePath : productsPath)) {
            if (fileReader.read() == -1) {
                return new JSONArray();
            } else {
                fileReader.close();
                return (JSONArray) parser.parse(new FileReader(def ? filePath : productsPath));
            }
        } catch (IOException e) {
            System.err.println("Error while reading data from file: " + e.getMessage());
            return new JSONArray();
        }
    }

    public void writeJSONArrayToFile(JSONArray jsonArray) throws IOException {
        try (FileWriter fileWriter = new FileWriter(filePath)) {
            fileWriter.write(jsonArray.toJSONString());
            fileWriter.flush();
            System.out.println("Data written to " + filePath + " successfully!");
        } catch (IOException e) {
            System.out.println("Error while writing data to file: " + e.getMessage());
        }
    }
}