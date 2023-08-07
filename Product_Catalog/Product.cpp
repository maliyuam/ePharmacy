#include <iostream>
#include <string.h>
#include <string>
#include <chrono>
#include <random>

using namespace std;
using namespace std::chrono;

class Product
{

private:
    int quantity;
    string name;
    string brand;
    string description;
    string code;
    float price;
    string dosageInstruction;
    string category;
    bool requires_prescription;

public:
    string getName()
    {
        // TODO Add code that return the Product Name
        return this->name;
    }

    string getBrand()
    {
        // TODO Add code that return the Product Brand
        return this->brand;
    }

    string getDecrisption()
    {
        // TODO Add code that return the Product Description
        return this->description;
    }

    string getDosageInstraction()
    {
        // TODO Add code that return the Product Dosage Instruction
        return this->dosageInstruction;
    }

    string getCategory()
    {
        // TODO Add code that return the Product Category
        return this->category;
    }

    int getQuantity()
    {
        // TODO Add code that return the Product Quantity
        return this->quantity;
    }

    float getPrice()
    {
        return this->price;
    }

    bool getRequiresPrescription()
    {
        // TODO Add code that return Product Requires Prescription status
        return this->requires_prescription;
    }

    string generateUniqueCode()
    {
        string characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

        string uniqueCode = "";
        auto now = system_clock::now();
        auto millis = duration_cast<milliseconds>(now.time_since_epoch());
        mt19937 generator(millis.count());
        uniform_int_distribution<int> distribution(0, 100000);

        // generate 10 characters long unique string

        for (int i = 0; i <= 10; i++)
        {
            int random_index = distribution(generator) % characters.length();
            uniqueCode += characters[random_index];
        }

        return uniqueCode;
    };

    string promptTextField(string promptText)
    {
        cout << promptText << ":" << endl;
        string userInput;
        cin >> userInput;
        if (userInput.length() == 0)
        {
            cout << "Invalid Input. Please try again." << endl;
            promptTextField(promptText);
        }
        return userInput;
    }

    // create a function that handles the get input

    float promptNumberField(string promptText)
    {
        cout << promptText << ":" << endl;
        float userInput;
        // Performing input validation to check if user input is a number
        while (!(cin >> userInput))
        {
            cout << "Invalid Input. Please enter a number." << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
    }

    bool promptRequirePrescription()
    {
        cout << "Does this product require prescription? (Y/N):" ;
        string userInput;
        cin >> userInput;
        if (userInput == "Y" || userInput == "y")
        {
            return true;
        }
        else if (userInput == "N" || userInput == "n")
        {
            return false;
        }
        else
        {
            cout << "Invalid Input. Please try again." << endl;
            promptRequirePrescription();
        }
    }

    void createProduct(){

        // TODO Add code that calls promptTextField() method and prompt user for entering product name and update the name field.
        this->name = promptTextField("Enter product name");
        // TODO Add code that calls promptTextField() method and prompt user for entering product brand and update the brand field.
        this->brand = promptTextField("Enter product brand");
        // TODO Add code that calls promptTextField() method and prompt user for entering product description and update the decription field.
        this->description = promptTextField("Enter product description");
        // TODO Add code that calls promptTextField() method and prompt user for entering product category and update the category field.
        this->category = promptTextField("Enter product category");
        // TODO Add code that calls promptTextField() method and prompt user for entering product dosageInstruction and update the dosage instruction field.
        this->dosageInstruction = promptTextField("Enter product dosage instruction");
        // TODO Add code that calls promptNumberField() method and prompt user for entering product quantity and update the quantity field.
        this->quantity = promptNumberField("Enter product quantity");
        // TODO Add code that calls promptNumberField() method and prompt user for entering product price and update the price field.
        this->price = promptNumberField("Enter product price");
        // TODO Add code that calls promptRequirePrescription() method and prompt user for entering product requires presc and update the requiresprescription field.
        this->requires_prescription = promptRequirePrescription();
        // Add code to generate Unique code for product using generateUniqueCode method
        this->code = generateUniqueCode();

    };

    string toJson()
    {
        string productInJson;
        productInJson = "{\"code\":\"" + this->code + "\"," +
                        "\"name\":\"" + this->name + "\","+
                        "\"brand\":\"" + this->brand + "\","+
                        "\"description\":\""+this->description + "\","+
                        "\"dosage_instruction\":\""+this->dosageInstruction +"\""+
                        "\"price\":"+to_string(this->price)+","+
                        "\"quantity\":"+to_string(this->quantity)+","+
                        "\"category\":\""+this->category+"\","+
                        "\"requires_prescription\":"+to_string(this->requires_prescription)+"}";


        return productInJson;
    };

    void productFromJson(string txt){
        // TODO Add code that parses the json string and update the product object  
        this->code = txt.substr(txt.find("code")+7,txt.find(",")-txt.find("code")-8);
        this->name = txt.substr(txt.find("name")+7,txt.find(",")-txt.find("name")-8);
        this->brand = txt.substr(txt.find("brand")+8,txt.find(",")-txt.find("brand")-9);
        this->description = txt.substr(txt.find("description")+13,txt.find(",")-txt.find("description")-14);
        this->dosageInstruction = txt.substr(txt.find("dosage_instruction")+21,txt.find(",")-txt.find("dosage_instruction")-22);
        this->price = stof(txt.substr(txt.find("price")+7,txt.find(",")-txt.find("price")-8));
        this->quantity = stoi(txt.substr(txt.find("quantity")+10,txt.find(",")-txt.find("quantity")-11));
        this->category = txt.substr(txt.find("category")+10,txt.find(",")-txt.find("category")-11);
        this->requires_prescription = txt.substr(txt.find("requires_prescription")+23,txt.find("}")-txt.find("requires_prescription")-24) == "true" ? true : false;
        

    };
};
