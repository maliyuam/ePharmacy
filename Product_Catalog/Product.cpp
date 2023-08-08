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

    // TODO Add other attributes as needed
    string getCode(string token,bool trimQuotes = false)
    {
        // split the token string into an array of strings based on the colon
        vector<string> parts;
        stringstream ss(token);
        string part;
        while (getline(ss, part, ':'))
        {
            parts.push_back(part);
        }
        string code = parts[1];
        if(trimQuotes){
            code = code.substr(1,code.length()-2);
        }
        return code;
    }
 

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
        cin >> userInput;
        return userInput;
    }

    bool promptRequirePrescription()
    {
        cout << "Does this product require prescription? (Y/N):";
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

    void createProduct()
    {

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
        cout << this->price << endl;
        cout << this->quantity << endl;
        string productInJson;
        productInJson = "{\"code\":\"" + this->code + "\"," +
                        "\"name\":\"" + this->name + "\"," +
                        "\"brand\":\"" + this->brand + "\"," +
                        "\"description\":\"" + this->description + "\"," +
                        "\"dosage_instruction\":\"" + this->dosageInstruction + "\"," +
                        "\"price\":" + to_string(this->price) + "," +
                        "\"quantity\":" + to_string(this->quantity) + "," +
                        "\"category\":\"" + this->category + "\"," +
                        "\"requires_prescription\":" + to_string(this->requires_prescription) + "}";

        return productInJson;
    };

    void productFromJson(string txt)
    {
        //    eliminate the first and last character of the string
        txt = txt.substr(1, txt.length() - 2);
        // split the string into an array of strings based on the comma
        std::vector<std::string> tokens;
        std::stringstream ss(txt);
        std::string token;
        while (std::getline(ss, token, ','))
        {
            tokens.push_back(token);
        }
        // loop through the array of strings and split each string into an array of strings based on the colon
        this->code = this->getCode(tokens[0], true);
        this->name = this->getCode(tokens[1], true);
        this->brand = this->getCode(tokens[2], true);
        this->description = this->getCode(tokens[3], true);
        this->dosageInstruction = this->getCode(tokens[4], true);
        this->price = stof(this->getCode(tokens[5], false));
        this->quantity = stoi(this->getCode(tokens[6], false));
        this->category = this->getCode(tokens[7], true);
        this->requires_prescription = stoi(this->getCode(tokens[8], false)) == 1 ? true : false;
    };

    friend std::ostream &operator<<(std::ostream &os, const Product &product)
    {
        os << "Code: " << product.code << "\n";
        os << "Name: " << product.name << "\n";
        os << "Brand: " << product.brand << "\n";
        os << "Description: " << product.description << "\n";
        os << "Dosage Instruction: " << product.dosageInstruction << "\n";
        os << "Price: " << product.price << "\n";
        os << "Quantity: " << product.quantity << "\n";
        os << "Category: " << product.category << "\n";
        return os;
    };
};
