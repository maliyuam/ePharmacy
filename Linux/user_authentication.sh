#!/bin/bash

credentials_file="data/credentials.txt"
credentials_path="data"

# Function to prompt for credentials
get_login_credentials() {
    # Prompt for username
    read -p "Enter username: " user
    # Prompt for password
    read -sp "Enter password: " pass
    echo -e "\n"
    # The password must be invisible while typing to ensure that no one can read it while inserting it
    return 0
}

# Function to prompt for credentials
get_create_acctcred() {
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
    # Insert code to register add the created user to a file called credentials.txt
    # Write your code here
    echo -e "Registration successful. You can now log in.\n"
}

# Function to verify credentials and privileges
verify_credentials() {
    #   check that the file exists
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
        echo "Stored password is $stored_pass"
        local salt=$(echo "$stored_cred" | cut -d ':' -f 2)
        echo "Stored salt is $salt"
        local hashed_pass=$(echo -n "$pass$salt" | sha256sum | awk '{print $1}')
        echo "Hashed password is $hashed_pass"
        echo "Stored Creds are $stored_cred"
        # Checking to see that the password of the correspoinding user matches the stored password
        if [[ "$stored_pass" == "$hashed_pass" ]]; then
            echo "Login successful"
            # check whether the user is an admin or a normal user
            local role=$(grep "^$user:" "$credentials_file" | cut -d ':' -f 3)
            echo "Role is $role"
            if [[ "$role" == "admin" ]]; then
                echo "Calling admin menu"
                admin_menu
            else

                echo "Calling user menu"
                user_menu
            fi
        else
            echo "The provided passwords don't match"
            return 1
        fi
        # Write here
        # On successful login remember to update the credentials.txt file for login status to 1
        # if the credentials provided are correct, check the role. If the role is admin, call the admin menu
        # write here
        # Otherwise call user menu
        # Write your code here
    fi
    echo -e "Unsuccessful login. Incorrect username or password. Please try again.\n"
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
user_menu() {
    echo "This is a normal user menu..."
    exit 0
}

# Function to display the main menu
# this function will need that we
main_menu() {
    echo "1. Login"
    echo "2. Register"
    echo "3. Logout"
    echo "4. Exit"
    echo -n "Enter your choice: "

}

# Main script execution starts here
echo "Welcome to the authentication system."

while true; do
    echo "================ User Authentication System ================"
    main_menu
    read user_choice
    echo "The choice entered is $user_choice"
    case $user_choice in
    1)
        get_login_credentials
        verify_credentials "$user" "$pass"
        ;;
    2)
        get_create_acctcred
        register_credentials
        ;;
    3)
        logout_user
        ;;
    4)
        echo "Exiting the application "
        exit 0
        ;;
    *)
        echo "Invalid choice. Please try again."
        ;;
    esac

done
