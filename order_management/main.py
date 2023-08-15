#!/usr/bin/python3
import os
from order_management import (
    UserManagement,
    Stock,
    Cart,
    Wrapper,
    Menu,
    BookRecords,
    
)

if __name__ == '__main__':
    # files path declaration
    current_folder = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.abspath(os.path.join(current_folder, '../data')) 
    credentials_file = os.path.join(data_folder, 'credentials.txt')
    stock_file = file_name = os.path.join(data_folder, 'products.json')
    sales_file =file_name = os.path.join(data_folder, 'sales.json')
    prescription_file = file_name = os.path.join(data_folder, 'prescriptions.json')
    login_creds = os.path.join(data_folder, '.logged_in')

    # load the user management file
    profiles = UserManagement.load(credentials_file)

    # get the logged in user
    pharmacist = profiles.get_logged_in_user()
    # make sure the logged in user is a pharmacist/salesperson
    assert (pharmacist.role == 'salesperson' or pharmacist.role == 'pharmacist'), 'You are not allowed to access this feature.'

    # load the resources that we need
    stock = Stock.load(stock_file)
    cart = Cart(stock=stock)

    wrap = Wrapper(stock, pharmacist.username)
    books = BookRecords.load(sales_file)

    # create an instance of the menu
    menu = Menu(stock, profiles, pharmacist, sales_file,
                prescription_file, stock_file)


    while True:
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.]")
        print("*******************************************")
        print("1. Order Management")
        print("2. Get Analytics")
        print("0. Back")
        choice = int(input("Enter your choice: "))
        os.system('cls')
        match choice:
            case 1:
                menu.handle_orders()
            case 2:
                menu.handle_analytics()
            case 0:
                print("Exiting...")
                exit()
            case default:
                print("Invalid choice. Try again.")
                continue


        
