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
    string getCode(string token, bool trimQuotes = false)
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
        if (trimQuotes)
        {
            code = code.substr(1, code.length() - 2);
        }
        return code;
    }

public:
    Product()
    {
    }
    Product(
        string name,
        string brand,
        string description,
        float price,
        string dosageInstruction,
        string category,
        bool requires_prescription,
        int quantity)
    {
        this->name = name;
        this->brand = brand;
        this->description = description;
        this->price = price;
        this->dosageInstruction = dosageInstruction;
        this->category = category;
        this->requires_prescription = requires_prescription;
        this->quantity = quantity;
    }

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

    bool compareCode(string code)
    {
        // TODO Add code that return true if the code matches the product code
        return this->code == code;
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
        getline(cin, userInput);
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
            cout << "Invalid Input. Please try again." << endl;
            cin.clear();
            cin.ignore(123, '\n');
            cout << promptText << ":" << endl;
        }
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
        return false;

    };

    void createProduct()
    {
        this->name = promptTextField("Enter product name");
        this->brand = promptTextField("Enter product brand");
        this->description = promptTextField("Enter product description");
        this->category = promptTextField("Enter product category");
        this->dosageInstruction = promptTextField("Enter product dosage instruction");
        this->quantity = promptNumberField("Enter product quantity");
        this->price = promptNumberField("Enter product price");
        this->requires_prescription = promptRequirePrescription();
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
        txt = txt.substr(1, txt.length() - 2);
        std::vector<std::string> tokens;
        std::stringstream ss(txt);
        std::string token;
        while (std::getline(ss, token, ','))
        {
            tokens.push_back(token);
        }
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
        os << "Code: " << product.code << " || ";
        os << "Name: " << product.name << " || ";
        os << "Brand: " << product.brand << " || ";
        os << "Description: " << product.description << " || ";
        os << "Dosage Instruction: " << product.dosageInstruction << " || ";
        os << "Price: " << product.price << " || ";
        os << "Quantity: " << product.quantity << " || ";
        os << "Category: " << product.category << " ||";
        os << "Requires Prescription: " << product.requires_prescription << " || \n";

        return os;
    };
};
