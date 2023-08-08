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
                    cin >> text;
                    cin.ignore();
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
                    cin >> text;
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
                    cin >> text;
                    cin.ignore();
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
                    cin >> text;
                    cin.ignore();
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
                    cin >> text;
                    cin.ignore();
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
        int i;
        int index = -1;

        for (i = 0; i < plist.size(); i++)
        {
            bool found = plist[i].compareCode(code);
            if (found == 1 || found == true)
            {
                product = std::make_unique<Product>(plist[i]);
                prod = plist[i];
                index = i;
                break;
            }
        }

        if (!product)
        {
            cout << "Product not found" << endl;
            return;
        }
        else
        {
            string newName;
            cout << "Enter new name:";
            getline(cin, newName);
            if (newName.size() == 0 || newName == "" || newName == " " || newName == "\n")
            {
                newName = prod.getName();
            }
            string newBrand;
            cout << "Enter new brand:";
            getline(cin, newBrand);
            if (newBrand.size() == 0 || newBrand == "" || newBrand == " " || newBrand == "\n")
            {
                newBrand = prod.getBrand();
            }
            string newCategory;
            cout << "Enter new category:";
            getline(cin, newCategory);
            if (newCategory.size() == 0 || newCategory == "" || newCategory == " " || newCategory == "\n")
            {
                newCategory = prod.getCategory();
            }
            string newDescription;
            cout << "Enter new description:";
            getline(cin, newDescription);
            if (newDescription.size() == 0 || newDescription == "" || newDescription == " " || newDescription == "\n")
            {
                newDescription = prod.getDecrisption();
            }
            string newPrice;
            float arrangedPrice;
            cout << "Enter new price:";
            getline(cin, newPrice);
            if (newPrice.size() == 0 || newPrice == "" || newPrice == " " || newPrice == "\n")
            {
                arrangedPrice = prod.getPrice();
            }
            else
            {
             
               cout<< "new price"<<newPrice<<endl;
                cout<< "old price"<<prod.getPrice()<<endl;
                cout<<"Testing"<< checkPrice(newPrice, prod.getPrice())<<endl;
                arrangedPrice = checkPrice(newPrice, prod.getPrice());

            }
            string newQuantity;
            int arrangedQuantity;
            cout << "Enter new quantity:";
            getline(cin, newQuantity);
            if (newQuantity.size() == 0 || newQuantity == "" || newQuantity == " " || newQuantity == "\n")
            {
                arrangedQuantity = prod.getQuantity();
            }
            else
            {

                arrangedQuantity = checkQuantity(newQuantity, prod.getQuantity());
            }
            string newDosageInstruction;
            cout << "Enter new dosage instruction:";
            getline(cin, newDosageInstruction);
            if (newDosageInstruction.size() == 0 || newDosageInstruction == "" || newDosageInstruction == " " || newDosageInstruction == "\n")
            {
                newDosageInstruction = prod.getDosageInstraction();
            }
            string newRequiresPrescription;
            bool arrangedPrescription;
            cout << "Enter new requires prescription(Y/N):";
            getline(cin, newRequiresPrescription);
            if (newRequiresPrescription.size() == 0 || newRequiresPrescription == "" || newRequiresPrescription == " " || newRequiresPrescription == "\n")
            {
                arrangedPrescription = prod.getRequiresPrescription();
            }
            else
            {
                arrangedPrescription = checkPrescription(newRequiresPrescription, prod.getRequiresPrescription());
            }
            string newExpiryDate;

            Product p(
                code, newName,
                newBrand,
                newDescription,
                arrangedPrice,
                newDosageInstruction,
                newCategory,
                arrangedPrescription,
                arrangedQuantity);

            plist[index] = p;
            fileHandler.updateFile(plist);
            cout << "Product updated successfully";
        }
    }
    float checkPrice(string price, float prodPrice)
    {
        float value;
        stringstream ss(price);

        if (ss >> value)
        {
            ss >> value;
            return value;
        }

        return prodPrice;
    }
    bool checkPrescription(string prescription, bool prodPrescription)
    {
        if (prescription == "true" || prescription == "True" || prescription == "Y" || prescription == "y" || prescription == "yes" || prescription == "Yes")
        {
            return true;
        }
        else if (prescription == "false" || prescription == "False" || prescription == "N" || prescription == "n" || prescription == "no" || prescription == "No")
        {
            return false;
        }
        else
        {
            return prodPrescription;
        }
    }

    int checkQuantity(string quantity, int prodQuantity)
    {

        int value;
        stringstream ss(quantity);

        if (ss >> value)
        {
            ss >> value;
            return value;
        }
        return prodQuantity;
    }

    void deleteProduct(string code)
    {
        vector<Product> plist = fileHandler.readJsonFile();
        int index = -1;
        for (int i = 0; i < plist.size(); i++)
        {
            bool found = plist[i].compareCode(code);
            if (found == 1 || found == true)
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
