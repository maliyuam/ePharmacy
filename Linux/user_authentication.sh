#!/bin/bash

credentials_file="data/credentials.txt"
credentials_path="data"

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
    # check that parameter one is not empty
    if [[ -z "$1" ]]; then
        role="customer"
    else
        role="$1"
    fi
    read -p "Enter name: " name
    read -p "Enter username: " user
    read -sp "Enter password: " pass
    read -sp "Confirm password: " confirm_pass
    local line=$(grep "^$user2:" "$credentials_file")
    if [[ -n "$line" ]]; then
        echo -e "The username already exists. Please try again with a different username.\n"
        return 1
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
        echo -e "\n"

        local user_id=$(generte_user_id)
        local pass=$(hash_password "$pass")
        local hashed_pass=$(echo "$pass" | cut -d ':' -f 1)
        local salt=$(echo "$pass" | cut -d ':' -f 2)
        echo -e "Registration successful. You can now log in.\n"
        echo -e "$user:$hashed_pass:$salt:$name:$role:0:$user_id" >>"$credentials_file"
    fi
}

generte_user_id() {
    generated_id=$(date +%Y%m%d%H%M%S%N)-$$
    echo "$generated_id "
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
    echo "Stored credentials are $stored_cred"
    if [[ -n "$stored_cred" ]]; then
        local stored_pass=$(echo "$stored_cred" | cut -d ':' -f 1)
        echo "Stored password is $stored_pass"
        local salt=$(echo "$stored_cred" | cut -d ':' -f 2)
        echo "Stored salt is $salt"
        local hashed_pass=$(echo -n "$pass$salt" | sha256sum | awk '{print $1}')
        local login_status=$(echo "$stored_cred" | cut -d ':' -f 5)
        echo "Login status is $login_status"

        if [[ "$stored_pass" == "$hashed_pass" ]]; then
            echo "Login successful"
            local line=$(grep "^$user:" "$credentials_file")
            if [[ "$login_status" == "0" ]]; then
                echo "Updating login status to 1"
                updated_line=$(echo "$line" | awk 'BEGIN{FS=OFS=":"} {$6="1"; print}')
                sed -i "s~$line~$updated_line~" "$credentials_file"
            fi
            echo "Line is $line"

            local role=$(echo "$stored_cred" | cut -d ':' -f 4)
            echo "Role is $role"
            if [[ "$role" == "admin" ]]; then
                echo "Calling admin menu"
                admin_menu
            elif [[ "$role" == "customer" ]]; then
                echo "Calling Customer menu"
                customer_menu
            elif [[ "$role" == "pharmacist" ]]; then
                echo "Calling Parmasist menu"
                pharmasist_menu

            else
                echo "The role is not defined. Exiting the application...."
                exit 1
            fi

        else
            echo "The provided passwords don't match"
            return 1
        fi
    else
        echo -e "Unsuccessful login. Incorrect username or password. Please try again.\n"
    fi

    return 1
}

# Function for the admin menu
admin_menu() {
    # write a logic that allows a user logged in as admin to create an account.
    # This function must allow the logged in user to create many users.

    # Write your code here
    return 0
}

logout_user() {
    #   handle the logout functionality here where we'll change the login status to 0
    echo "Logging out of the application"
}

# Function for the user menu
customer_menu() {
    echo "This is a normal user menu..."
    return 0
}

# Function for the pharmacist menu
pharmasist_menu() {
    echo "This is a pharmacist menu..."
    return 0
}

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
