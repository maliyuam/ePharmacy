#include "SearchProduct.cpp"

class ProductManager
{
private:
    Product prod;
    FileHandler fileHandler;
    SearchProduct searchProduct;

public:
    int getMenu()
    {
        int choice;
        bool validInput = false;

        while (!validInput)
        {
            cout << "1. Add Product" << endl;
            cout << "2. Search Product By Name" << endl;
            cout << "3. Search Product By Category" << endl;
            cout << "4. Search Product By Brand" << endl;
            cout << "5. Update Product" << endl;
            cout << "6. Delete Product" << endl;
            cout << "Enter Your choice:";

            string input;
            cin >> input;
            try
            {
                choice = std::stoi(input);
                validInput = true;
                string text;
                switch (choice)
                {
                case 1:
                    cout << "Adding Product Initiated...." << endl;
                    this->addProduct();
                    break;
                case 2:
                    cout << "Search Product By Name initiated.....\n";
                    cout << "Enter Product Name:";
                    getline(cin, text);
                    if (text.size() == 0)
                    {
                        cout << "Please enter name to search";
                        return 1;
                    }
                    else
                    {
                        searchProduct.showSearchResult(searchProduct.searchByName(text), text);
                    }
                    break;
                case 3:
                    cout << "Search Product By Category initiated.....";
                    cout << "Enter Required category:";
                    getline(cin, text);
                    if (text.size() == 0)
                    {
                        cout << "Please enter category to search";
                        return 1;
                    }
                    else
                    {
                        searchProduct.showSearchResult(searchProduct.searchByCategory(text), text);
                    }
                    break;
                case 4:
                    cout << "Search Product By Brand initiated.....";
                    cout << "Enter Required brand:";
                    getline(cin, text);
                    if (text.size() == 0)
                    {
                        cout << "Please enter category to search";
                        return 1;
                    }
                    else
                    {
                        searchProduct.showSearchResult(searchProduct.searchByBrand(text), text);
                    }
                    break;
                case 5:
                    cout << "Update Product....." << endl;
                    cout << "Enter Product Code:";
                    getline(cin, text);
                    if (text.size() == 0)
                    {
                        cout << "Please enter code to update";
                        return 1;
                    }
                    else
                    {
                        this->updateProduct(text);
                    }

                    break;
                case 6:
                    cout << "Delete Product initiated....." << endl;
                    cout << "Enter Product Code:";
                    getline(cin, text);
                    if (text.size() == 0)
                    {
                        cout << "Please enter code to delete";
                        return 1;
                    }
                    else
                    {
                        this->deleteProduct(text);
                    }
                    break;

                default:
                    break;
                }
            }
            catch (const std::invalid_argument &e)
            {
                cout << "Invalid input. Please enter an integer." << &e << endl;
            }
        }

        return 0;
    }

    void addProduct()
    {
        this->prod.createProduct();
        this->fileHandler.saveToJsonFile(this->prod);
    }

    void updateProduct(string code)
    {
        vector<Product> plist = fileHandler.readJsonFile();
        std::unique_ptr<Product> product = nullptr;
        for (Product p : plist)
        {
            if (p.compareCode(code))
            {
                prod = p;
                break;
            }
        }

        if (!product)
        {
            cout << "Product not found";
            return;
        }
        else
        {
            string newName;
            cout << "Enter new name:";
            getline(cin, newName);
            string newBrand;
            cout << "Enter new brand:";
            getline(cin, newBrand);
            string newCategory;
            cout << "Enter new category:";
            getline(cin, newCategory);
            string newDescription;
            cout << "Enter new description:";
            getline(cin, newDescription);
            string newPrice;
            cout << "Enter new price:";
            getline(cin, newPrice);
            string newQuantity;
            cout << "Enter new quantity:";
            getline(cin, newQuantity);
            string newDosageInstruction;
            cout << "Enter new dosage instruction:";
            getline(cin, newDosageInstruction);
            string newRequiresPrescription;
            cout << "Enter new requires prescription:";
            getline(cin, newRequiresPrescription);
            string newExpiryDate;

            Product p((newName.size() == 0) ? prod.getName() : newName,
                      (newBrand.size() == 0) ? prod.getBrand() : newBrand,
                      (newDescription.size() == 0) ? prod.getDecrisption() : newDescription,
                      checkPrice(newPrice, prod.getPrice()),
                      (newDosageInstruction.size() == 0) ? prod.getDosageInstraction() : newDosageInstruction,
                      (newCategory.size() == 0) ? prod.getCategory() : newCategory,
                      checkPrescription(newRequiresPrescription, prod.getRequiresPrescription()),
                      checkQuantity(newQuantity, prod.getQuantity()));

            // check to see product in plist with same code then update
            // else return product not found
            int index = -1;
            for (int i = 0; i < plist.size(); i++)
            {
                if (plist[i].compareCode(code))
                {
                    index = i;
                    break;
                }
            }
            if (index != -1)
            {
                plist[index] = p;
                fileHandler.updateFile(plist);
                cout << "Product updated successfully";
            }
            else
            {
                cout << "Product not found";
            }
        }
    }
    float checkPrice(string price, float prodPrice)
    {
        try
        {
            return std::stof(price);
        }
        catch (const std::invalid_argument &e)
        {
            cout << "Invalid input. Please enter an integer." << &e << endl;
            return prodPrice;
        }
    }
    bool checkPrescription(string prescription, bool prodPrescription)
    {
        if (prescription == "true")
        {
            return true;
        }
        else if (prescription == "false")
        {
            return false;
        }
        else
        {
            cout << "Invalid input. Please enter true or false." << endl;
            return prodPrescription;
        }
    }

    int checkQuantity(string quantity, int prodQuantity)
    {
        try
        {
            return std::stoi(quantity);
        }
        catch (const std::invalid_argument &e)
        {
            cout << "Invalid input. Please enter an integer." << &e << endl;
            return prodQuantity;
        }
    }

    void deleteProduct(string code)
    {
        vector<Product> plist = fileHandler.readJsonFile();
        int index = -1;
        for (int i = 0; i < plist.size(); i++)
        {
            if (plist[i].compareCode(code))
            {
                index = i;
                break;
            }
        }
        if (index != -1)
        {
            plist.erase(plist.begin() + index);
            fileHandler.updateFile(plist);
            cout << "Product deleted successfully";
        }
        else
        {
            cout << "Product not found";
        }
    }
};

int main()
{
    ProductManager manager;

    while (true)
    {
        manager.getMenu();
    }

    return 0;
}
