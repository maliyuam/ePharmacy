#include <sstream>
#include <vector>
#include <string.h>
#include <fstream>
#include <stdio.h>

// Importing Product class
#include "Product.cpp"

using namespace std;

class FileHandler
{
public:
    string filename;

    vector<Product> readJsonFile()
    {

        // Add code here
        vector<Product> prodList;
        vector<string> prodLines;
        string prodLine;
        Product manProd;

        if (filename.empty())
        {
            filename = "data/products.json";
        }
        ifstream prodsFile(filename);

        while (getline(prodsFile, prodLine))
        {
            prodLines.push_back(prodLine);

            if (prodLine.substr(0, 1) == "{")
            {
                manProd.productFromJson(prodLine);
                cout<<"PRODUCT DATA:"<< manProd<<endl;
                prodList.push_back(manProd);
            }
        }
        prodsFile.close();
        return prodList;
    };

    void saveToJsonFile(Product p)
    {
        // Add code here
        vector<Product> pList;

        pList = readJsonFile();

        pList.push_back(p);

        int ret = remove(filename.c_str());
        if (ret != 0)
        {
            std::cout << "Error deleting file: " << strerror(errno) << "\n";
            return;
        }

        ofstream jsonFile(filename);
        jsonFile << "[" << endl;
        for (int i = 0; i < pList.size(); i++)
        {
            jsonFile << pList[i].toJson()<<"\n";
            Product p ;
            p.productFromJson(pList[i].toJson());
            cout<<"PRODUCT DATA:"<< p<<endl;
            
            if (i != pList.size() - 1)
            {
                jsonFile << "," << endl;
            }
        }
        jsonFile << "]" << endl;
        jsonFile.close();
    }
};