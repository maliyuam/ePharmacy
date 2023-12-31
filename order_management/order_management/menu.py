from . import Stock, Cart, User, UserManagement, BookRecords, Wrapper, Prescription, Wrapper
import os
MSG_WRONG_INPUT = "Wrong input. Try again!"


class Menu:
    """Represents the menu class for the project

    Attributes: 
        stock: stock variable
        profiles: user management module
        pharmacist: account of the salesperson
        records_file: path to the file containing the sales
        prescriptions_file: path to the file containing the prescriptions.
        stock_file: path to the file containing the stock data
    """

    def __init__(self, stock: Stock, profiles: UserManagement, pharmacist: User, records_file: str, prescriptions_file: str, stock_file: str, wrapper: Wrapper) -> None:
        self.stock = stock
        self.profiles = profiles
        self.pharmacist = pharmacist
        self.cart = Cart(stock=stock)
        # use the file instead of the object so that we can keep track
        self.records_file = records_file
        self.prescriptions_file = prescriptions_file
        self.stock_file = stock_file
        self.wrapper = wrapper
        self.analytic = None

    # TODO: Create all the necessary functions/method to create and manage the menu using the
    # available variables and all the attributes of the class

    # Make sure to dump the prescriptions, stock, and sale data after every sale.
    def handle_orders(self) -> None:
        while True:
            print("*******************************************")
            print("Order Management and Analytics Menu")
            print("[loc:.order]")
            print("*******************************************")
            print("1. Add to cart")
            print("2. Remove from cart")
            print("3. Clear cart")
            print("4. Checkout")
            print("5. Back")
            choice = int(input("Enter your choice: "))
            os.system("clear")

            match choice:
                case 1:
                    self.handle_add_to_cart()
                case 2:
                    self.handle_remove_from_cart()
                case 3:
                    self.handle_cart_clear()  # self.handle_clear_cart()
                case 4:
                    self.handle_checkout()
                case 5:
                    os.system("clear")
                    break
                case defaut:
                    print(MSG_WRONG_INPUT)

    def handle_analytics(self) -> None:
        try:
            self.analytic = BookRecords.load(self.records_file)
            # records = BookRecords(self.records_file)
            while True:
                print("*******************************************")
                print("Order Management and Analytics Menu")
                print("[loc:.analytics]")
                print("*******************************************")
                print("1. Total income from purchases")
                print("2. Prescription statistics")
                print("3. Purchases for a user")
                print("4. Sales by an agent")
                print("5. Top sales")
                print("6. Back")
                choice = int(input("Enter your choice: "))
                os.system("clear")
                match choice:
                    case 1:
                        self.handle_total_income()
                    case 2:
                        self.handle_prescription_stats()
                    case 3:
                        self.handle_user_purchases()
                    case 4:
                        self.handle_agent_sales()
                    case 5:
                        self.handle_top_sales()
                    case 6:
                        os.system("clear")
                        break
                    case defaut:
                        print(MSG_WRONG_INPUT)
        except Exception as e:
            print(e)

    def handle_add_to_cart(self) -> None:
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.order.addToCart]")
        print("*******************************************")
        print("-"*176)
        print(f"|{'ID':<5}|{'Name':^20}|{'Brand':^20}|{'Description':^20}|{'Quantity':^20}|{'Price':^20}|{'Dosage':^20}|{'Prescription':^20}| {'Category':^20}|")
        print("-"*176)
        for i in range(len(self.stock.products)):
            print("|", i+1, " ", self.stock.products[i])
            print("_"*176)

        choice = int(input("Enter your choice: "))
        quantity = int(input("Enter quantity: "))
        if choice < 1 or choice > len(self.stock.products):
            os.system("clear")
            print("Wrong choice...")
            return
        if quantity > self.stock.products[choice-1].quantity:
            print("Insufficient stock")
            os.system("clear")
            return
        try:
            self.cart.add(self.stock.products[choice-1].code, quantity)
            print("Added to cart...")
            os.system("clear")
        except Exception as e:
            print(e)
        except ValueError as e:
            print(e)

    def handle_remove_from_cart(self) -> None:
        if len(self.cart.products) == 0:
            print("Cart is empty...")
            return
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.order.removeFromCart]")
        print("*******************************************")
        print("-"*80)
        print(self.cart.__str__())
        print("-"*80)
        choice = str(input("Enter the corresponding product code: "))
        try:
            self.cart.remove(choice)
            os.system("clear")
            print("Removed from cart...")
            print("Cart Content:", self.cart)
        except Exception as e:
            print(e)
        except ValueError as e:
            print(e)

    def handle_cart_clear(self) -> None:
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.order.clearCart]")
        print("*******************************************")
        print("Are you sure you want to clear the cart?")
        print("1. Yes")
        print("2. No")
        print("3. Back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            self.cart.clear()
            print("Cart cleared...")
            os.system("clear")
        elif choice == 2:
            os.system("clear")
            return
        elif choice == 3:
            os.system("clear")
            return
        else:
            os.system("clear")
            print(MSG_WRONG_INPUT)

    def handle_checkout(self) -> None:
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.order.checkout]")
        print("*******************************************")
        if len(self.cart.products) == 0:
            print("Cart is empty...")
            return
        print(
            f"|{'ID':^10} | {'Username':^20} | {'Full Name':^20} | {'Role':^20} | {'Logged in':^20}|")
        print("-"*110)
        for i, user in enumerate(self.profiles.users):
            print(f'| {i+1:^9} | {user.__str__()}|')
            print("-"*110)
        try:

            choice = int(input("Enter the corresponding user : "))
            user = self.profiles.users[choice-1]
            prescription = Prescription.get(
                infile=self.prescriptions_file, id=user.username)

            self.wrapper.checkout(self.cart, user.username, prescription)
            self.cart.clear()
            os.system("clear")
            print("Checkout successful...")
        except Exception as e:
            print(e)

    def handle_total_income(self) -> None:
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.analytics.totalIncome]")
        print("*******************************************")
        print("Total income:", self.analytic.totalTransactions(), "RWF")
        print("\n\n")

    def handle_prescription_stats(self) -> None:
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.analytics.prescriptionStats]")
        print("PRSCRIPTION STATISTICS")
        print("*******************************************")
        print(self.analytic.reportOnPrescriptions())

    def handle_user_purchases(self) -> None:
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.analytics.userPurchases]")
        print("*******************************************")
        print(
            f"|{'ID':^10} | {'Username':^20} | {'Full Name':^20} | {'Role':^20} | {'Logged in':^20}|")
        print("-"*110)
        for i, user in enumerate(self.profiles.users):
            print(f'| {i+1:^9} | {user.__str__()}|')
            print("-"*110)

        try:
            choice = int(input("Enter the corresponding user ID: "))
            user = self.profiles.users[choice-1]
            os.system("clear")
            print("Purchases for user:", user.username)
            print("-"*160)

            print(self.analytic.purchasesByUser(user.username))
        except Exception as e:
            print(e)

    def handle_agent_sales(self):
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.analytics.agentSales]")
        print("*******************************************")
        print("-"*105)
        print(
            f"|{'ID':^10} | {'Username':^20} | {'Full Name':^20} | {'Role':^20} | {'Logged in':^20}|")
        print("-"*105)
        for i, user in enumerate(self.profiles.users):
            print(f'| {i+1:^9} | {user.__str__()}|')
            print("_"*105)
        try:
            choice = int(input("Enter the corresponding user ID: "))
            user = self.profiles.users[choice-1]
            if user.role.strip() != 'salesperson' and user.role.strip() != 'pharmacist':
                print("User is not a salesperson or a pharmacist")
                return
            os.system("clear")
            print("Sales by agent:", user.username)
            print(self.analytic.salesByAgent(user.username))
        except Exception as e:
            print(e)

    def handle_top_sales(self):
        print("*******************************************")
        print("Order Management and Analytics Menu")
        print("[loc:.analytics.topSales]")
        print("*******************************************")
        print("Top sales:")
        try:
            print(self.analytic.topNSales())
        except Exception as e:
            print(e)
    # Your menu should have two main options with suboptions. Such as
    """
    1. Order management
        1.1. Adding to a cart (you need to show the list of products and ask the user to select one with ID. Bonus: Can you display with numbers and ask user to choose a number instead?
                Also ask for quantity.)
        1.2. Remove from a cart (display the cart and ask the user to select the element to remove. Remove by ID or by index (bonus))
        1.3. Clear the cart (self explanatory)
        1.4. Checkout (displays the cart with the total and ask for a prescription element. Proceed to checkout and show a message is successful or not).
    2. Analytics
        2.1. Total income from purchases
        2.2. Prescription statistics
        2.3. Purchases for a user
        2.4. Sales by an agent
        2.5. Top sales

    * For each of the menu items, when necessary, display a success or error message to guide the user.
    """

    # **CHALLENGE** (BONUS): Can you implement the menu to work as a USSD application? Implement and show your design
