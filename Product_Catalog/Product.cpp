#include <iostream>
#include <string.h>
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
        return name;
    }

    string getBrand()
    {
        // TODO Add code that return the Product Brand
        return brand;
    }

    string getDecrisption()
    {
        // TODO Add code that return the Product Description
        return description;
    }

    string getDosageInstraction()
    {
        // TODO Add code that return the Product Dosage Instruction
        return dosageInstruction;
    }

    string getCategory()
    {
        // TODO Add code that return the Product Category
        return category;
    }

    int getQuantity()
    {
        // TODO Add code that return the Product Quantity
        return quantity;
    }

    float getPrice()
    {
        return price;
    }

    bool getRequiresPrescription()
    {
        // TODO Add code that return Product Requires Prescription status
        return requires_prescription;
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
        // TODO Add code that calls promptTextField() method and prompt user for entering product brand and update the brand field.
        // TODO Add code that calls promptTextField() method and prompt user for entering product description and update the decription field.
        // TODO Add code that calls promptTextField() method and prompt user for entering product category and update the category field.
        // TODO Add code that calls promptTextField() method and prompt user for entering product dosageInstruction and update the dosage instruction field.
        // TODO Add code that calls promptNumberField() method and prompt user for entering product quantity and update the quantity field.
        // TODO Add code that calls promptNumberField() method and prompt user for entering product price and update the price field.
        // TODO Add code that calls promptRequirePrescription() method and prompt user for entering product requires presc and update the requiresprescription field.

        // Add code to generate Unique code for product using generateUniqueCode method

    };

    string toJson()
    {

        string productInJson;

        // TODO Add code for converting a product to json form from the private declared attributes.
        // The Output should look like:
        //{"code":"tgtwdNbCnwx","name":"name 1","brand":"br 2","description":"df","dosage_instruction":"dfg","price":123.000000,"quantity":13,"category":"des","requires_prescription":1}

        return productInJson;
    };

    void productFromJson(string txt){
        // TODO Add code to convert a json string product to product object
        //  string is in the form below
        //{"code":"tgtwdNbCnwx","name":"name 1","brand":"br 2","description":"df","dosage_instruction":"dfg","price":123.000000,"quantity":13,"category":"des","requires_prescription":1}
        //  You need to extract value for each field and update private attributes declared above.

    };
};
