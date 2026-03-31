#!/bin/bash

# Script to automate the dylib injection process into an IPA file

# Function to check if the necessary tools are installed
check_tools() {
    command -v unzip >/dev/null 2>&1 || { echo >&2 "unzip is required but it's not installed. Aborting."; exit 1; }
    command -v ldid >/dev/null 2>&1 || { echo >&2 "ldid is required but it's not installed. Aborting."; exit 1; }
}

# Function to inject dylib into an existing IPA
inject_dylib() {
    local ipa_file=$1
    local dylib_file=$2
    local app_name=$3

    # Unzip the IPA file
    unzip "$ipa_file" -d temp_ipa

    # Inject dylib into the executable
    local app_executable="temp_ipa/Payload/$app_name.app/$app_name"
    ldid -Sentitlements.xml "$app_executable"
    cp "$dylib_file" "temp_ipa/Payload/$app_name.app/"
    ldid -Sentitlements.xml "temp_ipa/Payload/$app_name.app/$dylib_file"

    # Rezip the IPA file
    cd temp_ipa
    zip -r "../${ipa_file%.ipa}_modified.ipa" .
    cd ..

    # Clean up
    rm -rf temp_ipa
}

# Main script execution
check_tools

# Example usage of the inject_dylib function
# You can modify this according to your needs
# inject_dylib "YourApp.ipa" "YourDylib.dylib" "YourApp"
