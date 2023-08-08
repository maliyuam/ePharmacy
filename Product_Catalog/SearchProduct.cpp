#include "FileHandler.cpp"
#include <regex>

class SearchProduct
{
private:
    string filename;

public:
    string searchText;
    FileHandler fHandler;

    string to_lowercase(const string &text)
    {
        string lowercase_text;
        for (char c : text)
        {
            lowercase_text += tolower(c);
        }
        return lowercase_text;
    }

    vector<Product> searchByName(string name)
    {
        this->searchText = this->to_lowercase(name);
        vector<Product> plist = fHandler.readJsonFile();
        vector<Product> foundProducts;
        regex pattern(".*" + this->searchText + ".*", std::regex_constants::icase);
        for (Product p : plist)
        {
            string prodName = this->to_lowercase(p.getName());
            if (regex_search(prodName, pattern))
            {
                foundProducts.push_back(p);
            }
        }
        return foundProducts;
    };

    vector<Product> searchByCategory(string categ)
    {
        this->searchText = this->to_lowercase(categ);
        vector<Product> plist = fHandler.readJsonFile();
        vector<Product> foundProducts;
        regex pattern(".*" + this->searchText + ".*", std::regex_constants::icase);
        for (Product p : plist)
        {
            string category = this->to_lowercase(p.getCategory());
            if (regex_search(category, pattern))
            {
                foundProducts.push_back(p);
            }
        }
        return foundProducts;
    };

    vector<Product> searchByBrand(string brand)
    {
        this->searchText = this->to_lowercase(brand);
        vector<Product> plist = fHandler.readJsonFile();
        vector<Product> foundProducts;
        regex pattern(".*" + this->searchText + ".*", std::regex_constants::icase);
        for (Product p : plist)
        {
            string brandName = this->to_lowercase(p.getBrand());
            if (regex_search(brandName, pattern))
            {
                foundProducts.push_back(p);
            }
        }
        return foundProducts;
    };

    void showSearchResult(vector<Product> plist, string sTxt)
    { 
        cout<<"------------------------------------------------------------------------------------------------------------------"<<endl;
        cout << "Search Result for " << sTxt << " returned " << plist.size() << " matching items"<<endl;
        cout<<"------------------------------------------------------------------------------------------------------------------"<<endl;
        for (Product p : plist)
        {
            cout << p;
        }
    }
};