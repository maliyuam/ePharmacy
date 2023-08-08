#include "SearchProduct.cpp"

class ProductManager
{
private:
    Product prod;
    FileHandler fileHandler;

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
            cout << "7. Delete Product" << endl;
            cout << "Enter Your choice:";

            string input;
            cin >> input;
            try
            {
                choice = std::stoi(input);
                validInput = true;
                switch (choice)
                {
                case 1:
                    cout << "Adding Product Initiated...." << endl;
                    this->addProduct();
                    break;
                case 2:
                    cout << "search Product initiated.....";
                    break;
                case 3:
                    cout << "search Product initiated.....";
                    break;
                case 4:
                    cout << "search Product initiated.....";
                    break;
                case 5:
                    cout << "Update Product.....";
                    break;
                case 6:
                    cout << "Update Product initiated.....";
                    break;
                case 7:
                    cout << "Delete Product initiated.....";
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
    Product updateProduct()
    {
    }
    void deleteProduct(string code)
    {
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
