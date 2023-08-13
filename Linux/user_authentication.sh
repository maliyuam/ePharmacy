#!/bin/bash

credentials_file="../data/credentials.txt"
login_data_file="../data/.logged_in"
credentials_path="../data"
# Function to prompt for credentials
get_login_credentials() {
    read -p "Enter username: " user
    read -sp "Enter password: " pass
    echo -e "\n"
    return 0
}

# Function to generate a salted hash of the password
hash_password() {
    local salt=$(openssl rand -hex 8)
    local hashed_pass=$(echo -n "$1$salt" | sha256sum | awk '{print $1}')
    echo "$hashed_pass:$salt"
}

# Function to register new credentials
register_credentials() {
    local role=""
    local genPass="0"
    # check that parameter one is not empty
    if [[ -z "$1" ]]; then
        role="customer"
    else
        role="$1"
        local genPass="1"
    fi
    read -p "Enter name: " name
    read -p "Enter username: " user
    read -sp "Enter password: " pass
    echo -e "\n"
    read -sp "Confirm password: " confirm_pass
    local line=$(grep "^$user:" "$credentials_file")
    if [[ -n "$line" ]]; then
        echo -e "\nThe username already exists. Please try again with a different username.\n"
        return 1
    else
        echo -e "\n Username is available."
    fi
    if [[ "$pass" != "$confirm_pass" ]]; then
        echo -e "\nPasswords do not match. Please try again.\n"
        echo "1. Retry"
        echo "2. Exit"
        echo -n "Enter your choice: "
        read choice
        case $choice in
        1)
            register_credentials
            ;;
        2)
            exit 0
            ;;
        *)
            echo "Invalid choice. Exiting the application..."
            exit 1
            ;;
        esac
    else
        if [[ ! -f "$credentials_file" ]]; then
            echo "Please wait creating credentials file..."
            mkdir -p "$credentials_path"
            touch "$credentials_file"
        fi
        echo -e "\n"
        local pass=$(hash_password "$pass")
        local hashed_pass=$(echo "$pass" | cut -d ':' -f 1)
        local salt=$(echo "$pass" | cut -d ':' -f 2)
        echo -e "Registration successful. You can now log in.\n"
        echo -e "$user:$hashed_pass:$salt:$name:$role:0:$genPass" >>"$credentials_file"
    fi
}

generte_user_id() {
    generated_id=$(date +%Y%m%d%H%M%S%N)-$$
    return 0
}

# Function to verify credentials and privileges
verify_credentials() {
    if [[ ! -f "$credentials_file" ]]; then
        echo "Please wait creating credentials file..."
        mkdir -p "$credentials_path"
        touch "$credentials_file"
    fi

    local user=$1
    local pass=$2

    echo "Verifying credentials..."

    local stored_cred=$(grep "^$user:" "$credentials_file" | cut -d ':' -f 2-)
    if [[ -n "$stored_cred" ]]; then
        local stored_pass=$(echo "$stored_cred" | cut -d ':' -f 1)
        local salt=$(echo "$stored_cred" | cut -d ':' -f 2)
        local hashed_pass=$(echo -n "$pass$salt" | sha256sum | awk '{print $1}')
        local login_status=$(echo "$stored_cred" | cut -d ':' -f 5)
        local createPassword=$(echo "$stored_cred" | cut -d ':' -f 6)
        echo "The status $createPassword"
        if [[ "$createPassword" == "1" ]]; then
            # request user to change password
            echo "Please change your password"
            read -sp "Enter password: " nPass
            echo -e "\n"
            read -sp "Confirm password: " nConf
            if [[ "$nPass" != "$nConf" ]]; then
                echo "Password do not match. Please try again"
                return
            else
                local newpass=$(hash_password "$nPass")
                local hashed_passed=$(echo "$newpass" | cut -d ':' -f 1)
                local salt=$(echo "$newpass" | cut -d ':' -f 2)
                local liner=$(grep "^$user:" "$credentials_file")
                updated_liner=$(echo "$liner" | awk 'BEGIN{FS=OFS=":"} {$2="'${hashed_passed}'"; print}')
                updated_liner=$(echo "$updated_liner" | awk 'BEGIN{FS=OFS=":"} {$3="'${salt}'"; print}')
                updated_liner=$(echo "$updated_liner" | awk 'BEGIN{FS=OFS=":"} {$6="1"; print}')
                updated_liner=$(echo "$updated_liner" | awk 'BEGIN{FS=OFS=":"} {$7="0"; print}')
                sed -i "s~$liner~$updated_liner~" "$credentials_file"
                echo "$user" >"$login_data_file"
                echo "Password changed successfully"
                local role=$(echo "$stored_cred" | cut -d ':' -f 4)
                if [[ "$role" == "admin" ]]; then
                    echo "$line"
                    admin_menu "$line"
                elif [[ "$role" == "customer" ]]; then
                    echo "Calling Customer menu"
                    customer_menu "$line"
                elif [[ "$role" == "pharmacist" ]]; then
                    echo "Calling Parmasist menu"
                    pharmasist_menu "$line"
                else
                    echo "The role is not defined. Exiting the application...."
                    logout_user
                    exit 0
                fi

            fi

        else
            if [[ "$stored_pass" == "$hashed_pass" ]]; then
                echo "Login successful"
                local line=$(grep "^$user:" "$credentials_file")
                if [[ "$login_status" == "0" ]]; then
                    updated_line=$(echo "$line" | awk 'BEGIN{FS=OFS=":"} {$6="1"; print}')
                    sed -i "s~$line~$updated_line~" "$credentials_file"
                    echo "$user" >"$login_data_file"
                fi
                local role=$(echo "$stored_cred" | cut -d ':' -f 4)
                if [[ "$role" == "admin" ]]; then
                    echo "$line"
                    admin_menu "$line"
                elif [[ "$role" == "customer" ]]; then
                    echo "Calling Customer menu"
                    customer_menu "$line"
                elif [[ "$role" == "pharmacist" ]]; then
                    echo "Calling Parmasist menu"
                    pharmasist_menu "$line"
                else
                    echo "The role is not defined. Exiting the application...."
                    logout_user
                    exit 0
                fi

            else
                echo "The provided passwords don't match"
                return 0
            fi
        fi

    else
        echo -e "Unsuccessful login. Incorrect username or password. Please try again.\n"
    fi

    return 0
}

# Function for the admin menu
admin_menu() {
    echo "This is Admin menu..."
    echo "1. Display Details"
    echo "2. Create User"
    read -p "Enter your choice: " choice
    case $choice in
    1)
        echo "Displaying Your details"
        display_details "$1"
        ;;
    2)
        echo "What type of user you want to create"
        echo "1. Customer"
        echo "2. Pharmasist"
        read -p "Enter your choice: " role
        case $role in
        1)
            echo "Creating a customer"
            register_credentials "customer"
            ;;
        2)
            echo "Creating a Pharmasist"
            register_credentials "pharmacist"
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
        esac

        ;;

    *)
        echo "Invalid choice. Please try again."
        ;;
    esac

    return 0

}

logout_user() {
    # read the username from the login data file
    local user=$(cat "$login_data_file")
    local line=$(grep "^$user:" "$credentials_file")
    updated_line=$(echo "$line" | awk 'BEGIN{FS=OFS=":"} {$6="0"; print}')
    sed -i "s~$line~$updated_line~" "$credentials_file"
    rm -f "$login_data_file"

    exit 0
}

# Function for the user menu
customer_menu() {
    echo "This is a customer menu..."
    echo "1. Display all products"
    echo "2. Search for a product"
    echo "3. Add a product to cart"
    echo "4. Remove a product from cart"
    echo "5. Display cart"
    echo "6. Checkout"
    echo "7. Display Details"
    read -p "Enter your choice: " choice
    case $choice in
    1)
        echo "Displaying all products..."
        ;;
    2)
        echo "Searching for a product..."
        ;;
    3)
        echo "Adding a product to cart..."
        ;;
    4)
        echo "Removing a product from cart..."
        ;;
    5)
        echo "Displaying cart..."
        ;;
    6)
        echo "Checking out..."
        ;;
    7)
        display_details "$1"
        ;;
    *)
        echo "Invalid choice. Please try again."
        ;;
    esac

    return 0

}

# Function to display the details of the user
display_details() {

    local line=$1
    local user=$(echo "$line" | cut -d ':' -f 1)
    local name=$(echo "$line" | cut -d ':' -f 4)
    local role=$(echo "$line" | cut -d ':' -f 5)
    local login_status=$(echo "$line" | cut -d ':' -f 6)

    echo "username: $user||name: $name||role: $role||login_status: 1"

}

# Function for the pharmacist menu
pharmasist_menu() {
    echo "This is a pharmacist menu..."
    return 0
}

function ctrl_c() {
    echo -e "\n Unexpected exit. Exiting the application..."
    logout_user
    exit 1
}
function on_exit() {
    echo -e "\n Script is exiting..."
    logout_user

}
trap on_exit EXIT
trap ctrl_c SIGINT

# Function to display the main menu
# this function will need that we
main_menu() {
    echo "1. Login"
    echo "2. Register"
    echo "3. Exit"
    echo -n "Enter your choice: "
}

# Main script execution starts here
echo "Welcome to the authentication system."

while true; do
    echo -e "\n================ User Authentication System ================"
    main_menu
    read user_choice
    case $user_choice in
    1)
        get_login_credentials

        verify_credentials "$user" "$pass"
        ;;
    2)
        register_credentials
        ;;
    3)
        echo "Exiting the application "
        exit 0
        ;;
    *)
        echo "Invalid choice. Please try again."
        ;;
    esac

done
