import shutil
import os
import math
import json

def split_file(src_file_path, dest_folder):
    # Get file size in bytes
    file_size = os.path.getsize(src_file_path)

    # Calculate number of fragments needed
    num_fragments = math.ceil(file_size / (512 * 1024 * 1024))

    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Split file into fragments and save to destination folder
    with open(src_file_path, "rb") as src_file:
        for i in range(num_fragments):
            # Get fragment file name
            fragment_file_name = f"{os.path.basename(src_file_path)}.part{i+1}"

            # Get full path of fragment file
            dest_path = os.path.join(dest_folder, fragment_file_name)

            # Calculate size of fragment in bytes
            fragment_size = min(512 * 1024 * 1024, file_size - i * (512 * 1024 * 1024))

            # Read fragment from source file and write to destination file
            with open(dest_path, "wb") as dest_file:
                dest_file.write(src_file.read(fragment_size))

            print(f"Fragment created: {dest_path}")

    # Create JSON file with file composition
    file_composition = {
        "filename": os.path.basename(src_file_path),
        "size": file_size,
        "num_fragments": num_fragments,
        "fragments": [f"{os.path.basename(src_file_path)}.part{i+1}" for i in range(num_fragments)]
    }
    with open(os.path.join(dest_folder, f"{os.path.basename(src_file_path)}.json"), "w") as json_file:
        json.dump(file_composition, json_file)

def backup_files(src_folder, dest_folder):
    # Get list of files in source folder
    files = os.listdir(src_folder)

    for file_name in files:
        # Get full path of source file
        src_path = os.path.join(src_folder, file_name)

        # Split file into fragments and save to destination folder
        split_file(src_path, dest_folder)

    print("Files splitted successfully!")

def restore_files(src_folder, dest_folder):
    # Get list of files in source folder
    files = os.listdir(src_folder)

    for file_name in files:
        # Ignore JSON files
        if file_name.endswith(".json"):
            continue

        # Get full path of source fragment file
        src_path = os.path.join(src_folder, file_name)

        # Get fragment number from file name
        fragment_num = int(file_name.split(".")[-1].replace("part", ""))

        # Get full path of destination file
        dest_file_name = ".".join(file_name.split(".")[:-1])
        dest_path = os.path.join(dest_folder, dest_file_name)

        # Restore fragment to destination file
        with open(dest_path, "ab") as dest_file:
            with open(src_path, "rb") as src_file:
                dest_file.write(src_file.read())

        print(f"Fragment restored: {dest_path}")
    
    # Get JSON file with file composition
    for file_name in files:
        if file_name.endswith(".json"):
            with open(os.path.join(src_folder, file_name), "r") as json_file:
                file_composition = json.load(json_file)
                file_size = file_composition["size"]
                num_fragments = file_composition["num_fragments"]
                
                # Get list of fragmented filenames
                fragment_filenames = []
                for i in range(num_fragments):
                    fragment_file_name = f"{file_composition['filename']}.part{i+1}"
                    fragment_filenames.append(fragment_file_name)

                if len(fragment_filenames) == num_fragments:
                    print(f"All fragments have been restored for {file_composition['filename']}")
                else:
                    print(f"Error: Not all fragments have been restored for {file_composition['filename']}")

if __name__ == "__main__":
    opc = int(input("Enter the option\n\r1) Back-up\n\r2) Restore back-up\nR=\ "))
    if opc == 1:
        # Backup files
        print(f'Back-up process')
        src_folder = input("Enter source folder path: ")
        dest_folder = input("Enter destination folder path: ")
        backup_files(src_folder, dest_folder)
    if opc == 2:
        # Restore files
        print(f'Restoring process')
        src_folder = input("Enter source folder path: ")
        dest_folder = input("Enter destination folder path: ")
        restore_files(src_folder, dest_folder)