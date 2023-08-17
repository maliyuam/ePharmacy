#include <sstream>
#include <vector>
#include <string.h>
#include <fstream>
#include <stdio.h>

// Importing Product class
#include "Product.cpp"
#include <filesystem> // Include the filesystem library
namespace fs = std::filesystem;

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
            //  std::cout << "Current Directory: " <<  << std::endl;
            fs::path currentDir = fs::current_path();
            fs::path parentDir = currentDir.parent_path();
            std::cout << "Parent Directory: " << parentDir << std::endl;
            string name = parentDir.string() + "/data/products.json";
            filename = name.c_str();
            // printf("File name: %s", filename.c_str());
        }

        ifstream prodsFile(filename);
        if (!prodsFile.is_open())
        {
            std::cerr << "Error opening file: " << filename << std::endl;
            return prodList;
        }
        else
        {
            cout << "File opened" << endl;
            // cout<<"FileData: "<<prodsFile<<endl;
        }

        if (!prodsFile.good())
        {
            cerr << "File is empty or unreadable" << endl;
            return prodList;
        }
        else{
            cout<<"File is readable"<<endl;
        }

        while (getline(prodsFile, prodLine))
        {
            prodLines.push_back(prodLine);

            if (prodLine.substr(0, 1) == "{")
            {

                manProd.productFromJson(prodLine);
                cout << manProd << endl;
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
            jsonFile << pList[i].toJson();
            if (i != pList.size() - 1)
            {
                jsonFile << "," << endl;
            }
            else
            {
                jsonFile << endl;
            }
        }
        jsonFile << "]" << endl;
        jsonFile.close();
    }
    void updateFile(vector<Product> pList)
    {
        vector<Product> dList;
        dList = readJsonFile();
        // pList.push_back(p);
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
            jsonFile << pList[i].toJson();
            if (i != pList.size() - 1)
            {
                jsonFile << "," << endl;
            }
            else
            {
                jsonFile << endl;
            }
        }
        jsonFile << "]" << endl;
        jsonFile.close();
    }
    void setProductFile(string filename)
    {
        this->filename = filename;
    }
};
